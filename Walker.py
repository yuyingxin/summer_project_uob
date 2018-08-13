import random

from pyprocessing import *


class Walker:

    def __init__(self):
        self.x = width/2
        self.y = height/2

    def walk(self, t):
        choice = random.randint(0, 1)
        #         #
        #         # if choice == 0:
        #         #     self.x += 1
        #         # elif choice == 1:
        #         #     self.x += -1
        #         # elif choice == 2:
        #         #     self.y += 1
        #         # elif choice == 3:
        #         #     self.y += -1

        if choice == 0:
            self.x = noise(t)
            # self.x = map(self.x, 0, 1, 0, width)
        if choice == 1:
            self.y = noise(t)
            # self.y = map(self.y, 0, 1, 0, height)

        print(self.x)
        print(self.y)

        self.x = constrain(self.x, 0, width-1)
        self.y = constrain(self.y, 0, height-1)

    def display(self):
        fill(0)
        stroke(0)
        ellipse(self.x, self.y, 2, 2)


