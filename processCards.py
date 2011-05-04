3# Process cards for the Set Solver game
# Stephen Mayhew - April 23, 2011

import gtk.gdk
import cv
import numpy
import time
import os
import string
import Image
import random
import numpy

def getMeaningFromCards(cards):
    """
    This takes a dictionary of the form:
         (x, y) : Card image
    and returns a dictionary of the form (note the alphabetical order of the characteristics):
         (x, y) : (color, fill, number, shape)

    (x, y) are the coordinates of the top left of the card
    """
    for k in cards.keys():
        card = cards[k]

        gray = cv.CreateImage((card.width, card.height), 8, 1)
        cv.CvtColor(card, gray, cv.CV_RGB2GRAY)
    
        cv.Smooth(gray, gray)
        

        cv.Threshold(gray, gray, 40, 255, cv.CV_THRESH_BINARY)

        #cv.Not(gray,gray)

        #cv.ShowImage("img", gray)
        #cv.WaitKey(0)

        cpy = cv.CloneImage(gray)
        storage = cv.CreateMemStorage (0)
        contours = cv.FindContours( cpy, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0,0) );

        area1, area2, area3 = 0, 0, 0
        rect1 = (0,0,0,0)
        rect2 = (0,0,0,0)
        rect3 = (0,0,0,0)
        
        perimeter = 0
        if contours:
            while(contours):
                area = cv.ContourArea(contours)
                
                if abs(area - card.height*card.width) < 2000:
                    contours = contours.h_next()
                    continue

                if area > area1:
                    perimeter = cv.ArcLength(contours, isClosed=1)
                    area3 = area2
                    area2 = area1
                    area1 = area

                    rect3 = rect2
                    rect2 = rect1
                    rect1 = cv.BoundingRect(contours)
                elif (area > area2):
                    area3 = area2
                    area2 = area

                    rect3 = rect2
                    rect2 = cv.BoundingRect(contours)
                elif (area > area3):
                    area3 = area

                    rect3 = cv.BoundingRect(contours)
                
                contours = contours.h_next()

        # Get number - 1, 2, 3
        # check if bounding the corners of bounding boxes are close to each other
        bb = [rect1, rect2, rect3]
        symbolsAreLargerThanThis = 100
        bbf = filter(lambda b: b[2]*b[3] > symbolsAreLargerThanThis, bb)
        distbb = findDistinctBoxes(bbf)
        number = len(distbb)

        # Get color - red, green, purple
        color = 0
        color_mask = cv.CreateImage(cv.GetSize(card), 8, 1)

        # Specify the minimum / maximum colors to look for:
        # Find the pixels within the color-range, and put the output in the color_mask
        min_color_red = (0, 0, 0)
        max_color_red = (1, 1, 255)
        cv.InRangeS(card, cv.Scalar(*min_color_red), cv.Scalar(*max_color_red), color_mask)
        reds = cv.CountNonZero(color_mask)
        cv.SetZero(color_mask)

        min_color_green = (0, 0, 0)
        max_color_green = (1, 255, 1)
        cv.InRangeS(card, cv.Scalar(*min_color_green), cv.Scalar(*max_color_green), color_mask)
        greens = cv.CountNonZero(color_mask)
        cv.SetZero(color_mask)

        min_color_purple = (0, 0, 0)
        max_color_purple = (255, 1, 1)
        cv.InRangeS(card, cv.Scalar(*min_color_purple), cv.Scalar(*max_color_purple), color_mask)
        purples = cv.CountNonZero(color_mask)

        #print reds, greens, purples
        #print "Std. Dev.:",numpy.std([reds, greens, purples])
        #cv.ShowImage("mask" + str(k), color_mask)
        #cv.WaitKey(0)

        # Here's a bad way to do this: red and green are always clear.
        # If it is clearly either red or green, call it as such. Otherwise, call it purple.
        m = max(reds, greens, purples)
        if reds == m:
            color = "red"
        elif greens == m:
            color = "green"
        else:
            color = "purple"

        # Draw rects
        #cv.Rectangle(card, (rect1[0], rect1[1]), ( rect1[0] + rect1[2], rect1[1] + rect1[3]), (255,0,0,0))
        #cv.Rectangle(card, (rect2[0], rect2[1]), ( rect2[0] + rect2[2], rect2[1] + rect2[3]), (255,0,0,0))
        #cv.Rectangle(card, (rect3[0], rect3[1]), ( rect3[0] + rect3[2], rect3[1] + rect3[3]), (255,0,0,0))

        
        # Get fill - empty, full, shaded
        r,g,b,total = 0,0,0,0
        cv.Erode(gray, gray, None, 3)
        cv.Dilate(gray, gray, None, 3)
        for i in range(rect1[1], rect1[1] + rect1[3]):
            pixel = cv.Get2D(card, i, rect1[0] + rect1[2]/2)
            r += pixel[2]
            g += pixel[1]
            b += pixel[0]

        # The hard numbers below are found by experimentation
        total = r + g + b
        if total < 10000:
            fill = "solid"
        elif total < 30000:
            fill = "striped"
        else:
            fill = "empty"
            
        
        # Get shape - oval, diamond, squiggly
        ratio = area1/perimeter
        if ratio < 16.5:
            shape = "diamond"
        elif ratio < 20:
            shape = "squiggle"
        else:
            shape = "oval"

        if number > 1: shape += "s"
        print number, fill, color, shape
        #cards[k] = (color, fill, number, shape)
        cv.ShowImage("img", card)
        cv.WaitKey(0)


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


