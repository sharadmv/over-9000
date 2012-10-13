from SimpleCV import *

import time
import urllib2 as url
import os
import socket

from urllib import urlretrieve

CAMERA_PROPERTIES = {'width':80, 'height':60}

class HandExtractor:

    def __init__(self):
        self.camera = Camera(prop_set=CAMERA_PROPERTIES)
        self.buffer = []
        self.difference = []
        # the number of past points do we keep
        self.length = 20

        #testing code
        self.penalty = 3
        self.count = 3
        self.current_direction = None

    def start(self):
        while True:
            f = self.camera.getImage()
            self.f = f.copy()
            self.f.show()
            hand = self.process_frame(f)
            if hand:
                self.process_hand(hand)
                gesture = self.get_gesture()
                if gesture:
                    self.trigger_gesture(gesture)
                    #time.sleep(0.02)

    def get_gesture(self):
        if self.count >= 7:
            self.penalty = 0
            self.count = 0
            return self.current_direction

    def process_hand(self, hand):
        if (len(self.buffer) > self.length):
            self.buffer.pop(0)
            self.difference.pop(0)

        if len(self.buffer) > 0:
            diff = (hand[0] - self.buffer[len(self.buffer)-1][0],
                    hand[1] - self.buffer[len(self.buffer)-1][1])
            self.difference.append(diff)

        self.buffer.append(hand)
        print(self.count)

        if self.difference:
            if self.current_direction == "left":
                if diff[0] > 0:
                    self.count += 1
                else:
                    self.penalty += 1

            elif self.current_direction == "right":
                if diff[0] < 0:
                    self.count += 1
                else:
                    self.penalty += 1

            else:
                if diff[0] > 0:
                    self.current_direction = "left"
                else:
                    self.current_direction = "right"

            if self.penalty == 3:
                self.penalty = 0
                self.count = 0
                self.current_direction = None

    def process_frame(self, image):
        #segment = HaarCascade("face.xml")
        #face = image.findHaarFeatures(segment)

       #for j in xrange(120):
       #    for i in xrange(160):
       #        h,s,v = image[i,j]
       #        if v>= 15 and v<=250 and h>=3 and h<=33:
       #            image[i,j] = (100,0,0)
       #        else:
       #            image[i,j] = (0,0,100)

        image = image.getSkintoneMask(0)
        blobs = image.findBlobs()
        if blobs:
            x,y = blobs[-1].centroid()
            """
            for b in blobs:
                b.drawHull(color=Color.GREEN,width=3,alpha=128)

            circleLayer = DrawingLayer((image.width, image.height))
            circleLayer.circle((x,y), 20, Color.RED, True)
            image.addDrawingLayer(circleLayer)
            image.applyLayers()
            image.show()
            """
            return (x,y)

    def trigger_gesture(self, gesture):
        #url.urlopen('http://localhost:8080/api/'+gesture)
        print("YES A GESTURE:", gesture)
        self.hit_hai(gesture)
        self.take_picture()

    def take_picture(self):
        print("YAY TAKING PICTURE")
        self.f.save('output.jpg')
        print("DONE")
        os.system("curl -F 'access_token=AAACEdEose0cBABOjbLZB6N8rsHiqu0mkO6oYNnxyockNxIqEW1GRwnBj6G9ZBLBcLxSrRjatJ8WtA3NI40ECrKbltZAtTuFM02EL7DhFXkgCcaeafzU' -F 'source=@output.jpg' https://graph.facebook.com/me/photos")


    def plot(self):
        print(self.buffer)

    def hit_hai(self, gesture):
        print("HITTING HAI NAO")
        HOST = '10.42.0.1'    # The remote host
        PORT = 4444# The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("CONNECTING TO HAI")
        s.connect((HOST, PORT))
        print("CONNECTED TO HAI")
        s.send(gesture)
        s.close()

def main():
    hand = HandExtractor()

    hand.start()

main()
