from pyprocessing import *
from Agent import Agent
import random


def setup():
    size(600, 400)
    noStroke()
    global agents
    agents = []
    agentType = random.randint(0, 3)
    for i in range(0, 50):
        agent = Agent(agentType)
        agents.append(agent)
    # frameRate(2)


def draw():
    background(255)
    myMouse = PVector(pmouse.x, pmouse.y)

    # fill(200)
    # stroke(0)
    # strokeWeight(2)
    # ellipse(myMouse.x, myMouse.y, 48, 48)

    global agents
    for i in range(0, len(agents)):
        agents[i].applyBehaviour(agents, myMouse)
        agents[i].borders()
        agents[i].update()
        agents[i].display()


run()
