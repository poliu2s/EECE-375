# TODO: Exit condition
# TODO: Send entire path rather than path segments to MCU at one go.

import threading
import math
#import serial
import time
import sys
import robot
import candle
import path
import os
import Global_Constants
from imageProcessing import ecePredator
from corner_detection import eceCorners
from astar_modified import PathFinder

def findCheckSum(distance) :
    total = 0
    while distance != 0: 
        total += distance%10
        distance = int(distance/10)
    return int(total%10)

def verifyCheckSum(gyro_data):
    total = gyro_data % 10
    sum = 0
    while gyro_data != 0:
        gyro_data = int(gyro_data / 10)
        sum += gyro_data % 10
    if sum == total:
        return true
    return false

def convertToSendable(data):
    data = str(data)
    if len(data) == 5:
        return str(data)
    elif len(data) < 5:
        while len(data) < 5:
            data = "0" + data
        return data
    
def addToOutgoingMessage(message):
    if self.outgoing_message == "00000":
        self.outgoing_message = message
    else:
        self.outgoing_message += message
    
# take picture and assign it name as given
# TODO: Change this eventually (add -i /dev/video1)
def takePicture(name):
    os.system("streamer -o "+name)

def getNextPictureName(number):
    return (Global_Constants.IMAGE_BASENAME + str(number) + Global_Constants.IMAGE_EXT)

def getPositionFromDisplacement(old_x, old_y, distance, angle):
    new_x = old_x + distance * math.cos(angle)
    new_y = old_y + distance * math.sin(angle)
    return (new_x, new_y)
    
# Call this function to run the algorithm. 
def getNextBestPathList(our_candle_list, attack_candle_list, robot):
    path_finder = astar()
    min_path_list = []
    min_distance = 0 
    min_number_segments = 0
    # Place obstacles on the field.
    # Find a way to place obstacle robot as an obstacle in case of "ALERT"
    path_finder.place_obstacles(our_candle_list)
    path_finder.place_obstacles(attack_candle_list)
    # Iterate through every candle that is left to be blown out in the attack_candle_list
    for candle in attack_candle_list : 
        current_candle_status = candle.getStatus()
        if current_candle_status == 0:
            # temp_path_list = path_finder.getAttackAlgorithm()
            x_robot = robot.getX()
            y_robot = robot.getY()
            angle_robot = robot.getCurrentAngle()
            # Find the "destination point" which is slightly different from the candle location
            x_dest, y_dest = path_finder.target(x_robot, y_robot, candle)
            route = path_finder.pathFind(x_robot, y_robot, x_dest, y_dest)
            temp_path_list = path_finder.generalize(x_robot, y_robot, angle_robot, route)
            if min_number_segments == 0 and min_distance == 0:
                min_path_list = temp_path_list
                min_number_segments = len(temp_path_list)
                for temp_path in temp_path_list:
                    min_distance += temp_path.getDistance()
            elif len(temp_path_list) < min_number_segments:
                min_path_list = temp_path_list
                min_number_segments = len(temp_path_list)
                min_distance = 0
                for temp_path in temp_path_list:
                    min_distance += temp_path.getDistance()
            elif len(temp_path_list) == min_number_segments:
                compare_distance = 0
                for temp_path in temp_path_list: 
                    compare_distance += temp_path.getDistance()
                if compare_distance < min_distance:
                    min_distance = compare_distance
                    min_path_list = temp_path_list
    return min_path_list
    
# Get candle coordinates from image processing, store them locally.
black_candle_list = []
white_candle_list = []

# Configure/Calibrate the camera
# camera.configure()
number_pictures = 0
name = getNextPictureName(number_pictures)
number_pictures += 1

