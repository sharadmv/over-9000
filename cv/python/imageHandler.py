from SimpleCV import *
import time

cam = Camera()

def imageHandler(image):
	img = Image(image);
	return
	

def imageShower():
	img = cam.getImage()
	img.show()
	time.sleep(1)
	img = img.edges(100,880)
	img.show()
	blobs = img.findBlobs()
	#biggestHull = max([(b,b.area()) for b in blobs],key=lambda x:x[1])
	#biggestHull[0].show()
	for b in blobs:
		time.sleep(1)
		b.show()	
		print(b.area)
		

imageShower()
		