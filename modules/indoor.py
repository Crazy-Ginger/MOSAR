# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Created on Jun  18 18:18:18 2020

@author: Mark A Post
@editted: Rebecca M Wardle
"""


from morse.builder import *
# from math import pi, cos
from modules.builder.robots.cubemodule import CubeModule

# Create Modules
numModules = 16
modules = []
# moduleColours = [[cos(x*2*pi/numModules), cos(x*2*pi/numModules-2*pi/3), cos(x*2*pi/numModules-4*pi/3), 1.0] for x in range(numModules)]
moduleColours = [[(1/numModules)*x, 0.0, 1-(1/numModules)*x, 1.0] for x in range(numModules)]
# Make a set of enumerated module robots
for num in range(numModules):
	moduleName = 'mod'+"{:03d}".format(num) +"_MOT"
	# Create module
	modules.append(CubeModule(moduleName, moduleColours[num % len(moduleColours)]))
	modules[-1].translate(y = 1+num*0.1, z = 1.0)

# Create some graspable objects
tape2 = PassiveObject(prefix='WhiteVideotape')
tape2.properties(Object = True, Graspable = True, Label = "WhiteTape")
tape2.translate(x=3, y=-3, z=0)


# Set environment
env = Environment('indoors-1/indoor-1', fastmode=False)
env.add_service('socket')
env.set_gravity(0.0)
