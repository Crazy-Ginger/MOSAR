# MOSAR
This is a program that rearranges cuboid robots using the Melt, Sort, Grow algorithm laid out in: <a href="http://groups.csail.mit.edu/drl/publications/papers/MeltSortGrow.pdf">Reconfiguration Planning for Heterogeneous Self-Reconfiguring Robots</a> . It is written exclusively in python and uses the MORSE simulator to demonstrate the algorithm.
<h2>Requirements:</h2>
<ul>
    <li><a href="https://github.com/morse-simulator/morse">morse simulator</a></li>
    <li><a href="https://www.blender.org/download/releases/2-79">blender 2.79</a>>=</li>
    <li><a href="https://www.python.org/downloads/release/python-350/">python3.5</a> (or version used to build blender)</li>
</ul>
<br/>
<h2>Installation:</h2>
This guide assumes that you have blender 2.79 installed and running as well as a properly configured MORSE setup. This can be difficult as even the MORSE page doens't mention that blender 2.79 is required as from version 2.80 they removed the game engine that MORSE uses to function.
To install the cube modules:
```bash
morse import modules
```
Then to run the simulation
```bash
morse run modules indoor.py
```
