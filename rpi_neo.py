# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

from neopixel import *
import time
class rpi_leds(object):

    def __init__(self,queue):
        self.strip=Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.q = queue;

    def start(self,updateTimeMs,quitEvent):
        self.strip.begin()
        done = False;
        while not done:
            self.update()
            time.sleep(updateTimeMs/1000.0)
            if quitEvent.isSet():
                done = True

    def update(self):
        if self.q.empty() == False:
            frame = self.q.get();
            flatten_list = frame.flatten();
            i = 0;
            print "printing LED list"
            for pixel in flatten_list:
                print "setting pixel {} to ({},{},{})".format(i,pixel[0],pixel[1],pixel[2])
                self.strip.setPixelColor(i,Color(pixel[0],pixel[1],pixel[2]))
            self.strip.show()
