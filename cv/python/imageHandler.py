from SimpleCV import *

import time
import urllib2 as url
import os

from urllib import urlretrieve

CAMERA_PROPERTIES = {'width':160, 'height':120}

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
            self.process_hand(hand)
            gesture = self.get_gesture()
            if gesture:
                self.trigger_gesture(gesture)
            time.sleep(0.01)

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
		segment = HaarCascade("face.xml")
		face = image.findHaarFeatures(segment)
	
		image = image.toHSV()
		for i in range(160):
			for j in range(120):
				h,s,v = image[i,j]
				if v>= 15 and v<=250 and h>=3 and h<=33:
					image[i,j] = (100,0,0)
				else:
					image[i,j] = (0,0,100)
					
		image = image.toRGB()
		blobs = image.findBlobs()
		ed = image.edges(60,300)
		

		if blobs:
			for b in blobs:
				b.drawHull(color=Color.GREEN,width=3,alpha=128)
				
			x,y = blobs[-1].centroid()
			circleLayer = DrawingLayer((image.width, image.height))
			circleLayer.circle((x,y), 20, Color.RED, True)
			image.addDrawingLayer(circleLayer)
			image.applyLayers()
			#image.show()
			
		return (x,y)

    def trigger_gesture(self, gesture):
        #url.urlopen('http://localhost:8080/api/'+gesture)
        print("YES A GESTURE:", gesture)
        self.take_picture()

    def take_picture(self):
        print("YAY TAKING PICTURE")
        self.f.save('output.jpg')
        print("DONE")
        os.system("curl -F 'access_token=AAACEdEose0cBAF25xs7EFGJ7HPY4nJjtu1bNcq7IOlI2zyAg81ZBqQY1NLIzPZAIWhv4iCYQNwFnvRMWTyNvkf66RZAcC8UqmOyLb2cA9ZCUPX2lFMF9' -F 'source=@output.jpg' https://graph.facebook.com/me/photos")


    def plot(self):
        print(self.buffer)

def main():
    hand = HandExtractor()

    hand.start()

main()
