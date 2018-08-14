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
        global subInterface, articleNum, entityNum, dateFrom, dateTo
        articleNum = int(subInterface.edArticleNum.text())
        entityNum = int(subInterface.edEntityNum.text())
        dateFrom = [subInterface.edYearFrom.text(), subInterface.edMonthFrom.text(), subInterface.edDayFrom.text()]
        dateTo = [subInterface.edYearTo.text(), subInterface.edMonthTo.text(), subInterface.edDayTo.text()]
        dateFrom = "-".join(dateFrom)
        dateTo = "-".join(dateTo)
        run()


def mousePressed():
    global isPlaying
    isPlaying = not isPlaying


def setup():
    size(960, 720)
    noStroke()
    global agents, emotionCount, isPlaying, isTextFollowing, isImageShowing, articleNum, entityNum, dateFrom, dateTo, \
        imagePaths, imageWidths, imageHeights, titles
    isPlaying = True
    isTextFollowing = False
    isImageShowing = False
    agents = []

    # Extracting features
    nlu = nluInit()
    emotionList, entityList, relevanceList, imagePaths, titles = featureExtract(nlu, articleNum, entityNum, dateFrom,
                                                                                dateTo)

    # Compress images
    compressImage(imagePaths)

    #  Parsing the responses
    groupSizes, emotionIndex, emotionCount, emotionLevel = paramExtract(entityList, emotionList)

    for i in range(0, articleNum):
        agent = Agent(emotionIndex[i], emotionLevel[i], titles[i], imagePaths[i])
        agents.append(agent)


def draw():
    global agents, emotionCount, isPlaying, isTextFollowing, isImageShowing, imagePaths, imageWidths, imageHeights,\
        titles
    background(255)
    smooth()
    labelDisplay(emotionCount)

    myMouse = PVector(pmouse.x, pmouse.y)

    # Stop the movement by mousePressed
    if not isPlaying:
        for i in range(0, len(agents)):
            agents[i].display()
            agents[i].detailDisplay(myMouse=myMouse, agents=agents)
    else:
        for i in range(0, len(agents)):
            agents[i].applyBehaviour(agents, myMouse)
            agents[i].borders()
            agents[i].update()
            agents[i].display()
            agents[i].detailDisplay(myMouse=myMouse, agents=agents)


if __name__ == '__main__':
    if canvas.window != None:
        # get rid of window created on an earlier call to size
        canvas.window.close()
        canvas.window = None
    app = QApplication(sys.argv)
    global subInterface
    subInterface = SubInterface()
    sys.exit(app.exec_())



