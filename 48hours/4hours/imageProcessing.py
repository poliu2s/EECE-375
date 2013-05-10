import cv
import math
from candle import Candle
import pdb

WIDTH = 600 
HEIGHT = 600 

def warpImage(image, corners):

    mat = cv.CreateMat(3, 3, cv.CV_32F)
    target = [(0,0),(600,0),(600,600),(0,600)]
    cv.GetPerspectiveTransform(corners, target, mat)
    out = cv.CreateMat(600, 600, cv.CV_8UC3)
    cv.WarpPerspective(image, out, mat, cv.CV_INTER_CUBIC)
    return out

def convertToCentimeters(pixels):
        return pixels * 0.61

class CandleProcessor:

    # Take picture and warp it using homography.
    def loadPicture(self, image_name): 
        self.target = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)] 
        self.image = cv.LoadImageM(image_name) 
        
    def warpPicture(self, corners) :
        mat = cv.CreateMat(3, 3, cv.CV_32F) #Move scalars.
        cv.GetPerspectiveTransform(corners, self.target, mat)
        self.warp = cv.CreateMat(HEIGHT, WIDTH, cv.CV_8UC3)
        cv.WarpPerspective(self.image, self.warp, mat, cv.CV_INTER_CUBIC)
        cv.SaveImage('warped.jpg', self.warp)


    # Call this function to find the white candles. This function will return a list of Candle objects
    def findWhiteCandles(self, corners):
        #--------------------------------------------------------
        #Using RGB filter - White
        imgThresholdW = cv.CreateImage(cv.GetSize(self.image), 8, 1)
        cv.InRangeS(self.image, cv.Scalar(120,120,120), cv.Scalar(255,255,255), imgThresholdW)
        #--------------------------------------------------------

        cv.SaveImage('finalfieldFindingCandlelightWhite.jpg', imgThresholdW)

        gray = cv.CreateImage(cv.GetSize(self.image), 8,1)
        edges = cv.CreateImage(cv.GetSize(self.image),8,1)

        cv.CvtColor(self.image, gray, cv.CV_BGR2GRAY)
        cv.Canny(gray, edges, 40, 250,3)
        cv.SaveImage('finalfieldEdges.jpg', edges)

        #White points list
        whitePoints = []
        for i in range(corners[0][1], corners[3][1]):
                for j in range(0, 1024):
                    #Search if points above are black

                    if (imgThresholdW[i, j] > 250):
                        whitePoints.append([i,j])
   


        #White edges
        edgePointsW = [ [0,0]]
        for i in range(corners[0][1], corners[3][1]):
                for j in range(0, 1024):
                    if ((edges[i,j] > 250) and (imgThresholdW[i,j] > 250)):
                        edgePointsW.append([i,j])
        edgePointsW.pop(0)

    

        destiny = cv.CreateImage(cv.GetSize(self.image),8,1)
        for i in range(0, len(edgePointsW)):
                destiny[edgePointsW[i][0],edgePointsW[i][1]] = 255
        cv.SaveImage('finalfieldEdgesW.jpg', destiny)



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
        self.whiteBottoms = []
    
        while len(volatile1):
                inRange = []
                count = 0
                absLowest = volatile1[0]
        
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




                                absLowest = i
                    self.whiteBottoms.append(absLowest)
                toRemove = []
                for i in range(len(toPop)):
                    toRemove.append(volatile1[toPop[i]])
                for i in range(len(toRemove)):
                    volatile1.remove(toRemove[i])
            


        
        
        toRemove = []
        for i in range(0, len(self.blackBottoms)):
                for j in range(0, len(self.whiteBottoms)):
                    yFit = bool (abs(self.whiteBottoms[j][0] - self.blackBottoms[i][0]) <= 35)
                    xFit = bool (abs(self.whiteBottoms[j][1] - self.blackBottoms[i][1]) <= 35) 
            
                    if yFit and xFit and (self.whiteBottoms[j] not in toRemove):
                        toRemove.append(self.whiteBottoms[j])
                        
        for i in range(len(toRemove)):
                self.whiteBottoms.remove(toRemove[i])


        destiny = cv.CreateImage(cv.GetSize(self.image),8,1)
        for i in range(0, len(self.whiteBottoms)):
                destiny[self.whiteBottoms[i][0],self.whiteBottoms[i][1]] = 255
        cv.SaveImage('finalfieldDaniersMagicW.jpg', destiny)
        
        
        imageWhite = cv.LoadImageM('finalfieldDaniersMagicW.jpg')
        myWhiteBases = warpImage(imageWhite, corners)
        cv.SaveImage('warpW.jpg', myWhiteBases)


        #Loop through each point in the warped image
        eliminateMultiple = cv.LoadImageM('warpW.jpg')
        warpWgray = cv.CreateImage(cv.GetSize(eliminateMultiple), 8,1)
        cv.CvtColor(eliminateMultiple, warpWgray, cv.CV_BGR2GRAY)
        
        
        finalWhiteBaseList = []
        for i in range(0, 600):
                for j in range(0, 600):
                        if (warpWgray[i, j] > 0):
                                finalWhiteBaseList.append([j,i])





        toRemove = []
        for i in range(0, len(finalWhiteBaseList)):
                for j in range(i, len(finalWhiteBaseList)):
                    yFit = bool (abs(finalWhiteBaseList[j][0] - finalWhiteBaseList[i][0]) < 10)
                    xFit = bool (abs(finalWhiteBaseList[j][1] - finalWhiteBaseList[i][1]) < 10) 
            
                    if (not(i==j)) and yFit and xFit and (finalWhiteBaseList[j] not in toRemove):
                        toRemove.append(finalWhiteBaseList[j])
                        
        for i in range(len(toRemove)):
               finalWhiteBaseList.remove(toRemove[i])

        # print len(finalWhiteBaseList)
        # print finalWhiteBaseList
        # Return white candles  

        white_candle_list = []
        for base in finalWhiteBaseList:
            white_candle_list.append(Candle(convertToCentimeters(int(base[0])), convertToCentimeters(int(base[1])), 1, 0))        
        return white_candle_list



    # Call this function to find the black candles. This function will return a list of Candle objects    
    def findBlackCandles(self, corners2):

        #--------------------------------------------------------
        #Using RGB filter - Black
        imgThresholdB = cv.CreateImage(cv.GetSize(self.image), 8, 1)
        cv.InRangeS(self.image, cv.Scalar(0,0,0), cv.Scalar(70,70,70), imgThresholdB)
        #--------------------------------------------------------

        cv.SaveImage('finalfieldFindingCandlelightBlack.jpg', imgThresholdB)
        gray = cv.CreateImage(cv.GetSize(self.image), 8,1)
        edges = cv.CreateImage(cv.GetSize(self.image),8,1)

        cv.CvtColor(self.image, gray, cv.CV_BGR2GRAY)
        cv.Canny(gray, edges, 40, 250,3)
        cv.SaveImage('finalfieldEdges.jpg', edges)


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




        THRESHOLD = 7 #8
        BOT_THRESH = 2
        self.blackBottoms = []
    
        while len(volatile):
                inRange = []
                count = 0
                absLowest = volatile[0]

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




                                absLowest = i
                    self.blackBottoms.append(absLowest)
                toRemove = []
                for i in range(len(toPop)):
                    toRemove.append(volatile[toPop[i]])
                for i in range(len(toRemove)):
                    volatile.remove(toRemove[i])


        destiny = cv.CreateImage(cv.GetSize(self.image),8,1)
        for i in range(0, len(self.blackBottoms)):
                destiny[self.blackBottoms[i][0],self.blackBottoms[i][1]] = 255
        cv.SaveImage('finalfieldDaniersMagicB.jpg', destiny)

        imageBlack = cv.LoadImageM('finalfieldDaniersMagicB.jpg')
        myBlackBases = warpImage(imageBlack, corners2)

        cv.SaveImage('warpB.jpg', myBlackBases)



        #Loop through each point in the warped image
        eliminateMultiple = cv.LoadImageM('warpB.jpg')
        warpBgray = cv.CreateImage(cv.GetSize(eliminateMultiple), 8,1)
        cv.CvtColor(eliminateMultiple, warpBgray, cv.CV_BGR2GRAY)
        
        
        finalBlackBaseList = []
        for i in range(0, 600):
                for j in range(0, 600):
                        if (warpBgray[i, j] > 0):
                                finalBlackBaseList.append([j,i])

        toRemove = []
        for i in range(0, len(finalBlackBaseList)):
                for j in range(i, len(finalBlackBaseList)):
                    yFit = bool (abs(finalBlackBaseList[j][0] - finalBlackBaseList[i][0]) < 10)
                    xFit = bool (abs(finalBlackBaseList[j][1] - finalBlackBaseList[i][1]) < 10) 
            
                    if (not(i==j)) and yFit and xFit and (finalBlackBaseList[j] not in toRemove):
                        toRemove.append(finalBlackBaseList[j])

        for i in range(len(toRemove)):
               finalBlackBaseList.remove(toRemove[i])
        
        
        black_candle_list = []
        for base in finalBlackBaseList:
            black_candle_list.append(Candle(convertToCentimeters(int(base[0])), convertToCentimeters(int(base[1])), 0, 0))
        
        # Find and return black candles
        return black_candle_list