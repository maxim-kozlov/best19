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

data = we.getData(team=COMMAND, task=1)
map_, data = we.parce(data)
we.takeText(map_, ("[", "]"))
MAP = np.fromstring(we.takeText(map_, ("[", "]")), dtype=int, sep=",")

data += '}'
data = json.loads('{' + data + '}')
data = data['data']
N = int(len(MAP)**(1/2))

MAP.resize((N, N))

x  =  np.arange(0, N)
y  =  np.arange(0, N)

'''
from mayavi import mlab

mlab.surf(MAP) 

mlab.show()
'''
def getMinEps(maybe):
    best_x, best_y, best_eps = maybe[0][0], maybe[0][1], maybe[0][2]
    for t in maybe:
        if best_eps > t[2]:
            best_eps = t[2]
            best_x = t[0]
            best_y = t[1]
    return best_x, best_y

def getNextMaybe(maybe, initdata, last_psi):
    temp = []
    target_x, target_y, best_target = 0, 0, m.inf
    for t in maybe:
        x, y, _ = t
        speed = initdata['speed'] if initdata['speed'] > 0 else 0.1
        sy = -round(speed * m.cos(last_psi), 6)
        sx = round(speed * m.sin(last_psi), 6)

        best_x, best_y, best_eps = x + sx, y + sy, m.inf
        eps_h = best_eps
        while 0 <= x <= n and 0 <= y <= n:
            if  best_eps > eps_h:
                best_eps = eps_h
                best_x = x
                best_y = y
            x += sx
            y += sy
            eps_h = abs(initdata['height'] - f(x, y))

        # print(f'x = {x:.0f}, y = {y:.0f} f(x, y) = {f(x, y)}')
        if 0 <= best_x <= n and 0 <= best_y <= n:
                if best_eps < data['height'] * 0.001:
                    temp.append((best_x, best_y, best_eps))
                    break
                else:
                    if best_eps < best_target:
                        target_x = best_x
                        target_y = best_y
                        best_target = best_eps
    if not temp:
        temp.append((target_x, target_y, best_target))
    return temp


def getData(x, y, ready = 1):
    a = we.getData( ready=ready, x=x, y=y)
    i = 0
    while a[i] != '{':
        i += 1
    a = a[i:]
    print(a)
    if not ('scores' in a or 'error' in a):
        return json.loads(a)['data']
    else:
        return json.loads(a)

f = interpolate.interp2d(x, y, MAP)
n = N - 1

# eps = 100


best_x, best_y, best_eps = 0, 0, m.inf
maybe = []
for x in range(N):
    for y in range(N):
        eps_h = abs(data['height'] - MAP[x][y])
        if eps_h < data['height'] * 0.001:
            maybe.append((x, y, eps_h))
        else:
            if best_eps > eps_h:
                best_eps = eps_h
                best_x = x
                best_y = y
        if len(maybe) > 10:
            break
if not maybe:
    maybe.append(best_x, best_y, best_eps)

last_psi = m.pi * data['psi'] / 180

initdata = getData(*getMinEps(maybe))

while not ('scores' in initdata or 'error' in initdata):
    maybe = getNextMaybe(maybe, initdata, last_psi)
    last_psi = m.pi * initdata['psi'] / 180 

    initdata = getData(*getMinEps(maybe))
if 'scores' in initdata:
    print(initdata['scores'])
else:
    print(initdata['error'])