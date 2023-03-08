import math
import numpy as np
from model import *


def B(n,i,t):
    return math.factorial(n)/(math.factorial(i)*math.factorial(n-i)) * t**i * (1-t)**(n-i)


def Bezier(p,n,c,dir):
    res = [(StartPoint[dir][0],StartPoint[dir][1],StartAng[dir])]
    temp = 0
    x1, y1 = p[0][0], p[0][1]
    for t in np.arange(0, 1+c, c):
        x0, y0 = 0, 0
        for i in range(n+1):
            x0 += B(n,i,t) * p[i][0]
            y0 += B(n,i,t) * p[i][1]

        dx = x0 - x1
        dy = y0 - y1
        x1 = x0
        y1 = y0
        temp += math.sqrt(dx*dx + dy*dy)

        if temp>=v*dt:
            theta = math.atan2(dy, dx)
            res.append((x0,y0,theta))
            temp -= v*dt
            dx1 = x0-EndPoint[dir][0]
            dy1 = y0-EndPoint[dir][1]
            if (dx1*dx1)+(dy1*dy1) < 1:
                break

    return res
