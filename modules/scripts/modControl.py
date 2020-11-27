#!/usr/local/bin/python3.5

import time

import pymorse

morse = pymorse.Morse()


def getPose(mod_id):
    moduleObject = getattr(morse, mod_id)
    pose = moduleObject.pose.get()

    return pose
    # print(pose)


def setDest(mod_id, x=0.0, y=0.0, z=0.0):
    moduleObject = getattr(morse, mod_id)
    destClient = moduleObject.destination
    destClient.publish({'x' : x, 'y' : y, 'z' : z})

def link(mod_a, mod_b):
    morse.rpc(mod_a, 'link', True, mod_b)

def unlink(mod_a, mod_b):
    morse.rpc(mod_a, 'link', False, mod_b)


def main():
    moduleNames = [
        mod_id for mod_id in dir(morse) if mod_id[:3] == 'mod'
        and mod_id[3:6].isnumeric() and mod_id[7:].isalpha()
    ]

    # rearranges modules along y axis

    for num in range(len(moduleNames)):
        moduleName = moduleNames[num]
        lastModuleName = moduleNames[num-1] if num-1 >= 0 else None
        setDest(moduleName, x = 2, y = 3.0 - num*0.1, z = 1)
        time.sleep(2)
        getPose(moduleName)

        if lastModuleName is not None:
            morse.rpc(moduleName, 'link', True, lastModuleName)
            #morse.rpc(moduleName, 'colour', [1.0, 1.0, 1.0, 1.0])
            #morse.rpc(lastModuleName+'.destination', 'set_property', 'RemainAtDestination', False)

    # moduleNames.reverse() #currently need to disconnect children before parent

    for num in range(len(moduleNames)):
        moduleName = moduleNames[num]
        lastModuleName = moduleNames[num+1] if num+1 < len(moduleNames) else None

        if lastModuleName is not None:
            morse.rpc(moduleName, 'link', False, lastModuleName)
        setDest(moduleName, x = 2, y = 3.0 - num*0.1, z = 0.1)
        time.sleep(2)
        getPose(moduleName)
        lastModuleName = moduleNames[num-1] if num-1 >= 0 else None

        if lastModuleName is not None:
            morse.rpc(moduleName, 'link', True, lastModuleName)
            #morse.rpc(moduleName, 'colour', [1.0, 1.0, 1.0, 1.0])
            #morse.rpc(lastModuleName+'.destination', 'set_property', 'RemainAtDestination', False)

if __name__ == "__main__":
	main()
