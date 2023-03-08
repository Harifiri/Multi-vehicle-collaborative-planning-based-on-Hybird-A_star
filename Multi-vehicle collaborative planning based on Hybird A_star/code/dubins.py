import sys
import math
from model import *

# [t,p,q]->[第一段曲线，第二段曲线，第三段曲线]
# [0,1,2]->[左转，直行，右转]

def unpack(alpha, beta):
    return math.sin(alpha), math.sin(beta), math.cos(alpha), math.cos(beta), math.cos(alpha-beta)

def mymodf(x, y):
    return x - y*math.floor(x/y)

def mod2pi(theta):
    return mymodf(theta, 2*math.pi)

# 构造LSL路径类型的的函数[t,p,q]->[第一段曲线，第二段曲线，第三段曲线],[0,1,2]->[左转，直行，右转]
def dubins_LSL(alpha, beta, d):
    sa, sb, ca, cb, c_ab = unpack(alpha, beta)

    p_squared = 2 + (d*d) - (2*c_ab) + (2*d*(sa-sb))
    if p_squared < 0:
        return -1

    tmp = math.atan2((cb-ca), (d+sa-sb))
    t = mod2pi(-alpha + tmp)
    p = math.sqrt(p_squared)
    q = mod2pi(beta - tmp)

    # res = [(t, 2), (p, 1), (q, 2)]
    res = t+p+q
    return res

# 构造RSR路径类型的的函数[0,1,2]->[左转，直行，右转]
def dubins_RSR(alpha, beta, d):
    sa, sb, ca, cb, c_ab = unpack(alpha, beta)

    p_squared = 2 + (d*d) - (2*c_ab) + (2*d*(sb-sa))
    if p_squared < 0:
        return -1

    tmp = math.atan2((ca-cb), (d-sa+sb))
    t = mod2pi(alpha - tmp)
    p = math.sqrt(p_squared)
    q = mod2pi(-beta + tmp)

    # res = [(t, 2), (p, 1), (q, 2)]
    res = t+p+q
    return res

# 构造LSR路径类型的的函数[0,1,2]->[左转，直行，右转]
def dubins_LSR(alpha, beta, d):
    sa, sb, ca, cb, c_ab = unpack(alpha, beta)

    p_squared = -2 + (d*d) + (2*c_ab) + (2*d*(sa+sb))
    if p_squared < 0:
        return -1

    p = math.sqrt(p_squared)
    tmp = math.atan2((-ca-cb), (d+sa+sb)) - math.atan2(-2, p)
    t = mod2pi(-alpha + tmp)
    q = mod2pi(-mod2pi(beta) + tmp)

    # res = [(t, 2), (p, 1), (q, 2)]
    res = t+p+q
    return res

# 构造LSR路径类型的的函数[0,1,2]->[左转，直行，右转]
def dubins_RSL(alpha, beta, d):
    sa, sb, ca, cb, c_ab = unpack(alpha, beta)

    p_squared = -2 + (d*d) + (2*c_ab) - (2*d*(sa+sb))
    if p_squared < 0:
        return -1

    p = math.sqrt(p_squared)
    tmp = math.atan2((ca+cb), (d-sa-sb)) - math.atan2(2, p)
    t = mod2pi(alpha-tmp)
    q = mod2pi(beta-tmp)

    # res = [(t, 2), (p, 1), (q, 2)]
    res = t+p+q
    return res

# 构造RLR路径类型的的函数[0,1,2]->[左转，直行，右转]
def dubins_RLR(alpha, beta, d):
    sa, sb, ca, cb, c_ab = unpack(alpha, beta)

    tmp = (6 - d*d + 2*c_ab + 2*d*(sa-sb)) / 8
    if abs(tmp) > 1:
        return -1

    p = mod2pi(2*math.pi - math.acos(tmp))
    t = mod2pi(alpha - math.atan2(ca-cb, d-sa+sb) + mod2pi(p/2))
    q = mod2pi(alpha - beta - t + mod2pi(p))

    # res = [(t, 2), (p, 1), (q, 2)]
    res = t+p+q
    return res

# 构造LRL路径类型的的函数[0,1,2]->[左转，直行，右转]
def dubins_LRL(alpha, beta, d):
    sa, sb, ca, cb, c_ab = unpack(alpha, beta)

    tmp = (6 - d*d + 2*c_ab + 2*d*(sb-sa)) / 8
    if abs(tmp) > 1:
        return -1

    p = mod2pi(2*math.pi - math.acos(tmp))
    t = mod2pi(-alpha - math.atan2(ca-cb, d+sa-sb) + p/2)
    q = mod2pi(mod2pi(beta) - alpha - t + mod2pi(p))

    # res = [(t, 2), (p, 1), (q, 2)]
    res = t+p+q
    return res

def dubins(start, dir):
    x0, y0, alpha = start
    x1, y1, beta = EndPoint[dir][0], EndPoint[dir][1], EndAng[dir]

    dx = x1-x0
    dy = y1-y0
    D = math.sqrt(dx*dx + dy*dy)
    d = D/r_min
    theta = 0

    if d > 0:
        theta = mod2pi(math.atan2(dy, dx))

    alpha = mod2pi(alpha-theta)
    beta = mod2pi(beta-theta)

    cost = sys.maxsize
    res = []
    #[0, 1, 2]->[左转，直行，右转]
    res.append(dubins_LSL(alpha, beta, d))
    res.append(dubins_RSR(alpha, beta, d))
    res.append(dubins_LSR(alpha, beta, d))
    res.append(dubins_RSL(alpha, beta, d))
    res.append(dubins_RLR(alpha, beta, d))
    res.append(dubins_LRL(alpha, beta, d))

    for i in range(6):
        if res[i] == -1:
            continue

        if res[i] < cost:
            cost = res[i]

    return cost*r_min
