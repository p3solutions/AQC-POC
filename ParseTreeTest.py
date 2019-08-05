from ParseTree import ParseTree
from Node import Node
from NodeInfo import NodeInfo
from TreeAdjustor import TreeAdjustor
from SyntacticEvaluator import SyntacticEvaluator
class ParseTreeTest:

    @staticmethod
    def testTranslation1() :
        tree = ParseTree()
        nodes = [ Node(index=-1, word="DEFAULT", posTag="DEFAULT") for i in range(0,6)]

        nodes[0] = Node(index = 0, word = "ROOT", posTag = "ROOT")
        nodes[0].info = NodeInfo(type="ROOT", value="ROOT")

        nodes[1] = Node(index=1, word="return", posTag="--")
        nodes[1].info = NodeInfo(type="SN", value="SELECT")

        nodes[2] = Node(index=2, word="titles", posTag="--")
        nodes[2].info = NodeInfo(type="NN", value="in.title")

        nodes[3] = Node(index=3, word="theory", posTag="--")
        nodes[3].info = NodeInfo(type="VN", value="in.area")

        nodes[4] = Node(index=4, word="before", posTag="--")
        nodes[4].info = NodeInfo(type="ON", value="<")

        nodes[5] = Node(index=5, word="1970", posTag="--")
        nodes[5].info = NodeInfo(type="VN", value="in.year")

        tree.root = nodes[0]
        tree.root.getChildren().append(nodes[1])
        nodes[1].children.append(nodes[2])
        nodes[2].parent = nodes[1]
        nodes[2].children.append(nodes[3])
        nodes[2].children.append(nodes[4])
        nodes[3].parent = nodes[2]
        nodes[4].parent = nodes[2]
        nodes[4].children.append(nodes[5])
        nodes[5].parent = nodes[4]

        print ("===========test for Running SyntacticEvaluator.numberOfInvalidNodes===========")
        print ("Input tree: ")
        print (tree)
        print ("Number of Invalid nodes: %d "%SyntacticEvaluator().numberOfInvalidNodes(tree)+"\n")
        print ("Invalid nodes: ")

        for i in range(1,tree.size()):
            if (nodes[i].isInvalid):
                print (nodes[i])

        print ("===========test for Running mergeLNQN===========")
        print ("Input tree:")
        print (tree)

        newTree = tree.mergeLNQN()

        print ("Output tree:")
        print (newTree)
        print ("===========test for Running adjust() in TreeAdjustor===========")
        print ("Input tree: ")
        print (tree)

        treeList = TreeAdjustor.adjust(tree)
        print ("Output size: %d"%len(treeList))
        print ("Output trees:")
        for i in range(0,len(treeList)):
            print ("Tree "+str(i)+" :")
            print (treeList[i])

        print ("===========test for Running getAdjustedTrees() in TreeAdjustor===========")
        print ("Number of possible trees for choice:")

        result = TreeAdjustor.getAdjustedTrees(tree)

        print (len(result))

        for t in result:
            print (t)
obj = ParseTreeTest()
obj.testTranslation1()





