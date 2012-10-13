from SimpleCV import *
import time

CAMERA_PROPERTIES = {'width':160, 'height':120}
cam = Camera(prop_set=CAMERA_PROPERTIES)

def process_frame(image):
	#image.show()
	img = image.edges(100,880)
	#img.show()
	blobs = img.findBlobs()
	if blobs:
		b = blobs[-1]
		b.show()
		print(b.area)
		print(b.centroid)

	#biggestHull = max([(b,b.area()) for b in blobs],key=lambda x:x[1])
	#biggestHull[0].show()
	#for b in blobs:
	#	time.sleep(1)
	#	b.show()	
	#	print(b.area)

def main():
    #cam = Camera(prop_set=CAMERA_PROPERTIES)
    while True:
        f = cam.getImage()
        process_frame(f)

	

def imageShower():
	img = cam.getImage();
	img.show()
	time.sleep(1)
	ed = img.edges(100,880)
	ed.show()
	blobs = img.findBlobs()
	#biggestHull = max([(b,b.area()) for b in blobs],key=lambda x:x[1])
	#biggestHull[0].show()
	#for b in blobs:
	#	time.sleep(1)
	#	b.show()	
	#	print(b.area)
	b = blobs[-1]
	b.show()
	print(b.area)
	print(b.centroid)

main()