def extractCards(fileName = None):
    """
    Given an image, this will extract the cards from it.

    This takes a filename as an optional argument
    This filename should be the name of an image file.

    This returns a dictionary of the form:
        (x, y) : Card image
    It is likely that the output from this will go to the
    getMeaningFromCards() function.
    """
    
    if fileName == None:
        print "File name cannot be none..."
        sys.exit(1)
    else:
        submat = cv.LoadImage(fileName)

    subImg = cv.CreateImageHeader((submat.width, submat.height), 8, 3)
    cv.SetData(subImg, submat.tostring())

    gray = cv.CreateImage((submat.width, submat.height), 8, 1)
    cv.CvtColor(submat, gray, cv.CV_RGB2GRAY)

    cv.Smooth(gray, gray)

    # Nice to have a dynamic way of finding this! -> AdaptiveThreshold is that
    thresh = 90 # play around with this 
    max_value = 255
    #cv.Threshold(gray, gray, thresh, max_value, cv.CV_THRESH_BINARY)
    #cv.AdaptiveThreshold(gray,gray,max_value)
    
    cpy1 = cv.CloneImage(gray)
    cv.Canny(gray, gray, 50,100)

    #cv.Erode(gray, gray)
    #cv.Erode(gray, gray)
    cv.Dilate(gray, gray)


    #cv.Not(gray,gray)
    cv.ShowImage("sub", gray)
    cv.WaitKey(0)

    storage = cv.CreateMemStorage (0)

    cpy = cv.CloneImage(gray)
    contours = cv.FindContours( cpy, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0,0) );
    #contours = cv.ApproxPoly(contours, cv.CreateMemStorage(), cv.CV_POLY_APPROX_DP, 3, 1)

    bboxesL = []
    bboxesS = []

    if contours:
        while(contours):
            area = cv.ContourArea(contours)
            # It turns out that all the cards are about 44000 in area...
            # It would definitely be nice to have a better way to do this:
            # ie, find the size of the card programmatically and use it then
            # For Set, we can statistically find the average...also use an
            # expected value
            storage2 = cv.CreateMemStorage (0)
            app = cv.ApproxPoly(contours, storage2, cv.CV_POLY_APPROX_DP, 0)
            
            if (area > 250 and area < 1000 and area < submat.width*submat.height*2/3):
                bboxesS.append(app)

            if (area > 1000 and area < submat.width*submat.height*2/3):
                bboxesL.append(app)
                
            contours = contours.h_next()


    #bboxesS = findDistinctBoxes(bboxesS)
    drawBoundingBoxes(bboxesL, submat)
    drawBoundingBoxes(bboxesS, submat, "red")


    # cards is a dictionary of the form:
    #    (x, y) : card     // still useful even for set, because we will want to project onto it.
    
    cards = {}
    
    #for box in bboxesL:
        #card = cv.GetSubRect(subImg, box)
        #cv.ShowImage("card", card)
        #cv.WaitKey(0)
        #cards[(box[0], box[1])] = card


    return cards
    
def findDistinctBoxes(boundingboxes):
    """Given a list of bounding boxes, with many duplicates, or boxes close to each other,
    find one box that represents each group"""

    # First, find distinct boundboxes. Would be better to sort them, and find the max...
    distbb = []
    nb = 20
    
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
    cards = {}
    for i in range(30):
        #n = random.randint(0, 80)
        name = 'images/image%05d.bmp' % i
        image = cv.LoadImage(name)
        cards[(0,i)] = image

    getMeaningFromCards(cards)

