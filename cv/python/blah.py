from SimpleCV import *

CAMERA_PROPERTIES = {'width':160, 'height':120}

def process_frame(image):
	#segment = HaarCascade("face.xml")
	result = image.copy()
	#face = result.findHaarFeatures(segment)
	face = None
	if face:
		face.draw(color=Color.CYAN)
		#f = result.crop(x=face.coordinates()[0][0],y=face.coordinates()[0][1],w=face.width(),h=face.height(),centered=True)
	mask = result.getSkintoneMask()
	result = result.applyBinaryMask(mask).medianFilter()
	#result = mask.medianFilter()

	blobs = result.findSkintoneBlobs(minsize=500,dilate_iter=1)
	if blobs:
		b = blobs[-1]
		b.draw()
		b.drawMinRect(color=Color.CYAN)
		#for b in blobs:
		#	if(b.isSquare(tolerance=0.1)):
		#		b.draw()

	#blobs = result.findBlobs(minsize=500)
	#corners = result.findCorners()
	#corners = False
	#if blobs:
	#	b = blobs[-1]
	#	rectH = b.minRectHeight()
	#	rectW = b.minRectWidth()
	#	if
	#	b.draw()
	
	#if corners:
	#	for cr in corners:
	#		cr.draw()
	return result

def blah():
	cam = Camera(prop_set=CAMERA_PROPERTIES)
	i = cam.getImage()
	disp = i.show()
	while(disp.isNotDone()):
		if disp.isDone():
			break
		i = cam.getImage()
		res = process_frame(i)
		img = i.sideBySide(res)
		res.save(disp)


blah()
