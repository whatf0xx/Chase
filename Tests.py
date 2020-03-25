# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 22:38:14 2020

@author: whatf

Early tests for these classes
"""

import Runners as r

world1 = r.World(start=
                 [[0, 0], #runner start
                 [1, 0], #runner starting velocity
                 [-1, 1], #chaser start
                 [-0.8, -0.6]]) #chaser starting velocity
world1.create()