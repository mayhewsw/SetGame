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
    groups is a list of lists. The internal lists each represent
    1 card, and have length of 1, 2 or 3, depending on the number
    of symbols on the card. Each element in an internal list is
    a tuple which is the bounding box of the symbol on the card.

    extractCards() returns a list of the desired type. It is likely
    that groups is the result of extractCards().

    """
    
    for g in groups:

        # Since all the symbols on any card are the same,
        # we will only concern ourselves with the first one
        firstSymbol = g[0]
        
        symbol = cv.GetSubRect(image, firstSymbol)
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

        # Ignore contours that are just outlines of the image
        while( abs(cv.ContourArea(contours) - symbol.width*symbol.height) < 15):
            contours = contours.h_next()

        perimeter = cv.ArcLength(contours, isClosed=1)

    
        # Get number ---------------------------------------
        number = len(g)
        # Got number --------------------------------------
        
        # Get color - red, green, purple ------------------
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
        saturatedImage = cv.CreateImage((symbol.width, symbol.height), 8, 3)
        cv.CvtColor(symbol, saturatedImage, cv.CV_BGR2HSV)

        saturationShift = 200 # this is huge. It makes the images somewhat ridiculous, but it may be useful.
        for i in range(saturatedImage.width):
            for j in range(saturatedImage.height):                
                p = cv.Get2D(saturatedImage, j, i)
                p = (p[0], p[1] + saturationShift, p[2])
                cv.Set2D(saturatedImage, j, i, p)

        # Convert the HSV img back to BGR
        cv.CvtColor(saturatedImage, saturatedImage, cv.CV_HSV2BGR)
        #cv.CvtColor(saturatedImg, symbol, cv.CV_HSV2BGR)

        # Just want a black image
        zeros = cv.CreateImage(cv.GetSize(symbol), 8, 3)
        cv.SetZero(zeros)

        # Copy the symbol over to zeros, with color_mask as the mask
        # This effectively copies only the symbol over.
        cv.Copy(saturatedImage, zeros, color_mask)
        saturatedImage = zeros

        # Split it into RGB channels
        rchannel = cv.CreateImage((saturatedImage.width, saturatedImage.height), 8, 1)
        gchannel = cv.CreateImage((saturatedImage.width, saturatedImage.height), 8, 1)
        bchannel = cv.CreateImage((saturatedImage.width, saturatedImage.height), 8, 1)
        cv.Split(saturatedImage,bchannel,gchannel,rchannel,None)

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

        # Got color -------------------------------------------------------------------------
            
        # For testing ++++++++++++++++++++++++++++++++
        #cv.ShowImage('rchan', rchannel)
        #cv.ShowImage('gchan', gchannel)
        #cv.ShowImage('bchan', bchannel)

        
        cv.ShowImage("gray", gray)
        cv.ShowImage("symbol", symbol)
        #cv.ShowImage("image", image)

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

        # not sure why these lines are here.
        # Anyone know? Speak now or forever hold your peace.
        cv.Erode(gray, gray, None, 3)
        cv.Dilate(gray, gray, None, 3)

        # Get fill - empty, full, shaded -------------------------------------------
        r,gr,b,total = 0,0,0,0

        # Loop over pixels in symbol from top to bottom
        # In the middle
        for row in range(firstSymbol[1], firstSymbol[1] + firstSymbol[3]):
            col = firstSymbol[0] + firstSymbol[2]/2
            pixel = cv.Get2D(image, row, col)
            r += pixel[2]
            gr += pixel[1]
            b += pixel[0]

        # The hard numbers below are found by experimentation
        # Have a softer method of grouping numbers?
        total = r + gr + b
        if total < 10000:
            fill = "solid"
        elif total < 30000:
            fill = "striped"
        else:
            fill = "empty"
        # Got fill ------------------------------------------------------------------

        print "Fill total:",total
        print "Maybe use this:",reds[0] +greens[0] +blues[0]

        
        # Get shape - oval, diamond, squiggly ----------------------------------------
        ratio = (symbol.width*symbol.height)/perimeter
        if ratio < 16.5:
            shape = "diamond"
        elif ratio < 20:
            shape = "squiggle"
        else:
            shape = "oval"
        # Got shape -----------------------------------------------------------------

        if number > 1: shape += "s"
        print number, fill, color, shape
        print
        #symbols[k] = (color, fill, number, shape)
        #cv.ShowImage("img", symbol)
        cv.WaitKey(0)
        



def findDistinctBoxes(boundingboxes):
    """ Given a list of bounding boxes, with many duplicates, or boxes close to each other, 
    find one box that represents each group """
    
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

    This returns a list of lists. The internal lists each represent
    1 card, and have length of 1, 2 or 3, depending on the number
    of symbols on the card. Each element in an internal list is
    a tuple which is the bounding box of the symbol on the card.

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
    all similar boxes together
    For example: a card with three symbols on it will be represented by a list with 3 tuples in it.
    Each tuple refers to the bounding box of a symbol on the card. 
    """
        
    # sort the list first by x, then by y
    # WARNING: could be fragile
    rowHeight = image.height/4

    # Since the symbols are identified by their top left corners, we can afford to push
    # rowHeight up (make it smaller), so that we avoid catching the wrong boxes
    offset = image.height/16

    # For testing: draws differentiation lines on the image +++++++++++++++++++++++++++++++++++++
    #for i in range(4):
        #cv.Line(image, (0, rowHeight*i-offset), (image.width-4, rowHeight*i-offset), (255,0,0,0))
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    topRow = filter(lambda b: b[1] < rowHeight-offset, boxes)
    topmiddleRow = filter(lambda b: rowHeight-offset < b[1] < rowHeight*2-offset, boxes)
    bottommiddleRow = filter(lambda b: rowHeight*2-offset < b[1] < rowHeight*3-offset, boxes)
    bottomRow = filter(lambda b: rowHeight*3-offset < b[1], boxes)
    
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


    # Testing: this will show each group of boxes as it is recognized +++++
    for g in groupsOfCards:
        for b in g:
            x = b[0]
            y = b[1]
            width = b[2]
            height = b[3]
        
            #cv.Rectangle(image, (x,y), (x+width, y+height), (0,255,0,0))

        #cv.ShowImage('img', image)
        #cv.WaitKey(0)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Give a warning for normal gameplay
    # (should be 12 cards)
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

    image = cv.LoadImage("images/lamp1.jpg")
    groups = extractCards(image)
    getMeaningFromCards(groups, image)

