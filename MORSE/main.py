#!/usr/bin/env python3.5
import pymorse
from morsecraft import Spacecraft as Craft

morse = pymorse.Morse()


def main():
    """main call function"""
    craft = Craft(tag_length=3, precision=0.01)
    craft.create_goal()
    # print(dir(morse))
    mod_ids = [mod_id for mod_id in dir(morse) if mod_id[:3] == 'mod' and mod_id[3:6].isnumeric() and mod_id[7:].isalpha()]
    print(mod_ids)
    for mod_id in mod_ids:
        craft.add_mod(mod_id)
        craft.goal.add_mod(mod_id)

    for indx in range(1, len(mod_ids)):
        if indx % 4 == 0:
            craft.goal.connect(mod_ids[indx], 3, mod_ids[indx/4-1], 1)
        else:
            craft.goal.connect(mod_ids[indx-1], 2, mod_ids[indx], 0)

    prev_mod = None
    for mod in craft.modules:
        if prev_mod:
            craft.connect(prev_mod, 0, mod, 2)
            prev_mod = mod


if __name__ == "__main__":
    main()
