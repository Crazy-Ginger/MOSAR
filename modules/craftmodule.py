#!/usr/bin/env python3.5
"""Module class to hold data on individual modules that form part of the morsecraft structure"""
from numpy import array, round

__author__ = "Rebecca Wardle"


class Module:
    """A module class that contains:
        position, rotation, connections, type, dimensions, id
    used within spacecraft"""
    def __init__(self, mod_id, dimensions=(0.1, 0.1, 0.1), position=(0, 0, 0)):
        self.cons = [None] * len(dimensions) * 2
        self.rotation = [1] + [0] * 3
        self.pos = tuple(round(array(position), 2))
        self.type = None
        self.id = mod_id
        self.dim = dimensions

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id
