#! /usr/bin/env morseexec

from morse.builder import *

# Add the MORSE mascott, MORSY.
robot = Morsy()
arm = PA10()
robo = Morsy()

# The list of the main methods to manipulate your components
robot.translate(1.0, 0.0, 0.0)
robot.rotate(0.0, 0.0, 3.5)

robo.translate(1.0, 1.0, 0.0)
robo.rotate(0.0, 0.0, 3.5)

# Add a motion controller
motion = MotionVW()
robot.append(motion)
robo.append(motion)

# arm.translate(0, 0, 0)
# arm.rotate(0,0,0)

# Add a keyboard controller to move the robot with arrow keys.
keyboard = Keyboard()
robot.append(keyboard)
robo.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Add a pose sensor that exports the current location and orientation
# of the robot in the world frame
pose = Pose()
robot.append(pose)
robo.append(pose)

robot.append(arm)

# To ease development and debugging, we add a socket interface to our robot.
robot.add_default_interface('socket')
robo.add_default_interface("socket")

# set 'fastmode' to True to switch to wireframe mode
env = Environment('sandbox', fastmode = False)
env.set_camera_location([-18.0, -6.7, 10.8])
env.set_camera_rotation([1.09, 0, -1.14])

