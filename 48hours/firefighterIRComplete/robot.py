#This class represents the Robot object. 

import threading


class Robot:
    def __init__(self, x_pos, y_pos, angle):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.angle = angle
        self.lock = threading.RLock()

    def getCurrentPosition(self):
        return (self.x_pos, self.y_pos)
    
    def getX(self):
        return self.x_pos
        
    def getY(self):
        return self.y_pos
    
    def getCurrentAngle(self):
        return self.angle
        
    def updatePosition(self, x, y):
        self.lock.acquire()
        self.x_pos = x
        self.y_pos = y
        self.lock.release()
        
    def updateAngle(self, angle):
        self.lock.acquire()
        self.angle = angle
        self.lock.release()