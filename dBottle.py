#!/usr/bin/env python

from threading import Thread,Event
import signal
import time
import Queue
from PyQt4.QtGui import *
from PyQt4 import QtCore
import sys
import random
#local files
import gui

#This is the base file for the dBottle project for the 2016 ling awards
#this is the main file.
class Pixel(object):
    def __init__(self,red,green,blue,brightness):
        self.red = red;
        self.green = green;
        self.blue = blue;
        self.brightness = brightness;
        self.set(red,green,blue,brightness)

    def set(self,red,green,blue,brightness):
        self.red = red;
        self.green = green;
        self.blue = blue;
        self.brightness = brightness;

    def clear(self):
        self.set(255,255,255,0)

    def toQuad(self):
        return (self.red,self.green,self.blue,self.brightness)

class Frame(object):
    """
    This is the frame object that defines 1 frame of the bottle
    pixels is the 5x30 struct of RGB-A pairs
    Frame linearizes for sending ot the LED string
    150 120  90  60  30
    149 119  89  59  29
    ... ... ... ... ...
    122  92  62  32   2
    121  91  61  31   1

    The pixels are stored by
    (0,0)  (0,1)  (0,2)  (0,3)  (0,4)
    (1,0)  (1,1)  (1,2)  (1,3)  (1,4)
    ...    ...    ...    ...    ...
    (28,0) (28,1) (28,2) (28,3) (28,4)
    (29,0) (29,1) (29,2) (29,3) (29,4)

    (150-(30*(column))-row)-1
    """
    rows = 30;
    columns=5;
    pixels = [[]]
    def __init__(self,previousFrame=None):
        if (previousFrame == None):
            self.pixels = [[Pixel(0,255,0,0) for x in range(self.columns)] for x in range(self.rows)]
        else:
            self.pixels = previousFrame.pixels;


    def clear(self):
        for m in self.rows:
            for n in self.columns:
                pixels[m][n].clear();

    def getPixel(self,r,c):
        return self.pixels[r][c];

    def flatten(self):
        i=0;
        for m in self.rows:
            for n in self.columns:
                i = (150-30*n-m)-1
                flat[i] = self.pixels[m][n].toQuad();
        return flat;

class dbFrame(Frame):
    def __init__(self,maxLevel,previousFrame=None):
        super(dbFrame,self).__init__(previousFrame);
        self.maxLevel = maxLevel;

    def setLevel(self,level):
        """ find our what row level corisponds to by finding out on a scale of 0 to maxLevel where it exist"""
        levelpx = min(round((float(level)/float(self.maxLevel))*self.rows),self.rows)
        print "setting levelPX to {}/{} = {}".format(level,self.maxLevel,levelpx)
        for i in range(0,self.rows):
            print 'checking row: ',i;
            if (i > levelpx):
                self.pixels[i] = [Pixel(255,255,255,0) for x in range(self.columns)]
            else:
                self.pixels[i] = [Pixel(0,255,0,0) for x in range(self.columns)]
class dbStepFrame(dbFrame):
    def __init__(self,maxLevel,previousFrame):
        super(dbFrame,self).__init__(maxLevel,previousFrame);
        if previousFrame == None or not previousFrame.has_attr('curLevel'):
            self.curLevel = 0;
        else:
            self.curLevel = previousFrame.curLevel;
    def setLevel(self,level):
        if (level > self.curLevel):
            self.currentLevel +=1;
        else (level < self.curLevel):
            self.currentLevel -=1;

def startGUI(frameBuffer,quitEvent):
    a = QApplication(sys.argv)
    main = gui.LEDFakeout(frameBuffer);
    main.show();
    while not quitEvent.isSet():
        a.processEvents();
    print "Quit Event Detected, Terminating"
    a.exit()

    return;

def signal_handler(signal,frame):
    print ("Ctrl + C detected")
    global quitEvent
    quitEvent.set();

def getMicLevel():
    "returns a db value from the mic"
    return random.randint(0,100);
def main():
    maxSize = 3600
    frameBuffer = Queue.Queue(maxsize=maxSize)
    global quitEvent
    quitEvent = Event();
    signal.signal(signal.SIGINT, signal_handler)

    guiThread= Thread(target=startGUI,args=(frameBuffer,quitEvent,))
    guiThread.start();
    previousFrame = None;
    #main loop
    while guiThread.isAlive():
        #Generate a frame, add it to buffer
        frame = dbFrame(100,previousFrame)
        miclvl = getMicLevel();
        print "getMicLevel=",miclvl
        frame.setLevel(miclvl)
        # push to buffer
        frameBuffer.put(frame,False)
        previousFrame = frame;
        time.sleep(1)
    sys.exit(0);

if __name__ == '__main__':
    main()
