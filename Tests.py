# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 22:38:14 2020

@author: whatf

Early tests for these classes
"""

import Runners as r

#%%
world1 = r.World(start=
                 [[4, 3], #runner start
                 [0, 0], #runner starting velocity
                 [-1, -1.5], #chaser start
                 [0, 0]]) #chaser starting velocity
world1.create()

#%% works, /0 runtime error but who cares
"""
c = r.Chaser([1, 1], [0, 0])
s = r.Scaper([0, 0], [0, -1])

s.isotropic_lines(c, 3)
"""