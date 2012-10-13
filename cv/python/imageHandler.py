#from SimpleCV import *
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CAMERA_PROPERTIES = {'width':160, 'height':120}

class HandExtractor:

  def __init__(self):
    #self.camera = Camera(prop_set=CAMERA_PROPERTIES)
    self.buffer = []
    self.difference = []
    self.length = 20


    #testing code
    self.penalty = 3
    self.count = 3
    self.cur_dir = None

  def start(self):
    while True:
      #f = self.camera.getImage()
      hand = self.process_frame(None)
      self.process_hand(hand)
      gesture = self.get_gesture()
      if gesture:
          self.trigger_gesture(gesture)
      time.sleep(0.1)

  def get_gesture(self):
      if self.count > 10:
          self.penalty = 0
          self.count = 0
          return self.cur_dir
      print(self.buffer)
      print(self.difference)
      pass

  def process_hand(self, hand):
      if (len(self.buffer) > self.length):
          self.buffer.pop(0) 
          self.difference.pop(0) 
      if len(self.buffer) > 0:
          diff = (hand[0] - self.buffer[len(self.buffer)-1][0],hand[1] - self.buffer[len(self.buffer)-1][1])
          self.difference.append(diff)
      self.buffer.append(hand)

      if self.difference:
        if self.cur_dir == "right":
            if diff[0] > 0:
                self.count += 1
            else:
                self.penalty += 1
        elif self.cur_dir == "left":
            if diff[0] < 0:
                self.count += 1
            else:
                self.penalty += 1
        else:
            if diff[0] > 0:
                self.cur_dir = "right"
            else:
                self.cur_dir = "left" 

        if self.penalty == 4:
            self.penalty = 4
            self.count = 0
            self.cur_dir = None
          

  def process_frame(self, image):
    return (-len(self.buffer),-len(self.buffer))
    img = image.edges(100,880)
    blobs = img.findBlobs()
    if blobs:
      b = blobs[-1]
      b.show()
    return (100,100)
  def trigger_gesture(self, gesture):
    print("YES A GESTURE:", gesture)

  def plot(self):
    print(self.buffer)

  

def main():
  hand = HandExtractor()
  hand.start()

main()
