#!/usr/local/bin/python3.5

# import math
import time

import pymorse

num_mod = 16

# morse = pymorse.Morse()
# morse.vehicle.arm.set_rotation("kuka_2", math.radians(-30)).result()


def get_pose(mod_id):
    module = getattr(morse, mod_id)
    pose = module.position.get()
    print(pose)


def set_dest(mod_id, x=0.0, y=0.0, z=0.0):
    module = getattr(morse, mod_id)
    destclient = module.destination
    destclient.publish({'x': x, 'y': y, 'z': z})


def main():
    mod_ids = [mod_id for mod_id in dir(morse) if mod_id[:3] == 'mod' and mod_id[3:].isnumeric()]
    num = 0
    for mod_id in mod_ids:
        set_dest(mod_id, x=1.0, y=1.0, z=2.0 - num*0.1)
        num += 1
        time.sleep(1)
        get_pose(mod_id)
    num = 0
    for mod_id in mod_ids:
        set_dest(mod_id, x=1.0 + num*0.1, y=0.0, z=2.0)
        num += 1
        time.sleep(1)
        get_pose(mod_id)


if __name__ == "__main__":
    main()
