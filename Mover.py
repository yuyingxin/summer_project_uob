import random

from pyprocessing import *


class Mover:

    def __init__(self, x, y, mover_color):
        self.loc = PVector(x, y)
        self.color = mover_color
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)

    def update(self):
        self.acc.x = random.random()
        self.acc.y = random.random()
        self.acc.x = map(self.acc.x, 0, 1, -0.01, 0.01)
        self.acc.y = map(self.acc.y, 0, 1, -0.01, 0.01)
        self.vel.add(self.acc)
        self.loc.add(self.vel)

    def display(self):
        fill(self.color)
        noStroke()
        ellipse(self.loc.x, self.loc.y, 5, 5)