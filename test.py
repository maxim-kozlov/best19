from send import *
from timeit import default_timer
import numpy as np

we = we()

data = we.getData(team=COMMAND, task=1)
map_, data = we.parce(data)

we.takeText(map_, ("[", "]"))

MAP = np.fromstring(we.takeText(map_, ("[", "]")), dtype=int, sep=",")


N = int(len(MAP)**(1/2))

MAP.resize((N, N))

print(MAP)

a = we.getData( ready=1, x=0, y=0)
print(a)
