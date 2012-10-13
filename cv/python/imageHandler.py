from SimpleCV import *
import time

cam = Camera()

CAMERA_PROPERTIES = {'width':160, 'height':120}

def process_frame(frame):
    frame.show()

def main():
    cam = Camera(prop_set=CAMERA_PROPERTIES)
    while True:
        f = cam.getImage()
        process_frame(f)

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
