#!/usr/bin/env python

from threading import Thread,Event
import signal
import time
import Queue
import sys
import random
from copy import deepcopy
#from neopixel import *
global debug;
debug = False
if debug:
    import gui
else:
    import rpi_neo
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
            self.pixels = deepcopy(previousFrame.pixels);

    def clear(self):
        for m in range(self.rows):
            for n in range(self.columns):
                pixels[m][n].clear();

    def getPixel(self,r,c):
        return self.pixels[r][c];

    def flatten(self):
        i=0;
        flat = [(0,0,0,0)]*150
        for r in range(self.rows):
            for c in range(self.columns):
                i = (150-30*c-r)-1
                flat[i] = self.getPixel(r,c).toQuad();
        return flat;

class dbFrame(Frame):
    def __init__(self,maxLevel,previousFrame=None):
        super(dbFrame,self).__init__(previousFrame);
        self.maxLevel = maxLevel;

    def setColourByLevel(self,level):
        p = Pixel(255,255,255,0);
        if 0 < level < 18:
            p = Pixel(0,255,0,0)
        elif 18 < level < 25:
            p = Pixel(255,255,0,0)
        elif 25 < level:
            p = Pixel(255,0,0,0)
        return p

    def setLevel(self,level):
        """ find our what row level corisponds to by finding out on a scale of 0 to maxLevel where it exist"""
        levelpx = min(round((float(level)/float(self.maxLevel))*self.rows),self.rows)
        #print "setting levelPX to {}/{} = {}".format(level,self.maxLevel,levelpx)
        for i in range(0,self.rows):
            #print 'checking row: ',i;
            if (i > levelpx):
                self.pixels[i] = [Pixel(255,255,255,0) for x in range(self.columns)]
            else:
                self.pixels[i] = [self.setColourByLevel(i) for x in range(self.columns)]

class dbStepFrame(dbFrame):
    def __init__(self,maxLevel,previousFrame,stepValue=1):
        super(dbStepFrame,self).__init__(maxLevel,previousFrame);
        if previousFrame == None or not hasattr(previousFrame,'currentLevel'):
            self.currentLevel = 0;
        else:
            self.currentLevel = previousFrame.currentLevel;
        self.stepValue = stepValue;

    def setLevel(self,level):
        stepvalue = min(self.stepValue,abs(level-self.currentLevel))

        if (level > self.currentLevel):
            self.currentLevel +=stepvalue
            self.currentLevel = min(self.currentLevel,self.maxLevel)
        elif(level < self.currentLevel):
            self.currentLevel -=stepvalue;
            self.currentLevel = max(self.currentLevel,0)

        super(dbStepFrame,self).setLevel(self.currentLevel)

def signal_handler(signal,frame):
    print ("Ctrl + C detected")
    global quitEvent
    quitEvent.set();

def getMicLevel():
    "returns a db value from the mic"
    return random.randint(0,100);

def isAlive():
    global debug
    global quitEvent
    if debug is True:
        global guiThread
        return guiThread.isAlive();
    elif quitEvent.isSet():
        return False
    else:
        return True

def main():
    maxSize = 0
    frameBuffer = Queue.Queue(maxsize=maxSize)
    signal.signal(signal.SIGINT, signal_handler)
    global quitEvent
    quitEvent = Event();

    if debug:
        global guiThread
        guiThread= Thread(target=gui.startGUI,args=(frameBuffer,quitEvent,))
        guiThread.start();

    leds = rpi_neo.rpi_leds(frameBuffer)
    ledThread = Thread(target=leds.start,args=(50,quitEvent,))
    ledThread.start()
    previousFrame = None;
    #main loop
    while isAlive(): #guiThread.isAlive():
        #Generate a frame, add it to buffer
        frame = dbStepFrame(100,previousFrame,stepValue=5)
        miclvl = getMicLevel();
        #print "getMicLevel=",miclvl
        frame.setLevel(miclvl)
        # push to buffer
        frameBuffer.put(frame,False)
        previousFrame = frame;

        time.sleep(1/60.0)
        print frameBuffer.qsize();
    sys.exit(0);

if __name__ == '__main__':

    #strip = Adafruit_NeoPixel()
    main()
