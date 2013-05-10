import mahotas.surf
import numpy as np
import cv
from PIL import Image as im
##import milk



if __name__ == '__main__':
    image = cv.LoadImageM('finalfield1.jpg')
    imgGray = cv.CreateImage(cv.GetSize(image), 8, 1)
    cv.CvtColor(image, imgGray, cv.CV_BGR2GRAY)
    cv.SaveImage('grayTest.jpg', imgGray)


    realImage = im.open('grayTest.jpg')
    realImage2 = np.array(realImage)
    
    spoints = mahotas.surf.surf(realImage2)
    print "Nr points: ", len(spoints)


##
##    try:
##        
##
##        # spoints includes both the detection information (such as the position
##        # and the scale) as well as the descriptor (i.e., what the area around
##        # the point looks like). We only want to use the descriptor for
##        # clustering. The descriptor starts at position 5:
##        descrs = spoints[:,5:]
##
##        # We use 5 colours just because if it was much larger, then the colours
##        # would look too similar in the output.
##        k = 5
##        values, _  = milk.kmeans(descrs, k)
##        colors = np.array([(255-52*i,25+52*i,37**i % 101) for i in xrange(k)])
##    except:
##        values = np.zeros(100)
##        colors = [(255,0,0)]
