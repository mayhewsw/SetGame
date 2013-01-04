import cv
import processCards

# create capture device
device = 0 # assume we want first device
capture = cv.CreateCameraCapture(device)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    
 
# check if capture device is OK
if not capture:
    print "Error opening capture device"
    sys.exit(1)

print capture


# do forever
    
# capture the current frame
frame = cv.QueryFrame(capture)

#groups = processCards.extractCards(frame)
#processCards.getMeaningFromCards(groups, frame)

if frame is None:
    print "nothing found..."

cv.ShowImage("webcam", frame)
cv.WaitKey(0)
cv.SaveImage("webcam.png", frame)
