import numpy as np

class Node():
    def __init__(self, parent, prior_p):
        self._parent = parent
        self.children = {}  # a map from action to TreeNode
        self._N = 0
        self._Q = 0
        self._u = 0
        self._W = 0
        self._P = prior_p

    def update(self, leaf_value):
        self._N += 1
        self._W += leaf_value
        self._Q = self._W / self._N
    def updateRecursive(self, leaf_value):
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def getValue(self, c_puct):
        self._u = c_puct * self._P * np.sqrt(self._parent._N / (1+self._N))
        return self._Q + self._u
    
    def isLeaf(self):
        return self.children=={}

class MCTS():
    pass