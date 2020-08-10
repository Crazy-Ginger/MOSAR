#!/usr/bin/env python3
from morsecraft import Spacecraft as Craft
import pymorse

morse = pymorse.Morse()


def main():
    """main call function"""
    craft = Craft(dimensions=3)
    print(dir(morse))
    mod_ids = [mod_id for mod_id in dir(morse) if mod_id[:3] == 'mod' and mod_id[3:6].isnumeric() and mod_id[7:].isalpha()]
    print(mod_ids)
    for mod_id in mod_ids:
        craft.add_module(mod_id)


if __name__ == "__main__":
    main()
