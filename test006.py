from pyprocessing import *

from Tree import Tree


def setup():
    size(400, 400)
    global tree, max_dist, min_dist
    tree = Tree()
    max_dist = 500
    min_dist = 10


def draw():
    background(51)
    global tree
    tree.display()


run()