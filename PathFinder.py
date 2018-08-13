import random
from pyprocessing import *


class PathFinder:

    paths = []

    def __init__(self, parent = None):
        if parent is None:
            self.location = PVector(width/2, height)
            self.lastLocation = PVector(self.location.x, self.location.y)
            self.velocity = PVector(0, -10)
            self.diameter = random.uniform(20, 30)
            self.isFinished = False
        else:
            self.location = parent.location.get()
            # print("parent.location:", parent.location)
            self.lastLocation = parent.lastLocation.get()
            # print("parent.lastLocation:", parent.lastLocation)
            self.velocity = parent.velocity.get()
            self.diameter = parent.diameter * 0.7
            self.isFinished = parent.isFinished
            parent.diameter = self.diameter

    def update(self):
        if self.location.x > -10 and self.location.x < width + 10 and self.location.y > -10 and self.location.y < height + 10:
            self.lastLocation.set(self.location.x, self.location.y)
            if self.diameter > 0.8:
                # count += 1
                bump = PVector(random.uniform(-1, 1), random.uniform(-1, 1))
                # print(self.velocity)
                self.velocity.normalize()
                # print(self.velocity)
                bump.mult(0.2)
                self.velocity.mult(0.7)
                self.velocity.add(bump)
                self.velocity.mult(random.uniform(4, 8))
                self.lastLocation = PVector(self.location)
                # print("lastLocation - in update:", self.lastLocation)
                self.location.add(self.velocity)
                # print("location - in update:", self.location)
                if self.diameter < 5 and random.uniform(0, 1) < 0.2:
                    noStroke()
                    fill(102, 194, 255, 100)    # color of leaves (163, 255, 102)
                    ellipse(self.location.x, self.location.y, 20, 20)
                    # stroke(136, 54, 0, 200)
                    fill(196)   # color of branches
                if random.uniform(0, 1) < 0.05:
                    path = PathFinder(self)
                    PathFinder.paths.append(path)
                    # fill(255, 0, 0, 200)    # color of flowers
                    # ellipse(self.location.x, self.location.y, 5, 5)
                    # # stroke(136, 54, 0, 200)
                    # fill(196)   # color of branches
                # else:
                    # if self.isFinished is False:
                    #     self.isFinished = True
                    # noStroke()
                    # fill(240, 230, 150, 100)
                    # ellipse(self.location.x, self.location.y, 10, 10)
                    # stroke(200, 0, 0, 200)




