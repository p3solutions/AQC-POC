class SchemaGraph:
    tables = None
    tableRows = None
    keys = None
    connectivity = None
    schemaText = ""

    def __init__(self, connection):

        SchemaGraph.tables = dict()
        SchemaGraph.tableRows = dict()

        print ("Retrieving schema graph...")
        cursor = connection.cursor()

        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
        table_names = cursor.fetchall()

        for table_name in table_names:
            # print table_name[0]
            SchemaGraph.tables[table_name[0]] = dict()
            SchemaGraph.tableRows[table_name[0]] = dict()

            cursor.execute("select column_name, data_type from information_schema.columns where table_name = '%s'" % (
            table_name[0]))
            col_info = cursor.fetchall()

            col_name_type_dict = dict()
            for col in col_info:
                col_name_type_dict[col[0]] = col[1]
            # print col_name_type_dict

            col_name_values_dict = dict()
            for col in col_info:
                cursor.execute("SELECT %s FROM %s ORDER BY RANDOM() LIMIT 20"
                               % (col[0], table_name[0]))
                row = cursor.fetchall()
                col_name_values_dict[col[0]] = row
            sb= []
            for table in SchemaGraph.tables:
                sb.append(table)
                sb.append("\n")

            SchemaGraph.schemaText = "".join(sb)
            SchemaGraph.tables[table_name[0]] = col_name_type_dict
            SchemaGraph.tableRows[table_name[0]] = col_name_values_dict


        print ("\nprinting tables...")
        print (SchemaGraph.tables)
        print ("\nprinting tablerows...")
        print (SchemaGraph.tableRows)
        print ("\n printing TableNames...\n")
        print (SchemaGraph.getTableNames(self))
        SchemaGraph.readPrimaryKeys(self, connection)
        SchemaGraph.findConnectivity(self, connection)

    def readPrimaryKeys(self, connection):
        SchemaGraph.keys = dict()
        cursor = connection.cursor()
        # get primary keys for each table
        for tableName in SchemaGraph.tables.iterkeys():
            cursor.execute("""SELECT a.attname, format_type(a.atttypid, a.atttypmod)
                              AS data_type FROM   pg_index i
                              JOIN   pg_attribute a ON a.attrelid = i.indrelid
                              AND a.attnum = ANY(i.indkey)
                              WHERE  i.indrelid = '%s'::regclass
                              AND i.indisprimary;""" % tableName)
            rsPrimaryKey = cursor.fetchall()

            SchemaGraph.keys[tableName] = dict()
            pkList = list()

            for row in rsPrimaryKey:
                pkList.append(row[0])

            SchemaGraph.keys[tableName] = pkList
        print ("\nprinting primary keys...")
        print (SchemaGraph.keys)

    def findConnectivity(self, connection):
        SchemaGraph.connectivity = dict()

        for tableName in SchemaGraph.tables:
            SchemaGraph.connectivity[tableName] = list()

        cursor = connection.cursor()

        # get foreign keys from table
        cursor.execute("""SELECT tc.table_name, kcu.column_name, ccu.table_name
                AS foreign_table_name, ccu.column_name
                AS foreign_column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY'""")

        foreignKeys = cursor.fetchall()

        for foreignKey in foreignKeys:
            table1 = foreignKey[0]
            table2 = foreignKey[2]
            if not table2 in SchemaGraph.connectivity[table1]:
                SchemaGraph.connectivity[table1].append(table2)
            if not table1 in SchemaGraph.connectivity[table2]:
                SchemaGraph.connectivity[table2].append(table1)
        print ("\nprinting connectivity: ")
        print (SchemaGraph.connectivity)

    def getJoinKeys(self, table1, table2):
        table1Keys = SchemaGraph.keys[table1]
        table2Keys = SchemaGraph.keys[table2]

        if table1Keys == table2Keys:
            return set()
        keys1ContainedIn2 = True

        for table1Key in table1Keys:
            if not table1Key in SchemaGraph.tables[table2]:
                keys1ContainedIn2 = False
                break

        if keys1ContainedIn2:
            return set(table1Keys)

        keys2ContainedIn1 = True
        for table2Key in table2Keys:
            if not table2Key in SchemaGraph.tables[table1]:
                keys2ContainedIn1 = False
                break

        if keys2ContainedIn1:
            return set(table2Keys)
        return set()

    def getJoinPath(self, table1, table2):
        # todo
        if not (table1 in SchemaGraph.tables) or not (table2 in SchemaGraph.tables):
            return list()

        visited = dict()
        for tableName in SchemaGraph.tables:
            visited[tableName] = False

        prev = dict()
        queue = list()
        queue.append(table1)
        visited[table1] = True
        found = False

        while len(queue)!=0 and not found:
            tableCurr = queue[0]
            del queue[0]  # remove first

            for tableNext in SchemaGraph.connectivity[tableCurr]:
                if not visited[tableNext]:
                    visited[tableNext] = True
                    queue.append(tableNext)
                    prev[tableNext] = tableCurr
                if tableNext == table2:
                    found = True

        path = list()

        if visited[table2]:
            tableEnd = table2
            path.insert(0, tableEnd)
            while tableEnd in prev:
                tableEnd = prev[tableEnd]
                path.insert(0, tableEnd)
        return path

    def getTableNames(self):
        tableList = []
        for tableName in self.tables:
            tableList.append(tableName)
        return tableList

    def getColumns(self, table):
        columnList = []

        for column in self.tables[table]:
            columnList.append(column)

        return columnList

    def getValues(self, tableName, columnName):
        return self.tableRows[tableName][columnName]


