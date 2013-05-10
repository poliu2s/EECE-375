#!/usr/bin/python
# This is a standalone program. Pass an image name as a first parameter of the program.

import sys
from math import sin, cos, sqrt, pi
import cv
import urllib2

# toggle between CV_HOUGH_STANDARD and CV_HOUGH_PROBILISTIC
USE_STANDARD = False

if __name__ == "__main__":

    filename = 'finalfield20Threshold.jpg'
    src = cv.LoadImage(filename, cv.CV_LOAD_IMAGE_GRAYSCALE)

    dst = cv.CreateImage(cv.GetSize(src), 8, 1)
    color_dst = cv.CreateImage(cv.GetSize(src), 8, 3)
    color_dstL = cv.CreateImage(cv.GetSize(src), 8, 3)
    color_dstR = cv.CreateImage(cv.GetSize(src), 8, 3)
    
    storage = cv.CreateMemStorage(0)
    lines = 0
    cv.Canny(src, dst, 50, 200, 3)
    cv.CvtColor(dst, color_dstL, cv.CV_GRAY2BGR)
    cv.CvtColor(dst, color_dstR, cv.CV_GRAY2BGR)
    cv.CvtColor(dst, color_dst, cv.CV_GRAY2BGR)

    

    if USE_STANDARD:
            lines = cv.HoughLines2(dst, storage, cv.CV_HOUGH_STANDARD, 1, pi / 180, 100, 0, 0)
            for (rho, theta) in lines[:100]:
                a = cos(theta)
                b = sin(theta)
                x0 = a * rho 
                y0 = b * rho
                pt1 = (cv.Round(x0 + 1000*(-b)), cv.Round(y0 + 1000*(a)))
                pt2 = (cv.Round(x0 - 1000*(-b)), cv.Round(y0 - 1000*(a)))
                cv.Line(color_dst, pt1, pt2, cv.RGB(255, 0, 0), 3, 8)
    else:
            lines = cv.HoughLines2(dst, storage, cv.CV_HOUGH_PROBABILISTIC, 1, pi / 180, 50, 50, 120)


            # Po's code

            #Find the vertical lines
            verticalDistanceTest = 10
            linesV = [ 0 ]
            linesV.pop(0)
            for line in lines:
                if (sqrt((line[0][1]-line[1][1])**2) > verticalDistanceTest):
                    linesV.append(1)
                    #If want to display all vertical lines detected
                    cv.Line(color_dst, line[0], line[1], cv.CV_RGB(255, 0, 0), 3, 8)
                else:
                    linesV.append(0)
            print 'LinesV: '
            print linesV
            print '------------'


            #Of the vertical lines, find the longest and save it separately
            Vmaximum = 0
            VlongestL = [0]
            VlongestL.pop(0)
            VlongIndex = 0
            i = 0
            for line in lines:
                #Search on the left side of the field
                if (line[0][0] < 512):
                    
                    if (linesV[i] == 1):
                        
                        #Test for absolute length
                        if (sqrt((line[0][0]-line[1][0])**2 + (line[0][1]-line[1][1])**2) > Vmaximum):
                            Vmaximum = sqrt((line[0][0]-line[1][0])**2 + (line[0][1]-line[1][1])**2)
                            VlongIndex = i
                            
                i = i + 1

            #Create a list with the that shows which line is the longest
            i = 0
            for line in lines:
                
                #Assume this line is not the longest, if it is, this will be popped
                VlongestL.append(0)
                
                if (i == VlongIndex):
                    VlongestL.pop()
                    VlongestL.append(1)
                i = i + 1
                
            print 'Longest Left: '
            print VlongestL
            print '-----------------'


            

##            #Pop off the longest vertical line from the list
##            for i in range(0, len(linesV)):
##                if (Vlongest[i] == 1):
##                    linesV.insert(i, 0)
##                    linesV.pop(i+1)


            #Find the second longest line
            Vmaximum = 0
            VlongestR = [0]
            VlongestR.pop(0)
            VlongIndex2 = 0
            i = 0
            for line in lines:

                #Look only at the right side of the field:
                if (line[0][0] > 512):
                
                    if (linesV[i] == 1):
                        
                        #Test for absolute length
                        if (sqrt((line[0][0]-line[1][0])**2 + (line[0][1]-line[1][1])**2) > Vmaximum):
                            Vmaximum = sqrt((line[0][0]-line[1][0])**2 + (line[0][1]-line[1][1])**2)
                            VlongIndex2 = i
                i = i + 1

            #Create a list with the that shows which line is the longest
            i = 0
            for line in lines:
                
                #Assume this line is not the longest, if it is, this will be popped
                VlongestR.append(0)
                
                if (i == VlongIndex2):
                    VlongestR.pop()
                    VlongestR.append(1)
                i = i + 1
                
            print 'Longest Right: '
            print VlongestR
            print '-----------------'




            #To display the left and right edges of the field
            i = 0
            for line in lines:
                if (VlongestL[i] == 1):
                    cv.Line(color_dstL, line[0], line[1], cv.CV_RGB(255, 0, 0), 3, 8)
                i = i + 1

            i = 0
            for line in lines:
                if (VlongestR[i] == 1):
                    cv.Line(color_dstR, line[0], line[1], cv.CV_RGB(255, 0, 0), 3, 8)
                i = i + 1
                                    
                

        
                

    #Debugging code to display
    cv.SaveImage('finalfield20hough.jpg', color_dst)
    cv.SaveImage('finalfield20houghL.jpg', color_dstL)
    cv.SaveImage('finalfield20houghR.jpg', color_dstR)


