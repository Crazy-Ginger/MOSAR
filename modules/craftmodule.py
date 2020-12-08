#!/usr/bin/env python3.5
"""Module class to hold data on individual modules that form part of the morsecraft structure"""
from numpy import round

__author__ = "Rebecca Wardle"
__copyright__ = "Copyright 2020 Rebecca Wardle"
__license__ = "MIT License"
__credit__ = ["Rebecca Wardle"]
__version__ = "0.5"


class Module:
    """
    A module class used in morsecraft
    """
    def __init__(self, mod_id, type, dimensions=(0.1, 0.1, 0.1), position=(0, 0, 0)):
        """
        Constructor
        :param mod_id: string, unique identifier of the module
        :param type: string, module type
        :param dimensions: (optional) integer tuple, dimensions of mod (in m)
        :param position: (optional) integer tuple, cartesian coords of mod
        """
        self.cons = [None] * len(dimensions) * 2
        self.rotation = [1] + [0] * 3
        self.pos = round(position, 3)
        self.type = type
        self.id = mod_id
        self.dims = dimensions

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id