corner_finder = eceCorners()
candle_finder = ecePredator()
#takePicture(name)
corners = corner_finder.findCorners(name)
# Load the most recently taken picture into candle_finder.
candle_finder.loadPicture(name)
# Once picture is loaded, its corners can be used to warp the image
candle_finder.warpPicture(corners)
# Once picture is warped, it can be used to find all the candles on the field.
print "Finding black candles"
black_candle_list = candle_finder.findBlackCandles(corners)
print "Finding white candles"
white_candle_list = candle_finder.findWhiteCandles(corners)
# Also find the initial position of the robot.

# This for loop is only to print candle locations. 
for black_candle in black_candle_list:
    x = black_candle.getX
    y = black_candle.getY
    status = black_candle.getStatus
    color = black_candle.getColor
    print "{0}, {1}, {2}, {3}".format(str(x()), str(y()), str(status()), str(color()))
    #print str(x()) + " , " + str(y()) + " , " + str(status()) + " , " + str(color())

# This for loop is only to print candle locations. 
for white_candle in white_candle_list:
    x = white_candle.getX
    y = white_candle.getY
    status = white_candle.getStatus
    color = white_candle.getColor
    print "{0}, {1}, {2}, {3}".format(str(x()), str(y()), str(status()), str(color()))
    #print str(x()) + " , " + str(y()) + " , " + str(status()) + " , " + str(color())


# Check the number of candles found. If the number is greater than expected, throw exception and restart image processing. Perhaps have some mechanism in image processing to ensure that only 4 are returned?
if len(black_candle_list) != Global_Constants.NUMBER_OF_BLACK_CANDLES or len(white_candle_list) != Global_Constants.NUMBER_OF_WHITE_CANDLES: 
    print "Error: Unexpected number of candles on field"
    print "Number of black candles found: {0}".format(len(black_candle_list))
    print "Number of white candles found: {0}".format(len(white_candle_list))
    exit()


attack_candle_list = black_candle_list
our_candle_list = white_candle_list
if( Global_Constants.CANDLES_TO_ATTACK == 1):
    attack_candle_list = white_candle_list
    our_candle_list = black_candle_list

# Keep track of current state by keeping a robot and a current_path object
bamf = robot(0, 0, 0)
# Keep track of path finding algorithm with a list of paths.
current_path_list = []

# Then send instructions to the robot and start listening on the XBee.
# Send instructions to MCU over XBee
try:
    # TODO: Change port while switching over to Unix.
    ser = serial.Serial(port='\\.\COM4')
    ser.flushInput()
    ser.flushOutput()
    ser.close()
    ser.baudrate = 115200
    ser.timeout = 1
    ser.open()
except: 
    print "Could not initiate serial communication. Terminating program."
    sys.exit()

