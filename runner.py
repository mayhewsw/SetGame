# Runner for BeagleSetGame

import cv
import processCards
import sys

# create capture device
device = 0 # assume we want first device
capture = cv.CreateCameraCapture(device)

f = open("cameraConfig.cfg")
hue = f.readline().split()[1]
brightness = f.readline().split()[1]
contrast = f.readline().split()[1]
f.close()
 
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_HUE , float(hue)) 
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_CONTRAST, float(contrast))
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_BRIGHTNESS, float(brightness))

# This doesn't work with our camera...
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES, 0)

# Set framerate - this doesn't work with the PS eye.
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FPS, 1)

# Set exposure
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_EXPOSURE, 40) # I have no idea about this value



# Set height and width of camera image
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    
 
# check if capture device is OK
if not capture:
    print "Error opening capture device"
    sys.exit(1)


#cv.NamedWindow("webcam", cv.CV_WINDOW_AUTOSIZE)

runAndProcess = True

# Infinite Loop
while 1:

    # capture the current frame
    frame = cv.QueryFrame(capture)

    if frame is None:
        print "No frame found. Exiting."
        break

    # Run the recognizer
    if runAndProcess:
        groups = processCards.extractCards(frame)
        cards = processCards.getMeaningFromCards(groups, frame)
        if cards == "break out of this loop":
            break
        processCards.SolveGame(cards)
    else:
        cv.ShowImage("webcam", frame)
        cv.WaitKey(100) # wait for a small amount of time




