import math

import numpy as np

v = 12.5
steer_max = 0.63
Lw = 4 #4
Lf = 0
Lr = 0
Lb = 2 #2
Lw_zone = 5
Lb_zone = 3
R = math.sqrt(pow(Lr+Lw, 2) + pow(Lb, 2))/2
r_min = Lw/math.sin(steer_max)
dt = 0.02
Rw = 11.25
Lane = 3.75
GreenBelt = 4
Bound = 25
GridSize = 0.05
AovidStep = 20

GreenTime = 12/dt
YellowTime = 3/dt
PhaseTime = GreenTime+YellowTime
CircleTime = 4*PhaseTime

w = 800
h = 600

StartAng = [0, 0, 0, math.pi/2, math.pi/2, math.pi/2, math.pi, math.pi, math.pi, 3*math.pi/2, 3*math.pi/2, 3*math.pi/2]
EndAng = [math.pi/2, 0, 3*math.pi/2, math.pi, math.pi/2, 0, 3*math.pi/2, math.pi, math.pi/2, 0, 3*math.pi/2, math.pi]

delta_G = v*dt
steer = {-1:-steer_max/6, -2:-steer_max/3, -3:-steer_max/2, -4:-2*steer_max/3, -5:-5*steer_max/6, -6:-steer_max, 0:0, 1:steer_max/6, 2:steer_max/3, 3:steer_max/2, 4:2*steer_max/3, 5:5*steer_max/6, 6:steer_max}
r = {1:Lw/math.sin(steer[1]), 2:Lw/math.sin(steer[2]), 3:Lw/math.sin(steer[3]), 4:Lw/math.sin(steer[4]), 5:Lw/math.sin(steer[5]), 6:Lw/math.sin(steer[6])}
ang = {1:2*math.asin((delta_G/2)/r[1]), 2:2*math.asin((delta_G/2)/r[2]), 3:2*math.asin((delta_G/2)/r[3]), 4:2*math.asin((delta_G/2)/r[4]), 5:2*math.asin((delta_G/2)/r[5]), 6:2*math.asin((delta_G/2)/r[6])}
G = {0:delta_G, 1:r[1]*ang[1], 2:r[2]*ang[2], 3:r[3]*ang[3], 4:r[4]*ang[4], 5:r[5]*ang[5], 6:r[6]*ang[6]}

StartPoint = [
	(-Rw-2*Lane, -Rw/6),
	(-Rw-2*Lane, -Rw/2),
	(-Rw-2*Lane, -5*Rw/6),
	(Rw/6, -Rw-2*Lane),
	(Rw/2, -Rw-2*Lane),
	(5*Rw/6, -Rw-2*Lane),
	(Rw+2*Lane, Rw/6),
	(Rw+2*Lane, Rw/2),
	(Rw+2*Lane, 5*Rw/6),
	(-Rw/6, Rw+2*Lane),
	(-Rw/2, Rw+2*Lane),
	(-5*Rw/6, Rw+2*Lane),
]

EndPoint = [
	(Rw/6, Rw+Lane+1),
	(Rw+Lane+1, -Rw/2),
	(-5*Rw/6, -Rw-Lane-1),
	(-Rw-Lane-1, Rw/6),
	(Rw/2, Rw+Lane+1),
	(Rw+Lane+1, -5*Rw/6),
	(-Rw/6, -Rw-Lane-1),
	(-Rw-Lane-1, Rw/2),
	(5*Rw/6, Rw+Lane+1),
	(Rw+Lane+1, -Rw/6),
	(-Rw/2, -Rw-Lane-1),
	(-Rw-Lane-1, 5*Rw/6)
]

#ROUND: (x,y,radius)
Round = [
	(-Rw-Lane, Rw+Lane, Lane),
	(-Rw-Lane, -Rw-Lane, Lane),
	(Rw+Lane, -Rw-Lane, Lane),
	(Rw+Lane, Rw+Lane, Lane),
]

LineParam = [
	[(0,h/2-Rw*10),(w/2-(Rw+Lane)*10+3,h/2-Rw*10)],
	[(0,h/2),(w/2-(Rw+Lane)*10,h/2)],
	[(0,h/2+Rw*10),(w/2-(Rw+Lane)*10+3,h/2+Rw*10)],

	[(w/2+(Rw+Lane)*10,h/2-Rw*10),(w,h/2-Rw*10)],
	[(w/2+(Rw+Lane)*10,h/2),(w,h/2)],
	[(w/2+(Rw+Lane)*10,h/2+Rw*10),(w,h/2+Rw*10)],

	[(w/2-Rw*10,0),(w/2-Rw*10,h/2-(Rw+Lane)*10+3)],
	[(w/2,0),(w/2,h/2-(Rw+Lane)*10)],
	[(w/2+Rw*10,0),(w/2+Rw*10,h/2-(Rw+Lane)*10+3)],

	[(w/2-Rw*10,h),(w/2-Rw*10,h/2+(Rw+Lane)*10)],
	[(w/2,h),(w/2,h/2+(Rw+Lane)*10)],
	[(w/2+Rw*10,h),(w/2+Rw*10,h/2+(Rw+Lane)*10)],
]

