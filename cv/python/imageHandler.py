from SimpleCV import *
import time

CAMERA_PROPERTIES = {'width':160, 'height':120}
cam = Camera(camera_index=1, prop_set=CAMERA_PROPERTIES)


def process_frame(image):
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
	return (x,y)

def main():
    #cam = Camera(prop_set=CAMERA_PROPERTIES)
	prev = cam.getImage()
	while True:
		f = cam.getImage()
		process_frame(f)
"""
def movement_check(x = 0,y = 0,t=1):
	direction = ""
	directionX = ""
	directionY = ""	
	if x > t:
		directionX = "Right"
	if x < -1*t:
		directionX = "Left"
	if y < -1*t:
		directionY = "Up"
	if y > t:
		directionY = "Down"

	direction = directionX #+ " " + directionY
	if direction is not "":
		return direction
	else:
		return "No Motion"

def main():
	scale_amount = (200,150)
	d = Display(scale_amount)
	cam = Camera(0)
	prev = cam.getImage().scale(scale_amount[0],scale_amount[1])
	time.sleep(0.5)
	t = 0.6
	buffer = 50
	count = 0
	while d.isNotDone():
		current = cam.getImage()
		current = current.scale(scale_amount[0],scale_amount[1])
		if( count < buffer ):
			count = count + 1
		else:
			fs = current.findMotion(prev, window=15, method="BM")
			lengthOfFs = len(fs)
			if fs:
							#~ fs.draw(color=Color.RED)
							dx = 0
							dy = 0
							for f in fs:
											dx = dx + f.dx
											dy = dy + f.dy

							dx = (dx / lengthOfFs)
							dy = (dy / lengthOfFs)
							motionStr = movement_check(dx,dy,t)
							current.drawText(motionStr,10,10)

		prev = current
		time.sleep(0.01)
		current.save(d)

if __name__ == '__main__':
    main()
"""

def imageShower():
	f = cam.getImage()
	process_frame(f)
	time.sleep(2)
	f = cam.getImage()
	process_frame(f)
	time.sleep(2)
	f = cam.getImage()
	process_frame(f)
	time.sleep(2)

main()
