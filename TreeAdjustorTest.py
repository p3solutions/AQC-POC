
from ParseTree import ParseTree
from Node import Node
from NodeInfo import NodeInfo
from TreeAdjustor import TreeAdjustor
from model.SchemaGraph import SchemaGraph


class TreeAdjustorTest:

    schema = None
    def __init__(self):
        return

    def getAdjustedTreesTest(self):



        T = ParseTree()
        nodes = [Node(index=-1, word="DEFAULT", posTag="DEFAULT") for i in range(0, 8)]

        nodes[0] = Node(index=0, word="ROOT", posTag="--")
        nodes[0].info = NodeInfo(type="ROOT", value="ROOT")
        nodes[1] = Node(index=1, word="return", posTag="--")
        nodes[1].info = NodeInfo(type="SN", value="SELECT")
        nodes[2] = Node(index=2, word="conference", posTag="--")
        nodes[2].info = NodeInfo(type="NN", value="Author")
        nodes[3] = Node(index=3, word="area", posTag="--")
        nodes[3].info = NodeInfo(type="NN", value="Title")
        nodes[4] = Node(index=4, word="papers", posTag="--")
        nodes[4].info = NodeInfo(type="NN", value="Author")
        nodes[5] = Node(index=5, word="citations", posTag="--")
        nodes[5].info = NodeInfo(type="NN", value="Journal")
        nodes[6] = Node(index=6, word="most", posTag="--")
        nodes[6].info = NodeInfo(type="FN", value=">")
        nodes[7] = Node(index=7, word="total", posTag="--")
        nodes[7].info = NodeInfo(type="FN", value="Year")

        T.root = nodes[0]
        nodes[0].children.append(nodes[1])
        nodes[1].parent = nodes[0]
        nodes[1].children.append(nodes[2])
        nodes[2].parent = nodes[1]
        nodes[2].children.append(nodes[3])
        nodes[3].parent = nodes[2]
        nodes[2].children.append(nodes[4])
        nodes[4].parent = nodes[2]
        nodes[4].children.append(nodes[5])
        nodes[5].parent = nodes[4]
        nodes[5].children.append(nodes[6])
        nodes[6].parent = nodes[5]
        nodes[5].children.append(nodes[7])
        nodes[7].parent = nodes[5]

        print ("===========test for Running getAdjustedTrees() in TreeAdjustor===========")
        print ("The original tree:")
        print (T.toString())
        print ("Number of possible trees for choice:")

        obj = TreeAdjustor()
        result = TreeAdjustor.getAdjustedTrees(T)
        # result = TreeAdjustor.adjust(T)

        print (len(result))
        # result = sorted(result,cmp=TreeAdjustorTest.cmpp)
        # l =sorted(m, cmp =TreeAdjustor.timeStampCompare)
        for i in range(0, len(result)):
             for j in range(i+1, len(result)):
                if(result[i].getScore() <= result[j].getScore()):
                    temp = result[i]
                    result[i] =result[j]
                    result[j] = temp
        print ("The three trees with highest scores look like:")
        for i in range(0,5):
           print (result[i])

        for tree in result:
            print (" treeList Result %s:%d" % (tree.getSentence(), tree.getScore()))
            tree.insertImplicitNodes()
            query = tree.translateToSQL(self.schema)
            print ("qUERY: " + query.toString())
      

    def adjustTest(self):
        T = ParseTree()
        nodes = [Node(index=-1, word="DEFAULT", posTag="DEFAULT") for i in range(0, 9)]
        nodes[0] = Node(index=0, word="ROOT",posTag= "--")
        nodes[0].info = NodeInfo(type="ROOT", value="ROOT")
        nodes[1] = Node(index=1, word="return", posTag="--")
        nodes[1].info = NodeInfo(type="SN", value="SELECT")
        nodes[2] = Node(index=2, word="conference", posTag="--")
        nodes[2].info = NodeInfo(type="NN", value="Author")
        nodes[3] = Node(index=3, word="area", posTag="--")
        nodes[3].info =NodeInfo(type="NN", value="Title")
        nodes[4] =Node(index=4, word="each", posTag="--")
        nodes[4].info = NodeInfo(type="QN", value=">")
        nodes[5] = Node(index=5, word="papers", posTag="--")
        nodes[5].info = NodeInfo(type="NN", value="Author")
        nodes[6] = Node(index=6, word="citations", posTag="--")
        nodes[6].info = NodeInfo(type="NN", value="Journal")
        nodes[7] = Node(index=7, word="most", posTag="--")
        nodes[7].info = NodeInfo(type="FN", value=">")
        nodes[8] = Node(index=8, word="total", posTag="--")
        nodes[8].info = NodeInfo(type="FN", value="Year")

        T.root = nodes[0]
        nodes[0].children.append(nodes[1])
        nodes[1].parent = nodes[0]
        nodes[1].children.append(nodes[2])
        nodes[2].parent = nodes[1]
        nodes[2].children.append(nodes[3])
        nodes[3].parent = nodes[2]
        nodes[2].children.append(nodes[5])
        nodes[5].parent = nodes[2]
        nodes[3].children.append(nodes[4])
        nodes[4].parent = nodes[3]
        nodes[5].children.append(nodes[6])
        nodes[6].parent = nodes[5]
        nodes[6].children.append(nodes[7])
        nodes[7].parent = nodes[6]
        nodes[6].children.append(nodes[8])
        nodes[8].parent = nodes[6]

        print ("===========test for Running adjust() in TreeAdjustor===========")

        treeList = TreeAdjustor.adjust(T)
        print ("Output size: %d"%len(treeList))

        print ("Output trees:")
        ctr=0
        for tr in treeList:
            print ("Tree %d %s"%(ctr, tr.getSentence()))
            ctr+=1
    @staticmethod
    def cmpp(a,b):

        return a.getScore() > b.getScore()

obj = TreeAdjustorTest()
obj.getAdjustedTreesTest()
# obj.adjustTest()



