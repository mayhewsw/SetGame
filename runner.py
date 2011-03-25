# Runner for BeagleSetGame

import cv
import processCards
import sys
import subprocess

# create capture device
device = 0 # assume we want first device
capture = cv.CreateCameraCapture(device)


#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_BRIGHTNESS , .) 
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_HUE , .68) 
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_CONTRAST, .20)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES, 0)

# Set framerate
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FPS, 4) # I have no idea about this value

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
        processCards.getMeaningFromCards(groups, frame)
    else:
        cv.ShowImage("webcam", frame)
        cv.WaitKey(100) # wait for a small amount of time




