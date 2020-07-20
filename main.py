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
    craft.connect("MOS2", 1, "MOS3", 3)
    craft.connect("MOS2", 2, "MOS4", 0)
    craft.connect("MOS4", 1, "MOS5", 3)
    craft.connect("MOS5", 1, "MOS6", 3)
    craft.connect("MOS7", 1, "MOS2", 3)
    craft.connect("MOS3", 2, "MOS5", 0)

    craft.display()


if __name__ == "__main__":
    main()
