#!/usr/bin/env python3
""" shut up error"""
import networkx as nx

class Spacecraft:
    """A generic spacecraft class that contains a dictionary of modules and connections"""
    def __init__(self, dimensions=2):
        self.modules = {}
        self._dimensions_ = dimensions
        self.root = None

    def add_module(self, new_id):
        """Add an unconnected module to the craft dictionary"""
        self.modules[str(new_id)] = [None]*(self._dimensions_*2)
        if self.root is None:
            self.root = str(new_id)

    def add_connected_module(self, a_id, b_id, a_port, b_port):
        """Adds a module that is connected and modifies the existing module to connect it"""
        if self.root is None:
            raise KeyError("There are no existing modules to connect to")

        self.modules[str(a_id)] = [None]*(self._dimensions_*2)
        self.connect(a_id, b_id, a_port, b_port)

    def connect(self, mod_a, mod_a_port, mod_b, mod_b_port):
        """Connects the 2 passed moduleswith the specified ports"""
        mod_a = str(mod_a)
        mod_b = str(mod_b)
        mod_a_port = int(mod_a_port)
        mod_b_port = int(mod_b_port)
        try:
            if self.modules[mod_a][mod_a_port] is not None:
                raise ValueError("The port on module A is already in use")
            if self.modules[mod_b][mod_b_port] is not None:
                raise ValueError("The port on module B is already in use")
        except IndexError:
            raise IndexError("That port number does not exist in this dimension")

        self.modules[mod_a][mod_a_port] = mod_b
        self.modules[mod_b][mod_b_port] = mod_a

    def get_nodes(self):
        """returns keys of modules as list"""
        return list(self.modules.keys())


CRAFT = Spacecraft()
CRAFT.add_module("MOS1")
CRAFT.add_module("MOS2")
CRAFT.add_module("MOS3")
GRAPH = nx.Graph()
GRAPH.add_nodes_from(CRAFT.get_nodes())
print(GRAPH.nodes())
print(GRAPH.edges())
