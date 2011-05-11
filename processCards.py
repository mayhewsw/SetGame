3# Process cards for the Set Solver game
# Stephen Mayhew - April 23, 2011

import cv

class Card:
    """ A useful way to store both bounding box and attributes """

    def __init__(self, symbols, attributes):
        self.symbols = symbols
        self.attributes = attributes

    def __str__(self):
        return "Card: " + str(symbols) + str( attributes)
    

def getThresholdsFromList(l):
    """ Given a list of numbers, this finds 3 different levels
    and computes the 2 thresholds between those levels

    Returns: bottomThresh, topThresh """
    
    # Make intensity thresholds based off these values
    l = sorted(l)

    # Find the largest jumps in the diffs list
    # thos jumps represent different levels.
    jumps = []
    for i in range(len(l)-1):
        jump = abs(l[i] - l[i+1])
        jumps.append((jump, i))

    # With tuples, sorted sorts by the first element anyway.
    # We want the largest elements at the beginning, so we reverse
    jumps = sorted(jumps, reverse=True)
    thresh1 = jumps[0][1] # largest jump
    thresh2 = jumps[1][1] # second largest jump

    # Set the thresholds to be in between the positions of the
    # largest jumps.
    thresh1 = l[thresh1] + jumps[thresh1][0]/2
    thresh2 = l[thresh2] + jumps[thresh2][0]/2

    # We will need this for later
    bottomThresh = min(thresh1, thresh2) 
    topThresh = max(thresh1, thresh2)
    return bottomThresh, topThresh

def makeBoardImage(cards):
    pass


