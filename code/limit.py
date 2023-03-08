import sys
import math
from model import *

# 在limitAng内是错误的角度
limitAng = [
    [(math.pi, 3*math.pi/2)],
    [(math.pi/2, 3*math.pi/2)],
    [(math.pi/2, math.pi)],
    [(3*math.pi/2, 2*math.pi)],
    [(math.pi, 2*math.pi)],
    [(math.pi, 3*math.pi/2)],
    [(0, math.pi/2)],
    [(3*math.pi/2, 2*math.pi), (0, math.pi/2)],
    [(3*math.pi/2, 2*math.pi)],
    [(math.pi/2, math.pi)],
    [(0, math.pi)],
    [(0, math.pi/2)],
]

# 在limitArea内是正确的区域[x_min, x_max, y_min, y_max]
limitArea = [
    [-Bound, Rw, -Rw, Bound],
    [-Bound, Bound, -Rw, 0],
    [-Bound, 0, -Bound, 0],
    [-Bound, Rw, -Bound, Rw],
    [0, Rw, -Bound, Bound],
    [0, Bound, -Bound, 0],
    [-Rw, Bound, -Bound, Rw],
    [-Bound, Bound, 0, Rw],
    [0, Bound, 0, Bound],
    [-Rw, Bound, -Rw, Bound],
    [-Rw, 0, -Bound, Bound],
    [-Bound, 0, 0, Bound],
]

def IsLimitPoint(dir, param):
    x, y, theta = param

    for item in limitAng[dir]:
        if theta>=item[0] and theta<=item[1]:
            return False

    Pol = Point2Pol(x, y, theta)
    for item in Pol:
        if item[0] < limitArea[dir][0] or item[0] > limitArea[dir][1] or item[1] < limitArea[dir][2] or item[1] > limitArea[dir][3]:
            return False

    return True
