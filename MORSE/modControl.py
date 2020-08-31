#!/usr/local/bin/python3.5
import time

import pymorse

num_mod = 16

# morse.vehicle.arm.set_rotation("kuka_2", math.radians(-30)).result()

morse = pymorse.Morse()

def get_pose(mod_id):
    # morse = pymorse.Morse()
    module = getattr(morse, mod_id)
    pose = module.position.get()
    return pose


def set_dest(mod_id, x=0.0, y=0.0, z=0.0):
    # morse = pymorse.Morse()
    module = getattr(morse, mod_id)
    destclient = module.destination
    destclient.publish({'x': x, 'y': y, 'z': z})


def main():
    mod_ids = [mod_id for mod_id in dir(morse) if mod_id[:3] == 'mod']
    print(mod_ids)
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
