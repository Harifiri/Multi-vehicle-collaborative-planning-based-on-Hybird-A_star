import sys
import time
import math
import logging
import numpy as np
from point import Point
from limit import IsLimitPoint
from dubins import dubins, mod2pi
from conflict import IsConflictPoint
from model import *


def SelectMinPoint(set):
    index = 0
    selected_index = -1
    min_cost = sys.maxsize
    for p in set:
        if p.cost < min_cost:
            min_cost = p.cost
            selected_index = index
        index += 1
    return selected_index


def IsStartPoint(start,p):
    if start == p:
        return True
    return False


def IsEndPoint(dir,p):
    dx = abs(EndPoint[dir][0]-p.x)
    dy = abs(EndPoint[dir][1]-p.y)
    if (dx*dx)+(dy*dy) < 1:
        return True
    return False


def BuildPath(start,p):
    path = []

    while True:
        path.append((p.x, p.y, p.theta))
        if IsStartPoint(start, p):
            break
        else:
            p = p.parent

    path.reverse()

    return path


def GetMapIndex(param, dir):
    i = int(dir/3)
    if i == 0:
        x, y, theta = param
    elif i == 1:
        x, y, theta = param[1], -param[0], mod2pi(param[2]-math.radians(90))
    elif i == 2:
        x, y, theta = -param[0], -param[1], mod2pi(param[2]-math.radians(180))
    elif i == 3:
        x, y, theta = -param[1], param[0], mod2pi(param[2]-math.radians(270))

    index1 = int((x+Bound)/GridSize)
    index2 = int((y+Bound)/GridSize)
    index3 = int(theta/math.radians(6))

    return index1, index2, index3


def HybirdAstar(dir, t, PathInfo, TimeInfo, TypeInfo):
    map_size = int(2*Bound/GridSize)
    MapSet = np.empty((map_size,map_size,60), dtype=bool)
    MapSet.fill(False)
    OpenSet = []
    CloseSet = []

    param = StartPoint[dir][0], StartPoint[dir][1], StartAng[dir]
    StartP = Point(param)
    StartP.t = t
    StartP.cost = 0

    OpenSet.append(StartP)

    count = 0

    while True:
        count += 1

        index = SelectMinPoint(OpenSet)

        if(len(OpenSet)==0):
            # logging.warning("set=0")
            return -1

        p = OpenSet.pop(index)
        CloseSet.append(p)

        # if count % 100 == 0:
        #     print('count, ', count,  'x =', p.x, ' y =', p.y)

        if(IsEndPoint(dir, p)):
            path = BuildPath(StartP, p)
            return path

        IndexSet = []
        # [-1,0,1]->[左转，直行，右转]
        for i in [-1, 0, 1]:
            param, next_turn = p.point_iter(i)
            index_m1_, index_m2_, index_m3_ = GetMapIndex(param, dir)
            # print(param,next_turn)
            if MapSet[index_m1_][index_m2_][index_m3_] == True:
                continue
            if IsConflictPoint(param, (p.t+1), PathInfo, TimeInfo, TypeInfo):
                continue
            if not IsLimitPoint(dir, param):
                continue
            IndexSet.append([index_m1_, index_m2_, index_m3_])
            p_temp = Point(param)
            p_temp.parent = p
            p_temp.t = p_temp.parent.t+1
            p_temp.turn = next_turn
            p_temp.get_G()
            p_temp.get_H(dir)
            # print('H =', p_temp.H, param)
            p_temp.get_cost()
            OpenSet.append(p_temp)

        for item in IndexSet:
            MapSet[item[0]][item[1]][item[2]] = True

#
# def isFinish():
#     for item in PathInfo:
#         if item == []:
#             return False
#     return True
#
#
# def FCFS_Policy():
#     selected_index = -1
#     min_time = sys.maxsize
#
#     for index in range(len(PathInfo)):
#         if TimeInfo[index] < min_time and PathInfo[index] == []:
#             min_time = TimeInfo[index]
#             selected_index = index
#
#     return selected_index
#
#
# def cps(para):  # change point size
# 	x, y = para
# 	x = x*10 + w/2
# 	y = -(y*10) + h/2
# 	return x, y
#
#
# if __name__ == '__main__':
#     qr = 30000  # car flow (veh/h)
#     T = 10  # amount of simulation time
#     s = 0  # random seed
#     mtd = 0.25  # minimum time headway
#     TimeInfo, CarInfo = generateCarFlow(qr, T, s, mtd, 1)
#
#     run_time = 0
#
#     for i in range(len(CarInfo)):
#         PathInfo.append([])
#
#     while not isFinish():
#         car_index = FCFS_Policy()
#
#         path = HybirdAstar(CarInfo[car_index], TimeInfo[car_index])
#
#         echo += 1
#
#         if path == -1:
#             TimeInfo[car_index] += 1
#             print(TimeInfo)
#             continue
#
#         PathInfo[car_index] = path
#         temp_time = TimeInfo[car_index]+len(PathInfo[car_index])
#         if temp_time > run_time:
#             run_time = temp_time
#
#     print(len(CarInfo), 'vehicles passed the intersection in', str(run_time*dt), 'seconds')
#
#     pygame.init()
#     screen = pygame.display.set_mode((w, h))
#     screen.fill((255, 255, 255))
#     # pygame.display.update()
#     # pygame.display.flip()
#     # time.sleep(3)
#
#     for t in range(run_time):
#         time.sleep(0.02)
#         screen.fill((255, 255, 255))
#         color = [0, 0, 0]
#         width = 2
#         # draw background
#         for i in range(4):
#             pygame.draw.arc(screen, color, RoundParam[i][0], RoundParam[i][1], RoundParam[i][2], width)
#
#         for index0 in range(len(PathInfo)):
#             if t < TimeInfo[index0] or t-TimeInfo[index0] >= len(PathInfo[index0]):
#                 continue
#             index1 = t-TimeInfo[index0]
#
#             p_temp = Point2Pol1(PathInfo[index0][index1][0], PathInfo[index0][index1][1], PathInfo[index0][index1][2])
#
#             polygon = [cps(p_temp[0]), cps(p_temp[1]), cps(p_temp[2]), cps(p_temp[3])]
#             pygame.draw.polygon(screen, [255, 0, 0], polygon, 0)
#
#         pygame.display.update()
#         pygame.display.flip()
#         # 8 - loop through the events
#         for event in pygame.event.get():
#             # check if the event is the X button
#             if event.type == pygame.QUIT:
#                 # if it is quit the game
#                 pygame.quit()
#                 exit(0)

    # screen.fill((255, 255, 255))
    # pygame.display.update()
    # pygame.display.flip()
    # time.sleep(2)