def getMeaningFromCards(groups, image):
    """
    groups is a list of lists. The internal lists each represent
    1 card, and have length of 1, 2 or 3, depending on the number
    of symbols on the card. Each element in an internal list is
    a tuple which is the bounding box of the symbol on the card.

    extractCards() returns a list of the desired type. It is likely
    that groups is the result of extractCards().

    For reference: my convention is that <<<<<<< opens a block, and
    >>>>>>>>>>>>>> closes a block. This is supposed to help with
    readability.

    """

    # For debugging. Add text to the string to catch debug flags
    # Options are number, fill, color, shape
    # The check is simply:
    #     if "number" in debug: ...
    debug = ""
    
    cards=[]

    # This loop is just for getting information on fill before we do the second (main) loop.
    intensityDiffs = []
    for g in groups:

        firstSymbol = g[0]
        
        total, totalOutside = 0,0

        grayImg = cv.CreateImage((image.width, image.height), 8, 1)
        cv.CvtColor(image, grayImg, cv.CV_BGR2GRAY)
     
        # This adds contrast to the image
        cv.EqualizeHist(grayImg, grayImg)

        # Go this much to the left of the left side of the bounding box
        # to sample a line in contrast with the center of the symbol
        leftOfBoundingBox = 3

        # Testing ++++++++++++++++++++++++++++++
        if "fill" in debug:
            cv.Line(grayImg, (firstSymbol[0] + firstSymbol[2]/2, firstSymbol[1]),
                    (firstSymbol[0] + firstSymbol[2]/2, firstSymbol[1] + firstSymbol[3]),
                    (0,0,255,0))

            cv.Line(grayImg, (firstSymbol[0]-leftOfBoundingBox-1, firstSymbol[1]),
                    (firstSymbol[0]-leftOfBoundingBox-1, firstSymbol[1] + firstSymbol[3]),
                    (0,0,255,0))
        
            #cv.ShowImage("gimg", grayImg)
            #cv.WaitKey(0)
        # +++++++++++++++++++++++++++++++++++++
    
        
        # Loop over pixels in grayscale image from top to bottom of symbol
        # in the middle. Also, just to the left
        for row in range(firstSymbol[1], firstSymbol[1] + firstSymbol[3]):
            col = firstSymbol[0] + firstSymbol[2]/2
            colOutside = firstSymbol[0] - leftOfBoundingBox # should be enough to get us outside the symbol

            pixelSymbol = cv.Get2D(grayImg, row, col)
            pixelOutside = cv.Get2D(grayImg, row, colOutside)

            total += pixelSymbol[0]
            totalOutside += pixelOutside[0]

        intensityDifference = abs(total - totalOutside)    
        intensityDiffs.append(intensityDifference)



    # Get fill section uses these
    # intensityDiffs (unsorted) is also used in the Get fill section
    bottomThresh, topThresh = getThresholdsFromList(intensityDiffs)
    count = 0

    # This is the main loop
    for g in groups:

        # Since all the symbols on any card are the same,
        # we will only concern ourselves with the first one
        # (we might consider looking at all symbols to get a more
        # accurate reading)
        firstSymbol = g[0]

        # Extract just the portion of the image that is the symbol
        # Also create a grayscale version and smooth it
        symbol = cv.GetSubRect(image, firstSymbol)
        gray = cv.CreateImage((symbol.width, symbol.height), 8, 1)
        cv.CvtColor(symbol, gray, cv.CV_BGR2GRAY)
        cv.Smooth(gray, gray)
        
        # Either this..........
        #cv.Threshold(gray, gray, 60, 255, cv.CV_THRESH_BINARY)
        #cv.AdaptiveThreshold(gray,gray,255,blockSize=3)
        #cv.Not(gray,gray)

        # Or this ...........
        cv.Canny(gray, gray, 50,100)
        
        #cv.Erode(gray, gray)
        #cv.Erode(gray, gray)
        #cv.Dilate(gray, gray)
        # .......................

    
        # Get number <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        number = len(g)
        
        if "number" in debug:
            print "Number:", number
        # Got number >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        
        # Get color - red, green, purple <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
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

        # For testing ++++++++++++++++++++++++++++++++
        if "color" in debug:
            cv.ShowImage('rchan', rchannel)
            cv.ShowImage('gchan', gchannel)
            cv.ShowImage('bchan', bchannel)

            cv.ShowImage("gray", gray)
            cv.ShowImage("symbol", symbol)
            cv.ShowImage("image", image)

            cv.MoveWindow("symbol", 20, 200)
            cv.MoveWindow("rchan", 70, 200)
            cv.MoveWindow("gchan", 120, 200)
            cv.MoveWindow("bchan", 170, 200)
            cv.MoveWindow("color", 220, 200)

        # Draw rects
        ##cv.Rectangle(symbol, (rect1[0], rect1[1]), ( rect1[0] + rect1[2], rect1[1] + rect1[3]), (255,0,0,0))
        #cv.Rectangle(symbol, (rect2[0], rect2[1]), ( rect2[0] + rect2[2], rect2[1] + rect2[3]), (255,0,0,0))
        #cv.Rectangle(symbol, (rect3[0], rect3[1]), ( rect3[0] + rect3[2], rect3[1] + rect3[3]), (255,0,0,0))
    
        # ++++++++++++++++++++++++++++++++++++++++++++++++

        # Got color >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        # Get fill <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        intensityDiff = intensityDiffs[count]

        if "fill" in debug:
            print "BottomThresh:", bottomThresh
            print "TopThresh:",topThresh
            print "IndtensityDiff:", intensityDiff
            
        if intensityDiff <= bottomThresh:
            fill = "empty"
        elif bottomThresh < intensityDiff < topThresh:
            fill = "striped"
        else:
            fill = "solid"

        count += 1
        # Got fill >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        

        # Get shape - oval, diamond, squiggly <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        cv.Dilate(gray, gray)
        cpy = cv.CloneImage(gray)
        storage = cv.CreateMemStorage (0)
        contours = cv.FindContours( cpy, storage)

        perimeter = cv.ArcLength(contours, isClosed=1)

        # Ignore contours that are just outlines of the image
        while( abs(cv.ContourArea(contours) - symbol.width*symbol.height) < 15 or
               perimeter < 60):
            contours = contours.h_next()
            perimeter = cv.ArcLength(contours, isClosed=1)

        contourRect = cv.BoundingRect(contours)
        cv.DrawContours(cpy,contours,(0,255,0,0),(255,0,0,0),1)

        cRectArea = contourRect[2]*contourRect[3]
        ratio = cRectArea/perimeter

        # For testing ++++++++++++++++++++++++++++++++++++
        if "shape" in debug:
            cv.ShowImage("gray", gray)
            cv.ShowImage("cpy",cpy)
            
            print cRectArea
            print "Perimeter: ", perimeter
            print "Ratio: ", ratio
        #+++++++++++++++++++++++++++++++++++++++++++++++

        if ratio < 16.5:
            shape = "diamond"
        elif ratio < 20:
            shape = "squiggle"
        else:
            shape = "oval"
        # Got shape >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        if number > 1: shape += "s"
        print number, fill, color, shape
        print

        cards.append(Card(g, (number, fill, color, shape)))

        #symbols[k] = (color, fill, number, shape)
        cv.ShowImage("img", image)
        #cv.WaitKey(0)

    # Draw results on image
    newImage = cv.CloneImage(image)
    for card in cards:
        fill = card.attributes[1] if card.attributes[1] != "empty" else ""
        color = card.attributes[2]
        shape = card.attributes[3]
        
        if shape[-1] == "s":
            shape = shape[0:-1]
        
        name = "symbolimages/" + color + shape + fill + ".png" # fill + color + shape
        symbolFake = cv.LoadImage(name)
        for g in card.symbols:
            tmp = cv.CreateImage((g[2], g[3]), 8, 3)
            cv.Resize(symbolFake, tmp)
            symbolFake = tmp
            cv.SetImageROI(newImage, g)
            if cv.GetSize(symbolFake) != cv.GetSize(newImage):
                print "Warning: size of new symbol doesn't match ROI"
                continue
            cv.Copy(symbolFake, newImage)

    cv.ResetImageROI(newImage)
    
    cv.ShowImage("NewImage", newImage)
    cv.ShowImage("Original Image", image)
    cv.MoveWindow("NewImage",650, 0)
    
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

    #cv.ShowImage("sub", cpy)
    #cv.WaitKey(0)

    bboxes = []

    if contours:
        while(contours):
            area = cv.ContourArea(contours)

            # We also want the area of the contours to be relatively close to the
            # area of the bounding boxes.
            b = cv.BoundingRect(contours)
            barea = b[2]*b[3]



            # Only accept contours within a certain area range
            if (area > 250 and area < 5000 and area < image.width*image.height*2/3):

                # So if the area of the box is much different from the area of the
                # contour, then ignore it (no code yet)
                #print barea, area
                #print "Area diff:", abs(barea-area)
                
                # Inflate the rectangles slightly (to make recognition a little easier
                amount = 5
                b0 = b[0] - amount if b[0] >= amount else b[0]
                b1 = b[1] - amount if b[1] >= amount else 0
                b2 = b[2] + 2*amount if b[2] < 2*amount+image.width else b[2]
                b3 = b[3] + 2*amount if b[2] < 2*amount+image.height else b[3]

                # Tuples cannot be modified, so we
                # create a new one
                b = (b0, b1, b2, b3)
                
                bboxes.append(b)
                
                # For testing ++++++++++++++++++++++++++++++++++++++++++++++++++++++
                #cv.Rectangle(image, (b[0],b[1]), (b[0]+b[2], b[1]+b[3]), (255,0,0,0))
                #cv.ShowImage("sub", image)
                #cv.WaitKey(0)
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                
            contours = contours.h_next()

    bboxes = findDistinctBoxes(bboxes)

    areas = []
    
    # Find average size of bounding boxes and remove those that are not close to the average
    for b in bboxes:
        areas.append(b[2]*b[3])

    areas = sorted(areas)
    #print areas

    # Get the average.
    # I may want the mode instead.
    avg = sum(areas)/len(areas)
    #print avg

    # remove boxes that are very far from the average
    #if box is less than half the average, or greater than twice the average, then skip it.
    for b in bboxes:
        #print b[2]*b[3]
        if avg/2 > b[2]*b[3] or b[2]*b[3] > 2*avg:
            bboxes.remove(b)
            #print "remove!"

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

