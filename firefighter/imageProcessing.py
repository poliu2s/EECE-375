## We need to make the image processing code slightly smarter. Here, I'm not referring to the technical details of the image processing algorithm, but just that the algorithm should be able to detect that there should only be 4 candles of each color on the field. If extra candles are found, do something to handle this. (Maybe retake a picture?) 
## Similarly, if we're looking for our robot and we find two robots, we should be able to have extra checks to figure out which one is actually ours. 


import cv
import math
from candle import Candle
import pdb

WIDTH = 600 ## Are these always going to be 600*600 ?
HEIGHT = 600 
corners = [(711,877),(1972,902),(2332,1448),(310,1410)]

def convertToMeters(pixels, totalPixels):
        return pixels * 9.0 / totalPixels * 0.3048

class ecePredator:

    # Take picture and warp it using homography.
    def loadPicture(self, file_name):        
        self.target = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)] # Make 0 a scalar.
        self.image = cv.LoadImageM(file_name) ## Currently image is being loaded by a file. Instead image needs to be taken directly from camera for this.
        
    # Using corners (constant) instead of corners2 for now.
    def warpPicture(self, corners2) :
        mat = cv.CreateMat(3, 3, cv.CV_32F) #Move scalars.
        cv.GetPerspectiveTransform(corners2, self.target, mat)
        self.warp = cv.CreateMat(HEIGHT, WIDTH, cv.CV_8UC3)
        cv.WarpPerspective(self.image, self.warp, mat, cv.CV_INTER_CUBIC)
        cv.SaveImage('warped.jpg', self.warp)


    # Call this function to find the white candles. This function will return a list of Candle objects
    def findWhiteCandles(self):
        self.imgThreshold = cv.CreateImage(cv.GetSize(self.warp), 8, 1)
        cv.InRangeS(self.warp, cv.Scalar(160,160,160), cv.Scalar(255,255,255), self.imgThreshold)
        cv.SaveImage('0white_Filter.jpg', self.imgThreshold)

        # Find and return white candles
        return self.__findCandles("white")

    # Call this function to find the black candles. This function will return a list of Candle objects    
    def findBlackCandles(self):
        self.imgThreshold = cv.CreateImage(cv.GetSize(self.warp), 8, 1) ## Remove scalars
        cv.InRangeS(self.warp, cv.Scalar(0,0,0), cv.Scalar(40,40,40), self.imgThreshold) ## Remove scalars
        cv.SaveImage('0black_Filter.jpg', self.imgThreshold)
        # Find and return black candles

        print 'Exiting Image Recognition'
        print '--------------------------'
        return self.__findCandles("black")

    # This function is called to 
    def __findCandles(self, color):
        #self.imgThreshold will contain the b/w image in which the candles need to be searched. 
        #The list that stores all the points that make up all black candles
        unfiltered_list = []

        #Figure out which points past filter are white
        for i in range(0, 600): ## Remove scalars
            for j in range(0, 600): ## Remove scalars
                if (self.imgThreshold[i, j] > 250) : ## Remove scalars
                    unfiltered_list.append([i, j])


        # Apply filters for outliers
        if (color == 'black'):
                potential_base_points = self.__findPotentialBasePointsB(unfiltered_list)

                destiny = cv.CreateImage(cv.GetSize(self.imgThreshold),8,1)
                for i in range(0, len(potential_base_points)):
                    destiny[potential_base_points[i][0],potential_base_points[i][1]] = 255
                cv.SaveImage('BasesBlack.jpg', destiny)
        elif (color == 'white'):
                potential_base_points = self.__findPotentialBasePointsW(unfiltered_list)

                destiny = cv.CreateImage(cv.GetSize(self.imgThreshold),8,1)
                for i in range(0, len(potential_base_points)):
                    destiny[potential_base_points[i][0],potential_base_points[i][1]] = 255
                cv.SaveImage('BasesWhite.jpg', destiny)

        
        # Remove multiple indicators for a single candle
        candle_indicators = self.__removeMultipleIndicators(potential_base_points)
        if (color == 'white'):
                destiny = cv.CreateImage(cv.GetSize(self.imgThreshold),8,1)
                for i in range(0, len(candle_indicators)):
                    destiny[candle_indicators[i][0],candle_indicators[i][1]] = 255
                cv.SaveImage('BasesWhiteAfterMultiRemoval.jpg', destiny)
        elif (color == 'black'):
                destiny = cv.CreateImage(cv.GetSize(self.imgThreshold),8,1)
                for i in range(0, len(candle_indicators)):
                    destiny[candle_indicators[i][0],candle_indicators[i][1]] = 255
                cv.SaveImage('BasesBlackAfterMultiRemoval.jpg', destiny)

        
        # Convert points representing candles into Candle objects
        candle_list = [] 
        for candle_base in candle_indicators:
            x_pos = convertToMeters(candle_base[1], WIDTH) 
            y_pos = convertToMeters(candle_base[0], HEIGHT)
            candle = Candle(x_pos, y_pos, color, 0)
            candle_list.append(candle)


        return candle_list

    def __removeMultipleIndicators(self, potential_base_points):
        candle_indicators = []
        Xlimit = 7
        Ylimit = 7
        
        for i in range(0, len(potential_base_points)):
            flag_multiple_indicators = False
            for j in range(i, len(potential_base_points)):
                if ( i != j ):
                    Ydifference = math.fabs(potential_base_points[i][0] - potential_base_points[j][0])
                    Xdifference = math.fabs(potential_base_points[j][1] - potential_base_points[i][1])

                    #If there are more than one point per candle, delete it from the stack
                    if (Ydifference < Ylimit) and (Xdifference < Xlimit) :
                        flag_multiple_indicators = True

                    #(White only) If two points show up to represent one candle, eliminate the topmost point
                    Ydifference = potential_base_points[i][0] - potential_base_points[j][0]
                    Xdifference = potential_base_points[j][1] - potential_base_points[i][1]
                    if ((Ydifference < 0) and (Ydifference > -70) and (Xdifference < 15) and (Xdifference > -15)):
                            flag_multiple_indicators = True
            if flag_multiple_indicators==False:
                candle_indicators.append(potential_base_points[i])
        return candle_indicators
    
    def __findPotentialBasePointsB(self, unfiltered_list): 
        potential_base_points = []
        number_unfiltered = len(unfiltered_list)
        searchUpPositive = 20  
        #Loop through each element and compare if fits profile
        for i in range(0, number_unfiltered):
            flag_base = True # used to determine whether to append
            for j in range(0, number_unfiltered): #comparing against all number_unfiltered
                if (not(i==j)):
                    Ydifference = unfiltered_list[j][0] - unfiltered_list[i][0]
                    Xdifference = math.fabs(unfiltered_list[j][1] - unfiltered_list[i][1])
                    #If any other points appear right below this one, it is not a candle base
                    if (Ydifference < 10) and (Ydifference > 0) and (Xdifference < 10) and (Xdifference > 0): ## Remove scalars
                        flag_base = False
                        break
            if flag_base:
                number_points_above_current = 0
                #count the number points above the high chance point
                for j in range(0, number_unfiltered):
                    if (not(i==j)):
                        Ydifference = unfiltered_list[i][0] - unfiltered_list[j][0]
                        Xdifference = math.fabs(unfiltered_list[j][1] - unfiltered_list[i][1])
                        #If many points appear above, it must be a candle base
                        if (Ydifference < 10) and (Ydifference > 0) and (Xdifference < 10) and (Xdifference > 0): ## Remove scalars
                            number_points_above_current += 1
                        ##TODO: If there is already another point beside this point, then take the leftmost 
                if (number_points_above_current > searchUpPositive): ## Remove scalars
                    potential_base_points.append(unfiltered_list[i])
        return potential_base_points




    def __findPotentialBasePointsW(self, unfiltered_list):

        warpedPic = cv.LoadImageM('warped.jpg')
        gray = cv.CreateImage(cv.GetSize(warpedPic), 8,1)
        edges = cv.CreateImage(cv.GetSize(warpedPic),8,1)
        
        cv.CvtColor(self.warp, gray, cv.CV_BGR2GRAY)
        cv.Canny(gray, edges, 30,100,3)
        cv.SaveImage('warpedEdges.jpg', edges)

        
        potential_base_points = []
        number_unfiltered = len(unfiltered_list)
        #Loop through each element and compare if fits profile
        searchUpPositive =  7   #how many points there must appear above
        aroundLimit = 4
        
        for i in range(0, number_unfiltered):
            flag_base = True # used to determine whether to append
            for j in range(0, number_unfiltered): #comparing against all number_unfiltered
                if (not(i==j)):
                    Ydifference = unfiltered_list[j][0] - unfiltered_list[i][0]
                    Xdifference = math.fabs(unfiltered_list[j][1] - unfiltered_list[i][1])
                    #If any other points appear right below this one, it is not a candle base
                    if (Ydifference < 10) and (Ydifference > 0) and (Xdifference < 10) and (Xdifference > 0): ## Remove scalars
                        flag_base = False
                        break
            if flag_base:
                number_points_above_current = 0
                number_points_around_current = 0
                #count the number points above the high chance point
                for j in range(0, number_unfiltered):
                    if (not(i==j)):
                        Ydifference = unfiltered_list[i][0] - unfiltered_list[j][0]
                        Xdifference = math.fabs(unfiltered_list[j][1] - unfiltered_list[i][1])
                        #If many points appear above, it must be a candle base
                        if (Ydifference < 10) and (Ydifference > 0) and (Xdifference < 10) and (Xdifference > 0): ## Remove scalars
                            number_points_above_current += 1

                        #Counts the number of points to the left and right to see if the base exists
                        if ((math.fabs(Ydifference) < 2) and (Xdifference < 5)):
                            number_points_around_current += 1    
                        ##TODO: If there is already another point beside this point, then take the leftmost 
                if ((number_points_above_current > searchUpPositive) and (number_points_around_current > aroundLimit)):
                    potential_base_points.append(unfiltered_list[i])
        return potential_base_points
