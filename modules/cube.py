# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Created on Sep  20 21:13:10 2020

@author: Mark A Post
@editted: Rebecca M Wardle
"""


from modules.builder.robots.cubemodule import CubeModule
from morse.builder import *

# Create Modules
NumModules = 16
modules = []
ModuleColours = [[(1/NumModules)*x, 0.0, 1-(1/NumModules)*x, 1.0] for x in range(NumModules)]
# Make a set of enumerated module robots
for i in range(NumModules):
    ModuleName = 'mod' + "{:03d}".format(i) + "_MOT"
    modules.append(CubeModule(name=ModuleName, colour=ModuleColours[i % len(ModuleColours)]))
    modules[-1].translate(x=1+(i % 4)*0.1, y=1+(i//4)*0.1, z=1.0)


# Create some graspable objects
tape2 = PassiveObject(prefix='WhiteVideotape')
tape2.properties(Object = True, Graspable = True, Label = "WhiteTape")
tape2.translate(x=3, y=-3, z=0)


# Set environment
env = Environment('indoors-1/indoor-1', fastmode=False)
env.add_service('socket')
env.set_gravity(0.0)
