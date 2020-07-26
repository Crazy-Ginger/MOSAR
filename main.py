#!/usr/bin/env python3
import spacecraft


def main():
    """main call function"""
    craft = spacecraft.Spacecraft()
    craft.add_module("MOS1")
    craft.add_module("MOS2")
    craft.add_module("MOS3")
    craft.add_module("MOS4")
    craft.add_module("MOS5")
    craft.add_module("MOS6")
    craft.add_module("MOS7")

    craft.connect("MOS1", 2, "MOS2", 0)
    craft.connect("MOS2", 2, "MOS3", 0)
    craft.connect("MOS1", 1, "MOS4", 3)
    craft.connect("MOS4", 2, "MOS5", 0)
    craft.connect("MOS5", 2, "MOS6", 0)
    craft.connect("MOS5", 1, "MOS7", 3)
    craft.connect("MOS2", 1, "MOS5", 3)
    craft.connect("MOS3", 1, "MOS6", 3)

    # craft.export_to_file("goal")
    craft.goal = craft
    print(craft._get_goal_order())
    # craft = spacecraft.Spacecraft()
    # craft = craft.import_from_file("test.json", False)


if __name__ == "__main__":
    main()
