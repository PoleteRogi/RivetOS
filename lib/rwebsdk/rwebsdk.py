
#* -----------------
#* | Rivet Web SDK |
#* -----------------

#? Allows for web rendering on Rivet apps.

#! This is trash, I have to learn another way.

# rwebsdk.py [URL] [X] [Y] [WIDTH] [HEIGHT]

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtGui

import sys

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.page().profile().setHttpUserAgent("Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30")
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.browser.setUrl(QUrl(sys.argv[1]))

        screen_resolution = app.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()

        self.move(int(sys.argv[2]) + int(width / 2 - 400 / 2), int(sys.argv[3]) + int(height / 2 - 800 / 2))
        self.resize(int(sys.argv[4]), int(sys.argv[5]))

        self.setCentralWidget(self.browser)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.show()

app = QApplication(sys.argv)
window = MainWindow()

app.exec_()