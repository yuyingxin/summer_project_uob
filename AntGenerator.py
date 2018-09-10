import random
from pyprocessing import *

from Ant import Ant
from Hill import Hill


def setup():
    size(600, 600)
    smooth()
    noStroke()
    # colorMode(HSB)
    # background(0, 1, 255)
    background(255)
    global t, ants, hills
    t = 0
    hills = []
    ants = []
    for i in range(0, 4):
        hill = Hill()
        print(hill.r, hill.g, hill.b)
        ant = Ant(hill.location.x, hill.location.y, hill.r, hill.g, hill.b, hill)
        hills.append(hill)
        ants.append(ant)


def draw():
    global t, ants, hills
    t += 1
    for i in range(0, len(ants)):
        ants[i].display()
    for j in range(0, len(hills)):
        # hills[j].display()
        if t % (2 * len(hills)) == 0:
            ant = Ant(hills[j].location.x, hills[j].location.y, hills[j].r, hills[j].g, hills[j].b, hills[j])
            ants.append(ant)
            print(ant.r, ant.g, ant.b)
    if t % 120 == 0:
        hill = Hill()
        hills.append(hill)
    while len(ants) > 300:
        num = random.randint(0, len(ants))
        del ants[num - 1]

    # if t % 20 == 0:
    #     for i in range(0, len(ants)):
    #         for j in range(0, len(ants)):
    #             d = dist(ants[i].location.x, ants[j].location.x, ants[i].location.y, ants[j].location.y)
    #             if 1 < d < 100:
    #                 meanLoc = PVector((ants[i].location.x + ants[j].location.x) / 2,
    #                                   (ants[i].location.y + ants[j].location.y) / 2)
    #
    #                 meanCol = [(ants[i].hill.colorElements[0] + ants[j].hill.colorElements[0]) / 2,
    #                            (ants[i].hill.colorElements[1] + ants[j].hill.colorElements[1]) / 2,
    #                            (ants[i].hill.colorElements[2] + ants[j].hill.colorElements[2]) / 2]
    #
    #                 hill = Hill(meanLoc, meanCol[0], meanCol[1], meanCol[2])
    #                 hills.append(hill)


run()

