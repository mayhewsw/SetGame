import cv 

# create capture device
device = 0 # assume we want first device
capture = cv.CreateCameraCapture(device)

amount = 0
dosaturate = False

def on_trackbar(position):
    global capture

    # Set brightness
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_BRIGHTNESS , position/100.0)

def on_trackbargain(position):
    global capture

    # Set gain
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_GAIN , position/100.0)

def on_trackbarcontrast(position):
    global capture

    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_CONTRAST , position/100.0)

def on_trackbarhue(position):
    global capture

    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_HUE , position/100.0)

def on_trackbarsaturation(position):
    global amount
    global dosaturate
    
    amount = position
    dosaturate = True

def saturate(frame, amount):
    #Convert to HSV first, increase saturation, and convert back
    saturatedImage = cv.CreateImage((frame.width, frame.height), 8, 3)
    schan = cv.CreateImage((frame.width, frame.height), 8, 1)
    cv.CvtColor(frame, saturatedImage, cv.CV_BGR2HSV)
    
    saturationShift = amount 

    cv.Split(saturatedImage, None, schan, None, None)
    cv.AddS(schan, amount, schan)
    cv.Merge(None, schan, None, None, saturatedImage)

    # Convert the HSV img back to BGR
    cv.CvtColor(saturatedImage, frame, cv.CV_HSV2BGR)
    return frame

if __name__ == '__main__':
    global amount
    original = cv.LoadImage('/media/sda1/BeagleSetGame/images/lamp1.jpg')
    cv.ShowImage('originalimage', original)

    #print "Frame count", cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT)
    #print "Brightness",cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_BRIGHTNESS) 
    #print "Contrast",cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_CONTRAST) 
    #print "Sat",cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_SATURATION) 
    #print "Hue",cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_HUE) 
    #print "FPS",cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)  
    
    # Set height and width of camera image
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    

    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES, 0)
    
    # check if capture device is OK
    #if not capture:
    #    print "Error opening capture device"
    #    sys.exit(1)

    cv.NamedWindow("contours", 1)

    cv.CreateTrackbar("Brightness", "contours", 0, 100, on_trackbar)
    #cv.CreateTrackbar("Gain", "contours", 0, 100, on_trackbargain)
    cv.CreateTrackbar("Contrast", "contours", 0, 100, on_trackbarcontrast)
    cv.CreateTrackbar("Saturation", "contours", 0, 100, on_trackbarsaturation)
    cv.CreateTrackbar("Hue", "contours", 0, 100, on_trackbarhue)

    orig = cv.QueryFrame(capture)

    on_trackbar(9)
    #on_trackbargain(0)
    on_trackbarcontrast(0)
    on_trackbarsaturation(0)
    on_trackbarhue(0)
       
    while 1:
        frame = cv.QueryFrame(capture)

        #if dosaturate:
        frame = saturate(orig, amount)

        #print dosaturate
        #dosaturate = False

        cv.ShowImage("contours",frame)
        cv.WaitKey(100)
    
