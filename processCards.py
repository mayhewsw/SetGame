3# Process cards for the Set Solver game
# Stephen Mayhew - April 23, 2011


#import gtk.gdk
import cv
#import numpy
#import time
#import os
#import string
#import Image
#import random
#import numpy

def getMeaningFromCards(groups, image):
    """
    This takes a dictionary of the form:
         (x, y) : Card image
    and returns a dictionary of the form (note the alphabetical order of the characteristics):
         (x, y) : (color, fill, number, shape)

    (x, y) are the coordinates of the top left of the card
    """
    print len(groups)
    for g in groups:
        
        print g[0]
        symbol = cv.GetSubRect(image, g[0])
        gray = cv.CreateImage((symbol.width, symbol.height), 8, 1)
        cv.CvtColor(symbol, gray, cv.CV_BGR2GRAY)
    
        cv.Smooth(gray, gray)
        
        # Either this..........
        #cv.Threshold(gray, gray, 60, 255, cv.CV_THRESH_BINARY)
        #cv.AdaptiveThreshold(gray,gray,255,blockSize=3)
        #cv.Not(gray,gray)

        # Or this ...........
        cpy1 = cv.CloneImage(gray)
        cv.Canny(gray, gray, 50,100)
        
        #cv.Erode(gray, gray)
        #cv.Erode(gray, gray)
        #cv.Dilate(gray, gray)
        # .......................

    
        #cv.ShowImage("symbol", symbol)
        #cv.ShowImage("img", gray)
        #cv.WaitKey(0)

        cpy = cv.CloneImage(gray)
        storage = cv.CreateMemStorage (0)
        contours = cv.FindContours( cpy, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0,0) )

        #print cv.ContourArea(contours)
        #print symbol.width*symbol.height
        #print abs(cv.ContourArea(contours) - symbol.width*symbol.height)
        
        while( abs(cv.ContourArea(contours) - symbol.width*symbol.height) < 15):
            contours = contours.h_next()

        perimeter = cv.ArcLength(contours, isClosed=1)
    
        # g is the group of all symbols on the cards
        number = len(g)


        
        # Get color - red, green, purple
        color = "undefined"

        # color mask is a binary image
        # white for pixels we are interested in
        # black for pixels not interested in
        color_mask = cv.CreateImage(cv.GetSize(symbol), 8, 1)

        # mask out the background -> put it to black
        # The background is mostly white,
        # So find all pixels that are above a certain threshold
        min_color = (140, 140, 140)
        max_color = (255, 255, 255)
        cv.InRangeS(symbol, cv.Scalar(*min_color), cv.Scalar(*max_color), color_mask)

        # Those pixels will go to black, so invert the image
        cv.Not(color_mask, color_mask)

        
        #cv.ShowImage('color', color_mask)        


        #Convert to HSV first, increase saturation, and convert back
        hsvimg = cv.CreateImage((symbol.width, symbol.height), 8, 3)
        cv.CvtColor(symbol, hsvimg, cv.CV_BGR2HSV)

        saturationShift = 200 # this is huge. It makes the images somewhat ridiculous, but it may be useful.
        for i in range(hsvimg.width):
            for j in range(hsvimg.height):                
                p = cv.Get2D(hsvimg, j, i)
                p = (p[0], p[1] + saturationShift, p[2])
                cv.Set2D(hsvimg, j, i, p)

        # Convert the HSV img back to BGR
        cv.CvtColor(hsvimg, symbol, cv.CV_HSV2BGR)

        # Just want a black image
        zeros = cv.CreateImage(cv.GetSize(symbol), 8, 3)
        cv.SetZero(zeros)

        # Copy the symbol over to zeros, with color_mask as the mask
        # This effectively copies only the symbol over.
        cv.Copy(symbol, zeros, color_mask)
        symbol = zeros

        # Split it into RGB channels
        rchannel = cv.CreateImage((symbol.width, symbol.height), 8, 1)
        gchannel = cv.CreateImage((symbol.width, symbol.height), 8, 1)
        bchannel = cv.CreateImage((symbol.width, symbol.height), 8, 1)
        cv.Split(symbol,bchannel,gchannel,rchannel,None)

        # The result of cv.Sum() is a tuple. We want the first value
        reds = cv.Sum(rchannel)
        greens = cv.Sum(gchannel)
        blues = cv.Sum(bchannel)
        #print reds[0], greens[0], blues[0]

        # Just a simple max of summed values
        m = max(reds[0], greens[0], blues[0])        
        if m == reds[0]:
            color = "red"
        elif m == greens[0]:
            color = "green"
        else:
            color = "purple"

        # For testing ++++++++++++++++++++++++++++++++
        #cv.ShowImage('rchan', rchannel)
        #cv.ShowImage('gchan', gchannel)
        #cv.ShowImage('bchan', bchannel)

                     
        cv.ShowImage("symbol", image)

        #cv.MoveWindow("symbol", 20, 200)
        #cv.MoveWindow("rchan", 70, 200)
        #cv.MoveWindow("gchan", 120, 200)
        #cv.MoveWindow("bchan", 170, 200)
        #cv.MoveWindow("color", 220, 200)
    
        # ++++++++++++++++++++++++++++++++++++++++++++++++

        
        # Draw rects
        ##cv.Rectangle(symbol, (rect1[0], rect1[1]), ( rect1[0] + rect1[2], rect1[1] + rect1[3]), (255,0,0,0))
        #cv.Rectangle(symbol, (rect2[0], rect2[1]), ( rect2[0] + rect2[2], rect2[1] + rect2[3]), (255,0,0,0))
        #cv.Rectangle(symbol, (rect3[0], rect3[1]), ( rect3[0] + rect3[2], rect3[1] + rect3[3]), (255,0,0,0))

        # Get fill - empty, full, shaded
        r,gr,b,total = 0,0,0,0
        cv.Erode(gray, gray, None, 3)
        cv.Dilate(gray, gray, None, 3)
        for i in range(g[0][1], g[0][1] + g[0][3]):
            pixel = cv.Get2D(image, i, g[0][0] + g[0][2]/2)
            r += pixel[2]
            gr += pixel[1]
            b += pixel[0]

        # The hard numbers below are found by experimentation
        total = r + gr + b
        if total < 10000:
            fill = "solid"
        elif total < 30000:
            fill = "striped"
        else:
            fill = "empty"

        print "Fill total:",total

        
        # Get shape - oval, diamond, squiggly
        ratio = (symbol.width*symbol.height)/perimeter
        if ratio < 16.5:
            shape = "diamond"
        elif ratio < 20:
            shape = "squiggle"
        else:
            shape = "oval"

        if number > 1: shape += "s"
        print number, fill, color, shape
        #symbols[k] = (color, fill, number, shape)
        #cv.ShowImage("img", symbol)
        #cv.WaitKey(0)
        #cv.WaitKey(0)


