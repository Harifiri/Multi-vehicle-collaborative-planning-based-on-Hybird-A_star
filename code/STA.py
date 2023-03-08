import matplotlib.pyplot as plt
import numpy as np
from conflict import IsConflictPoint, IsConflictPoint1
from bezier import Bezier
from model import *

STA_point_ = [[] for i in range(12)]

LeftTurnPoint = [[(-Rw-2*Lane, -Rw/6), (-Rw, -Rw/12), (0, 0), (Rw/12, Rw), (Rw/6, Rw+2*Lane)],
                 [(Rw/6, -Rw-2*Lane), (Rw/12, -Rw), (0, 0), (-Rw, Rw/12), (-Rw-2*Lane, Rw/6)],
                 [(Rw+2*Lane, Rw/6), (Rw, Rw/12), (0, 0), (-Rw/12, -Rw), (-Rw/6, -Rw-2*Lane)],
                 [(-Rw/6, Rw+2*Lane), (-Rw/12, Rw), (0, 0), (Rw, -Rw/12), (Rw+2*Lane, -Rw/6)]]

RightTurnPoint = [[(-Rw-2*Lane, -5*Rw/6), (-Rw, -5*Rw/6), (-11*Rw/12, -11*Rw/12), (-5*Rw/6, -Rw), (-5*Rw/6, -Rw-2*Lane)],
                 [(5*Rw/6, -Rw-2*Lane), (5*Rw/6, -Rw), (11*Rw/12, -11*Rw/12), (Rw, -5*Rw/6), (Rw+2*Lane, -5*Rw/6)],
                 [(Rw+2*Lane, 5*Rw/6), (Rw, 5*Rw/6), (11*Rw/12, 11*Rw/12), (5*Rw/6, Rw), (5*Rw/6, Rw+2*Lane)],
                 [(-5*Rw/6, Rw+2*Lane), (-5*Rw/6, Rw), (-11*Rw/12, 11*Rw/12), (-Rw, 5*Rw/6), (-Rw-2*Lane, 5*Rw/6)]]

def GetSTAPoint():
    for value in np.arange(-Rw-Lane,Rw+Lane,v*dt):
        if abs(value-Rw-Lane)<1:
            break
        STA_point_[1].append((value, -Rw/2, 0))
        STA_point_[4].append((Rw/2, value, math.pi/2))
        STA_point_[7].append((-value, Rw/2, math.pi))
        STA_point_[10].append((-Rw/2, -value, 3*math.pi/2))

    for i in range(4):
        STA_point_[i*3] = Bezier(LeftTurnPoint[i], len(LeftTurnPoint[i])-1, 0.0001, i*3)
        STA_point_[i*3+2] = Bezier(RightTurnPoint[i], len(RightTurnPoint[i])-1, 0.0001, i*3+2)

# @return lane(0-3), state([True,Flase]->[Green,Yellow])
def GetSignalState(dir, t):
    if dir%3 ==2:
        return True

    lane = int(t/PhaseTime)%4
    state = t%PhaseTime < GreenTime
    if int(dir/3) == lane and state == True:
        return True

    return False


def STA(dir, t, PathInfo, TimeInfo):
    if not GetSignalState(dir, t):
        return -1
    else:
        for index in range(len(STA_point_[dir])):
            if IsConflictPoint1(STA_point_[dir][index], t+index, PathInfo, TimeInfo):
                return -1

    return STA_point_[dir]



if __name__=="__main__":
    GetSTAPoint()

    for Point in STA_point_:
        print(len(Point))
        print(Point)
        x = []
        y = []
        for p in Point:
            x.append(p[0])
            y.append(p[1])
        plt.plot(x, y, color='b', linewidth=1, linestyle='--')

    plt.show()