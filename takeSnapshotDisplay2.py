from VideoCapture import Device
import cv
import pygame

def main():


    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Display an image")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((96, 96, 0))

    mypygame = pygame.image.load('field3.jpg')
    mypygame = mypygame.convert()

    clock = pygame.time.Clock()
    keepGoing = True
    try:
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                    break

            screen.blit(background, (0, 0))
            screen.blit(mypygame, (0, 0))

            pygame.display.flip()
    finally:
        pygame.quit()

if __name__ == "__main__":
    cam = Device(0,0) # change to 1 for external camera
    #cam.setResolution(320,240)
    cam.saveSnapshot('field3.jpg')
    frame = cv.LoadImageM('field3.jpg')
    del cam
    main()
    
