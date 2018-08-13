from pyprocessing import *

from Branch import Branch
from Leaf import Leaf


class Tree:

    def __init__(self):
        self.leaves = []
        self.branches = []
        for i in range(0, 100):
            leaf = Leaf()
            self.leaves.append(leaf)
        position = PVector(width/2, height/2)
        direction = PVector(0, -1)
        self.root = Branch(None, position, direction)
        self.branches.append(self.root)

    def display(self):
        for i in range(0, len(self.leaves)):
            self.leaves[i].display()