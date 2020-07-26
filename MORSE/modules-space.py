#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun  18 18:18:18 2020

@author: Mark A Post
"""

numModules = 16

from morse.builder import *
from math import pi
# import CubeModule

# Create Modules
modules = []
# Make a set of enumerated module robots
for num in range (numModules):
    moduleName = 'mod'+"{:03d}".format(num)
    # Create module
    modules.append(CubeModule(moduleName))
    modules[-1].translate(x = 1+num*0.1, z = 0.1)
    # Add a position sensor
    position = Pose()
    modules[-1].append(position)
    position.add_stream('socket')
    # Add a holonomic movement actuator
    destination = Destination()
    modules[-1].append(destination)
    destination.add_stream('socket')
    destination.properties(Speed=1.0, Tolerance=0.1, RemainAtDestination = True)
    # Add a socket interface to read properties
    modules[-1].add_service('socket')
    # modules[-1].make_ghost(alpha=1.0) #doesn't work with actuator

# Keyboard (arrow keys) control of vehicle (or module)
keyb = Keyboard()
keyb.properties(Speed=2.0)
modules[-1].append(keyb)

# Set environment
env = Environment('empty', fastmode=False)
env.add_service('socket')
env.set_gravity(0.0)
