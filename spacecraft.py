#!/usr/bin/env python3
""" shut up error"""
import operator as op
import networkx as nx
from matplotlib import pyplot as plt

class Spacecraft:
    """A generic spacecraft class that contains a dictionary of modules and connections"""
    def __init__(self, dimensions=2):
        self.modules = {}
        self._dimensions = dimensions
        self.root = None
        self.connections = []
        self.positions = {}

    def add_module(self, new_id):
        """Add an unconnected module to the craft dictionary"""
        self.modules[str(new_id)] = [None]*(self._dimensions*2)
        if self.root is None:
            self.root = str(new_id)
            self.positions[str(new_id)] = (0, 0)

    def add_connected_module(self, a_id, b_id, a_port, b_port):
        """Adds a module that is connected and modifies the existing module to connect it"""
        if self.root is None:
            raise KeyError("There are no existing modules to connect to")

        self.modules[str(a_id)] = [None]*(self._dimensions*2)
        self.connect(a_id, b_id, a_port, b_port)

    def connect(self, mod_a, mod_a_port, mod_b, mod_b_port):
        """Connects the 2 passed moduleswith the specified ports
        as orientation is going to be considered in future code it takes both ports"""
        mod_a = str(mod_a)
        mod_b = str(mod_b)
        mod_a_port = int(mod_a_port)
        mod_b_port = int(mod_b_port)

        # as orienttation is not yet supported checks that modules are all aligned
        if mod_a_port == mod_b_port and {mod_a_port, mod_b_port} != {0, 2}:
            raise ValueError("Ports must match 0, 2 or 1,3 (orientation is not supported")
        if mod_a_port == mod_b_port and {mod_a_port, mod_b_port} != {1, 3}:
            raise ValueError("Ports must match 0, 2 or 1,3 (orientation is not supported")

        # checks that the ports are not already in use
        try:
            if self.modules[mod_a][mod_a_port] is not None:
                raise ValueError("The port %d on module A is already in use" %(mod_a_port))
            if self.modules[mod_b][mod_b_port] is not None:
                raise ValueError("The port %d on module B is already in use" %(mod_b_port))
        except IndexError:
            raise IndexError("That port number does not exist in this dimension")

        if (mod_a in self.positions) and (mod_b in self.positions):
            if abs(sum(tuple(map(op.sub, self.positions[mod_a], self.positions[mod_b])))) != 1:
                raise KeyError("Modules %s, %s cannot be connected" %(mod_a, mod_b))
        elif mod_a in self.positions:
            self.positions[str(mod_b)] = self._position_get(mod_a_port, mod_a)
        elif mod_b in self.positions:
            self.positions[str(mod_a)] = self._position_get(mod_b_port, mod_b)

        self.modules[mod_a][mod_a_port] = mod_b
        self.modules[mod_b][mod_b_port] = mod_a
        self.connections.append((mod_a, mod_b))

    def disconnect(self, mod_id, port_id):
        """takes a module id and port number and disconnects that port"""
        mod_id = str(mod_id)
        port_id = int(port_id)
        if self.modules[mod_id][port_id] is None:
            raise ValueError("Port %d on module: %s is not connected" %(port_id, mod_id))

        self.modules[self.modules[mod_id][port_id]][(port_id+2)%(self._dimensions*2)] = None

        try:
            self.connections.remove(mod_id, self.modules[mod_id][port_id])
        except ValueError:
            self.connections.remove(self.modules[mod_id][port_id], mod_id)
        self.modules[mod_id][port_id] = None

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

    def _position_get(self, port, mod_id):
        """pass port of unconnected module and id of connected module
        returns position of newly connected module"""
        if  port in (0, 2):
            position = tuple(map(op.add, self.positions[mod_id], (port-1, 0)))
        elif  port in (1, 3):
            position = tuple(map(op.add, self.positions[mod_id], (0, (port-2)*-1)))
        return position

    def display(self):
        """displays a graph of the modules"""
        graph = self.get_graph()
        nx.draw(graph, pos=self.positions, with_labels=True)
        plt.show()
