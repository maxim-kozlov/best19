import math as m
from scipy import interpolate
from random import uniform, randint

from send import *
import numpy as np
import json

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

we = we()

data = we.getData(w=False, team=COMMAND, task=1)
map_, data = we.parce(data) # '='
we.takeText(map_, ("[", "]"))
MAP = np.fromstring(we.takeText(map_, ("[", "]")), dtype=int, sep=",")

data += '}'
data = json.loads('{' + data + '}')
data = data['data']
N = int(len(MAP)**(1/2))

MAP.resize((N, N))

'''
from mayavi import mlab

mlab.surf(MAP) 

mlab.show()
'''

def getMinEps(maybe):
    best_x, best_y, best_eps = maybe[0][0], maybe[0][1], maybe[0][2]
    for t in maybe:
        s = abs(data['height'] - f(t[0], t[1]))
        if best_eps > s:
            best_eps = s
            best_x = t[0]
            best_y = t[1]
    return best_x, best_y


def getNextMaybe(maybe, initdata, last_psi, last_x, last_y):
    temp = []

    speed = initdata['speed']
    if speed > 0:
        sx = round(speed * m.cos(last_psi), 2)
        sy = round(speed * m.sin(last_psi), 2)
    else:
        sx = round(1 * m.cos(last_psi), 2)
        sy = round(1 * m.sin(last_psi), 2)

    the_best_eps = m.inf
    the_best_x = last_x + sx
    the_best_y = last_y + sy
    

    maybe.append((the_best_x, the_best_y, m.inf))
    for t in maybe:
        x, y, _ = t

        best_x, best_y, best_eps = x, y, m.inf
        eps_h = best_eps
        if not (0 < x < n and 0 < y < n):
            x = x % N
            y = y % N

        x += sx
        y += sy
        while 1 < x < n and 1 < y < n:
            eps_h = abs(initdata['height'] - f(x, y))
            if  best_eps > eps_h:
                best_eps = eps_h
                best_x = x
                best_y = y
                if best_eps < 900:
                    break
            if eps_h > 900:
                break
            x += sx
            y += sy

        if abs(best_eps) < 900:
            if the_best_eps > best_eps:
                the_best_eps = best_eps
                the_best_x = best_x
                the_best_y = best_y
        else:
            if abs(best_eps) < abs(the_best_eps):
                the_best_x = best_x
                the_best_y = best_y
                the_best_eps = abs(best_eps)

        temp.append((the_best_x, the_best_y, abs(the_best_eps)))

    if not temp:
        temp.append((the_best_x, the_best_y, the_best_eps))

    return temp, the_best_x, the_best_y


def getData(x, y, ready = 1):
    # print(x, y)
    a = we.getData( ready=ready, x=x, y=y)
    i = 0
    while a[i] != '{':
        i += 1
    a = a[i:]
    # print(a)
    if not ('scores' in a or 'error' in a):
        return json.loads(a)['data']
    else:
        return json.loads(a)

def f(x, y):
    x = round(x)
    y = round(y)
    return MAP[x][y]

# f = interpolate.interp2d(x, y, MAP, bounds_error=True)
n = N - 1
# eps = 100
'''
best_x, best_y, best_eps = 0, 0, m.inf
maybe = []
for x in range(N):
    for y in range(N):  
        eps_h = abs(data['height'] - MAP[x][y])
        if abs(eps_h) < 1000:
            maybe.append((x, y, eps_h))
        else:
            if abs(best_eps) > eps_h:
                best_eps = eps_h
                best_x = x
                best_y = y
if not maybe:
    maybe.append(best_x, best_y, abs(best_eps))

last_psi = m.pi * data['psi'] / 180

x, y = getMinEps(maybe)

initdata = getData(x, y)
'''
x, y = N/2, N/2
initdata = getData(x, y)

while not ('scores' in initdata or 'error' in initdata):
    initdata = getData(N/2, N/2)

    '''
    maybe, x, y = getNextMaybe(maybe, initdata, last_psi, x, y)
    last_psi = m.pi * initdata['psi'] / 180

    initdata = getData(x, y)
    '''

if 'scores' in initdata:
    print(initdata['scores'])
else:
    print(initdata['error'])