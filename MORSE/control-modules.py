#!/usr/local/bin/python3.5

import time
import math
import pymorse

numModules = 16

morse = pymorse.Morse()
# morse.vehicle.arm.set_rotation("kuka_2", math.radians(-30)).result()


def getPose(moduleName):
    moduleObject = getattr(morse, moduleName)
    pose = moduleObject.position.get()
    print(pose)


def setDest(moduleName, x=0.0, y=0.0, z=0.0):
    moduleObject = getattr(morse, moduleName)
    destClient = moduleObject.destination
    destClient.publish({'x': x, 'y': y, 'z': z})


def main():
    moduleNames = [moduleName for moduleName in dir(morse) if moduleName[:3] == 'mod' and moduleName[3:].isnumeric()]
    num = 0
    for moduleName in moduleNames:
        setDest(moduleName, x = 1.0, y = 1.0, z = 2.0 - num*0.1)
        num += 1
        time.sleep(1)
        getPose(moduleName)
    num = 0
    for moduleName in moduleNames:
        setDest(moduleName, x=1.0 + num*0.1, y=0.0, z=2.0)
        num += 1
        time.sleep(1)
        getPose(moduleName)


if __name__ == "__main__":
    main()
