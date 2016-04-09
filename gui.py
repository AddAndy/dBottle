#!/usr/bin/env python

import sys
import time
import random
from threading import Thread
import Queue
from PyQt4.QtGui import *
from PyQt4 import QtCore

class LEDFakeout(QTableWidget):

    def __init__(self,frameBuffer):
        self.frameBuffer = frameBuffer;
        QTableWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.resize(640,1080)
        self.setWindowTitle("dbottle")
        self.setRowCount(30);
        self.setColumnCount(5);

        for c in range(0,5):
            for r in range(0,30):
                self.setItem(r,c,QTableWidgetItem("{},{}".format(r,c)))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateBackground)
        #60 FPS, 1000ms/60 frams
        self.timer.start((1000/60))
        self.show()

    def updateBackground(self):
        if self.frameBuffer.empty() == False:
            frame = self.frameBuffer.get();
            for c in range(0,5):
                for r in range(0,30):
                    tableItem = self.item(r,c);
                    (R,G,B,Bri) = frame.getPixel(r,c).toQuad();
                    tableItem.setBackground(QColor(R,G,B))


if __name__ == '__main__':
    print "Error, please run dBottle.py"
