import json
import struct
import math as m
import numpy
import copy
from server_work import Courier

def getMinEps(maybe):
    best_x, best_y, best_eps = maybe[0][0], maybe[0][1], maybe[0][2]
    for t in maybe:
        s = abs(data['height'] - f(t[0], t[1]))
        if best_eps > s:
            best_eps = s
            best_x = t[0]
            best_y = t[1]
    return best_x, best_y


def getData(x, y, ready = 1):
    # print(x, y)
    server.send_data(
    json.dumps({"ready": ready, "x": round(x), "y": round(y)}))

    a = server.get_next_json()
    # print(a)
    if not ('scores' in a or 'error' in a):
        return a["data"]
    else:
        return a

server = Courier()

MAP = server.get_next_json()["map"]

N = int(m.sqrt(len(MAP)))
MAP = numpy.array(MAP).reshape((N, N))
print("map: ", MAP)


def getNextMaybe(maybe, initdata, last_psi, last_x, last_y):
    temp = []

    speed = initdata['speed']
    if speed > 0:
        sx = round(2*speed * m.cos(last_psi), 2)
        sy = round(2*speed * m.sin(last_psi), 2)
    else:
        sx = round(2 * m.cos(last_psi), 2)
        sy = round(2 * m.sin(last_psi), 2)

    the_best_eps = m.inf
    the_best_x = last_x + sx
    the_best_y = last_y + sy
    
    if (0 <= the_best_x <= n and 0 <= the_best_y <= n):
        maybe.append((N//2, N//2, m.inf))
    else:
        maybe.append((the_best_x, the_best_y, sx))

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

    return list(set(temp)), the_best_x, the_best_y



def f(x, y):
    x = round(x)
    y = round(y)
    return MAP[x][y]

# f = interpolate.interp2d(x, y, MAP, bounds_error=True)
n = N - 1
# eps = 100

data = server.get_next_json()['data']
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
while not ('scores' in initdata or 'error' in initdata):
    # initdata = getData(N/2, N/2)
    '''
    server.send_data(json.dumps({"ready": 1, "x": N//2, "y": N//2}))
    initdata = server.get_next_json()
    '''
    
    maybe, x, y = getNextMaybe(maybe, initdata, last_psi, x, y)
    last_psi = m.pi * initdata['psi'] / 180

    initdata = getData(y, x)
    

if 'scores' in initdata:
    print(initdata['scores'])
else:
    print(initdata['error'])
    