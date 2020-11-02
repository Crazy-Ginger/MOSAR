# MOSAR
This is a program that rearranges cuboid robots using the Melt, Sort, Grow algorithm laid out in: [Planning for Heterogeneous Self-Reconfiguring Robots](http://groups.csail.mit.edu/drl/publications/papers/MeltSortGrow.pdf">Reconfiguration). It is written exclusively in python and uses the MORSE simulator to demonstrate the algorithm.

Requirements:
------------

- [Morse Simulator](https://github.com/morse-simulator/morse)
- [Blender v2.79](https://www.blender.org/download/releases/2-79)>=
- [Python 3.5](https://www.python.org/downloads/release/python-350/) or the same python version used to build blender
- Linux based OS as MORSE has not been written to run on Windows

Installation:
-------------

This guide assumes that you have blender 2.79 installed and running as well as a properly configured MORSE setup. This can be difficult as even the MORSE page doens't mention that blender 2.79 is required as from version 2.80 they removed the game engine that MORSE uses to function.

To install the cube modules:

    morse import modules

Then to etablish the simulation

    morse run modules indoor.py


---------

Modules can be designated with different colours and types.
The modules are then loaded into [`spacecraft`] class which stores connections, position, rotation, type and more. This class can be passed a goal structure and will rearrange the modules to this structure.
