# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 12:59:10 2020

@author: whatf

Class code for the in-game runners
"""

import matplotlib.pyplot as plt
import numpy as np

class Runner():
    """
    Class describing how an sprite in the virtual environment behaves, 
    moving to track, or evade, its opponent.
    """
    def __init__(self, pos=[0,0], vel=[0,0], radius=0.2, colour='gray'):
        self._pos = np.array(pos)
        self._vel = np.array(vel)
        self._radius = radius
        self._patch = plt.Circle(self._pos, radius, fc=colour)
        
    def get_patch(self):
        """
        Returns the runner's current patch
        """
        self._patch.center = list(self._pos)
        return self._patch
    
    def move(self, dt):
        self._pos = self._pos + self._vel*dt
        
    def setvel(self, newvel=[0,0]):
        self._vel = np.array(newvel)
        
    def seek(self, other):
        """
        Returns unit vector pointing from self to other.
        """
        direction = other._pos - self._pos
        absolute = np.sqrt(direction[0]**2 + direction[1]**2)
        return (direction/absolute)
    
    def separation(self, other):
        return np.sqrt(
                    (self._pos[0]-other._pos[0])**2
                    + (self._pos[0]-other._pos[0])**2)

class Chaser(Runner):
    """
    Class to describe a chaser, a kind of runner that chases a given target
    by adjusting its velocity to track it.
    """
    def __init__(self, cpos, cvel):
        Runner.__init__(self, pos=cpos, vel=cvel, colour='red')
        
    def follow(self, other):
        self.setvel(self.seek(other))
        
class Scaper(Runner):
    """
    Class for 'scapers', the particles that avoid the chasers.
    They also have to avoid the walls.
    """
    def __init__(self, spos, svel):
        Runner.__init__(self, pos=spos, vel=svel, colour='blue')
        
    def trackback(self, other):
        x = np.linspace(self._pos[0], other._pos[0], 10)
        y = np.linspace(self._pos[1], other._pos[1], 10)        
        plt.plot(x, y)
    
    def isotropic_lines(self, other, n=1):
        r = self.seek(other)
        rotate = np.array([[np.cos(2*np.pi/(n+1)), -np.sin(2*np.pi/(n+1))],
                            [np.sin(2*np.pi/(n+1)), np.cos(2*np.pi/(n+1))]])
        for i in range(0, n):
            r = np.matmul(rotate, r)
            x0 = self._pos[0]
            y0 = self._pos[1]
            mu = []
            mu.append((10-y0)/r[1])
            mu.append((-10-y0)/r[1])
            mu.append((10-x0)/r[0])
            mu.append((-10-x0)/r[0])
            
            mu_chosen = 10
            for j in range(0, 4):
               if(mu[j] > 0 and mu[j] < mu_chosen):
                   mu_chosen = mu[j]
    
            x = np.linspace(x0, (x0+mu_chosen*r[0]), 10)
            y = np.linspace(y0, (y0+mu_chosen*r[1]), 10)
            plt.plot(x, y)
            
    def flee(self, other, xlim, ylim):
        x_wall = self._pos[0]/(xlim-self._pos[0]**2)**4
        x_chase = 1/(other._pos[0]-self._pos[0])**5
#        x_wall = 0 #for testing
        x_slope = x_wall+x_chase
        
        y_wall = self._pos[1]/(ylim-self._pos[1]**2)**4
        y_chase = 1/(other._pos[1]-self._pos[1])**5
#        y_wall = 0 #for testing
        y_slope = y_wall+y_chase
        
        mag = np.sqrt(x_slope**2 + y_slope**2)
        newvel = np.array([-x_slope, -y_slope])
        
        self.setvel(newvel/mag)

class World():
    """
    Class describing the world in which the runners operate.
    """
    def __init__(self, x=10, y=10, dt=0.02, start=
                 [[0,0], [0,0], [0,0], [0,0]]):
        self._lenx = x
        self._leny = y
        self._dt = dt    
        self._scaper = Scaper(spos=start[0], svel=start[1])    
        self._chaser = Chaser(cpos=start[2], cvel=start[3])
    
    def create(self, first_frame=False, definition=1):
        ax = plt.axes(xlim=(-self._lenx/2, self._lenx/2),
                                ylim=(-self._leny/2, self._leny/2),
                                aspect=1)
        ax.add_artist(self._chaser.get_patch())
        ax.add_artist(self._scaper.get_patch())
        
        if(first_frame == True):
            self._scaper.trackback(self._chaser)
            self._scaper.isotropic_lines(self._chaser, definition)
        
        while(first_frame == False):
            plt.pause(self._dt)
            
            self._chaser.follow(self._scaper)
#            print("{:.3f}".format(self._scaper.separation(self._chaser)))
            self._scaper.flee(self._chaser,
                              self._lenx/2, self._leny/2)
            
            self._scaper.move(self._dt)
            self._chaser.move(self._dt)
            
            ax.add_patch(self._scaper.get_patch())
            #ax.add_patch(self._scaper.trackback(self._chaser))
            ax.add_patch(self._chaser.get_patch())
            
            if(abs(self._scaper._pos[0]) > self._lenx/2 or 
               abs(self._scaper._pos[1]) > self._leny/2):
                print("Out of bounds!")
                break
            elif(self._chaser.separation(self._scaper) 
            < self._chaser._radius + self._scaper._radius):
                print("Caught!")
                break
            