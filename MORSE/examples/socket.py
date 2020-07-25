#! /usr/bin/env morseexec
from morse.builder import *

atrv = ATRV()

motion = MotionVW()
motion.translate(z=0.3)
atrv.append(motion)

pose = Pose()
pose.translate(z=0.83)
atrv.append(pose)

pose.add_stream("socket")
pose.add_service("socket")
motion.add_service("socket")

env = Environment("indoors-1/indoor-1")
env.set_camera_location([5, -5, 6])
env.set_camera_rotation([1.0470, 0, 0.7854])