# Given a list of bounding boxes, with many duplicates, or boxes close to each other, 
# find one box that represents each group
def findDistinctBoxes(boundingboxes):
    # First, find distinct boundboxes. Would be better to sort them, and find the max...
    distbb = []
    nb = 75
    
    boundingboxes = sorted(boundingboxes, key = lambda boundingboxes : boundingboxes.x)

    for b in boundingboxes:
        toadd = True

        for d in distbb:
            # if there is a box with similar characteristics, then don't add
            if (d.x-nb < b.x < d.x+nb and 
                d.y-nb < b.y < d.y+nb):
                toadd = False

        if toadd:
            distbb.append(b)

    return distbb


def extractCards(image):
    """
    Given an image, this will extract the cards from it.

    This takes a filename as an optional argument
    This filename should be the name of an image file.

    This returns a dictionary of the form:
        (x, y) : Card image
    It is likely that the output from this will go to the
    getMeaningFromCards() function.
    """
    
    #if fileName == None:
    #    print "File name cannot be none..."
    #    sys.exit(1)
    #else:
    #    image = cv.LoadImage(fileName)

    #subImg = cv.CreateImageHeader((submat.width, submat.height), 8, 3)
    #cv.SetData(subImg, submat.tostring())

    gray = cv.CreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, gray, cv.CV_RGB2GRAY)

    cv.Smooth(gray, gray)

    # Nice to have a dynamic way of finding this! -> AdaptiveThreshold is that
    thresh = 90 # play around with this 
    max_value = 255
    #cv.Threshold(gray, gray, thresh, max_value, cv.CV_THRESH_BINARY)
    #cv.AdaptiveThreshold(gray,gray,max_value,blockSize=11)
    
    cpy1 = cv.CloneImage(gray)
    cv.Canny(gray, gray, 50,100)

    #cv.Erode(gray, gray)
    #cv.Erode(gray, gray)
    cv.Dilate(gray, gray)


    #cv.Not(gray,gray)
    #cv.ShowImage("sub", gray)
    #cv.WaitKey(0)

    storage = cv.CreateMemStorage (0)

    cpy = cv.CloneImage(gray)
    contours = cv.FindContours( cpy, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0,0) );
    #contours = cv.ApproxPoly(contours, cv.CreateMemStorage(), cv.CV_POLY_APPROX_DP, 3, 1)

    bboxes = []

    if contours:
        while(contours):
            area = cv.ContourArea(contours)
            # It turns out that all the cards are about 44000 in area...
            # It would definitely be nice to have a better way to do this:
            # ie, find the size of the card programmatically and use it then
            # For Set, we can statistically find the average...also use an
            # expected value
            storage2 = cv.CreateMemStorage (0)
            #app = cv.ApproxPoly(contours, storage2, cv.CV_POLY_APPROX_DP, 0)
            app = contours
            
            if (area > 250 and area < 5000 and area < image.width*image.height*2/3):
                b = cv.BoundingRect(app)

                # Inflate the rectangles slightly
                amount = 5
                b0 = b[0] - amount if b[0] >= amount else b[0]
                b1 = b[1] #- amount if b[1] >= amount else 0
                b2 = b[2] + 2*amount if b[2] < 2*amount+image.width else b[2]
                b3 = b[3] + 2*amount if b[2] < 2*amount+image.height else b[3]

                b = (b0, b1, b2, b3)
                
                
                bboxes.append(b)
                
            contours = contours.h_next()


    bboxes = findDistinctBoxes(bboxes)

    #for c in bboxesS:
    #    cv.DrawContours(image,c,(0,255,0,0) ,(255,0,0,),1)

    return groupBoxes(bboxes, image)


