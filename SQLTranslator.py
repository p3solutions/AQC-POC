from model.SQLQuery import SQLQuery


class SQLTranslator:
    query =None
    schema = None
    blockCounter = 1

    def __init__(self, root, schema, block):
        if block is None:
            block = False

        if not block:
            self.schema = schema
            self.query = SQLQuery()

            self.translateSClause(root.getChildren()[0])
            if (len(root.getChildren()) >= 2):
                self.translateComplexCondition(root.getChildren()[1])

            if schema is not None:
                self.addJoinPath()
        else:
            self.schema = schema
            self.query = SQLQuery()
            self.translateGNP(root)

    def getResult(self):
        return self.query

    def isNumber(self, str):
        length = len(str)
        if (length == 0):
            return False
        i =0
        if (str[0] == '-'):
            if (length == 1):
                return False
            i =1
        for x in range(i,length):
            c = str[x]
            if (c < '0' or c > '9' and c != '.'):
                return False
        return  True

    def translateCondition(self, node):
        attribute = "ATTRIBUTE"
        compareSymbol = "="
        value = "VALUE"
        if (node.getInfo().getType() == "VN"):
            attribute = node.getInfo().getValue()
            value = node.getWord()
        elif (node.getInfo().getType() == "ON"):
            compareSymbol = node.getInfo().getValue()
            print ("Node : "+node.getWord()+" children: ")
            print (node.getChildren())
            VN = node.getChildren()[0]
            attribute = VN.getInfo().getValue()
            value = VN.getWord()
        if not(self.isNumber(value)):
            value = "\'" + value + "\'"

        self.query.add("WHERE", attribute + " " + compareSymbol + " " + value)
        self.query.add("FROM", attribute.split(".")[0])

    def translateNN(self, node,valueFN=None):
        if valueFN is None:
            self.translateNN(node, valueFN="")
        else:
            if not(node.getInfo().getType() == "NN"):
                return
            if not(valueFN == ""):
                self.query.add("SELECT", valueFN + "(" + node.getInfo().getValue() + ")")
            else:
                self.query.add("SELECT", node.getInfo().getValue())
            self.query.add("FROM", node.getInfo().getValue().split(".")[0])

    def translateNP(self, node, valueFN=None):
        if valueFN is None:
            self.translateNP(node, valueFN="")
        else:
            self.translateNN(node, valueFN)
            for child in node.getChildren():
                if (child.getInfo().getType() == "NN"):
                    self.translateNN(child)
                elif (child.getInfo().getType() == "ON" or child.getInfo().getType() == "VN"):
                    self.translateCondition(child)

    def translateGNP(self, node):
        if (node.getInfo().getType() == "FN"):
            if (len(node.getChildren()) == 0):
                return
            self.translateNP(node.getChildren()[0], node.getInfo().getValue())
        elif (node.getInfo().getType() == "NN"):
            self.translateNP(node)

    def translateComplexCondition(self, node):
        if not(node.getInfo().getType() == "ON"):
            return
        if (len(node.getChildren()) != 2):
            return
        transLeft = SQLTranslator(node.getChildren()[0], self.schema, block=True)
        transRight = SQLTranslator(node.getChildren()[1], self.schema, block=True)
        self.query.addBlock(transLeft.getResult())
        self.query.addBlock(transRight.getResult())
        self.query.add("WHERE","BLOCK" + str(self.blockCounter) + " " + node.getInfo().getValue() + " " + "BLOCK" + str(self.blockCounter+1))
        self.blockCounter+=2

    def translateSClause(self, node):
        if not(node.getInfo().getType() == "SN"):
            return
        self.translateGNP(node.getChildren()[0])


    def addJoinKeys(self, table1, table2):
        joinKeys = self.schema.getJoinKeys(table1, table2)
        for joinKey in joinKeys:
            self.query.add("WHERE", table1 + "." + joinKey + " = " + table2 + "." + joinKey)

    def addJoinPath(self ,joinPath = None):
        if joinPath is None:
            fromTables = list(self.query.getCollection("FROM"))
            if (len(fromTables) <= 1):
                return
            for i in range(0, len(fromTables)-1):
                for j in range(i+1, len(fromTables)):
                    joinPath = self.schema.getJoinPath(fromTables[i], fromTables[j])
                    self.addJoinPath(joinPath)
        else:
            for i in range(0,len(joinPath)-1):
                self.addJoinKeys(joinPath[i], joinPath[i+1])





