import sys
import time
import math
import logging
import numpy as np
from model import *
import pygame
from pygame.locals import *
from generate_flow import generateCarFlow
from hybirdAstar import HybirdAstar
from STA import GetSTAPoint, STA


def isFinish():
    for item in PathInfo:
        if item == []:
            return False
    return True


def FCFS_Policy():
    selected_index = -1
    min_time = sys.maxsize

    for index in range(len(PathInfo)):
        if TimeInfo[index] < min_time and PathInfo[index] == []:
            min_time = TimeInfo[index]
            selected_index = index

    return selected_index

def HVsFirst():
    selected_index = -1
    min_time = sys.maxsize

    for index in range(len(PathInfo)):
        if TimeInfo[index] < min_time and PathInfo[index] == [] and TypeInfo[index] == 0:
            min_time = TimeInfo[index]
            selected_index = index

    return selected_index

def cps(para):  # change point size
	x, y = para
	x = x*10 + w/2
	y = -(y*10) + h/2
	return x, y

def drawText(screen,text,posx,posy,textHeight=32,fontColor=(0,0,0)):
    myfont = pygame.font.Font(None,textHeight)
    textSurfaceObj = myfont.render(text, True, fontColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (posx,posy)
    screen.blit(textSurfaceObj,textRectObj.center)

def process_bar(num, total, t):
    rate = float(num)/total
    ratenum = int(100*rate)
    r = '\r[{}{}]{}%{}{}{}'.format('-'*ratenum,' '*(100-ratenum), ratenum, '   The estimated time is',round(t*0.02,1), 's')
    sys.stdout.write(r)
    sys.stdout.flush()


def DrawBackground(t):
    screen.fill((255, 255, 255))
    text = "time: " + str(round(t * dt, 1)) + ' s'
    drawText(screen, text, 50, 50)
    color = [0, 0, 0]
    width = 2

    colorParam = [[0, 255, 0], [255, 255, 0], [255, 0, 0]]
    colorIndex = [2,2,2,2]

    i = int(t/PhaseTime)%4

    if t%PhaseTime < GreenTime:
        colorIndex[i] = 0
    else:
        colorIndex[i] = 1

    for i in range(len(SignleParam)):
        pygame.draw.polygon(screen, colorParam[colorIndex[i]], SignleParam[i], 0)
    for Param in RoundParam:
        pygame.draw.arc(screen, color, Param[0], Param[1], Param[2], width)
    for Param in LineParam:
        pygame.draw.line(screen, color, Param[0], Param[1], width)


    # Phase = int((t % CircleTime) / PhaseTime)

if __name__ == '__main__':
    qr = 7000  # car flow (veh/h)
    T = 60  # amount of simulation time
    s = 0  # random seed
    mtd = 0.05  # minimum time headway
    ratio = 1 # ratio of AVs
    TimeInfo, CarInfo, TypeInfo = generateCarFlow(qr, T, s, mtd, ratio)

    GetSTAPoint()
    total = len(TimeInfo)

    print(TimeInfo)
    print(CarInfo)
    print(TypeInfo)
    print('vehicle nums = ', total)

    PathInfo = [[] for i in range(total)]

    # PathInfo = []
    # TimeInfo, CarInfo, TypeInfo = [], [], []
    run_time = 0
    planned_num = 0
    HVsFinishFlag = False

    while not isFinish():
        if not HVsFinishFlag:
            car_index = HVsFirst()
            if car_index == -1:
                HVsFinishFlag = True
                continue
        else:
            car_index = FCFS_Policy()

        if TypeInfo[car_index] == 0:
            path = STA(CarInfo[car_index], TimeInfo[car_index], PathInfo, TimeInfo)
        else:
            path = HybirdAstar(CarInfo[car_index], TimeInfo[car_index], PathInfo, TimeInfo, TypeInfo)

        if path == -1:
            TimeInfo[car_index] += 1
            continue

        PathInfo[car_index] = path
        planned_num += 1
        temp_time = TimeInfo[car_index]+len(PathInfo[car_index])
        if temp_time > run_time:
            run_time = temp_time
        process_bar(planned_num, total, run_time)

    print(len(CarInfo), 'vehicles passed the intersection in', str(run_time * dt), 'seconds')

    pygame.init()
    screen = pygame.display.set_mode((w, h))
    screen.fill((255, 255, 255))
    pygame.display.update()
    pygame.display.flip()
    time.sleep(1)

    # run_time = 100000
    for t in range(run_time):
        time.sleep(0.01)

        DrawBackground(t)

        for index0 in range(len(PathInfo)):
            if t < TimeInfo[index0] or t - TimeInfo[index0] >= len(PathInfo[index0]):
                continue
            index1 = t - TimeInfo[index0]

            p_temp = Point2Pol1(PathInfo[index0][index1][0], PathInfo[index0][index1][1], PathInfo[index0][index1][2])

            polygon = [cps(p_temp[0]), cps(p_temp[1]), cps(p_temp[2]), cps(p_temp[3])]

            if TypeInfo[index0] == 1:
                pygame.draw.polygon(screen, [255, 0, 0], polygon, 0)
            else:
                pygame.draw.polygon(screen, [0, 0, 255], polygon, 0)

        pygame.display.update()
        pygame.display.flip()
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)

    screen.fill((255, 255, 255))
    pygame.display.update()
    pygame.display.flip()
    time.sleep(3)