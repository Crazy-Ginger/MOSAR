#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun  18 18:18:18 2020

@author: Mark A Post
"""


# from math import pi

from morse.builder import *

# Create Modules
modules = []
num_mod = 16
# Make a set of enumerated module robots
for num in range(num_mod):
    mod_id = 'mod'+"{:03d}".format(num) + "_MOT"

    # Create module
    modules.append(CubeModule(mod_id))
    modules[-1].translate(x=0.1, y=0.1*num, z=1.0)

    # Add a position sensor
    position = Pose()
    modules[-1].append(position)
    position.add_stream('socket')

    # Add a holonomic movement actuator
    destination = Destination()
    modules[-1].append(destination)
    destination.add_stream('socket')
    destination.properties(Speed=1.0, Tolerance=0.1, RemainAtDestination=True)
    # Add a socket interface to read properties
    modules[-1].add_service('socket')

# Create a mobile robot with arm and gripper
# vehicle = ATRV('vehicle')
# position = Pose()
# vehicle.append(position)
# position.add_stream('socket')
# vehicle.add_service('socket')
# arm = KukaLWR()
# vehicle.append(arm)
# arm.translate(x=0.0, z=0.74)
# arm.add_service('socket')
# gripper = Gripper('gripper')
# gripper.translate(z=1.28)
# arm.append(gripper)
# gripper.properties(Angle = 180.0, Distance=2.0)
# gripper.add_service('socket')

# Create some graspable objects
tape1 = PassiveObject(prefix='BlackVideotape')
tape1.properties(Object = True, Graspable = True, Label = "BlackTape")
tape1.translate(x=3, y=3, z=0)
tape2 = PassiveObject(prefix='WhiteVideotape')
tape2.properties(Object = True, Graspable = True, Label = "WhiteTape")
tape2.translate(x=3, y=-3, z=0)

# Keyboard (arrow keys) control of vehicle (or module)
# keyb = Keyboard()
# keyb.properties(Speed=2.0)
# vehicle.append(keyb)
# Note that you can use keyboard control on modules
# 'keyb' only controls the last robot it is appended to
# modules[-1].append(keyb)

# Set environment
env = Environment('indoors-1/indoor-1', fastmode=False)
env.add_service('socket')
env.set_gravity(0.0)
