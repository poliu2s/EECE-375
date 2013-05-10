
import cv

if __name__ == '__main__':
    
    image = cv.LoadImageM('finalfield20.jpg')
    imgHSV = cv.CreateImage(cv.GetSize(image), 8, 3)
    cv.CvtColor(image, imgHSV, cv.CV_BGR2HSV)

    
    imgThreshold = cv.CreateImage(cv.GetSize(image), 8, 1)
    cv.InRangeS(imgHSV, cv.Scalar(100,40,180), cv.Scalar(130,240,300), imgThreshold)



    cv.SaveImage('finalfield20HSV.jpg', imgHSV)
    cv.SaveImage('finalfield20Threshold.jpg', imgThreshold)

    
