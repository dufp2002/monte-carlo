from ising import *

g = AnimatedGrid(15,method='bath',show_animation=True,frame=6000,heat_schedule=[0,0,0],schedule='off')
print(g.run())