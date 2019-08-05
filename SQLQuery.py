

class SQLQuery:

    blocks = list()
    map = dict()

    def __init__(self):
        self.map = dict()
        self.map["SELECT"] = list()
        self.map["FROM"] = set()
        self.map["WHERE"] = set()
        self.blocks = list()

    def get(self):
        return SQLQuery.toString()

    def getCollection(self, keyWord):
        return list(self.map[keyWord])

    def addBlock(self, query):
        self.blocks.append(query)
        SQLQuery.add(self, "FROM", "BLOCK%d"%len(self.blocks))

    def add(self, key, value):
        if self.isSet(key):
            self.map[key].add(value)
        else:
            self.map[key].append(value)

    def isSet(self, key):
        if(key == "SELECT"):
            return False
        else:
            return True

    @staticmethod
    def toSBLine( SELECT):
        sb = []
        for val in SELECT:
            if len(sb) == 0:
                sb.append(val)
            else:
                sb.append(", ")
                sb.append(val)
        return ''.join(sb)

    @staticmethod
    def toSBLineCondition(WHERE):
        sb = []
        for val in WHERE:
            if len(sb) == 0:
                sb.append(val)
            else:
                sb.append(" AND ")
                sb.append(val)
        return ''.join(sb)

    def toString(self):
        if len(self.map["SELECT"]) == 0 or len(self.map["FROM"]) == 0:
            return "Illegal Query"

        sb = []
        for i in range(0, len(self.blocks)):
            sb.append("BLOCK%d:\n"%(i+1))
            sb.append("%s\n"%self.blocks[i].toString())
            ''.join(sb)

        sb.append("SELECT ")
        sb.append("%s\n"%SQLQuery.toSBLine(self.map["SELECT"]))
        sb.append("FROM ")
        sb.append("%s\n" % SQLQuery.toSBLine(self.map["FROM"]))

        if len(self.map["WHERE"]) != 0:
            sb.append("WHERE ")
            sb.append("%s\n"%SQLQuery.toSBLineCondition(self.map["WHERE"]))

        sb.append(";\n")
        return ''.join(sb)


