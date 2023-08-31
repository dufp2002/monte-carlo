import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx

class AnimatedGrid:
    def __init__(self, size=10, show_animation=True, frame=2000, T=0, interval_time=0.05, method='metropolis',heat_schedule=[0,0,0],schedule='off'):
        self.grid_size = size
        self.grid = np.random.randint(2, size=(self.grid_size, self.grid_size))
        self.show_animation = show_animation
        self.g = nx.grid_2d_graph(self.grid_size,self.grid_size,periodic=True)
        self.mag = None
        self.frame = frame
        self.heat_schedule = heat_schedule
        self.T = self.heat_schedule[0]
        self.interval_time = interval_time
        self.method = method
        self.schedule = schedule
        
        if self.show_animation:
            self.fig, self.ax = plt.subplots()
            colors = {0: 'blue', 1: 'red'}
            bounds = [0, 1, 2]
            self.cmap = plt.cm.colors.ListedColormap([colors[0], colors[1]])
            self.norm = plt.cm.colors.BoundaryNorm(bounds, self.cmap.N)
            self.im = self.ax.imshow(self.grid, cmap=self.cmap, norm=self.norm)
            self.frame_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes)

    def update(self, frame):
        if self.schedule=='on':
            self.heat_schedule(frame)
        before = 0
        after = 0
        self.mag_update()
        J = 1
        T = 0
        s = (np.random.randint(self.grid_size),np.random.randint(self.grid_size))
        for edge in self.g.edges(s):
            if (1-self.grid[s[0],s[1]])==self.grid[edge[1][0],edge[1][1]]:
                before+= J
                after+= -J
            else:
                before+= -J
                after+= J
        
        delta = after-before
        delta+= self.mag*(self.grid[s[0],s[1]]-1/2) # converges faster
        
        if delta<0:
            self.grid[s[0], s[1]] = 1 - self.grid[s[0],s[1]]
        else:
            if self.T==0:
                pass
            elif self.method=='metropolis':
                if np.random.randint(0,2)<np.exp(-delta/self.T):
                    self.grid[s[0],s[1]] = (1-self.grid[s[0],s[1]])
            elif self.method=='bath':
                if np.random.randint(0,2)<2/(1+np.exp(delta/self.T)):
                    self.grid[s[0],s[1]] = (1-self.grid[s[0],s[1]])
            else:pass
        
        self.mag_update()
        
        if self.show_animation:
            self.im.set_data(self.grid)
            self.frame_text.set_text(f'Frame: {frame}'f'T: {self.T}'f'H: {self.mag}')
            return [self.im,self.frame_text]
        else:
            return None
    
    def mag_update(self):
        m = 0.0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                m+= self.grid[i,j]
        m+= -(self.grid_size*self.grid_size)/2
        m = 2*m/(self.grid_size*self.grid_size)
        self.mag = m
        
    def schedule(self,frame):
        if frame<self.heat_schedule[2]:
            pass
        else:
            self.T = (self.heat_schedule[1]-self.heat_schedule[0])/(self.frame-self.heat_schedule[2])*(frame-self.heat_schedule[2])

    def run(self):
        if self.show_animation:
            ani = FuncAnimation(self.fig if self.show_animation else plt.figure(), 
                        self.update, frames=self.frame, blit=True, interval=self.interval_time,repeat=False)
            plt.show()
        else:
            for i in range(self.frame):
                self.update(i)
        
        return self.mag