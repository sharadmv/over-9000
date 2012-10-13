from SimpleCV import *

CAMERA_PROPERTIES = {'width':160, 'height':120}

def process_frame(frame):
    frame.show()

if __name__ == 'main':
    cam = Camera(prop_set=CAMERA_PROPERTIES)
    while True:
        f = cam.getImage()
        process_frame(f)
