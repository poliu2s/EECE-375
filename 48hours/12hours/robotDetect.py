import cv
import math



class robotDetect:
    def __init__(self):
        #constants used to be 600
        self.width = 600
        self.height = 600

    


        
    def findRobot(self):
        global warp
        global imgThreshold

        corners = [(237,112),(817,118),(988,444),(31,429)]

        #Load the picture that was taken
        target = [(0,0),(self.width,0),(self.width,self.height),(0,self.height)]
        image = cv.LoadImageM('finalDayRedSkirt17.jpg')


        #Using RGB to filter for red
        redFilter = cv.CreateImage(cv.GetSize(image), 8, 1)
        cv.InRangeS(image, cv.Scalar(0,0,130), cv.Scalar(100,100,255), redFilter)   #Filter for red - BGR
        cv.SaveImage('finalDayRedSkirt17filter.jpg', redFilter)


        redPoints = [ [0,0] ]

        # Collect all red points into a list called redPoints
        for i in range(0, 576):
            for j in range(0, 1024):
                if (redFilter[i,j] > 250):
                    redPoints.append([i, j])
                    
        redPoints.pop(0)

        print 'Number of red points: '
        print len(redPoints)
        print '----------------------'


        #Filter redPoints for all who have upNumber red pts above
        rpFilter1 = [ [0,0]]
        rpCount = 0
        upNumber = 15
        for i in range(0, len(redPoints)):

            rpCount = 0
            flag = 0
            for j in range(0, len(redPoints)):
                if (not (i == j)):
                    Ydifference = redPoints[i][0] - redPoints[j][0]
                    Xdifference = math.fabs(redPoints[i][1] - redPoints[j][1])

                    #Check number of points above
                    if (redPoints[i][1] == redPoints[j][1]) and (Ydifference > 0) and (Ydifference <upNumber):
                        rpCount = rpCount + 1

                    #Check number of points below
                    if (Xdifference < 5) and (Ydifference <0) and (Ydifference > -15):
                        flag = 1

            if (rpCount > upNumber-5) and (flag == 0):
                rpFilter1.append(redPoints[i])

        rpFilter1.pop(0)
        
        debugPic1 = cv.CreateImage(cv.GetSize(image), 8, 1)
        for i in range(0, len(rpFilter1)):
            debugPic1[rpFilter1[i][0], rpFilter1[i][1]] = 255
        cv.SaveImage('finalDayRedSkirt17RedFilter1.jpg', debugPic1)

        print 'Number of pts after rpFilter1'
        print len(rpFilter1)
        print '-------------------------------'



        #Take an arbitrary point for every group of points
        surroundingBox = 10
        rpFilter2 = [ [0,0] ]
        flagList = [ 0 ]
        flagList.pop(0)

        for i in range(0, len(rpFilter1)):   #list of flags for points
            flagList.append(0)
        
        for i in range(0, len(rpFilter1)):
            

            for j in range(0, len(rpFilter1)):
                if (not(i==j)):
                    Ydifference = math.fabs(rpFilter1[i][0] - rpFilter1[j][0])
                    Xdifference = math.fabs(rpFilter1[i][1] - rpFilter1[j][1])

                    if (Ydifference < surroundingBox) and (Xdifference < surroundingBox):
                        if (flagList[i] == 0):
                            flagList[j] = 1

        for i in range(0, len(flagList)):
            if (flagList[i] == 0):
                rpFilter2.append(rpFilter1[i])
   
        rpFilter2.pop(0)

        
        debugPic2 = cv.CreateImage(cv.GetSize(image), 8, 1)
        for i in range(0, len(rpFilter2)):
            debugPic2[rpFilter2[i][0], rpFilter2[i][1]] = 255
        cv.SaveImage('finalDayRedSkirt17final.jpg', debugPic2)

        print 'Number of pts after rpFilter2'
        print len(rpFilter2)
        print '-------------------------------'



        #Search through predicted x,y coordinates of robot and
        #find the closest object that matches
        x = 0
        y = 0
        minX = 99999
        minY = 99999
        minDistance = minX*minY
        minRed = -1
        for i in range(0, len(rpFilter2)):
            Xdifference = rpFilter2[i][1] - minX
            Ydifference = rpFilter2[i][0] - minY

            if (Xdifference*Ydifference < minDistance):
                minDistance = Xdifference*Ydifference
                minRed = i

        print 'Found Robot at'
        print rpFilter2[minRed]
        print 'Will return the above values to Anuj'
        print '--------------'
  

if __name__=='__main__':

    b = robotDetect()
    b.findRobot()

    print 'Done with program'
