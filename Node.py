import copy

from model.NodeInfo import NodeInfo
from Utils import Utils

class Node:
    outside = False
    index = 0
    info = None
    word = None
    posTag = None
    parent = None
    children = list()
    isInvalid = False
    utils = None
    def __init__(self, word, posTag, index=0, info=None):
        self.index = index
        self.word = word
        self.posTag = posTag
        self.info = info
        self.outside = False
        self.parent = None
        self.isInvalid = False
        self.children = list()
        self.utils = Utils()

    def cloneNode(self, node):
        if node is None:
            return None

        copy = Node(index=node.index, word=node.word, posTag=node.posTag, info=node.info)

        for child in node.children:
            copyChild = self.cloneNode(child)
            copyChild.parent = copy
            copy.children.append(copyChild)

        return copy

    def clone(self):
        # print "fff"
        # print self.cloneNode(self)
        return self.cloneNode(self)

    def getInfo(self):
        return self.info

    def setInfo(self, info):
        self.info = info

    def getWord(self):
        return self.word

    def setWord(self, word):
        self.word = word

    def getPosTag(self):
        return self.posTag

    def getChildren(self):
        return self.children

    def setChild(self, child):
        self.children.append(child)

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getOutside(self):
        return self.outside

    def setOutside(self, outside):
        self.outside = outside

    def removeChild(self, child):
        self.children = [childeNode for childeNode in self.children if childeNode != child]
        return

    def printNodeArray(self):
        nodes = self.genNodesArray(self)
        for node in nodes:
            print ("type: " + node.getInfo().getType() + " value: " + nodes.getInfo().getValue())

    def genNodesArray(self):
        nodesList = list()
        stack = list()
        stack.insert(0, self)

        while len(stack) != 0:
            curr = stack.pop(-len(stack))
            nodesList.append(curr)
            currChildren = curr.getChildren()
            for i in range(len(currChildren) - 1, -1, -1):
                stack.insert(0, currChildren[i])

        nodes = list()
        for node in nodesList:
            nodes.append(node)

        return nodes

    def __hash__(self):
        prime = 31
        result = 17
        result = prime * result + self.index
        result = prime * result + (0 if (self.posTag is None) else hash(self.posTag))
        result = prime * result + (0 if (self.word is None) else hash(self.word))
        result = prime * result + (0 if (self.info is None) else (self.info).__hash__())

        if self.children is not None:
            for child in self.children:
                # result = self.utils.calc(prime , result , child.__hash__())
                result = prime * result + child.__hash__()
        return result

    def equals(self, obj):

        if obj is None:
            return False
        if not (self.__class__ == obj.__class__):
            return False

        other = obj
        if not self.index == other.index:
            return False

        if not self.word == other.word:
            return False

        if not self.posTag == other.posTag:
            return False

        if not self.info == other.info:
            if (self.info is None) or (other.info is None):
                return False
            if not self.info == other.info:
                return False

        if self.children != other.children:
            if (self.children is None) or (other.children is None):
                return False
            if len(self.children) != len(other.children):
                return False

            if not self.isEqualsNodeList(self.children, other.children):
                return False
        return True

    def isEqualsNodeList(self, list1, list2):
        for node1 in list1:
            if node1 not in list2:
                return False
        return True

    def toString(self):
        s = "( %s ) %s" % (self.index, self.word)
        if not self.info is None:
            s = s + "(" + self.info.getType() + ":" + self.info.getValue() + ")"
        return s

    def __str__(self):
        s = "( %s ) %s" % (self.index, self.word)
        if not self.info is None:
            s = s + "(" + self.info.getType() + ":" + self.info.getValue() + ")"
        return s

    def __eq__(self, obj):

        if obj is None:
            return False
        if not (self.__class__ == obj.__class__):
            return False

        other = obj
        if not self.index == other.index:
            return False

        if not self.word == other.word:
            return False

        if not self.posTag == other.posTag:
            return False

        if not self.info == other.info:
            if (self.info is None) or (other.info is None):
                return False
            if not self.info == other.info:
                return False

        if self.children != other.children:
            if (self.children is None) or (other.children is None):
                return False
            if len(self.children) != len(other.children):
                return False
            if not self.isEqualsNodeList(self.children, other.children):
                return False
        return True
