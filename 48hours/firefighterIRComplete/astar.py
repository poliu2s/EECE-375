# EECE375/474 Team 15
# Robot Implementation
# A* Pathfinding Algorithm
#
# Pathfinding adapted from:
# http://code.activestate.com/recipes/577519-a-star-shortest-path-algorithm/
#
# Copyright (C) 2011 by Jake Davis, Po Liu, Anuj Mehta, Vincent Quach, Yuyang Sun, Ian Tu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# IMPORT DECLARATIONS
from heapq import heappush, heappop # for priority queue
import math
import time
import imageProcessing
import random
from candle import Candle
from path import Path
import os
import Global_Constants

# GLOBAL VARIABLES
candle_list = []
# for i in [0,1,2,3,4,5,6,7]:
    # candle_list.append(Candle(random.randrange(15, 45, 1),
                              # random.randrange(15, 45, 1),
                              # "Black", 1, 0))
the_map = Global_Constants.map_global
n = Global_Constants.n_global
m = Global_Constants.m_global
dx = Global_Constants.dx_global
dy = Global_Constants.dy_global
dirs = Global_Constants.dirs_global
step = Global_Constants.step_global 

##########
# A*STAR #
##########

class node:
    xPos = 0 # x position
    yPos = 0 # y position
    distance = 0 # total distance already travelled to reach the node
    priority = 0 # priority = distance + remaining distance estimate
    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority
    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority
    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10 # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self, dirs, d): # d: direction to move
        if dirs == 8 and d % 2 != 0:
            self.distance += 19
        else:
            self.distance += 10
    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        d = math.sqrt(xd * xd + yd * yd)
        return(d)

# generalize is a function that takes a path result and discretizes it
# further into a set of distances and angles that can be sent to the
# robot
def generalize(initx, inity, robot_angle, path):

    turns = 0
    segments = []
    angle = int(path[0]) * 45 - robot_angle
    print 'Angle: ', angle
    distance = 0
    segment = ''

    segments.append(Path(initx,inity, robot_angle, distance * math.cos(robot_angle), distance * math.sin(robot_angle), angle, segment))

    # for each node step in the path (type: str)
    for i in range(len(path)):

        distance += step * math.sqrt(int(path[i]) % 2 + 1)
        
        # if the current element of the path is not equal to the next
        # one, that means we can anticipate a turn. Calculate our
        # current angle, the next angle, take the difference, and
        # perform some operations to gain the relative angle to turn
        if i == (len(path) - 1):
            turns += 1
            seg = Path(initx, inity, robot_angle, distance * math.cos(robot_angle), distance * math.sin(robot_angle), angle, 1)
            segments.append(seg)
            print 'Distance: ', distance
            print 'Angle: ', angle
        else:
            if path[i] != path[i+1]:
                turns += 1
                curr_angle = int(path[i]) * 45 # current angle of path
                next_angle = int(path[i+1]) * 45 # next angle of path
                diff_angle = next_angle - curr_angle # difference in angles
                if(abs(diff_angle) < 180):
                    angle = diff_angle
                else:
                    if(diff_angle < 0):
                        angle += 360
                    else:
                        angle -= 360
                        seg = Path(initx, inity, robot_angle, distance * math.cos(robot_angle), distance * math.sin(robot_angle), angle, 0)
                        segments.append(seg)
                print 'Distance: ', distance
                print 'Angle: ', angle
                distance = 0

    print 'Turns: ', turns
    return segments

# target() simply determines which of the four corners of a buffered
# candle the robot should go to. There is a destination, but it is
# inaccessible due to the surrounding buffer created within the
# place_obstacles function. Depending on the robot's position, one of the
# four corners will be chosen as the destination.
def target(xA, yA, candle):
    xB = -1 if (xA - candle.getX() < 0) else 1
    yB = -1 if (yA - candle.getY() < 0) else 1
    xB = xB * 2 + candle.getX()
    yB = yB * 2 + candle.getY()
    print 'Candle X: {0} \nCandle Y:{1}\nRobot X: {2}\nRobot Y:{3}'.format(candle.getX(), candle.getY(), xA, yA)
    return xB, yB

