#!/usr/bin/env python

#This is the base file for the dBottle project for the 2016 ling awards
#this is the main file.
class pixel(object):
    self.red=0
    self.green=0
    self.blue =0
    self.brightness = 0

    def __init__(self,red,green,blue,brightness):
        self.set(red,green,blue,brightness)

    def set(self,red,green,blue,brightness):
        self.red = red;
        self.green = green;
        self.blue = blue;
        self.brightness=brightness;

    def clear(self):
        self.set(0,0,0,0)

    def toQuad(self):
        return (self.red,self.green,self.blue,self.brightness)

class frame(object):
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
    self.rows = 30;
    self.columns=5;
    self.pixels = []
    def ___init__(self,previousFrame=None):
        self.pixels = previousFrame.pixels;
        if (previousFrame == None):
            for m in self.rows:
                for n in self.columns:
                    pixels[m][n] = new pixel(0,0,0,0)
    def clear(self):
        for m in self.rows:
            for n in self.columns:
                pixels[m][n].clear();

    def flatten(self):
        i=0;
        for m in self.rows:
            for n in self.columns:
                i = (150-30*n-m)-1
                flat[i] = self.pixels[m][n].toQuad();
        return flat;
