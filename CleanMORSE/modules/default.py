#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <modules> environment

Feel free to edit this template as you like!
"""

from modules.builder.robots.cubemodule import CubeModule
from morse.builder import *

# Out-the-box available robots are listed here:
# http://www.openrobots.org/morse/doc/stable/components_library.html
#
# 'morse add robot <name> modules' can help you to build custom robots.
robot = CubeModule('mod000')
mod1 = CubeModule('mod001')
mod2 = CubeModule('mod002')

# The list of the main methods to manipulate your components
# is here: http://www.openrobots.org/morse/doc/stable/user/builder_overview.html
robot.translate(0.0, 0.0, 0.0)
robot.rotate(0.0, 0.0, 3.5)
robot.translate(0.1, 0.0, 0.0)
robot.translate(0.2, 0.0, 0.0)

# Add a motion controller
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
#
# 'morse add actuator <name> modules' can help you with the creation of a custom
# actuator.
# motion = MotionVW()
# robot.append(motion)


# Add a keyboard controller to move the robot with arrow keys.
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Add a pose sensor that exports the current location and orientation
# of the robot in the world frame
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#sensors
#
# 'morse add sensor <name> modules' can help you with the creation of a custom
# sensor.
# pose = Pose()
# robot.append(pose)

# To ease development and debugging, we add a socket interface to our robot.
#
# Check here: http://www.openrobots.org/morse/doc/stable/user/integration.html
# the other available interfaces (like ROS, YARP...)
robot.add_default_interface('socket')
robot.add_service('socket')
mod1.add_service('socket')
mod2.add_service('socket')

# set 'fastmode' to True to switch to wireframe mode
env = Environment('sandbox', fastmode = False)
env.set_camera_location([-18.0, -6.7, 10.8])
env.set_camera_rotation([1.09, 0, -1.14])
