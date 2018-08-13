from pyprocessing import *

from PathFinder import PathFinder


#def generator(index_doc):

def setup():
    size(800, 600)
    background(0)
    # frameRate(10)
    ellipseMode(CENTER)
    stroke(136, 54, 0, 200)
    smooth()
    global num
    num = 2
    # count = 0
    for i in range(0, num):
        path = PathFinder()
        PathFinder.paths.append(path)


def draw():
    for i in range(0, len(PathFinder.paths)):
        loc = PathFinder.paths[i].location
        lastLoc = PathFinder.paths[i].lastLocation
        # strokeWeight(PathFinder.paths[i].diameter)
        # print(i, "- lastLoc:", lastLoc)
        # print(i, "- loc:", loc)
        noStroke()
        fill(196)   # color of branches
        ellipse(loc.x, loc.y, PathFinder.paths[i].diameter, PathFinder.paths[i].diameter)
        ellipse((loc.x + lastLoc.x)/2, (loc.y + lastLoc.y)/2, PathFinder.paths[i].diameter, PathFinder.paths[i].diameter)
        # line(lastLoc.x, lastLoc.y, loc.x, loc.y)
        PathFinder.paths[i].update()

def mousePressed():
    background(0)
    global num
    PathFinder.paths = []

    for i in range(0, num):
        path = PathFinder()
        PathFinder.paths.append(path)


run()
