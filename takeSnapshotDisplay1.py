from VideoCapture import Device
import cv
import pygame


device = 1
capture = cv.CreateCameraCapture(1)
##cv.SetCaptureProperty(capture, cv.CAP_PROP_FRAME_WIDTH, 640)
##cv.SetCaptureProperty(capture, cv.CAP_PROP_FRAME_HEIGHT, 480)
picture = cv.QueryFrame(capture)
cv.SaveImage('blah.jpg', picture)



##if not capture:
##        print "Error opening capture device"
##        sys.exit(1)
## 
##while 1:
##    # do forever
##    print "in while now..."
##    # capture the current frame
##    frame = cv.QueryFrame(capture)
##    if frame is None:
##        break
## 
##        # mirror
##    cv.Flip(frame, None, 1)
## 
##        # face detection
##    detect(frame)
## 
##        # display webcam image
##    cv.ShowImage('Camera', frame)
## 
##        # handle events
##    k = cv.WaitKey(10)
## 
##    if k == 0x1b: # ESC
##        print 'ESC pressed. Exiting ...'
##        break


##cam = Device(1) # change to 1 for external camera
##cam.saveSnapshot('image.jpg')
##frame = cv.LoadImageM('image.jpg')
##
##
##w = 640
##h = 480
##screen = pygame.display.set_mode((w,h))
##graphic = pygame.image.load("image.jpg").convert()
##screen.blit(graphic, (0,0))
##pygame.display.flip()
##
##running = 0
##while running:
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            running = 0
##    screen.blit(graphic, (0,0))
##    pygame.display.flip()

    
##
##
##def main():
##
##
##    screen = pygame.display.set_mode((640, 480))
##    pygame.display.set_caption("Display an image")
##
##    background = pygame.Surface(screen.get_size())
##    background = background.convert()
##    background.fill((96, 96, 0))
##
##    mypygame = pygame.image.load("image.jpg")
##    mypygame = mypygame.convert()
##
##    clock = pygame.time.Clock()
##    keepGoing = True
##    try:
##        while keepGoing:
##            clock.tick(30)
##            for event in pygame.event.get():
##                if event.type == pygame.QUIT:
##                    keepGoing = False
##                    break
##
##            screen.blit(background, (0, 0))
##            screen.blit(mypygame, (0, 0))
##
##            pygame.display.flip()
##    finally:
##        pygame.quit()
##
##if __name__ == "__main__":
##    cam = Device(0) # change to 1 for external camera
##    cam.saveSnapshot('image.jpg')
##    frame = cv.LoadImageM('image.jpg')
##    main()
##    
