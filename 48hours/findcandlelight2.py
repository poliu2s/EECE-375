import math
import cv

if __name__ == '__main__':
    
    image = cv.LoadImageM('finalfield21.jpg')

    #--------------------------------------------------------
    #Using RGB filter - White
    imgThresholdW = cv.CreateImage(cv.GetSize(image), 8, 1)
    cv.InRangeS(image, cv.Scalar(110,110,110), cv.Scalar(255,255,255), imgThresholdW)
    #--------------------------------------------------------

    #--------------------------------------------------------
    #Using RGB filter - Black
    imgThresholdB = cv.CreateImage(cv.GetSize(image), 8, 1)
    cv.InRangeS(image, cv.Scalar(0,0,0), cv.Scalar(70,70,70), imgThresholdB)
    #--------------------------------------------------------

    
    cv.SaveImage('finalfield21FindingCandlelightWhite.jpg', imgThresholdW)
    cv.SaveImage('finalfield21FindingCandlelightBlack.jpg', imgThresholdB)




    gray = cv.CreateImage(cv.GetSize(image), 8,1)
    edges = cv.CreateImage(cv.GetSize(image),8,1)

    cv.CvtColor(image, gray, cv.CV_BGR2GRAY)
    cv.Canny(gray, edges, 40, 250,3)
    cv.SaveImage('finalfield21Edges.jpg', edges)


    #White points list
    whitePoints = []
    for i in range(0, 576):
        for j in range(0, 1024):
            #Search if points above are black

            if (imgThresholdW[i, j] > 250):
                whitePoints.append([i,j])
   
    
    #Find black candle positions
    edgePointsB = [ [0,0]]
    for i in range(0, 576):
        for j in range(0, 1024):
            if (edges[i,j] > 250):

                #Search if points above are black
                for k in range(0, 10):
                    if ((i-k > 0) and (imgThresholdB[i-k, j] > 250)):
                        edgePointsB.append([i,j])
                        break
    edgePointsB.pop(0)
   
    
    destiny = cv.CreateImage(cv.GetSize(image),8,1)
    for i in range(0, len(edgePointsB)):
        destiny[edgePointsB[i][0],edgePointsB[i][1]] = 255
    cv.SaveImage('finalfield21EdgesB.jpg', destiny)




    #White edges
    edgePointsW = [ [0,0]]
    for i in range(0, 576):
        for j in range(0, 1024):
            if ((edges[i,j] > 250) and (imgThresholdW[i,j] > 250)):
                edgePointsW.append([i,j])
    edgePointsW.pop(0)

    

    destiny = cv.CreateImage(cv.GetSize(image),8,1)
    for i in range(0, len(edgePointsW)):
        destiny[edgePointsW[i][0],edgePointsW[i][1]] = 255
    cv.SaveImage('finalfield21EdgesW.jpg', destiny)


    
    toRemove = []
    for i in range(0, len(blackBottoms)):
        for j in range(0, len(whiteBottoms)):
            yFit = bool (abs(whiteBottoms[j][0] - blackBottoms[i][0]) <= 35)
            xFit = bool (abs(whiteBottoms[j][1] - blackBottoms[i][1]) <= 35) 
            
            if yFit and xFit and (whiteBottoms[j] not in toRemove):
                toRemove.append(whiteBottoms[j])
    for i in range(len(toRemove)):
        whiteBottoms.remove(toRemove[i])



    destiny = cv.CreateImage(cv.GetSize(image),8,1)
    for i in range(0, len(whiteBottoms)):
        destiny[whiteBottoms[i][0],whiteBottoms[i][1]] = 255
    cv.SaveImage('finalfield21DaniersMagicW.jpg', destiny)
        


#----------------------------------------------------------------
#----------------------------------------------------------------


    #Daniel
    #For finding 
    volatile1 = []

    for i in range(len(whitePoints)):
            inserted = False
            for j in range(len(volatile1)):
                if whitePoints[i][0] < volatile1[j][0]:
                    volatile1.insert( j, whitePoints[i])
                    inserted = True
                elif whitePoints[i][0] == volatile1[j][0]:
                    if whitePoints[i][1] < volatile1[j][1]:
                        volatile1.insert( j, whitePoints[i])
            if not inserted:
                volatile1.append([whitePoints[i][0], whitePoints[i][1]])


    THRESHOLD = 40 #8
    BOT_THRESH = 2
    whiteBottoms = []
    
    while len(volatile1):
        inRange = []
        count = 0
        absLowest = volatile1[0]
        print absLowest
        toPop = []
        for i in range(len(volatile1)):
            yFit = bool ((volatile1[i][0] <= volatile1[0][0] + 45) and (volatile1[0][0] <= volatile1[i][0]))
            xFit = bool (abs(volatile1[i][1] - volatile1[0][1]) <= 50) 
            if yFit and xFit:
                inRange.append(volatile1[i])
                count += 1
                toPop.append(i)
        if count >= THRESHOLD:
            for i in inRange:
                if i[0] > absLowest[0]:
##                    for j in inRange:
##                        counter = 0
##                        yFit = bool (abs(i[0] - j[0]) <= 2)
##                        xFit = bool (abs(i[1] - j[1]) <= 10)
##                        if yFit and xFit:
##                            counter += 1
##                    if counter >= BOT_THRESH:
                        absLowest = i
            whiteBottoms.append(absLowest)
        toRemove = []
        for i in range(len(toPop)):
            toRemove.append(volatile1[toPop[i]])
        for i in range(len(toRemove)):
            volatile1.remove(toRemove[i])
            
    print whiteBottoms



##    For finding black base points

    volatile = []
    for i in range(len(edgePointsB)):
            inserted = False
            for j in range(len(volatile)):
                if edgePointsB[i][0] < volatile[j][0]:
                    volatile.insert( j, edgePointsB[i])
                    inserted = True
                elif edgePointsB[i][0] == volatile[j][0]:
                    if edgePointsB[i][1] < volatile[j][1]:
                        volatile.insert( j, edgePointsB[i])
            if not inserted:
                volatile.append([edgePointsB[i][0], edgePointsB[i][1]])




    THRESHOLD = 8
    BOT_THRESH = 2
    blackBottoms = []
    
    while len(volatile):
        inRange = []
        count = 0
        absLowest = volatile[0]
        print absLowest
        toPop = []
        for i in range(len(volatile)):
            yFit = bool ((volatile[i][0] <= volatile[0][0] + 45) and (volatile[0][0] <= volatile[i][0]))
            xFit = bool (abs(volatile[i][1] - volatile[0][1]) <= 50) 
            if yFit and xFit:
                inRange.append(volatile[i])
                count += 1
                toPop.append(i)
        if count >= THRESHOLD:
            for i in inRange:
                if i[0] > absLowest[0]:
##                    for j in inRange:
##                        counter = 0
##                        yFit = bool (abs(i[0] - j[0]) <= 2)
##                        xFit = bool (abs(i[1] - j[1]) <= 10)
##                        if yFit and xFit:
##                            counter += 1
##                    if counter >= BOT_THRESH:
                        absLowest = i
            blackBottoms.append(absLowest)
        toRemove = []
        for i in range(len(toPop)):
            toRemove.append(volatile[toPop[i]])
        for i in range(len(toRemove)):
            volatile.remove(toRemove[i])
    print blackBottoms

    destiny = cv.CreateImage(cv.GetSize(image),8,1)
    for i in range(0, len(blackBottoms)):
        destiny[blackBottoms[i][0],blackBottoms[i][1]] = 255
    cv.SaveImage('finalfield21DaniersMagicB.jpg', destiny)







    


    
    

    
