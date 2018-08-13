import random
from pyprocessing import *
import datetime


class Hill:
    def __init__(self):
        self.location = PVector(random.uniform(20, 580), random.uniform(20, 580))
        self.hillSize = 10
        # self.colorElements = [h, s, b]
        # h = random.randint(0, 360)
        # s = random.randint(0, 100)
        # b = random.randint(20, 200)
        # self.color = color(h, s, b, 30)
        palette = [(166, 158, 176), (239, 239, 242), (242, 226, 205), (218, 218, 227), (20, 20, 20)]
        random.seed(datetime.datetime.now())
        choice = random.randint(0, 4)
        self.r = random.randint(palette[choice][0] - 5, palette[choice][0] + 5)
        self.g = random.randint(palette[choice][1] - 5, palette[choice][1] + 5)
        self.b = random.randint(palette[choice][2] - 5, palette[choice][2] + 5)
        self.color = color(self.r, self.g, self.b, 50)

    def display(self):
        fill(self.color)
        ellipse(self.location.x, self.location.y, self.hillSize, self.hillSize)
