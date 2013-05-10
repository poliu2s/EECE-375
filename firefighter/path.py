#This class represents the Path object. To represent the best set of paths, a list of Path objects can be created. 

class Path:
    def __init__(self, x_pos, y_pos, angle_facing, x_dest, y_dest, angle_turn, path_to_candle):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.angle_facing = angle_facing
        self.x_dest = x_dest
        self.y_dest = y_dest
        self.angle_turn = angle_turn
        self.path_to_candle = path_to_candle
    
    def getInitialPosition(self):
        return (self.x_pos, self.y_pos)
    
    def getAngleFacing(self):
        return self.angle_facing
        
    def getDestinationCoordinates(self):
        return (self.x_dest, self.y_dest)
        
    def getAngleToTurn(self):
        return self.angle_turn
        
    def getToCandle(self):
        return self.path_to_candle
        
    def setAngleFacing(self, angle):
        self.angle_facing = angle
        
    def setAngleToTurn(self, angle):
        self.angle_turn = angle
        
    def getDistance(self):
       distance = int(round(math.sqrt(pow(x_dest - x_pos, 2) + pow(y_dest - y_pos, 2))))
       return distance
        
    