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

data = we.getData(team=COMMAND, task=2)
map_, data = we.parce(data, '=')
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
    print('len =', len(maybe))
    best_x, best_y, best_eps = maybe[0][0], maybe[0][1], maybe[0][2]
    for t in maybe:
        s = abs(data['height'] - f(t[0], t[1]))
        if best_eps > s:
            best_eps = s
            best_x = t[0]
            best_y = t[1]
    print(best_x, best_y, f(best_x, best_y))
    print('best_eps =', best_eps)
    print('height =', data['height'])
    return best_x, best_y


def getNextMaybe(maybe, initdata, last_psi):
    temp = []
    target_x, target_y, best_target = 0, 0, m.inf
    print('len(maybe) =',len(maybe))

    the_best_eps = m.inf
    the_best_x = 0
    the_best_y = 0
    for t in maybe:
        x, y, _ = t
        speed = initdata['speed']
        sx = round(2 * m.cos(last_psi), 2)
        sy = round(2 * m.sin(last_psi), 2)

        best_x, best_y, best_eps = x + sx, y + sy, m.inf
        eps_h = best_eps
        if not (0 < x < n and 0 < y < n):
            continue

        if abs(f(best_x, best_y) - initdata['height']) > 500:
            continue 
        if n < x M and n < y M and 0 < x < 10 and 0 < y < 10 :
            continue

        while 10 < x < M and 10 < y < M:
            if  best_eps > eps_h:
                best_eps = eps_h
                best_x = x
                best_y = y

            if best_eps < 1000:
                break

            eps_h = abs(initdata['height'] - f(x, y))
            x += sx
            y += sy

        if abs(best_eps) < 1000:
            if the_best_eps > best_eps:
                the_best_eps = best_eps
                the_best_x = best_x
                the_best_y = best_y
            temp.append((best_x, best_y, abs(best_eps)))
        else:
            if abs(best_eps) < abs(the_best_eps):
                the_best_x = best_x
                the_best_y = best_y
                the_best_eps = abs(best_eps)

    if not temp:
        temp.append((target_x, target_y, best_target))
    return temp, the_best_x, the_best_y


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

def f(x, y):
    x = round(x)
    y = round(y)
    return MAP[x][y]

# f = interpolate.interp2d(x, y, MAP, bounds_error=True)
n = N - 1
M = n - 10
# eps = 100


best_x, best_y, best_eps = 0, 0, m.inf
maybe = []
print(data['height'])
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

initdata = getData(*getMinEps(maybe))

while not ('scores' in initdata or 'error' in initdata):
    maybe, x, y = getNextMaybe(maybe, initdata, last_psi)
    last_psi = m.pi * initdata['psi'] / 180 
    print("x = ", x)
    print("y = ", y)
    initdata = getData(x, y)

if 'scores' in initdata:
    print(initdata['scores'])
else:
    print(initdata['error'])