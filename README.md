# MOSAR Automated Reconfiguration
This is a program that rearranges cuboid robots using the Melt, Sort, Grow algorithm laid out in: [Planning for Heterogeneous Self-Reconfiguring Robots](http://groups.csail.mit.edu/drl/publications/papers/MeltSortGrow.pdf). It is written exclusively in python and uses the MORSE simulator to demonstrate.

Requirements:
------------

- [Morse Simulator](https://github.com/morse-simulator/morse)
- [Blender v2.79](https://www.blender.org/download/releases/2-79)>=
- [Python 3.5](https://www.python.org/downloads/release/python-350/) or the same python version used to build blender
- Linux OS

These requirements are based around the requirements of MORSE.

Installation:
-------------

This guide assumes that you have MORSE setup with blender 2.79.
To install the cube modules:

    morse import modules

Then to etablish the simulation

    morse run modules line.py

To run the self-configuration run

    python3.5 main.py

---------

Modules can be designated with different colours and types.
The modules are then loaded into [`spacecraft`] class which stores connections, position, rotation, type and more. This class can be passed a goal structure and will rearrange the modules to this structure.
