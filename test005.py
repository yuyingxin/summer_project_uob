from pyprocessing import *
from random import random
from Mover import Mover


def setup():
    size(600, 600)
    background(0)
    global mover1, mover2, mover3
    mover1 = Mover(300, 300, color(255, 0, 0))
    mover2 = Mover(100, 100, color(0, 255, 0))
    mover3 = Mover(400, 200, color(0, 0, 255))


def draw():
    global mover1, mover2, mover3
    mover1.update()
    mover2.update()
    mover3.update()
    mover1.display()
    mover2.display()
    mover3.display()


run()

