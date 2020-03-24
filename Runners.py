# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 12:59:10 2020

@author: whatf

Class code for the in-game runners
"""

import pylab as pl
import numpy as np

class Runner():
    """
    Class describing how an sprite in the virtual environment behaves, 
    moving to track, or evade, its opponent.
    """
    def __init__(self, pos=[0,0], vel=[0,0], colour='gray'):
        self._pos = np.array(pos)
        self._vel = np.array(vel)
        self._patch = pl.Circle(self._pos, 0.2, fc=colour)
        
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

class Chaser(Runner):
    """
    Class to describe a chaser, a kind of runner that chases a given target
    by adjusting its velocity to track it.
    """
    def __init__(self):
        Runner.__init__(self, pos=[-1,0], colour='red')
        
    def seek(self, other):
        direction = other._pos - self._pos
        absolute = np.sqrt(direction[0]**2 + direction[1]**2)
        self.setvel(direction/absolute)
        
class World():
    """
    Class describing the world in which the runners operate.
    """
    def __init__(self, x=10, y=10, dt=0.02):
        self._lenx = x
        self._leny = y
        self._dt = dt
        self._chaser = Chaser()
        self._runner = Runner(pos=[1,0], vel=[0,1])
        
    def create(self):
        ax = pl.axes(xlim=(-self._lenx/2, self._lenx/2),
                                ylim=(-self._leny/2, self._leny/2),
                                aspect=1)
        ax.add_artist(self._chaser.get_patch())
        ax.add_artist(self._runner.get_patch())
        while(True):
            pl.pause(self._dt)
            self._chaser.seek(self._runner)
            self._runner.move(self._dt)
            self._chaser.move(self._dt)
            ax.add_patch(self._runner.get_patch())
            ax.add_patch(self._chaser.get_patch())
            
            if(self._runner._pos[0] > 5 or self._runner._pos[1] > 5):
                break
            