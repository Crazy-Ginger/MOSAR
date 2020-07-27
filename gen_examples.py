#!/usr/bin/env python3
from spacecraft import Spacecraft


def main():
    """main call function"""
    craft = Spacecraft()
    goal = Spacecraft()
    craft.add_module("MOS1_MOT")
    craft.add_module("MOS2_MOT")
    craft.add_module("MOS3_REC")
    craft.add_module("MOS4_REC")
    craft.add_module("MOS5_TAN")
    craft.add_module("MOS6_SOL")
    craft.add_module("MOS7_RAD")

    goal.add_module("MOS1_MOT")
    goal.add_module("MOS2_MOT")
    goal.add_module("MOS3_REC")
    goal.add_module("MOS4_REC")
    goal.add_module("MOS5_TAN")
    goal.add_module("MOS6_SOL")
    goal.add_module("MOS7_RAD")

    craft.connect("MOS1_MOT", 2, "MOS2_MOT", 0)
    craft.connect("MOS2_MOT", 1, "MOS3_REC", 3)
    craft.connect("MOS2_MOT", 2, "MOS4_REC", 0)
    craft.connect("MOS4_REC", 1, "MOS5_TAN", 3)
    craft.connect("MOS3_REC", 2, "MOS5_TAN", 0)
    craft.connect("MOS5_TAN", 1, "MOS6_SOL", 3)
    craft.connect("MOS2_MOT", 3, "MOS7_RAD", 1)

    goal.connect("MOS1_MOT", 2, "MOS2_MOT", 0)
    goal.connect("MOS2_MOT", 2, "MOS3_REC", 0)
    goal.connect("MOS1_MOT", 1, "MOS4_REC", 3)
    goal.connect("MOS4_REC", 2, "MOS5_TAN", 0)
    goal.connect("MOS5_TAN", 2, "MOS6_SOL", 0)
    goal.connect("MOS5_TAN", 1, "MOS7_RAD", 3)
    goal.connect("MOS2_MOT", 1, "MOS5_TAN", 3)
    goal.connect("MOS3_REC", 1, "MOS6_SOL", 3)

    craft.goal = goal
    craft.export_to_file("test")
    craft.goal.export_to_file("goal")
    # order = craft.melt()
    craft.display()
    craft.goal.display()
    # craft.sort(order)


if __name__ == "__main__":
    main()
