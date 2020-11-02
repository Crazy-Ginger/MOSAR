#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun  18 18:18:18 2020

@author: Mark A Post
"""

numModules = 16

from morse.builder import *
from modules.builder.robots.cubemodule import CubeModule

#Create Modules
modules = []
moduleColours = moduleColours = [[1.0,1.0,1.0,1.0],[1.0,0.0,0.0,1.0],[1.0,1.0,0.0,1.0],[0.0,1.0,0.0,1.0],[0.0,1.0,1.0,1.0],[0.0,0.0,1.0,1.0],[1.0,0.0,1.0,1.0]]
#Make a set of enumerated module robots
for num in range (numModules):
	moduleName = 'mod'+"{:03d}".format(num)
	#Create module
	modules.append(CubeModule(moduleName, moduleColours[num % len(moduleColours)]))
	modules[-1].translate(x = 1+num*0.1, z = 0.1)

#Keyboard (arrow keys) control of vehicle (or module)
keyb = Keyboard()
keyb.properties(Speed=2.0)
modules[-1].append(keyb)

#Set environment
env = Environment('empty', fastmode=False)
env.add_service('socket')
env.set_gravity(0.0)
env.set_ambient_color((1.0, 1.0, 1.0))
