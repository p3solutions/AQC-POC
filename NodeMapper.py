from model.NodeInfo import NodeInfo
from model.WordSimilarity import WordSimilarity
from operator import attrgetter


class NodeMapper:

    map = None
    wordSimilarity = None

    def __init__(self):
        self.wordSimilarity = WordSimilarity()
        self.map = dict()

        self.map["return"] = NodeInfo("SN", "SELECT")
        self.map["fetch"] = NodeInfo("SN", "SELECT")
        self.map["give"] = NodeInfo("SN", "SELECT")
        self.map["print"] = NodeInfo("SN", "SELECT")

        self.map["equals"]= NodeInfo("ON", "=") # Operator Node
        self.map["less"] = NodeInfo("ON", "<")
        self.map["greater"] = NodeInfo("ON", ">")
        self.map["not"] = NodeInfo("ON", "!=")
        self.map["before"] = NodeInfo("ON", "<")
        self.map["after"] = NodeInfo("ON", ">")
        self.map["more"] = NodeInfo("ON", ">")
        self.map["older"] = NodeInfo("ON", ">")
        self.map["newer"] = NodeInfo("ON", "<")

        self.map["fn"] = NodeInfo("FN", "AVG") # Function Node
        self.map["average"] = NodeInfo("FN", "AVG")
        self.map["most"] = NodeInfo("FN", "MAX")
        self.map["total"] = NodeInfo("FN", "SUM")
        self.map["number"] = NodeInfo("FN", "COUNT")
        self.map["count"] = NodeInfo("FN", "COUNT")

        self.map["all"] = NodeInfo("QN", "ALL") # Quantifier Node
        self.map["any"] = NodeInfo("QN", "ANY")
        self.map["each"] = NodeInfo("QN", "EACH")

        self.map["and"] = NodeInfo("LN", "AND") # Logic Node
        self.map["or"] = NodeInfo("LN", "OR")

    def reverseScoreComparator(self, a, b):
        if a.score < b.score:
            return 1
        elif a.score > b.score:
            return -1
        else:
            return 0

    def getNodeInfoChoices(self , node, schema):
        result = set() #final output

        if node.getWord() == "ROOT":
            result.add(NodeInfo("ROOT", "ROOT"))
            return list(result)

        valueNodes = set()
        word = node.getWord().lower()

        if word in self.map:
            result.add( self.map[word] )
            return list(result)

        for tableName in schema.getTableNames():
            result.add(NodeInfo("NN", tableName, self.wordSimilarity.getSimilarity(word, tableName)))

            for colName in schema.getColumns(tableName):
                result.add(NodeInfo("NN", tableName + "." + colName, self.wordSimilarity.getSimilarity(word, colName)))

                for value in schema.getValues(tableName, colName):
                    if (word is None) or (value is None):
                        print "Comparing %s and %s"%(word, value)
                        print "In table %s column %s"%(tableName, colName)

                    valueNodes.add(NodeInfo("VN", tableName+"."+colName, self.wordSimilarity.getSimilarity(word, value)))

        for nodeInfo in valueNodes:
            result.add(nodeInfo)

        sortedResultList = sorted(result, cmp = self.reverseScoreComparator)

        if self.isclose(float(sortedResultList[0].getScore()),1.0):
            sortedResultList.insert(1, NodeInfo("UNKNOWN", "meaningless", 1.0))
        else:
            sortedResultList.insert(0, NodeInfo("UNKNOWN", "meaningless", 1.0))

        return sortedResultList

    def isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

