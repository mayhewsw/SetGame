# Runner for BeagleSetGame

import cv
import processCards
import sys

# create capture device
device = 0 # assume we want first device
capture = cv.CreateCameraCapture(device)

#var = float(raw_input("Set gain: "))
# Set gain
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_GAIN , .1) # I have no idea about this value
#var = float(raw_input("Set brightness: "))
# Set brightness
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_BRIGHTNESS , .2) # I have no idea about this value

# Set framerate
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FPS, 4) # I have no idea about this value

# Set exposure
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_EXPOSURE, 40) # I have no idea about this value

# Set height and width of camera image
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    
 
# check if capture device is OK
if not capture:
    print "Error opening capture device"
    sys.exit(1)

print capture

cv.NamedWindow("webcam", cv.CV_WINDOW_AUTOSIZE)

# Infinite Loop
while 1:


    # capture the current frame
    frame = cv.QueryFrame(capture)

    if frame is None:
        print "No frame found. Exiting."
        break

    # Run the recognizer
    groups = processCards.extractCards(frame)
    processCards.getMeaningFromCards(groups, frame)

    cv.ShowImage("webcam", frame)
    cv.WaitKey(100) # wait for a small amount of time
