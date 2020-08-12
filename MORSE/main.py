#!/usr/bin/env python3
import pymorse
from morsecraft import Spacecraft as Craft

morse = pymorse.Morse()


def main():
    """main call function"""
    craft = Craft(dimensions=3)
    # print(dir(morse))
    mod_ids = [mod_id for mod_id in dir(morse) if mod_id[:3] == 'mod' and mod_id[3:6].isnumeric() and mod_id[7:].isalpha()]
    print(mod_ids)
    for mod_id in mod_ids:
        craft.add_module(mod_id)

    prev_mod = None
    for mod in craft.modules:
        if prev_mod:
            craft.connect(prev_mod, 0, mod, 2)
            prev_mod = mod


if __name__ == "__main__":
    main()
