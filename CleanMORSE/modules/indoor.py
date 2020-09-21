#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun  18 18:18:18 2020

@author: Mark A Post
"""


from math import cos, pi

from morse.builder import *
# from modules.builder.robots.cubemodule import CubeModule
from src.modules.builder.robots.cubemodule import CubeModule

# Create Modules
numModules = 16
modules = []
moduleColours = [[cos(x*2*pi/numModules), cos(x*2*pi/numModules-2*pi/3), cos(x*2*pi/numModules-4*pi/3), 1.0] for x in range(numModules)]
print(moduleColours)
# Make a set of enumerated module robots
for num in range(numModules):
    moduleName = 'mod'+"{:03d}".format(num)  # + "_MOT"
    print(moduleName)
    # Create module
    print(moduleColours[num % len(moduleColours)])
    modules.append(CubeModule(moduleName, moduleColours[num % len(moduleColours)]))
    modules[-1].translate(x = 1+num*0.1, z = 0.1)

# Create a mobile robot with arm and gripper
vehicle = ATRV('vehicle')
pose = Pose()
vehicle.append(pose)
pose.add_stream('socket')
vehicle.add_service('socket')
arm = KukaLWR()
vehicle.append(arm)
arm.translate(x=0.0, z=0.74)
arm.add_service('socket')
gripper = Gripper('gripper')
gripper.translate(z=1.28)
arm.append(gripper)
gripper.properties(Angle = 180.0, Distance=2.0)
gripper.add_service('socket')

# Create some graspable objects
tape1 = PassiveObject(prefix='BlackVideotape')
tape1.properties(Object = True, Graspable = True, Label = "BlackTape")
tape1.translate(x=3, y=3, z=0)
tape2 = PassiveObject(prefix='WhiteVideotape')
tape2.properties(Object = True, Graspable = True, Label = "WhiteTape")
tape2.translate(x=3, y=-3, z=0)

#Keyboard (arrow keys) control of vehicle (or module)
keyb = Keyboard()
keyb.properties(Speed=2.0)
vehicle.append(keyb)
#Note that you can use keyboard control on modules
#'keyb' only controls the last robot it is appended to
#modules[-1].append(keyb)

#Set environment
env = Environment('indoors-1/indoor-1', fastmode=False)
env.add_service('socket')
env.set_gravity(9.81)
