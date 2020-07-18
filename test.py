#!/usr/bin/env python3
""" shut up error"""
import networkx as nx
from matplotlib import pyplot as plt

class Spacecraft:
    """A generic spacecraft class that contains a dictionary of modules and connections"""
    def __init__(self, dimensions=2):
        self.modules = {}
        self._dimensions_ = dimensions
        self.root = None
        self.connections = []

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
                raise ValueError("The port %d on module A is already in use" %(mod_a_port))
            if self.modules[mod_b][mod_b_port] is not None:
                raise ValueError("The port %d on module B is already in use" %(mod_b_port))
        except IndexError:
            raise IndexError("That port number does not exist in this dimension")

        self.modules[mod_a][mod_a_port] = mod_b
        self.modules[mod_b][mod_b_port] = mod_a
        self.connections.append((mod_a, mod_b))

    def get_graph(self):
        """returns a graph with nodes and edges"""
        graph = nx.Graph()
        graph.add_nodes_from(self.modules.keys())
        if len(self.connections) != 0:
            graph.add_edges_from(self.connections)
        return graph

    def get_connections(self):
        """outputs all the connections between all the moduels"""
        output = ""
        for key in self.modules:
            output += key
            output += str(self.modules[key]) + "\n"
        print(output)


CRAFT = Spacecraft()
CRAFT.add_module("MOS1")
CRAFT.add_module("MOS2")
CRAFT.add_module("MOS3")
CRAFT.connect("MOS1", 1, "MOS2", 2)
CRAFT.connect("MOS2", 3, "MOS3", 0)
GRAPH = CRAFT.get_graph()
print(CRAFT.root)
nx.draw(GRAPH, with_labels=True)
plt.show()
