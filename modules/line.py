# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Created on Jun  18 18:18:18 2020

@author: Mark A Post
@editted: Rebecca M Wardle
"""


# from math import pi, cos
from Modules.builder.robots.cubemodule import CubeModule
from morse.builder import *

# Create Modules
NumModules = 16
Modules = []
# ModuelColours = [[cos(x*2*pi/NumModules), cos(x*2*pi/NumModules-2*pi/3), cos(x*2*pi/NumModules-4*pi/3), 1.0] for x in range(NumModules)]
ModuelColours = [[(1/NumModules)*x, 0.0, 1-(1/NumModules)*x, 1.0] for x in range(NumModules)]
# Make a set of enumerated module robots
for num in range(NumModules):
    ModuleName = 'mod' + "{:03d}".format(num) + "_MOT"
    # Create module
    Modules.append(CubeModule(ModuleName, ModuelColours[num % len(ModuelColours)]))
    Modules[-1].translate(y=1+num*0.1, z=1.0)

# Create some graspable objects
tape2 = PassiveObject(prefix='WhiteVideotape')
tape2.properties(Object=True, Graspable=True, Label="WhiteTape")
tape2.translate(x=3, y=-3, z=0)


# Set environment
env = Environment('indoors-1/indoor-1', fastmode=False)
env.add_service('socket')
env.set_gravity(0.0)
