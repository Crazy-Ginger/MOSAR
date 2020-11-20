#!/usr/bin/env python3.5
from subprocess import DEVNULL, Popen
from time import sleep

import pymorse
from modules.morsecraft import Spacecraft as Craft
from modules.scripts import modControl

__authors__ = ["Mark A Post", "Rebecca Wardle"]
__copyright__ = "Copyright 2020 Rebecca Wardle"
__license__ = "MIT License"
__credit__ = ["Mark A Post", "Rebecca Wardle"]
__version__ = "0.5"
"""Manipulates the modules in morse to a new structure, rewrite to change order"""

# launches the simulation
# SIMULATION = Popen(["morse", "run", "modules-indoor.py"], stdout=DEVNULL)
morse = None

while morse is None:
    try:
        morse = pymorse.Morse()
    except ConnectionRefusedError:
        sleep(0.5)


def write(craft, mod_ids, filename="output.txt"):
    print("adding to file")
    file = open(filename, "w")

    for mod_id in mod_ids:
        file.write(str(craft.modules[mod_id].pos) + "\n")
    print("written")


def main():
    """main call function"""
    craft = Craft(tag_length=3, precision=0.05)
    craft.create_goal()

    mod_ids = [
        mod_id for mod_id in dir(morse) if mod_id[:3] == 'mod'
        and mod_id[3:6].isnumeric() and mod_id[7:].isalpha()
    ]
    print(mod_ids)

    for mod_id in mod_ids:
        position = modControl.getPose(mod_id)
        position = [position["x"]] + [position["y"]] + [position["z"]]
        craft.add_mod(mod_id, position)
        craft.goal.add_mod(mod_id, position)
        # print(mod_id, ":", craft.modules[mod_id].pos)
    print("Added modules to craft")

    for indx in range(1, len(mod_ids)):
        if indx % 4 == 0:
            craft.goal.connect(mod_ids[indx], 3, mod_ids[int(indx / 4) - 1], 1)
        else:
            craft.goal.connect(mod_ids[indx - 1], 2, mod_ids[indx], 0)

    print("built goal structure")

    for mod in mod_ids:
        craft.connect_all(mod)
    print("connected chain")

    print("sorting")
    craft.sort(mod_ids)
    print("sorted")


if __name__ == "__main__":
    main()
