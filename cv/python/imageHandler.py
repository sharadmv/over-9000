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
		self.length = 10
		self.GESTURE_THRESH = 4
		self.DEBUG_COMMUNICATE = False
		self.PENALTY_THRESH = 8
		self.DEBUG_SKIP = False
		self.DETECT_MOTION = True
		self.MOTION_THRESH = 15.0
		self.MOTION_COEFF = 2
		self.current = None
		self.previous = None
		
		#testing code
		self.penalty = 3
		self.count = 3
		self.current_direction = None

	def start(self):
		while True:
			self.previous = self.current
			f = self.camera.getImage()
			self.current = f.copy()
			#self.f.show()
			hand = self.process_frame(f)
			if(hand):
				self.process_hand(hand[0])
				gesture = self.get_gesture()
				if gesture:
					self.trigger_gesture(gesture)
	
	def process_takePic(self, hands):
		hand1 = hands[0]
		hand2 = hands[1]
		return hand1


	def get_gesture(self):
		if self.count >= self.GESTURE_THRESH:
			self.penalty = 0
			self.count = 0
			return self.current_direction

	def process_hand(self, hand):
		if (len(self.buffer) > self.length):
			self.buffer.pop(0)
			self.difference.pop(0)

		if len(self.buffer) > 0:
			diff = (hand[0] - self.buffer[-1][0], hand[1] - self.buffer[-1][1])
			self.difference.append(diff)

		self.buffer.append(hand)

		if self.difference:
			if self.current_direction == "left":
				if diff[0] > 1.0:
					self.count += 1
				else:
					self.penalty += 1

			elif self.current_direction == "right":
				if diff[0] < -1.0:
					self.count += 1
				else:
					self.penalty += 1

			else:
				if diff[0] > 0:
					self.current_direction = "left"
				else:
					self.current_direction = "right"
			
			if self.penalty == self.PENALTY_THRESH:
				self.penalty = 0
				self.count = 0
				self.current_direction = None

	def movementCheck(self, x=0, y=0, t=1):
		direction = ""
		directionX = ""
		directionY = ""
		if x > self.MOTION_COEFF*t:
			directionX = "Right"
		if x < -1*self.MOTION_COEFF*t:
			directionX = "Left"
		if y < -1*self.MOTION_COEFF*t:
			directionY = "Up"
		if y > 1*self.MOTION_COEFF*t:
			directionY = "Down"
		direction = directionX + " " + directionY
		if direction is not "":
			return direction
		else:
			return "No Motion"

	def process_frame(self, image):
		if(self.DEBUG_SKIP):
			image.show()
			return [(0,0)]

		if(self.current and self.previous and self.DETECT_MOTION):
			t = 0.5
			motion = self.current.findMotion(self.previous, window=15, method="BM")
			lenMotion = len(motion)
			if(motion):
				dx = 0
				dy = 0
				for f in motion:
					dx += f.dx
					dy += f.dy
				dx = dx/lenMotion
				dy = dy/lenMotion
				direction = self.movementCheck(dx,dy,t)
				print direction
			
			#diff = self.current - self.previous
			#matrix = diff.getNumpy()
			#mean = matrix.mean()
			#if mean >= self.MOTION_THRESH:
			#	print "MOTION!"
			#	return [(0,0)]
			image.show()
			return [(0,0)]

		segment = HaarCascade("face.xml")
		result = image
		face = result.findHaarFeatures(segment)

		mask = result.getSkintoneMask()
		result = result.applyBinaryMask(mask).medianFilter()

		blobs = result.findSkintoneBlobs(minsize=500, dilate_iter=1)
		x1,y1 = (0,0)
		x2,y2 = (0,0)
		if blobs:
			b1 = blobs[-1]
			x1,y1 = b1.centroid()
			b1.drawMinRect(color=Color.CYAN)
			if(len(blobs)>=2):
				b2 = blobs[-2]
				x2,y2 = b2.centroid() 
				b2.drawMinRect(color=Color.CYAN)
			if face:
				face.show()
		result.show()
		return [(x1,y1),(x2,y2)]
		
	def trigger_gesture(self, gesture):
		#url.urlopen('http://localhost:8080/api/'+gesture)
		print("YES A GESTURE:", gesture)
		if self.DEBUG_COMMUNICATE:
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
