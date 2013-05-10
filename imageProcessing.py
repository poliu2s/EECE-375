## We need to make the image processing code slightly smarter. Here, I'm not referring to the technical details of the image processing algorithm, but just that the algorithm should be able to detect that there should only be 4 candles of each color on the field. If extra candles are found, do something to handle this. (Maybe retake a picture?) 
## Similarly, if we're looking for our robot and we find two robots, we should be able to have extra checks to figure out which one is actually ours. 


import cv
import math
from candle import Candle
import pdb

file_name = 'bigblue.jpg'
corners = [(711,877),(1972,902),(2332,1448),(310,1410)] ## Find a way to calibrate field corners automatically. I think Po's already working on this.
WIDTH = 600 ## Are these always going to be 600*600 ?
HEIGHT = 600


def convertToMeters(pixels, totalPixels):
        return pixels * 9.0 / totalPixels * 0.3048

class ecePredator:

        
    #Po's awesomeness - Finds corners of the field once picture is taken
    def findCorners(self):
        



    

    # Take picture and warp it using homography.
    def takePicture(self):        
        target = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
        image = cv.LoadImageM(file_name) ## Currently image is being loaded by a file. Instead image needs to be taken directly from camera for this.
        mat = cv.CreateMat(3, 3, cv.CV_32F)
        cv.GetPerspectiveTransform(corners, target, mat)
        self.warp = cv.CreateMat(HEIGHT, WIDTH, cv.CV_8UC3)
        cv.WarpPerspective(image, self.warp, mat, cv.CV_INTER_CUBIC)




    # Call this function to find the white candles. This function will return a list of Candle objects
    def findWhiteCandles(self):
        self.imgThreshold = cv.CreateImage(cv.GetSize(self.warp), 8, 1)
        cv.InRangeS(self.warp, cv.Scalar(140,140,140), cv.Scalar(255,255,255), self.imgThreshold)
        # Find and return white candles
        return self.__findCandles("white")

    # Call this function to find the black candles. This function will return a list of Candle objects    
    def findBlackCandles(self):
        self.imgThreshold = cv.CreateImage(cv.GetSize(self.warp), 8, 1) ## Remove scalars
        cv.InRangeS(self.warp, cv.Scalar(0,0,0), cv.Scalar(40,40,40), self.imgThreshold) ## Remove scalars
        # Find and return black candles
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
        potential_base_points = self.__findPotentialBasePoints(unfiltered_list)
        
        # Remove multiple indicators for a single candle
        candle_indicators = self.__removeMultipleIndicators(potential_base_points)
        
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
        for i in range(0, len(potential_base_points)):
            flag_multiple_indicators = False
            for j in range(i, len(potential_base_points)):
                if ( i != j ):
                    Ydifference = math.fabs(potential_base_points[i][0] - potential_base_points[j][0])
                    Xdifference = math.fabs(potential_base_points[j][1] - potential_base_points[i][1])

                    #If there are more than one point per candle, delete it from the stack
                    if (Ydifference < 4) and (Xdifference < 4) : ## Remove scalars
                        flag_multiple_indicators = True
            if flag_multiple_indicators==False:
                candle_indicators.append(potential_base_points[i])
        return candle_indicators
    
    def __findPotentialBasePoints(self, unfiltered_list): 
        potential_base_points = []
        number_unfiltered = len(unfiltered_list)
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
                if (number_points_above_current > 20): ## Remove scalars
                    potential_base_points.append(unfiltered_list[i])
        return potential_base_points