# place_obstacles takes in a list of candle objects and 
def place_obstacles(candleList):
    for candle in candleList:
        the_map[candle.getX()][candle.getY()] = 1
        for ddx,ddy in ((-1,-1), (-1, 0), (-1, 1), (0, -1),
                        ( 0, 1), (1, -1), ( 1, 0), ( 1, 1),
                        (0, -2), (1, -2), (-1,-2),     # left side
                        ( 0, 2), ( 1, 2), (-1, 2),     # right side
                        ( 2, 1), ( 2, 0), (2, -1),     # bottom side
                        (-2, 1), (-2, 0), (-2,-1)):    # top side
            the_map[candle.getX() + ddx][candle.getY() + ddy] = 1

# A-star algorithm.
# The path returned will be a string of digits of directions.
def pathFind(xA, yA, xB, yB):

    closed_nodes_map = [] # map of closed (tried-out) nodes
    open_nodes_map = [] # map of open (not-yet-tried) nodes
    dir_map = [] # map of dirs
    # checkpoint = [yA][xA] # start point of a path
    row = [0] * n
    for i in range(m): # create 2d arrays
        closed_nodes_map.append(list(row))
        open_nodes_map.append(list(row))
        dir_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0 # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, 0, 0)
    n0.updatePriority(xB, yB)
    heappush(pq[pqi], n0)
    open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map

    # A* search
    while len(pq[pqi]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node
        n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
        # nextpoint = [n1.yPos][n1.xPos] # specify nextpoint for walkable()
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi]) # remove the node from the open list
        open_nodes_map[y][x] = 0
        closed_nodes_map[y][x] = 1 # mark it on the closed nodes map

        # quit searching when the goal is reached
        # if n0.estimate(xB, yB) == 0:
        if x == xB and y == yB:
            # generate the path from finish to start
            # by following the dirs
            path = ''
            while not (x == xA and y == yA):
                j = dir_map[y][x]
                c = str((j + dirs / 2) % dirs)
                path = c + path
                x += dx[j]
                y += dy[j]
            return path

        # generate moves (child nodes) in all possible dirs
        for i in range(dirs):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                    or the_map[ydy][xdx] == 1 or closed_nodes_map[ydy][xdx] == 1):
                # generate a child node
                m0 = node(xdx, ydy, n0.distance, n0.priority)
                m0.nextMove(dirs, i)
                m0.updatePriority(xB, yB)
                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:
                    open_nodes_map[ydy][xdx] = m0.priority
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                elif open_nodes_map[ydy][xdx] > m0.priority:
                    # update the priority
                    open_nodes_map[ydy][xdx] = m0.priority
                    # update the parent direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
    return '' # if no route found

# MAIN
row = [0] * n
for i in range(m): # create empty map
    the_map.append(list(row))

xA = 0
yA = 10

# place candles in the map, set the target for the robot
place_obstacles(candle_list)
xB, yB = target(xA, yA, candle_list[4])

t = time.time()
route = pathFind(xA, yA, xB, yB)
print 'Time (seconds):', time.time() - t
print 'Route:', route

# generate segment distance/angle instructions
instructions = generalize(xA, yA, 0, route)

# mark the route on the map
if len(route) > 0:
    x = xA
    y = yA
    the_map[y][x] = 2
    for i in range(len(route)):
        j = int(route[i])
        x += dx[j]
        y += dy[j]
        the_map[y][x] = 3
    the_map[y][x] = 4


# display the map with the route added
print 'Map:'
for y in range(m):
    for x in range(n):
        xy = the_map[y][x]
        if xy == 0:
            print '.', # space
        elif xy == 1:
            print 'O', # obstacle
        elif xy == 2:
            print 'S', # start
        elif xy == 3:
            print '&', # route
        elif xy == 4:
            print 'F', # finish
    print

