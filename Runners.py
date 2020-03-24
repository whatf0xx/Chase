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
    def __init__(self, pos=[0,0], vel=[0,0]):
        self._pos = np.array(pos)
        self._vel = np.array(vel)
        self._patch = pl.Circle(self._pos, 0.2, fc='gray')
        
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

class World():
    """
    Class describing the world in which the runners operate.
    """
    def __init__(self, x=10, y=10, dt=0.02):
        self._lenx = x
        self._leny = y
        self._dt = dt
        self._runner = Runner(vel=[1,0])
        
    def create(self):
        ax = pl.axes(xlim=(-self._lenx/2, self._lenx/2),
                                ylim=(-self._leny/2, self._leny/2),
                                aspect=1)
        ax.add_artist(self._runner.get_patch())
        while(True):
            pl.pause(self._dt)
            self._runner.move(self._dt)
            ax.add_patch(self._runner.get_patch())
            
            if(self._runner._pos[0] > 10):
                break
            