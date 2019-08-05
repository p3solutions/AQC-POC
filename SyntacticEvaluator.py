
class SyntacticEvaluator:
    numOfInvalid = 0
    def __init__(self):
        self.numOfInvalid =0

    def checkROOT(self, node):
        numOfInvalid = 0
        children = node.getChildren()
        sizeOfChildren = len(children)

        if (sizeOfChildren == 0):
            numOfInvalid += 1
            node.isInvalid = True
        elif(sizeOfChildren == 1 and (not children[0].getInfo().getType() =="SN")):
            numOfInvalid += 1
            node.isInvalid = True
        elif(sizeOfChildren > 1):
            if (not (children[0].getInfo().getType() =="SN")):
                numOfInvalid += 1
                node.isInvalid = True
            else:
                for j in range(1, sizeOfChildren):
                    if (not (children[j].getInfo().getType() =="ON")):
                        numOfInvalid += 1
                        node.isInvalid = True
        return numOfInvalid


    def checkSN(self, node):
        numOfInvalid = 0
        children = node.getChildren()
        sizeOfChildren = len(children)

        if (sizeOfChildren != 1):
            numOfInvalid += 1
            node.isInvalid = True
        else:
            childType = children[0].getInfo().getType()
            if (not(childType =="NN" or childType =="FN")):
                numOfInvalid += 1
                node.isInvalid = True

        return numOfInvalid


    def checkON(self, node):
        numOfInvalid = 0
        parentType = node.getParent().getInfo().getType()
        children = node.getChildren()
        sizeOfChildren = len(children)

        if (parentType =="ROOT"):
            if (sizeOfChildren != 2):
                numOfInvalid += 1
                node.isInvalid = True
            else:
                for j in range(0,sizeOfChildren):
                    childType = children[j].getInfo().getType()
                    if (j == 0):
                        if (not(childType =="NN" or childType =="FN")):
                            numOfInvalid += 1
                            node.isInvalid = True
                            break
                    elif j == 1:
                        if (childType =="ON"):
                            numOfInvalid += 1
                            node.isInvalid = True
                            break
        elif (parentType =="NN"):
            if (sizeOfChildren != 1):
                numOfInvalid += 1;
                node.isInvalid = True;
            elif (not children[0].getInfo().getType() =="VN"):
                numOfInvalid += 1;
                node.isInvalid = True

        return numOfInvalid

    def checkNN(self, node):
        numOfInvalid = 0
        parentType = node.getParent().getInfo().getType()
        children = node.getChildren()
        sizeOfChildren = len(children)

        if (parentType =="NN"):
            if (sizeOfChildren != 0):
                numOfInvalid += 1;
                node.isInvalid = True
        elif (parentType =="SN" or parentType =="FN" or parentType =="ON"):
            if (sizeOfChildren != 0):
                for j in range(0,sizeOfChildren):
                    childType = children[j].getInfo().getType()
                    if (not(childType =="NN" or childType =="VN" or childType =="ON")):
                        numOfInvalid += 1;
                        node.isInvalid = True
                        break

        return numOfInvalid


    def checkVN(self, node):
        numOfInvalid = 0
        children = node.getChildren();
        sizeOfChildren = len(children)
        if (sizeOfChildren != 0):
            numOfInvalid += 1;
            node.isInvalid = True

        return numOfInvalid


    def checkFN(self, node):
        numOfInvalid = 0
        parentType = node.getParent().getInfo().getType()
        children = node.getChildren()
        sizeOfChildren = len(children)
        if (sizeOfChildren == 0):
            if (not parentType =="ON"):
                numOfInvalid += 1;
                node.isInvalid = True;
        elif (sizeOfChildren == 1):
            childType = children[0].getInfo().getType()
            if (not(parentType =="ON" or parentType =="SN")):
                numOfInvalid += 1;
                node.isInvalid = True
            elif (not childType =="NN"):
                numOfInvalid += 1;
                node.isInvalid = True
        else:
            numOfInvalid += 1;
            node.isInvalid = True
        return numOfInvalid

    def numberOfInvalidNodes (self, T):
        numOfInvalid = 0
        # print T
        for curNode in T:
            # print "Node"
            # print curNode
            curType = curNode.getInfo().getType()
            if (curType =="ROOT"):
                numOfInvalid = numOfInvalid + self.checkROOT(curNode)
            if (curType =="SN"):
                numOfInvalid = numOfInvalid + self.checkSN(curNode)
            elif (curType =="ON"):
                numOfInvalid = numOfInvalid + self.checkON(curNode)
            elif (curType =="NN"):
                numOfInvalid = numOfInvalid + self.checkNN(curNode)
            elif (curType =="VN"):
                numOfInvalid = numOfInvalid + self.checkVN(curNode)
            elif (curType =="FN"):
                numOfInvalid = numOfInvalid + self.checkFN(curNode)

        return numOfInvalid

