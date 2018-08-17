from Interface import Interface
from pyprocessing import *
from Agent import Agent
from Utils import *
from pyprocessing import *
from PyQt5.QtWidgets import QApplication
import sys


class SubInterface(Interface):
    @classmethod
    def on_click(cls):
        global subInterface, articleNum, dateFrom, dateTo
        articleNum = int(subInterface.edArticleNum.text())
        dateFrom = [subInterface.edYearFrom.text(), subInterface.edMonthFrom.text(), subInterface.edDayFrom.text()]
        dateTo = [subInterface.edYearTo.text(), subInterface.edMonthTo.text(), subInterface.edDayTo.text()]
        dateFrom = "-".join(dateFrom)
        dateTo = "-".join(dateTo)
        run()


def keyPressed():
    global isTopicFollowing
    isTopicFollowing = not isTopicFollowing


def mousePressed():
    global isPlaying
    isPlaying = not isPlaying


def setup():
    size(600, 400)
    noStroke()
    global agents, emotionCount, isPlaying, isTopicFollowing, articleNum, dateFrom, dateTo, imagePaths, titles
    isPlaying = False
    isTopicFollowing = False
    agents = []

    # Extracting features
    nlu = nluInit()
    emotionList, entityList, imagePaths, titles = featureExtract(nlu, articleNum, dateFrom, dateTo)

    # Compress images
    compressImage(imagePaths)

    #  Parsing the responses
    emotionIndex, emotionCount, emotionLevel = paramExtract(emotionList)

    for i in range(0, articleNum):
        agent = Agent(emotionIndex[i], emotionLevel[i], titles[i], imagePaths[i], entityList[i])
        agents.append(agent)


def draw():
    global agents, emotionCount, isPlaying, isTopicFollowing, imagePaths, titles
    background(255)
    smooth()
    labelDisplay(emotionCount)

    myMouse = PVector(pmouse.x, pmouse.y)

    # Stop the movement by mousePressed
    if not isPlaying:
        for i in range(0, len(agents)):
            agents[i].display()
            agents[i].detailDisplay(myMouse=myMouse, agents=agents)
            if isTopicFollowing:
                agents[i].topicFollow()
    else:
        for i in range(0, len(agents)):
            agents[i].applyBehaviour(agents, myMouse)
            agents[i].borders()
            agents[i].update()
            agents[i].display()
            agents[i].detailDisplay(myMouse=myMouse, agents=agents)
            if isTopicFollowing:
                agents[i].topicFollow()


if __name__ == '__main__':
    if canvas.window != None:
        # get rid of window created on an earlier call to size
        canvas.window.close()
        canvas.window = None
    app = QApplication(sys.argv)
    global subInterface
    subInterface = SubInterface()
    sys.exit(app.exec_())



