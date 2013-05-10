
import cv

def warpImage(image, corners, target):
    mat = cv.CreateMat(3, 3, cv.CV_32F)
    cv.GetPerspectiveTransform(corners, target, mat)
    out = cv.CreateMat(height, width, cv.CV_8UC3)
    cv.WarpPerspective(image, out, mat, cv.CV_INTER_CUBIC)
    return out

if __name__ == '__main__':
    width, height = 600, 600
    corners = [(711,877),(1972,902),(2332,1448),(310,1410)]
    target = [(0,0),(width,0),(width,height),(0,height)]
    image = cv.LoadImageM('bigblue.jpg')
    out = warpImage(image, corners, target)
    #cv.SaveImage('bigblue_warped1.jpg', out)

    imgHSV = cv.CreateImage(cv.GetSize(out), 8, 3)
    #cv.CvtColor(out, imgHSV, cv.CV_BGR2HSV)
    imgThreshold = cv.CreateImage(cv.GetSize(out), 8, 1)


    #Filter for black candles
    #HSVcv.InRangeS(imgHSV, cv.Scalar(0,0,100), cv.Scalar(255,255,255), imgThreshold)
    cv.InRangeS(out, cv.Scalar(0,0,0), cv.Scalar(40,40,40), imgThreshold)

    #Filter for white candles
    #cv.InRangeS(out, cv.Scalar(140,140,140), cv.Scalar(255,255,255), imgThreshold)    


    cv.SaveImage('bigblueThreshold.jpg', imgThreshold)

    
