import random
import datetime
from pyprocessing import *


class Ant:
    def __init__(self, x, y, r, g, b, hill):
        self.location = PVector(x, y)
        random.seed(datetime.datetime.now())
        self.r = random.randint(r - 2, r + 2)
        self.g = random.randint(g - 2, g + 2)
        self.b = random.randint(b - 2, b + 2)
        self.color = color(self.r, self.g, self.b, 50)
        self.hill = hill
        self.speed = 1 + random.randint(0, 1)
        self.direction = random.randint(0, 360)

    def move(self):
        self.location.x += self.speed * cos(self.direction)
        self.location.y += self.speed * sin(self.direction)
        self.direction = random.randint(0, 360)
        # self.direction = map(noise(self.location.x, self.location.y), 0, 1, -10, 10)

    # def chooseColor(self, col):
        # h = hue(self.color) + hue(get(self.location.x, self.location.y))
        # b = dist(self.location.x, self.location.y, self.hill.location.x, self.hill.location.y)
        # s = saturation(self.color)
        # self.color = color(h, s, b)

    def display(self):
        self.move()
        fill(self.color)
        ellipse(self.location.x, self.location.y, 8, 8)


