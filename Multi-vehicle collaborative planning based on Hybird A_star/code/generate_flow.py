# ---------------------------------------------------------------------------------
# @Desciption: generate car flow or people flow by Possion Distribution
# @Author: Pinlong Cai
# @Date: January 8th, 2022 
# @Input: real flow, maximum time, random seed, minimum time headway
# @Output: list, consist of arrival time of indivials (car or people)
# ---------------------------------------------------------------------------------
import random, math

import numpy as np
from model import *
# qr (veh/h): real flow, which represents the amount of arrivals in unit time (per hour)
# T (sec.): maximum simulation time
# s: random seed to ensure consistant simulation
# mtd (sec.): the minimum of time headway for safety
# ratio (sec.): the ratio of AVs
def generateCarFlow(qr, T, s, mtd, ratio):
    random.seed(s)
    lampda = qr/3600  # the reciprocal of average time headway
    ArrivalTime = 0   # init arrival time of current vehicle
    last_ArrivalTime = 0  # init arrival time of last vehicle
    TimeFlow = []
    CarFlow = []

    while(1):
        #  generate time headway for each randomly, which must be larger than mtd
        timeheadway = max(-1/lampda*math.log(random.random()), mtd)
        ArrivalTime = last_ArrivalTime+timeheadway
        if ArrivalTime - T > 0:
            break
        TimeFlow.append(int(ArrivalTime/dt)) # accurate to two decimal places (optional)

        CarFlow.append(len(TimeFlow)%12)
        last_ArrivalTime = ArrivalTime

    TypeFlow = [0 for i in range(len(CarFlow))]

    for i in range(int(ratio*len(CarFlow))):
        TypeFlow[i] = 1

    random.shuffle(TimeFlow)
    random.shuffle(CarFlow)
    random.shuffle(TypeFlow)

    return TimeFlow, CarFlow, TypeFlow

# example
if __name__ == "__main__":
    qr = 12000  # car flow (veh/h)
    T = 15   # amount of simulation time
    s = 0     # random seed
    mtd = 0.1   # minimum time headway
    TimeInfo, CarInfo = generateCarFlow(qr, T, s, mtd)

    print("Arival time for ", str(len(TimeInfo)), " vehicles in ", str(T) , " s are present as belows: ")
    print(TimeInfo)
    print(CarInfo)