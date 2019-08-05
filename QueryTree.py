from Queue import PriorityQueue

class QueryTree:
    results = list()
    def __init__(self,T = None):
        if T is None:
            return
        else:
            self.results = list()
            Q = PriorityQueue()
            Q.put(T)
            H = dict()
            H[self.hashing(T)] = T
            T.setEdit(0)

            while not Q.empty():
                oriTree = Q.poll()
                treeList = self.adjuster(oriTree)
                treeScore = self.evaluate(oriTree)
                for i in range(0,len(treeList)):
                    currentTree = treeList[i]
                    hashValue = self.hashing(currentTree)
                    if (oriTree.getEdit() < 10 and not H.containsKey(hashValue)):
                        H[hashValue]  = currentTree
                        currentTree.setEdit(oriTree.getEdit() + 1)
                        if (self.evaluate(currentTree) >= treeScore):
                            Q.put(currentTree)
                            self.results.append(currentTree)


    def  adjuster (self, T):
        treeList = list()
        #TODO: generate all possible parse trees in one subtree move operation
        return treeList

    def evaluate (self, T):
        score = 0

        # TODO: generate the evaluation criteria
        return score

    def hashing (self, T):
        hashValue = 0
        #TODO: how to get a reasonable hash value for each parse tree (with different node orders)
        return hashValue