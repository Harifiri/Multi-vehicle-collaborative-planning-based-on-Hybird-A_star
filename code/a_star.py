import sys
import math
import numpy as np
from sys import maxsize # 导入最大数，2^63-1
from model import *
from point import Point
from map import Map
import a_star
import logging


def HA2A(point):
    x = int((point[0] + Bound) / Tile_size)
    y = int((-point[1] + Bound) / Tile_size)

    print([x, y])
    return [x, y]

def SelectMinPoint(set):
    selected_index = -1
    min_cost = sys.maxsize
    min_H = sys.maxsize
    for index in range(len(set)):
        p = set[index]
        if p.cost <= min_cost and p.H < min_H:
            min_cost = p.cost
            min_H = p.H
            selected_index = index
    return selected_index

def IsInPointList(x, y, point_list):
    for point in point_list:
        if x == point.x and y == point.y:
            return True
    return False

def IsStartPoint(start,p):
    if start[0]-p.x == 0 and start[1]-p.y == 0:
        return True
    return False

def IsEndPoint(end,p):
    if end[0]-p.x == 0 and end[1]-p.y == 0:
        return True
    return False

def IsConflictPoint(x, y, m):
    if(m.map[x][y] != 0):
        logging.error("IsConflictPoint!!!")
        return True

    R_temp = math.ceil(R/Tile_size)

    for i in range(-R_temp, R_temp+1):
        for j in range(-R_temp, R_temp+1):
            if i == 0 and j == 0:
                continue
            px = x+i
            py = y+j
            if px < 0 or px >= m.row:
                continue
            if py < 0 or py >= m.col:
                continue
            if(m.map[px][py] != 0):
                logging.error("IsConflictPoint!!!")
                return True

    return False

def BuildPath(start,p):
    path = []
    while True:
        path.append((p.x, p.y))
        if IsStartPoint(start, p):
            break
        else:
            p = p.parent
    return path

def Astar(start,end,m):
    OpenSet = []
    CloseSet = []

    StartPoint = PointA(start)
    StartPoint.G = 0
    StartPoint.H = 0
    StartPoint.cost = 0

    OpenSet.append(StartPoint)

    # count = 0

    while True:
        index = SelectMinPoint(OpenSet)
        if(len(OpenSet)==0):
            logging.error("set=None!!!")
            return -1
        if(index>=len(OpenSet)):
            logging.error("Out of Range!!!")
            return -1
        if(index<0):
            logging.error("No path found, algorithm failed!!!")
            return -1

        p = OpenSet[index]
        # count += 1
        # logging.warning("ehco%d,%d,%d", count, p.x, p.y)
        #m.map[p.x][p.y] = 2

        if(IsEndPoint(end, p)):
            # return p.G
            path = BuildPath((start[0], start[1]), p)
            return path

        del OpenSet[index]
        CloseSet.append(p)

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                px = p.x + i
                py = p.y + j
                if px < 0 or px >= m.row:
                    print(p.x,m.row)
                    continue
                if py < 0 or py >= m.col:
                    continue
                if IsConflictPoint(px, py, m):
                    continue
                if IsInPointList(px, py, CloseSet):
                    continue
                p_temp = PointA((px, py))
                p_temp.parent = p
                p_temp.get_G(i, j)
                p_temp.get_H(end)
                p_temp.get_cost()
                OpenSet.append(p_temp)

if __name__ == '__main__':
    # map_size = int(2*Bound/Tile_size)
    # print(map_size)
    # background = Map(map_size, map_size)
    #
    # start_point = (-15, -5, 0)
    # end_point = (5, 15, math.pi/2)
    #
    # path = Astar(HA2A(start_point), HA2A(end_point), background)

    # for iter in path:
    #     background.map[iter[0]][iter[1]] = 2