RoundParam = [
	[(w/2-Rw*10-Lane*20+3, h/2-Rw*10-Lane*20+3, Lane*20, Lane*20), math.radians(270), math.radians(0)],
	[(w/2-Rw*10-Lane*20+3, h/2+Rw*10, Lane*20, Lane*20), math.radians(0), math.radians(90)],
	[(w/2+Rw*10, h/2+Rw*10, Lane*20, Lane*20), math.radians(90), math.radians(180)],
	[(w/2+Rw*10, h/2-Rw*10-Lane*20+3, Lane*20, Lane*20), math.radians(180), math.radians(270)],
]


SignleParam = [
	[(w/2-(Rw+Lane)*10-2, h/2-Rw*10), (w/2-(Rw+Lane)*10, h/2-Rw*10), (w/2-(Rw+Lane)*10, h/2), (w/2-(Rw+Lane)*10-2, h/2)],
	[(w/2+Rw*10, h/2+(Rw+Lane)*10), (w/2+Rw*10, h/2+(Rw+Lane)*10+2), (w/2, h/2+(Rw+Lane)*10+2), (w/2, h/2+(Rw+Lane)*10)],
	[(w/2+(Rw+Lane)*10, h/2-Rw*10), (w/2+(Rw+Lane)*10+2, h/2-Rw*10), (w/2+(Rw+Lane)*10+2, h/2), (w/2+(Rw+Lane)*10, h/2)],
	[(w/2-Rw*10, h/2-(Rw+Lane)*10-2), (w/2, h/2-(Rw+Lane)*10-2), (w/2, h/2-(Rw+Lane)*10), (w/2-Rw*10, h/2-(Rw+Lane)*10)],
]


#Block: [(left,top),width,length]
Block1 = [
	(-Bound, Bound),
	Bound-Rw,
	Bound-Rw,
]
Block2 = [
	(Rw, Bound),
	Bound-Rw,
	Bound-Rw,
]
Block3 = [
	(Rw, -Rw),
	Bound-Rw,
	Bound-Rw,
]
Block4 = [
	(-Bound, -Rw),
	Bound-Rw,
	Bound-Rw,
]


def Point2Pol(x, y, ang):
    p1 = (x-Lb_zone/2*math.sin(ang)-Lr*math.cos(ang), y+Lb_zone/2*math.cos(ang)-Lr*math.sin(ang))
    p2 = (x+Lb_zone/2*math.sin(ang)-Lr*math.cos(ang), y-Lb_zone/2*math.cos(ang)-Lr*math.sin(ang))
    p3 = (x+Lb_zone/2*math.sin(ang)+Lw_zone*math.cos(ang), y-Lb_zone/2*math.cos(ang)+Lw_zone*math.sin(ang))
    p4 = (x-Lb_zone/2*math.sin(ang)+Lw_zone*math.cos(ang), y+Lb_zone/2*math.cos(ang)+Lw_zone*math.sin(ang))

    pol = [p1, p2, p3, p4]

    return pol

def Point2Pol1(x, y, ang):
    p1 = (x-Lb/2*math.sin(ang), y+Lb/2*math.cos(ang))
    p2 = (x+Lb/2*math.sin(ang), y-Lb/2*math.cos(ang))
    p3 = (x+Lb/2*math.sin(ang)+Lw*math.cos(ang), y-Lb/2*math.cos(ang)+Lw*math.sin(ang))
    p4 = (x-Lb/2*math.sin(ang)+Lw*math.cos(ang), y+Lb/2*math.cos(ang)+Lw*math.sin(ang))

    pol = [p1, p2, p3, p4]

    return pol


def Rec2Pol(rec):
    p1, w, l = rec
    p2 = (p1[0], p1[1] - l)
    p3 = (p1[0] + w, p1[1] - l)
    p4 = (p1[0] + w, p1[1])

    pol = [p1, p2, p3, p4]

    return pol


#item: [dir, x, y, v, steer, ang]
# def car_init(dir,x0,y0):
# 	x = x0
# 	y = y0
# 	v = 10
# 	steer = 0
# 	lane = int(dir/4)
# 	ang = lane * math.pi
#
# 	CarInfo = [dir, x, y, v, steer, ang]
#
# 	return CarInfo
#
# 	# xc = x + (Lw + Lf - Lr) / 2 * math.cos(ang)
# 	# yc = y + (Lw + Lf - Lr) / 2 * math.sin(ang)
#
# def car_iter(item,a,w):
# 	dir, x, y, v, steer, ang = item
# 	v += a*dt
# 	steer += w*dt
# 	if (abs(v) > v_max):
# 		if v > 0:
# 			v = v_max
# 		else:
# 			v = -v_max
# 	if (abs(steer) > steer_max):
# 		if steer > 0:
# 			steer = steer_max
# 		else:
# 			steer = -steer_max
# 	ang += v * math.tan(steer) / Lw
# 	x += v * math.cos(ang)
# 	y += v * math.sin(ang)
# 	# xc = x + (Lr + Lf - Lr) / 2 * math.cos(ang)
# 	# yc = y + (Lr + Lf - Lr) / 2 * math.sin(ang)
#
# 	CarInfo = [dir, x, y, v, steer, ang]
#
# 	tf += dt
#
# 	return CarInfo

if __name__ == '__main__':
	for i in np.arange(0, AovidStep,5):
		print(i)




	