# Start a thread to receive incoming messages and put them in a queue
self.outgoing_message = "00000"
last_outgoing_message = "00000"
last_request = "00000"
while True:
    if self.outgoing_message != "00000":
        last_outgoing_message = self.outgoing_message[:5]
        self.outgoing_message = self.outgoing_message[5:]
        ser.write(last_outgoing_message)
        if len(self.outgoing_message) == 0:
            self.outgoing_message = "00000"
        continue
    if ser.inWaiting >= 5:
        data = ser.read(5)
        if data == "FIRST":
            # This means that its the first time the MCU sent a request to the controller.
            # Get 5 more bytes for location of robot.
            # Initialise robot position to those 5 bytes.
            # Initialise path finding algorithm. 
            # Send distance to move to MCU.
            print "Received 'FIRST' from the MCU"
            while ser.inWaiting < 5:
                continue
            distance_moved_data = ser.read(5)
            distance_moved = distance_moved_data[:-1] if verifyCheckSum(distance_moved_data) else 0
            old_x = bamf.getX()
            old_y = bamf.getY()
            # Here I'm assuming angle should be zero, ie robot is moving in x direction. What if our orientation is different?
            new_x, new_y = getPositionFromDisplacement(old_x, old_y, distance_moved, 0)
            bamf.updatePosition(new_x, new_y)
            current_path_list = getNextBestPathList( our_candle_list, attack_candle_list, bamf)
            current_path = current_path_list.pop(0)
            addToOutgoingMessage(convertToSendable(current_path.getDistance()))
            addToOutgoingMessage(convertToSendable(current_path.getCurrentAngle()))
            addToOutgoingMessage(convertToSendable(current_path.getToCandle()))
            last_request = data
        elif data == "RECVD":
            print "Received 'RECVD' from the MCU"
            last_outgoing_message = "00000"
            last_request = data
            # This means instructions were received.
        elif data == "ALERT":
            print "Received 'ALERT' from the MCU"
            # ? Get obstacle distance information from IR sensor ? 
            # Take picture. Run pathfinding algorithm to get new algorithm
            name = getNextPictureName(number_pictures)
            number_pictures += 1
            takePicture(name)
            # robot_finder = eceRobot()
            # robot_finder.loadPicture(name)
            # robot_finder.warpPicture(corners)
            # robot_finder.getRobotPosition(bamf)
            # Add an robot obstacle to the algorithm finder thing
            # Do algorithm stuff
            last_request = data
            
        elif data == "TRACK":
            # Receive five more bytes of data and then create new thread to store it
            # Store this in robot object
            print "Tracking readings are being received now"
            last_request = data
            while ser.inWaiting < 5:
                continue
            track_data = ser.read(5)
            if verifyCheckSum(track_data):
                new_x += track_data *  math.cos(bamf.getCurrentAngle())
                new_y += track_data * math.sin(bamf.getCurrentAngle())
                bamf.updatePosition(new_x, new_y)
        elif data == "RQDIS":
            # Since robot is asking for distance, it has finished the most recent part of the segment.
            # Check if there are any more parts of the segment left. If not, set that candle's status to extinguished. Generate new algorithm for next candles. 
            # If there are more segments left, move on to the next part of the path_list and send that distance to the MCU. 
            # Before sending message, make sure you assign a checksum to it. 
            last_request = data
            if current_path_list != 0:
                current_path = current_path_list.pop(0)
                addToOutgoingMessage(convertToSendable(current_path.getDistance()))
            print "Sending distance instruction to MCU"
        elif data == "RQANG":
            # Send the angle to turn to the robot to get the end of the next segment
            # Ensure angle is checksumed. 
            last_request = data
            addToOutgoingMessage(convertToSendable(current_path.getDistance()))
            print "Sending angle to MCU"
        elif data == "GYROS":
            # Listen for five more bytes of data from the serial port. Create new thread to store the angle information
            # Store this in robot.
            print "Gyroscope readings being received now"
            while ser.inWaiting < 5:
                continue
            gyro_data = ser.read(5)
            if verifyCheckSum(gyro_data):
                # Assuming angles are given +/-
                new_angle += bamf.getCurrentAngle()
                bamf.updateAngle(new_angle)
        elif data == "CANDL":
            # Return whether there's a candle at the end of the current_path or not
            print "Request received for CANDL"
            if current_path.getToCandle() == 0:
                addToOutgoingMessage(convertToSendable("0"))
            else:
                addToOutgoingMessage(convertToSendable("1"))
        elif data == "RPEAT":
            # Resend last sent message
            if last_request == "RQANG" or last_request == "RQDIS" or last_request == "CANDL":
                addToOutgoingMessage(last_outgoing_message)
            elif last_request == "ALERT" or last_request == "FIRST":
                addToOutgoingMessage(convertToSendable(current_path.getDistance()))
                addToOutgoingMessage(convertToSendable(current_path.getCurrentAngle()))
                addToOutgoingMessage(convertToSendable(current_path.getToCandle()))
            print "Request received for resending data"
        elif data == "DONEX":
            # Kill the loop
            print "Received Done- Killing loop"
            break;
        else:
            # Unrecognized request received. Send a resend request. 
            print "Random data received - " + data
