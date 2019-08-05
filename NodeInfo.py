from Utils import Utils

class NodeInfo:
    type = None
    value = None
    score = 1.0
    utils = None

    def __init__(self, type, value, score=1.0):
        self.type = type
        self.value = value
        self.score = score
        self.utils =Utils()

    def getType(self):
        return self.type

    def getScore(self):
        return self.score

    def getValue(self):
        return self.value

    @staticmethod
    def reverseScoreComparator(a, b):
        if a.score < b.score:
            return 1
        elif a.score > b.score:
            return -1
        else:
            return 0

    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + (0 if self.type is None else hash(self.type))
        result = prime * result + (0 if self.value is None else hash(self.value))

        return result

    def __eq__(self, other):
        # if self == other:
        #     return True
        if other is None:
            return False

        if not (self.__class__ == other.__class__):
            return False

        if self.type is None:
            if other.type is not None:
                return False
        elif self.type != other.type:
            return False
        if self.value is None:
            if other.value is not None:
                return False
        elif self.value != other.value:
            return False
        return True

    def ExactSameSchema(self, other):
        if self.type is None or \
                        other.getType() is None or \
                        self.value is None or \
                        other.getValue() is None:
            return False

        if self.type == other.getType() and self.value == other.getValue():
            return True

        return False

    def sameSchema(self, other):
        if self.type is None or other.getType() is None or self.value is None or other.getValue() is None:
            return False

        try:
            indexOfDot_Other = other.getValue().index('.')
        except ValueError:
            indexOfDot_Other = -1

        try:
            indexOfDot = self.value.index('.')
        except ValueError:
            indexOfDot = -1

        if indexOfDot_Other == -1:
            indexOfDot_Other = len(other.getValue())

        if indexOfDot == -1:
            indexOfDot = len(self.value)

        if other.getValue()[0 : indexOfDot_Other - 1] == self.value[0 : indexOfDot - 1]:
            return True

        return False
