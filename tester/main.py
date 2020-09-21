#!/usr/bin/env python3
from testcraft import Module, Spacecraft


def main():
    """main call function"""
    craft = Spacecraft()
    craft = craft.import_from_file("test.json", goal=False)
    order = craft.melt("MOS1_MOT")
    # craft.display()
    order = craft.sort(order)
    # craft.goal.display()
    craft.grow(order)
    # craft.display()


if __name__ == "__main__":
    main()
