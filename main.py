#!/usr/bin/env python3
from spacecraft import Spacecraft


def main():
    """main call function"""
    craft = Spacecraft()
    craft = craft.import_from_file("test.json", goal=False)
    craft.display()
    # craft.goal.display()
    order = craft.melt("MOS1_MOT")
    craft.display()
    craft.sort(order)
    craft.display()


if __name__ == "__main__":
    main()
