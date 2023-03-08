import math
import logging
from model import Point2Pol
from model import *


def GetCross(p, p1, p2):
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p[0] - p1[0]) * (p2[1] - p1[1])

def IsPointInRec(p, rec):
    p1,p2,p3,p4 = rec
    return GetCross(p,p1,p2) * GetCross(p,p3,p4) >= 0 and GetCross(p,p2,p3) * GetCross(p,p4,p1) >= 0

def isConflictRec(param):
    x, y, theta = param
    # xc = x - Lw / 2 * math.cos(theta)
    # yc = y - Lw / 2 * math.sin(theta)
    Pol = Point2Pol(x, y, theta)

    for p in Pol:
        for item in Round:
            dx = p[0]-item[0]
            dy = p[1]-item[1]

            if (dx*dx + dy*dy) < Rw*Rw:
                return True

    return False


def isConflictCar(param1, param2):
    x1, y1, theta1 = param1
    x2, y2, theta2 = param2
    x1c = x1 - Lw/2*math.cos(theta1)
    y1c = y1 - Lw/2*math.sin(theta1)
    x2c = x2 - Lw/2*math.cos(theta2)
    y2c = y2 - Lw/2*math.sin(theta2)

    if pow(x1c-x2c, 2) + pow(y1c-y2c, 2) > pow(3*R, 2):
        return False

    Pol1 = Point2Pol(x1, y1, theta1)
    Pol2 = Point2Pol(x2, y2, theta2)
    for p in Pol1:
        if IsPointInRec(p, Pol2):
            return True
    for p in Pol2:
        if IsPointInRec(p, Pol1):
            return True

    return False

def IsConflictPoint(param, t, PathInfo, TimeInfo, TypeInfo):
    if isConflictRec(param):
        return True

    for index0 in range(len(PathInfo)):
        if PathInfo[index0] == []:
            continue
        if t < TimeInfo[index0] or t - TimeInfo[index0] >= len(PathInfo[index0]):
            continue
        if TypeInfo[index0] == 1:
            index1 = t - TimeInfo[index0]
            if isConflictCar(param, PathInfo[index0][index1]):
                return True
        else:
            for i in [0,5,10,15,20]:
                index1 = t - TimeInfo[index0] + i
                if index1 >= len(PathInfo[index0]):
                    break
                if isConflictCar(param, PathInfo[index0][index1]):
                    return True

    return False


def IsConflictPoint1(param, t, PathInfo, TimeInfo):
    for index0 in range(len(PathInfo)):
        if PathInfo[index0] == []:
            continue
        if t < TimeInfo[index0] or t - TimeInfo[index0] >= len(PathInfo[index0]):
            continue
        index1 = t - TimeInfo[index0]
        if isConflictCar(param, PathInfo[index0][index1]):
            return True

    return False