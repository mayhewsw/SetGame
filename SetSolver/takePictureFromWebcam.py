
import cv

#capture = cv.CaptureFromCAM(-1)
#capture = cv.CreateCameraCapture(0)

#print capture
#for i in range(1):
#    img =  cv.QueryFrame(capture)
#    print img

#cv.ShowImage("img",img)
#cv.WaitKey(0)


# create capture device
device = 1 # assume we want first device
capture = cv.CreateCameraCapture(device)
#cv.SetCaptureProperty(capture, cv.CAP_PROP_FRAME_WIDTH, 640)
#cv.SetCaptureProperty(capture, cv.CAP_PROP_FRAME_HEIGHT, 480)    
 
# check if capture device is OK
if not capture:
    print "Error opening capture device"
    sys.exit(1)

print capture

while 1:
    # do forever
    
    # capture the current frame
    frame = cv.QueryFrame(capture)
    if frame is None:
        print "nothing found..."
        break
