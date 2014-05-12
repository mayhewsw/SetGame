import cv 
import os

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

def on_trackbarexp(position):
    global capture

    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_EXPOSURE , position/1000.0)

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

def equalizeColors(frame):
    bchan = cv.CreateImage((frame.width, frame.height), 8, 1)
    gchan = cv.CreateImage((frame.width, frame.height), 8, 1)
    rchan = cv.CreateImage((frame.width, frame.height), 8, 1)

    cv.Split(frame, bchan, gchan, rchan, None)
    cv.EqualizeHist(bchan, bchan)
    cv.EqualizeHist(gchan, gchan)
    cv.EqualizeHist(rchan, rchan)

    cv.Merge(bchan, gchan, rchan, None, frame)
    return frame

if __name__ == '__main__':
    global amount

    hue = 0
    brightness = 0
    contrast = 0

    cfg = "cameraConfig.cfg"
    if os.path.exists(cfg):
        f = open(cfg, 'r')
        hue = float(f.readline().split()[1])
        brightness = float(f.readline().split()[1])
        contrast = float(f.readline().split()[1])
        f.close()
    
    # Set capture properties
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES, 0)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_BRIGHTNESS, brightness)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_HUE, hue)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_CONTRAST, contrast)
    
    wnd = "Trackbartest"
    cv.NamedWindow(wnd, 1)

    cv.CreateTrackbar("Brightness", wnd, 0, 100, on_trackbar)
    cv.CreateTrackbar("Contrast", wnd, 0, 100, on_trackbarcontrast)    
    cv.CreateTrackbar("Hue", wnd, 0, 100, on_trackbarhue)
    
    #cv.CreateTrackbar("Gain", wnd, 0, 100, on_trackbargain)
    #cv.CreateTrackbar("Saturation", wnd, 0, 100, on_trackbarsaturation)
    #cv.CreateTrackbar("Exp", wnd, 0, 100, on_trackbarexp)

    cv.SetTrackbarPos("Hue", wnd, int(hue*100))
    cv.SetTrackbarPos("Brightness", wnd, int(brightness*100))
    cv.SetTrackbarPos("Contrast", wnd, int(contrast*100))

    on_trackbar(0)
    #on_trackbargain(0)
    on_trackbarcontrast(0)
    #on_trackbarsaturation(0)
    on_trackbarhue(0)
    #on_trackbarexp(0)

    f = open("cameraConfig.cfg", "w")

    orig = cv.QueryFrame(capture)    
       
    while 1:
        frame = cv.QueryFrame(capture)

        #frame = equalizeColors(frame)
        #if dosaturate:
        #frame = saturate(orig, amount)

        #print dosaturate
        #dosaturate = False

        cv.ShowImage(wnd,frame)
        c = cv.WaitKey(100)
        #print c
        enter = 1048586
        esc = 1048603
        if c == enter:
            hue =  cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_HUE)
            brightness = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_BRIGHTNESS)
            contrast = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_CONTRAST)            
            f.write("HUE " + str(hue) + "\n")
            f.write("BRIGHTNESS " + str(brightness) + "\n")
            f.write("CONTRAST " + str(contrast) + "\n")
            print "Data saved to", cfg
        elif c == esc:
            print "Leaving now..."
            f.close()
            break
        
    
