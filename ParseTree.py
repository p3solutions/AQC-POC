from nltk.tree import ParentedTree
from nltk.tree import Tree

from Node import Node
from model.TreeAdjustor import TreeAdjustor
from model.NodeInfo import NodeInfo
from model.SQLTranslator import SQLTranslator
from model.SyntacticEvaluator import SyntacticEvaluator
from model.Utils import Utils


class ParseTree:
    edit = None
    root = None
    nodes = list()
    time = None
    utils = None
    removed = False
    indexOfRightCoreNode = -1
    indexOfLeftCoreNode = -1
    # TODO: This is created for the priority q . still have to check if its working
    def __lt__(self, t2):
        # print "!!"
        # print self.toString()
        a = self.getScore()
        b = t2.getScore()
        # if(self.getScore() != t2.getScore()):
        #     return  self.getScore() >  t2.getScore()
        # else:
        #     return self.time < t2.time
        return self.getScore() > t2.getScore()

    def __init__(self, text=None, parser=None, node=None, other=None):


        #self.root =None
        #self.nodes = list()
        self.time = None
        self.indexOfRightCoreNode = -1
        self.indexOfLeftCoreNode = -1
        self.utils = Utils()
        self.removed = False

        def traverseTree(tree):
            print("tree:", tree.label())
            parInd = self.findNodeInd(tree.label())
            # print parInd
            # print tree.get_children()
            for subtree in tree:
                if type(subtree) == Tree:
                    childInd = self.findNodeInd(subtree.label())
                    self.nodes[parInd].setChild(self.nodes[childInd])
                    self.nodes[childInd].setParent(self.nodes[parInd])
                    traverseTree(subtree)
                else:
                    childInd = self.findNodeInd(subtree.encode('ascii', 'ignore'))
                    self.nodes[parInd].setChild(self.nodes[childInd])
                    self.nodes[childInd].setParent(self.nodes[parInd])
                    print (type(subtree.encode('ascii', 'ignore')))

        if text is None and parser is not None and node is None and other is None:
            pass

        if text is not None and parser is not None and node is None and other is None:
            tagged = parser.tagger.tag(text.split())
            print (tagged)
            gs_graph_iter = parser.parser.raw_parse(text)
            self.root = Node(index=0, word="ROOT", posTag="ROOT")

            self.nodes.append(self.root)

            for child in gs_graph_iter:
                gs_graph = child.tree()
                p_gs_graph = ParentedTree.convert(gs_graph)
                print (p_gs_graph)
                break

            gs_graph.pprint()

            ind = 0
            for word in text.split():
                # print tagged[ind][1]
                self.nodes.append(Node(index=ind + 1, word=word, posTag=tagged[ind][1]))
                ind += 1

            rootInd = self.findNodeInd("ROOT")
            retInd = self.findNodeInd(gs_graph.label())
            self.nodes[rootInd].setChild(self.nodes[retInd])
            self.nodes[retInd].setParent(self.nodes[rootInd])
            traverseTree(gs_graph)
            print ("....................")
            # self.nodes[1].setChild(self.nodes[3])
            for n in self.nodes:
                print (n.getWord())
                print ([word.getWord() for word in n.getChildren()])
        elif (node is not None):
            self.root = node.clone()
        elif other is not None:
            ParseTree(node= other.root)


    def findNodeInd(self, word):
        ind = 0
        for i in self.nodes:
            if i.getWord() == word:
                return ind
            ind += 1
        return None

    def size(self):
        return len(self.root.genNodesArray())

    def getEdit(self):
        return self.edit

    def setEdit(self, edit):
        self.edit = edit

    def removeMeaninglessNodes2(self, curr):
        if curr is None:
            return
        currChildren = list(curr.getChildren())


        for i in range(0, len(currChildren)):
            print ("aaaaaaaaaaaaa")
            print (curr)
            print (currChildren)
            print ("ki:----------------------------- ")
            print (currChildren[i])
            self.removeMeaninglessNodes2(currChildren[i])
            # if(self.removed == True):
            #     i = i-1
            #     self.removed = False


        if (not curr == self.root) and curr.getInfo().getType() == "UNKNOWN":
            print ("current: ")
            print (curr)
            curr.parent.getChildren().remove(curr)
            self.removed = True
            print ("After removeing curr.parent.getChildren(): ")
            ctr =0
            for c in curr.parent.getChildren():
                print ("Node %d : " %ctr)
                print (c)
            for child in curr.getChildren():
                curr.parent.getChildren().append(child)
                child.parent = curr.parent

    def removeMeaningLessNodes(self):
        if self.root.getChildren()[0].getInfo() is None:
            print ("ERR! Node info not yet mapped!")
        self.removeMeaninglessNodes2(self.root)

    def insertImplicitNodes(self):
        childrenOfRoot = self.root.getChildren()

        if len(childrenOfRoot) <= 1:
            return

        # phase 1, add nodes under select to left subtree
        print ("Phase 1, add nodes under select node to left subtree")

        IndexOfSN = 0
        for i in range(0, len(childrenOfRoot)):
            if (childrenOfRoot[i].getInfo().getType() == "SN"):
                IndexOfSN = i
                break

        # start from the name node

        SN = childrenOfRoot[IndexOfSN]
        SN_children = SN.getChildren()
        IndexOfSN_NN = 0

        for i in range(0, len(SN_children)):

            if (SN_children[i].getInfo().getType() == "NN"):
                IndexOfSN_NN = i
                break

        # add them to left subtree of all branches

        copy = None
        indexOfAppendedNode = None
        SN_NN = SN_children[IndexOfSN_NN]

        for i in range(0, len(childrenOfRoot)):

            if i != IndexOfSN:

                nodes_SN_NN = childrenOfRoot[i].genNodesArray()
                indexOfAppendedNode = self.nameNodeToBeAppended(nodes_SN_NN)

                if indexOfAppendedNode != -1:
                    copy = SN_NN.clone()
                    copy.setOutside(True)

                    nodes_SN_NN[indexOfAppendedNode].setChild(copy)
                    copy.setParent(nodes_SN_NN[indexOfAppendedNode])

        # phase 2, compare left core node with right core node
        print ("Phase 2, core node insertion")
        self.indexOfRightCoreNode = -1
        self.indexOfLeftCoreNode = -1

        for i in range(0, len(childrenOfRoot)):

            if (i != IndexOfSN):

                nodes = childrenOfRoot[i].genNodesArray()
                startOfRightBranch = self.endOfLeftBranch(nodes) + 1
                sizeOfRightTree = len(nodes[startOfRightBranch].getChildren()) + 1

                # if right tree only contains numbers, skip it

                if sizeOfRightTree != 1 or (not self.isNumeric(nodes[startOfRightBranch].getWord())):

                    self.indexOfLeftCoreNode = self.coreNode(nodes, left=True)
                    self.indexOfRightCoreNode = self.coreNode(nodes, left=False)

                    # if left core node exists

                    if self.indexOfLeftCoreNode != -1:

                        doInsert = False

                        # if right subtree neither have core node nor it only contains number
                        if self.indexOfRightCoreNode == -1:

                            # copy core node only

                            doInsert = True
                        elif not nodes[self.indexOfRightCoreNode].getInfo().ExactSameSchema(nodes[self.indexOfLeftCoreNode].getInfo()):
                            # if right core node & left core node are different schema
                            # copy core node only
                            doInsert = True

                        if doInsert:

                            copy = nodes[self.indexOfLeftCoreNode].clone()
                            copy.children = list()
                            copy.setOutside(True)

                            insertAroundFN = False

                            indexOfNewRightCN = self.IndexToInsertCN(nodes)

                            if (indexOfNewRightCN == -1):

                                for j in range(len(nodes) - 1, self.endOfLeftBranch(nodes), -1):

                                    if (nodes[j].getInfo().getType() == "FN"):
                                        indexOfNewRightCN = j + 1
                                        insertAroundFN = True
                                        break

                            if (insertAroundFN):

                                # THIS ONLY HANDLES FN NODE HAS NO CHILD OR ONE NAME NODE CHILD

                                FN_children = nodes[indexOfNewRightCN - 1].getChildren()

                                for j in range(0, len(FN_children)):
                                    copy.setChild(FN_children[j])
                                    FN_children[j].setParent(copy)

                                copy.setParent(nodes[indexOfNewRightCN - 1])
                                nodes[indexOfNewRightCN - 1].children = list()
                                nodes[indexOfNewRightCN - 1].setChild(copy)
                            else:

                                # if right subtree only contains VN, adjust index

                                if (indexOfNewRightCN == -1):
                                    indexOfNewRightCN = self.endOfLeftBranch(nodes) + 1

                                copy.setChild(nodes[indexOfNewRightCN])
                                copy.setParent(nodes[indexOfNewRightCN].getParent())
                                nodes[indexOfNewRightCN].getParent().removeChild(nodes[indexOfNewRightCN])
                                nodes[indexOfNewRightCN].getParent().setChild(copy)
                                nodes[indexOfNewRightCN].setParent(copy)

                        # phase 3, map each NV under left core node to right core node

                        print ("Phase 3, transfer constrain nodes from left to right")
                        NV_children_left = nodes[self.indexOfLeftCoreNode].getChildren()

                        for j in range(0, len(NV_children_left)):

                            nodes_new = childrenOfRoot[i].genNodesArray()
                            self.indexOfRightCoreNode = self.coreNode(nodes_new, left=False)
                            NV_children_right = nodes_new[self.indexOfRightCoreNode].getChildren()
                            found_NV = False

                            curr_left = NV_children_left[j]
                            curr_left_type = curr_left.getInfo().getType()

                            for k in range(0, len(NV_children_right)):
                                # compare
                                curr_right = NV_children_right[k]

                                # strictly compare, exact match ON

                                if (curr_left_type == "ON"):

                                    if (curr_left == curr_right):
                                        found_NV = True
                                        break
                                else:

                                    if (curr_left.getInfo().sameSchema(curr_right.getInfo())):
                                        found_NV = True
                                        break

                            if (not found_NV):
                                # insert

                                copy = curr_left.clone()
                                nodes_new[self.indexOfRightCoreNode].setChild(copy)
                                copy.setOutside(True)
                                copy.setParent(nodes_new[self.indexOfRightCoreNode])

                        # phase 4, insert function node

                        print ("Phase 4, insert missing function node")

                        nodes_final_temp = childrenOfRoot[i].genNodesArray()
                        indexOfLeftFN_Tail = -1

                        for j in range(self.indexOfLeftCoreNode, -1, -1):

                            if (nodes_final_temp[j].getInfo().getType() == "FN"):
                                indexOfLeftFN_Tail = j
                                break

                        if (indexOfLeftFN_Tail != -1):

                            for k in range(1, indexOfLeftFN_Tail + 1):

                                nodes_final = childrenOfRoot[i].genNodesArray()
                                self.indexOfRightCoreNode = self.coreNode(nodes_final, left=False)

                                found_FN = False

                                for j in range(self.endOfLeftBranch(nodes_final) + 1, self.indexOfRightCoreNode):

                                    if (nodes_final[j].getInfo().ExactSameSchema(nodes_final[k].getInfo())):
                                        found_FN = True

                                if (not found_FN):
                                    copy = nodes_final[k].clone()
                                    copy.setOutside(True)
                                    copy.children = list()
                                    nodes[0].removeChild(nodes_final[self.endOfLeftBranch(nodes_final) + 1])
                                    nodes[0].setChild(copy)

                                    copy.setParent(nodes[0])
                                    copy.setChild(nodes[self.endOfLeftBranch(nodes_final) + 1])
                                    nodes[self.endOfLeftBranch(nodes_final) + 1].setParent(copy)

    def IndexToInsertCN(self, nodes):
        for i in range(self.endOfLeftBranch(nodes) + 1, len(nodes)):

            if (nodes[i].getInfo().getType() == "NN"):
                return i

        return -1

    def nameNodeToBeAppended(self, nodes):

        for i in range(self.endOfLeftBranch(nodes), 0, -1):

            if (nodes[i].getInfo().getType() == "NN"):
                return i

        return -1

    def endOfLeftBranch(self, nodes):

        for i in range(2, len(nodes)):

            if (nodes[i].getParent() == nodes[0]):
                return i - 1

        return -1

    def isNumeric(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def coreNode(self, nodes, left):
        startIndex = 1
        endIndex = self.endOfLeftBranch(nodes)

        if (not left):
            startIndex = self.endOfLeftBranch(nodes) + 1
            endIndex = len(nodes) - 1

        for i in range(startIndex, endIndex+1):

            if (nodes[i].getInfo().getType() == "NN"):
                return i

        return -1

    def mergeLNQN(self):
        nodes = self.root.genNodesArray()
        for i in range(0, self.size()):
            if (nodes[i].getInfo().getType() == "LN") or nodes[i].getInfo().getType() == "QN":
                word = "(" + nodes[i].getWord() + ")"
                parentWord = nodes[i].getParent().getWord() + word
                nodes[i].getParent().setWord(parentWord)
                self.removeNode(nodes[i])

        tree = ParseTree(node = self.root)
        return tree

    def removeNode(self, curNode):
        curNode.getParent().getChildren().remove(curNode)
        for child in curNode.getChildren():
            child.setParent(curNode.getParent())
            curNode.getParent().setChild(child)

    def addON(self):

        # print "www"
        # print self

        root = self.root.clone()

        on = Node(index=0, word="equals", posTag="postag")
        on.info = NodeInfo(type="ON", value="=")
        root.setChild(on)
        on.setParent(root)
        tree = ParseTree(node = root)

        # print "qqq"
        # print tree

        return tree

    def compare(self, t1, t2):
        if (t1.getScore() != t2.getScore()):
            return  - t1.getScore() + t2.getScore()
        else:
            return t1.getEdit() - t2.getEdit()

    def getAdjustedTrees(self):
        result = TreeAdjustor.getAdjustedTrees(tree=self)
        result = sorted(result, cmp=self.compare)
        # for i in range(0, 100):
        #     for j in range(i + 1, len(result)):
        #         if (result[i].getScore() <= result[j].getScore()):
        #             temp = result[i]
        #             result[i] = result[j]
        #             result[j] = temp
        for tree in result:
             print ("Final Tree: %s %d"%(tree.getSentence(), tree.getScore()))
        return result[0:4]

    def translateToSQL(self, schema = None):
        translator = SQLTranslator(root=self.root, schema=schema, block=None)
        return translator.getResult()

    def __hash__(self):
        prime = 31
        result = 17
        result = prime * result + (0 if self.root is None else (self.root).__hash__())

        # prime = 31
        # result = 17
        # print "calling with a =%d, b= %d, c =%d"%(prime, result, (0 if self.root is None else (self.root).__hash__()))
        # result = self.utils.calc(prime , result , (0 if self.root is None else (self.root).__hash__()))
        return result

    def __eq__(self, obj):
        # if (self == obj):
        #     return True
        if (obj is None):
            return False
        if (self.__class__ != obj.__class__):
            return False

        if (self.root is None):
            if (obj.root is not None):
                return False

        elif (not self.root == obj.root):
            return False
        return True


    def equals(self, obj):
        # if (self == obj):
        #     return True
        if (obj is None):
            return False
        if (self.__class__ != obj.__class__):
            return False

        if (self.root is None):
            if (obj.root is not None):
                return False

        elif (not self.root == obj.root):
            return False
        return True

    #### TODO : public class ParseTreeIterator implements Iterator<Node>
    def nodeToString(self,curr):
        if curr is None :
            return ""
        s = curr.toString() + " -> "
        #print curr.getChildren()
        s += ''.join( [ child.toString()  for child in curr.getChildren()]) + "\n"
        for child in curr.getChildren():
            s += self.nodeToString(child)
        return s


    def getSentence(self):
        sb = []
        first = True
        for node in self:
            if (first):
                sb.append(node.getWord())
                first = False
            else:
                sb.append(" ")
                sb.append(node.getWord())
        return ''.join(sb)

    def toString(self):
        s ="Sentence: " + self.getSentence()+"\n"+self.nodeToString(self.root)
        return s

    def __str__(self):
        s = "Sentence: " + self.getSentence() + "\n" + self.nodeToString(self.root)
        return s


    def getScore(self):
        #print "Parse tree: getScore()"
        return - SyntacticEvaluator().numberOfInvalidNodes(T=self)

    def iterator(self, rootNode):
        return self.ParseTreeIterator(rootNode)

    def __iter__(self):
        #print 123
        self.stack = list()
        self.stack.insert(0, self.root)

        return self

    stack = list()

    def next(self):  # Python 3: def __next__(self)
       # print 4
        if len(self.stack) == 0:
            raise StopIteration
        else:
            curr = self.stack.pop(0)
           # print curr
            if(curr is None):
                print ("Self: ")
                print (self)
            children = curr.getChildren()
            #print children
            for i in range(len(children) - 1, -1, -1):
                self.stack.insert(0, children[i])
                if children[i] is None:
                    print ("hahaha:")
                    print (self)
            return curr


    class ParseTreeIterator:
        stack = list()

        def __init__(self, rootNode):
            self.stack.insert(0, rootNode)

        def hasNext(self):
            if len(self.stack) == 0:
                return False
            return True

        def getNext(self):
            curr = self.stack.pop(0)
            children = curr.getChildren()
            for i in range(len(children)-1,-1,-1):
                self.stack.insert(0,children[i])
            return curr



#
# a = NLParser()
# ParseTree(text="Return the number of authors who published theory papers before 1980 .", parser=a)
