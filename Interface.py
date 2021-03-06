import os
import shutil

from PyQt5.QtGui import QValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QLabel, QGroupBox, QGridLayout, \
    QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtCore import pyqtSlot, Qt
import sys
import datetime


class Interface(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'News Visualization'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400

        # Initialize the LineEdit
        today = datetime.date.today()
        self.edYearFrom = QLineEdit(str(today.year))
        self.edMonthFrom = QLineEdit(str(today.month).zfill(2))
        yesterday = today - datetime.timedelta(days=2)
        self.edDayFrom = QLineEdit(str(yesterday.day).zfill(2))

        self.edYearTo = QLineEdit(str(today.year))
        self.edMonthTo = QLineEdit(str(today.month).zfill(2))
        self.edDayTo = QLineEdit(str(today.day).zfill(2))

        self.edArticleNum = QLineEdit("30")
        validator = QIntValidator(0, 50)
        self.edArticleNum.setValidator(validator)

        self.edKeywordSearch = QLineEdit("")
        # self.edKeywordSearch.setDisabled(True)

        self.gbDate = QGroupBox("Date")
        self.gbNum = QGroupBox("Input")
        self.hbCreate = QHBoxLayout()
        self.initUI()

    def initUI(self):
        # Set the window location and size
        self.setGeometry(self.left, self.top, self.width, self.height)  # location of top-left and bottom-right
        self.setWindowTitle(self.title)

        # Create button
        btnCreate = QPushButton('Create', self)
        btnCreate.setToolTip('Click to create the art visual for news')
        btnCreate.clicked.connect(self.on_click)

        self.createGridLayoutDate()
        self.createGridLayoutNum()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.gbDate)
        windowLayout.addWidget(self.gbNum)
        windowLayout.addWidget(btnCreate, alignment=Qt.AlignRight)
        self.setLayout(windowLayout)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print("clicked!")

    def createGridLayoutDate(self):
        # The grid Layout of inputting date period
        grid = QGridLayout()
        grid.setColumnStretch(0, 4)
        grid.setColumnStretch(1, 4)
        grid.setColumnStretch(2, 1)
        grid.setColumnStretch(3, 2)
        grid.setColumnStretch(4, 1)
        grid.setColumnStretch(5, 3)

        grid.addWidget(QLabel("From:  "), 0, 0)
        grid.addWidget(self.edYearFrom, 0, 1)
        grid.addWidget(QLabel("-"), 0, 2)
        grid.addWidget(self.edMonthFrom, 0, 3)
        grid.addWidget(QLabel("-"), 0, 4)
        grid.addWidget(self.edDayFrom, 0, 5)

        grid.addWidget(QLabel("To:  "), 1, 0)
        grid.addWidget(self.edYearTo, 1, 1)
        grid.addWidget(QLabel("-"), 1, 2)
        grid.addWidget(self.edMonthTo, 1, 3)
        grid.addWidget(QLabel("-"), 1, 4)
        grid.addWidget(self.edDayTo, 1, 5)

        self.gbDate.setLayout(grid)

    def createGridLayoutNum(self):
        # The gird layout of inputting other parameters
        grid = QGridLayout()
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 1)

        grid.addWidget(QLabel("News articles (max: 50):"), 0, 0)
        grid.addWidget(self.edArticleNum, 0, 1)

        grid.addWidget(QLabel("Keyword search"), 1, 0)
        grid.addWidget(self.edKeywordSearch, 1, 1)

        self.gbNum.setLayout(grid)

    def closeEvent(self, QCloseEvent):
        """
        override closeEvent method to run some code when window is closed
        :param QCloseEvent: event occurred when close() is called
        :return: None
        """
        downloadPath = "downloads"
        if os.path.exists(downloadPath):
            shutil.rmtree(downloadPath)
        # os.rmdir("downloads")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())
