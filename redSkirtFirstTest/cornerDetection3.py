import cv
import math

class eceCorners:
    def __init__(self):
        #constants used to be 600
        self.width = 600
        self.height = 480
        self.warp = cv.CreateMat(600,600,cv.CV_8UC3)
        self.imgThreshold = cv.CreateMat(600,600,cv.CV_8UC3)
        whiteCandleList = [ [0,0] ]
        blackCandleList = [ [0,0] ]
    
        
    def findCorners(self):
        global warp
        global imgThreshold

        corners = [(711,877),(1972,902),(2332,1448),(310,1410)]

        #Load the picture that was taken
        target = [(0,0),(self.width,0),(self.width,self.height),(0,self.height)]
        image = cv.LoadImageM('redSkirtTestPic.jpg')


        #For Finding Corners
        imgThreshold = cv.CreateImage(cv.GetSize(image), 8, 1)
        imgThreshold2 = cv.CreateImage(cv.GetSize(image), 8, 1)
        cv.InRangeS(image, cv.Scalar(120,120,0), cv.Scalar(255,255,160), imgThreshold)   #Filter for blue; if selected, shows as white point
        cv.InRangeS(image, cv.Scalar(120,120,0), cv.Scalar(255,255,160), imgThreshold2)
        cv.SaveImage('findingCorners.jpg', imgThreshold)


        
        
        #Turn imgThreshold into a grayscale and apply Canny
        gray = cv.CreateImage(cv.GetSize(image), 8,1)
        edges = cv.CreateImage(cv.GetSize(image),8,1)
        
        cv.CvtColor(image, gray, cv.CV_BGR2GRAY)
        cv.Canny(gray, edges, 30,200,3)               # Canny parameters thresholds
        cv.SaveImage('findingCorners2.jpg', edges)

        
        #Lists that will be used for filtering the field corners
        bluePoints = [ [0,0] ]
        edgePoints = [ [0,0]]
        edgePoints2 = [ [0,0]]
        cornerUpper = [ [0,0] ]
        cornerLower = [ [0,0] ]
        cornerUL = [[0,0]]
        cornerUR = [[0,0]]
        cornerLL = [[0,0]]
        cornerLR = [[0,0]]
        imgWidth,imgHeight = cv.GetSize(imgThreshold)

        #Loop through each element that passed Canny filter
        for i in range(0, 576):     #replace later with imgHeight
            for j in range(0, 1024):    #replace later with imgWidth
                if ( edges[i,j] > 250):
                    edgePoints.append([i,j])
                    edgePoints2.append([i,j])
        edgePoints.pop(0)
        edgePoints2.pop(0)

        print 'Number of edgePoints: '
        print len(edgePoints)
        print '----'

        

        #Find Upper Corners
        searchDown = 30         #The number of pixels to look downwards
        searchPositive = 20     #The number of pixels need to fit profile
        i = 0
        while (i< len(edgePoints) - 1):
            i = i + 1
            imgX = edgePoints[i][0]
            imgY = edgePoints[i][1]

            blueCount = 0

            #Search for points underneath the canny edges
            for j in range (0, searchDown):
                imgX = imgX + j

                if (imgX < imgHeight): #Catches array out of bounds errors
                    
                    if (imgThreshold[imgX,  imgY] > 250):
                        blueCount = blueCount + 1
                                        
              
            if (blueCount > searchPositive ):
                cornerUpper.append(edgePoints[i])

        cornerUpper.pop(0)
        print 'Number of CornerUpper Points: '
        print len(cornerUpper)
        print '----'


        #UpperLeft Point
        i = 0
        searchPositive = 20
        Ylimit = 2
        Xlimit = -5
        while (i < len(cornerUpper)):
            upperEdgeCount = 0
            for j in range (i, len(cornerUpper)):
                if (not(i==j)):
                    Xdifference = cornerUpper[i][0] - cornerUpper[j][0]
                    Ydifference = math.fabs(cornerUpper[i][0] - cornerUpper[j][0])

                    if ((Ydifference < Ylimit) and (Xdifference < 0) and (Xdifference > Xlimit)):
                        upperEdgeCount = upperEdgeCount + 1
            if (upperEdgeCount > searchPositive):
                cornerUL.append(cornerUpper[i])

            i = i + 1

        cornerUL.pop(0)      
        print 'Number of UL points: '
        print len(cornerUL)
        print '-----'
        

        #UpperRight Point Filter
        i = 0
        searchPositive = 60
        Ylimit = 2
        Xlimit = 10
        
        while (i < len(cornerUpper)):
            upperEdgeCount = 0
            for j in range (0, len(cornerUpper)):
                if (not(i==j)):
                    Xdifference = cornerUpper[i][0] - cornerUpper[j][0]
                    Ydifference = math.fabs(cornerUpper[i][0] - cornerUpper[j][0])

                    if ((Ydifference < Ylimit) and (Xdifference < Xlimit) and (Xdifference > 0)):
                        upperEdgeCount = upperEdgeCount + 1
            if (upperEdgeCount > searchPositive):
                cornerUR.append(cornerUpper[i])

            i = i + 1

        cornerUR.pop(0)
        print 'Number of UR points: '
        print len(cornerUR)
        print '-----'



        #Find Lower Corners
        searchUp = 30         #The number of pixels to look downwards
        searchPositive = 20     #The number of pixels need to fit profile
        i = 0
        while (i< len(edgePoints2)):
            
            imgXa = edgePoints2[i][0]
            imgYa = edgePoints2[i][1]
            blueCount1 = 0
                                        
            for j in range (0, searchUp):
                if (imgXa-j > 0):
                    if (imgThreshold[imgXa-j,imgYa] > 250 ):
                        
                        blueCount1= blueCount1 + 1

            if (blueCount1>searchPositive):
                cornerLower.append(edgePoints2[i])

            i = i + 1

        cornerLower.pop(0)
        print 'Number of CornerLower Points: '
        print len(cornerLower)
        print '----'
            
        

        #LowerLeft Point
        i = 0
        searchPositive = 20
        Ylimit = 2
        Xlimit = -5
        while (i < len(cornerLower)):
            lowerEdgeCount = 0
            for j in range (i, len(cornerLower)):
                if (not(i==j)):
                    Xdifference = cornerLower[i][0] - cornerLower[j][0]
                    Ydifference = math.fabs(cornerLower[i][0] - cornerLower[j][0])

                    if ((Ydifference < Ylimit) and (Xdifference < 0) and (Xdifference > Xlimit)):
                        lowerEdgeCount = lowerEdgeCount + 1
            if (lowerEdgeCount > searchPositive):
                cornerLL.append(cornerLower[i])

            i = i + 1

        cornerLL.pop(0)      
        print 'Number of LL points: '
        print len(cornerLL)
        print '-----'


        #LL -- find the min
        minimumY = 20000
        for i in range(0, len(cornerLL)):
            if (minimumY > cornerLL[i][1]):
                minimumY = cornerLL[i][1]
                minimumX = cornerLL[i][0]

        
        #LR -- find the max
        maximumY = 0
        for i in range(0, len(cornerLL)):
            if(maximumY < cornerLL[i][1]):
                maximumY = cornerLL[i][1]
                maximumX = cornerLL[i][0]
                
            
        #Collect the corners into a list
        corners = [ (cornerUL[0][1], cornerUL[0][0]),
                    (cornerUR[len(cornerUR)-1][1], cornerUR[len(cornerUR)-1][0]),
                    (maximumY, maximumX),
                    (minimumY, minimumX)
                    ]


        print corners




        #Debugging plots - Don't Remove! will need for calibration
        
        print 'Plot debugging stuff now...'
        destiny = cv.CreateImage(cv.GetSize(image),8,1)
        destiny1 = cv.CreateImage(cv.GetSize(image),8,1)
        destiny2 = cv.CreateImage(cv.GetSize(image),8,1)
        destiny3 = cv.CreateImage(cv.GetSize(image),8,1)
        destiny4 = cv.CreateImage(cv.GetSize(image),8,1)
        destiny5 = cv.CreateImage(cv.GetSize(image),8,1)
        destinyUL = cv.CreateImage(cv.GetSize(image),8,1)
        destinyUR = cv.CreateImage(cv.GetSize(image),8,1)
        destinyLL = cv.CreateImage(cv.GetSize(image),8,1)
        destinyLR = cv.CreateImage(cv.GetSize(image),8,1)
        destinyZ = cv.CreateImage(cv.GetSize(image),8,1)



        for i in range(0, len(cornerUpper)):
            destiny[cornerUpper[i][0],cornerUpper[i][1]] = 255
        cv.SaveImage('findingCorners3.jpg', destiny)

        for i in range(0, len(cornerUL)):
            destiny1[cornerUL[i][0],cornerUL[i][1]] = 255
        cv.SaveImage('findingCorners4.jpg', destiny1)

        for i in range(0, len(cornerUR)):
            destiny2[cornerUR[i][0],cornerUR[i][1]] = 255
        cv.SaveImage('findingCorners5.jpg', destiny2)

        for i in range(0, len(cornerLower)):
            destiny3[cornerLower[i][0],cornerLower[i][1]] = 255
        cv.SaveImage('findingCorners6.jpg', destiny3)

        for i in range(0, len(cornerLL)):
            destiny4[cornerLL[i][0],cornerLL[i][1]] = 255
        cv.SaveImage('findingCorners7.jpg', destiny4)

        
        #-------------
        #Plot UL point
        #-------------
        for i in range(0, imgWidth):
            destinyUL[cornerUL[0][0],i] = 255
            destinyUL[cornerUL[0][0]+1, i] = 255
                        
        for i in range(0, imgHeight):
            destinyUL[i,cornerUL[0][1]] = 255
            destinyUL[i,cornerUL[0][1]+1] = 255

        

        cv.Circle(destinyUL, (cornerUL[0][1], cornerUL[0][0]), 30, 200, 5, 8, 0)
        cv.SaveImage('findingCornersUL.jpg', destinyUL)

        #--------------
        #Plot UR point
        #--------------
        for i in range(0, imgWidth):
            destinyUR[cornerUR[len(cornerUR)-1][0],i] = 255
            destinyUR[cornerUR[len(cornerUR)-1][0]+1, i] = 255
                        
        for i in range(0, imgHeight):
            destinyUR[i,cornerUR[len(cornerUR)-1][1]] = 255
            destinyUR[i,cornerUR[len(cornerUR)-1][1]+1] = 255

        cv.SaveImage('findingCornersUR.jpg', destinyUR)

        #--------------
        #Plot LL point
        #--------------
        for i in range(0, imgWidth):
            destinyLL[minimumX,i] = 255
            destinyLL[minimumX+1, i] = 255
                        
        for i in range(0, imgHeight):
            destinyLL[i,minimumY] = 255
            destinyLL[i,minimumY+1] = 255

        cv.SaveImage('findingCornersLL.jpg', destinyLL)


        #--------------
        #Plot LR point
        #--------------
        for i in range(0, imgWidth):
            destinyLR[maximumX,i] = 255
            destinyLR[maximumX+1, i] = 255
                        
        for i in range(0, imgHeight):
            destinyLR[i,maximumY] = 255
            destinyLR[i,maximumY+1] = 255

        cv.SaveImage('findingCornersLR.jpg', destinyLR)

        

        
        


        # Use the corners to warp
        mat = cv.CreateMat(3, 3, cv.CV_32F)
        cv.GetPerspectiveTransform(corners, target, mat)
        out = cv.CreateMat(self.height, self.width, cv.CV_8UC3)
        warp = out
        cv.WarpPerspective(image, out, mat, cv.CV_INTER_CUBIC)

        cv.SaveImage('bigblue_warped.jpg', out)

        

            
  

if __name__=='__main__':

    b = eceCorners()
    b.findCorners()

    print 'Done with program'

    
    
    
