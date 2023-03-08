import sys
import math
from model import *
from dubins import dubins, mod2pi

turn_cost = {0:0, 1:0.075}#0.005-0.01, 0.025

class Point:
    def __init__(self, param):
        self.x, self.y, self.theta = param
        self.turn = 0
        self.G = 0
        self.H = 0
        self.cost = sys.maxsize
        self.parent = None

    def point_iter(self, i):
        next_x = self.x + delta_G*math.cos(self.theta)
        next_y = self.y + delta_G*math.sin(self.theta)
        next_turn = max(min(self.turn+i,6),-6)
        next_theta = mod2pi(self.theta + delta_G/Lw*math.tan(steer[next_turn]))

        param = next_x, next_y, next_theta
        return param, next_turn

    def get_G(self):
        self.G = self.parent.G + G[abs(self.turn)]*(1 + turn_cost[abs(self.turn-self.parent.turn)])

    def get_H(self, dir):
        start = self.x, self.y, self.theta
        self.H = dubins(start, dir)

    def get_cost(self):
        self.cost = self.G + self.H

# def Euclid(start, end):
#     dx = abs(start[0]-end[0])
#     dy = abs(start[1]-end[1])
#
#     return math.sqrt(dx*dx + dy*dy)

# class PointA:
#     def __init__(self, start):
#         self.x = start[0]
#         self.y = start[1]
#         self.G = 0
#         self.H = 0
#         self.cost = 0
#         self.parent = None
#
#     def get_G(self, i, j):
#         self.G = self.parent.G + math.sqrt(abs(i)+abs(j))
#
#     def get_H(self, end):
#         dx = abs(self.x - end[0])
#         dy = abs(self.y - end[1])
#         self.H = abs(dx - dy) + math.sqrt(2)*min(dx, dy)
#
#     def get_cost(self):
#         self.cost = self.G + self.H

if __name__ == '__main__':
    print(steer)
    print(r)
    print(ang)
    print(G)
