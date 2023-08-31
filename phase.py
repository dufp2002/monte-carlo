import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from copy import *
from ising import *
import multiprocessing
from multiprocessing import Pool

def f(x):
    grid = AnimatedGrid(size,show_animation=False,frame=frame,heat_schedule=[x,0,0])
    return grid.run()

temp = [i/2000 for i in range(40)]
data = []
nrep = 30
size = 30
frame = 6000

for i in temp:
    with Pool(multiprocessing.cpu_count()) as p:
        data.append(p.map(f, [i for j in range(nrep)]))
        
ave = []
for i in data:
    foo = 0
    for j in i:
        foo+= np.abs(j)
    foo = foo/len(i)
    ave.append(foo)
    
plt.plot(temp,ave)
plt.savefig('phase_dia.png')