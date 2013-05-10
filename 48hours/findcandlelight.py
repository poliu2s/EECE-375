
import cv

if __name__ == '__main__':
    
    image = cv.LoadImageM('finalfield41.jpg')

    #--------------------------------------------------------
    #Using RGB filter
    imgThreshold = cv.CreateImage(cv.GetSize(image), 8, 1)
    cv.InRangeS(image, cv.Scalar(235,235,235), cv.Scalar(255,255,255), imgThreshold)
    #--------------------------------------------------------


    #If you want to filter using HSV
##    imgHSV = cv.CreateImage(cv.GetSize(image), 8, 3)
##    cv.CvtColor(image, imgHSV, cv.CV_BGR2HSV)    

##    cv.InRangeS(imgHSV, cv.Scalar(100,40,180), cv.Scalar(130,240,300), imgThreshold)
##    cv.SaveImage('finalfield21HSV.jpg', imgHSV)


    
    cv.SaveImage('finalfield41FindingCandlelight.jpg', imgThreshold)

    
