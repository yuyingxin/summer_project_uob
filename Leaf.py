
import random

from pyprocessing import *


class Leaf:
    def __init__(self):
        self.pos = PVector(random.uniform(0, width), random.uniform(0, height))

    def display(self):
        fill(255)
        noStroke()
        ellipse(self.pos.x, self.pos.y, 4, 4)
