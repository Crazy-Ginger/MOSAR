#! /usr/bin/env python3
"""
Test client for the <modules> simulation environment.

This simple program shows how to control a robot from Python.

For real applications, you may want to rely on a full middleware,
like ROS (www.ros.org).
"""

import sys

try:
    from pymorse import Morse
except ImportError:
    print("you need first to install pymorse, the Python bindings for MORSE!")
    sys.exit(1)


def getpose(moduleobject):
    pose = moduleobject.pose.get()
    print(pose)


def setdest(moduleobject, x=0.0, y=0.0, z=0.0):
    destclient = moduleobject.destination
    destclient.publish({'x': x, 'y': y, 'z': z})


def main():
    with Morse() as morse:
        motion = morse.mod001_MOT.motion
        pose = morse.mod001_MOT.pose

        v = 0.0
        w = 0.0

        # populates list of module ids
        moduleNames = [
            mod_id for mod_id in dir(morse) if mod_id[:3] == 'mod'
            and mod_id[3:6].isnumeric() and mod_id[7:].isalpha()
        ]

        # moves modules from one chain to another
        num = 0
        for moduleName in moduleNames:
            moduleObject = getattr(morse, moduleName)
            setdest(moduleObject, x=1.0, y=1.0, z=2.0 - num*0.1)
            num += 1
            getpose(moduleObject)
        num = 0

        for moduleName in moduleNames:
            moduleObject = getattr(morse, moduleName)
            setdest(moduleObject, x=1.0 + num*0.1, y=0.0, z=2.0)
            num += 1
            getpose(moduleObject)

        # gets input from the user and uses ot to set motion of mod1
        while True:
            key = input("WASD?")

            if key.lower() == "w":
                v += 0.1
            elif key.lower() == "s":
                v -= 0.1
            elif key.lower() == "a":
                w += 0.1
            elif key.lower() == "d":
                w -= 0.1
            else:
                continue

            # here, we call 'get' on the pose sensor: this is a blocking
            # call. Check pymorse documentation for alternatives, including
            # asynchronous stream subscription.
            print("The robot is currently at: %s" % pose.get())

            v = 0.0
            w = 0.0
            motion.publish({"v": v, "w": w})
            # morse.vehicle.arm.set_rotation("kuka_2", math.radians(-30)).result()


if __name__ == "__main__":
    print("Use WASD to control the robot")
    main()