def groupBoxes(boxes, image):
    """ this takes a list of lots of boxes, and returns a list of boxes that has grouped
    all similar boxes together  """
        
    # sort the list first by x, then by y
    # WARNING: could be fragile
    rowHeight = image.height/4

    topRow = filter(lambda b: b[1] < rowHeight, boxes)
    topmiddleRow = filter(lambda b: rowHeight < b[1] < rowHeight*2, boxes)
    bottommiddleRow = filter(lambda b: rowHeight*2 < b[1] < rowHeight*3, boxes)
    bottomRow = filter(lambda b: rowHeight*3 < b[1], boxes)

    print len(topRow), len(topmiddleRow, len(bottommiddleRow), len(bottomRow)
    
    rows = [topRow, topmiddleRow, bottommiddleRow, bottomRow]

    final = []
    
    for r in rows:
         final += sorted(r, key=lambda p: p[0])

    groupsOfCards = []
    currentGroup = []

    fudge = 7
    for b in final:
        l = len(currentGroup)
        if l == 0:
            currentGroup.append(b)
        elif l == 1 or l == 2:
            # check if x-distance (might be fragile) from last element
            # in current group is above a certain threshold compared to b
            last = currentGroup[l-1]
            # if above, append, and clear
            if abs(last[0] - b[0]) > last[2]+fudge:
                groupsOfCards.append(currentGroup)
                currentGroup = [b]
            else:  # if below, add, and continue
                currentGroup.append(b)
        else:
            groupsOfCards.append(currentGroup)
            currentGroup = [b]

    # This will be the last card
    groupsOfCards.append(currentGroup)


    # entirely for testing +++++
    for g in groupsOfCards:
        for b in g:
            x = b[0]
            y = b[1]
            width = b[2]
            height = b[3]
        
            cv.Rectangle(image, (x,y), (x+width, y+height), (0,255,0,0))

        cv.ShowImage('img', image)
        cv.WaitKey(0)
    # ++++++++++++++++++++++++++++++

    # Give a warning for normal gameplay
    # (thre are 12 cards)
    if len(groupsOfCards) != 12:
        print "Warning: groupboxes has detected " + str(len(groupsOfCards)) + " cards."
    return groupsOfCards
        

    
def drawBoundingBoxes(bb, img):
    for b in bb:
        x = b[0]
        y = b[1]
        width = b[2]
        height = b[3]
        #cv.Rectangle(img, (x,y), (x+width, y+height), (0,255,0,0))

    #cv.ShowImage("bb", img)
    #cv.WaitKey(0)
    
def findDistinctBoxes(boundingboxes):
    """Given a list of bounding boxes, with many duplicates, or boxes close to each other,
    find one box that represents each group"""

    # First, find distinct boundboxes. Would be better to sort them, and find the max...
    distbb = []
    nb = 20

    boundingboxes.reverse()
    
    #boundingboxes = sorted(boundingboxes, key = lambda boundingboxes : boundingboxes.x)

    for b in boundingboxes:
        toadd = True

        for d in distbb:
            # if there is a box with similar characteristics, then don't add
            if (d[0]-nb < b[0] < d[0]+nb and
                d[1]-nb < b[1] < d[1]+nb):
                toadd = False

        if toadd:
            distbb.append(b)

    return distbb



if __name__ == '__main__':
    #cards = {}
    #for i in range(0):
    #    n = random.randint(0, 80)
    #    name = 'images/image%05d.bmp' % i
    #    image = cv.LoadImage(name)
    #    cards[(0,i)] = image

    image = cv.LoadImage("images/lamp1_rotate.jpg")
    groups = extractCards(image)
    getMeaningFromCards(groups, image)

