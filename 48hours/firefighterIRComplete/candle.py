#This class represents the candle object. 
from time import time

class Candle:
    def __init__(self, x_pos, y_pos, color, status):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.status = status # 0 for not extinguished, 1 for extinguished.
        self.last_updated = time()
    
    
	#overloaded equality operator: we dont care about the status or last_updated
	def __eq__(self,that):
		return (self.x_pos == that.x_pos and
				self.y_pos == that.y_pos and
				self.color == that.color)

	def __str__(self):
		return [self.x_pos, self.y_pos, self.color, self.status].__str__()
    
    def getColor(self):
        return self.color
    
    def getStatus(self):
        return self.status
        
    def getPosition(self):
        return (self.x_pos, self.y_pos)
    
    def getX(self):
        return self.x_pos
        
    def getY(self):
        return self.y_pos
        
    def setCandleExtinguished(self):
        self.status = 1
        self.last_updated = time()