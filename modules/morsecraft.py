#!/usr/bin/env python3.5
"""Spacecraft made up of Modules used in conjunction with morse for simulation"""
import math
import operator as op

import numpy as np

import jsonpickle as pickler

from .craftmodule import Module as Module
from .scripts import modControl as modCon

__authors__ = ["Mark A Post", "Rebecca Wardle"]
__copyright__ = "Copyright 2020 Rebecca Wardle"
__license__ = "MIT License"
__credit__ = ["Mark A Post", "Rebecca Wardle", "Robert Fitch", "Daniela Rus", "Zachary Butler"]
__version__ = "0.5"


class Spacecraft:
    """A generic spacecraft class that contains a dictionary of modules and connections"""
    def __init__(self, tag_length=3, precision=0.01, is_goal=False):
        self._root = None
        self.modules = {}
        self.goal = None
        self.tag_len = tag_length
        self.precision = precision
        self.is_goal = is_goal

    def add_mod(self,
                new_id,
                position=(0, 0, 0),
                size=(0.1, 0.1, 0.1),
                rotation=(0, 0, 0)):
        """Add an unconnected module to the craft dictionary"""
        new_mod = Module(new_id, size, position)
        new_mod.type = new_id[-self.tag_len:]

        if not self._root:
            self._root = new_mod
        x = math.radians(rotation[0]) / 2
        y = math.radians(rotation[1]) / 2
        z = math.radians(rotation[2]) / 2
        cos = math.cos
        sin = math.sin
        new_mod.rotation = [
            cos(x) * cos(y) * cos(z) + sin(x) * sin(y) * sin(z),
            sin(x) * cos(y) * cos(z) - cos(x) * sin(y) * sin(z),
            cos(x) * sin(y) * cos(z) + sin(x) * cos(y) * sin(z),
            cos(x) * cos(y) * sin(z) - sin(x) * sin(y) * cos(z)
        ]
        self.modules[str(new_id)] = new_mod

    def set_rotation(self, mod_id, rotation):
        """"pass mod_id and new rotation and the module's rotation will be set accordingly"""
        x = math.radians(rotation[0]) / 2
        y = math.radians(rotation[1]) / 2
        z = math.radians(rotation[2]) / 2
        cos = math.cos
        sin = math.sin
        self.modules[mod_id].rotation = [
            cos(x) * cos(y) * cos(z) + sin(x) * sin(y) * sin(z),
            sin(x) * cos(y) * cos(z) - cos(x) * sin(y) * sin(z),
            cos(x) * sin(y) * cos(z) + sin(x) * cos(y) * sin(z),
            cos(x) * cos(y) * sin(z) - sin(x) * sin(y) * cos(z)
        ]
        # if rotation is added to modController uncomment to implement the effects on the simulator
        # modCon.set_rotation(rotation)

    def create_goal(self):
        """creates a sub-object that can then be manipulated to set the goal state of the spacecraft"""
        self.goal = Spacecraft(self.tag_len, self.precision, is_goal=True)

    def get_new_position(self, fixed_mod, moving_mod, port_id):
        """returns the coordinates of the connected module based off the given module and port"""
        fixed_mod = self.modules[fixed_mod]
        moving_mod = self.modules[moving_mod]

        # detect modules with more than one port per face (change offset)

        # first get x, y, z diffs to be added
        x_diff = (fixed_mod.dim[0] / 2) + (moving_mod.dim[0] / 2)
        y_diff = (fixed_mod.dim[1] / 2) + moving_mod.dim[1] / 2
        z_diff = fixed_mod.dim[2] / 2 + moving_mod.dim[2] / 2

        # np.array allows port_id to index the correct offset
        ports = [[-x_diff, 0, 0], [0, y_diff, 0], [x_diff, 0, 0],
                 [0, -y_diff, 0], [0, 0, z_diff], [0, 0, -z_diff]]

        # convert quaternions to rotation matrix which can be applied upon the ports
        q = fixed_mod.rotation
        rotation = np.array([[
            1 - 2 * (q[2]**2 + q[3]**2), 2 * (q[1] * q[2] - q[3] * q[0]),
            2 * (q[1] * q[3] + q[2] * q[0]), 0
        ],
                             [
                                 2 * (q[1] * q[2] + q[3] * q[0]),
                                 1 - 2 * (q[1]**2 + q[3]**2),
                                 2 * (q[2] * q[3] - q[1] * q[0]), 0
                             ],
                             [
                                 2 * (q[1] * q[3] - q[2] * q[0]),
                                 2 * (q[2] * q[3] + q[1] * q[0]),
                                 1 - 2 * (q[1]**2 + q[2]**2), 0
                             ], [0, 0, 0, 1]])

        # select the port from port_id
        diff = np.array(ports[port_id] + [0])

        # apply rotation matrix to get new direction of offset then add to fixed mod position

        return tuple(map(op.add, fixed_mod.pos, tuple(rotation.dot(diff))[:3]))

    def check_adjacency(self, mod_a, mod_b):
        """ returns true and the unrotated port_id if mod_a and mod_b are next to each other (based on their positions)"""
        mod_a = self.modules[mod_a]
        mod_b = self.modules[mod_b]

        for i in range(len(mod_a.pos) * 2):
            # ensures that both directions of each dim are tested

            if i % 2 == 0:
                mul = 1
            else:
                mul = -1
            # sets only one dim to the offset the modules would be
            difference = [0] * len(mod_a.pos)
            difference[i % len(mod_a.pos)] = mul * ((mod_a.dim[i % 3] / 2) +
                                                    (mod_b.dim[i % 3] / 2))

            mod_position = tuple(
                map(op.add, tuple(mod_a.pos), tuple(difference)))

            # refactor into single line without for loop (using sum)
            to_return = True

            for j in range(len(mod_position)):
                if abs(mod_position[j] - mod_b.pos[j]) >= self.precision:
                    to_return = False

                    break

            if to_return:
                base_cons = [2, 3, 4, 0, 1, 5]

                return base_cons[i]

        return None

    def check_chain(self, mod):
        """returns max length of line originating on given module"""
        max_length = 0

        for port in self.modules[mod].cons:
            if port is not None:
                max_length += 1
                # diff = list(map(op.sub, self.modules[mod].pos, self.modules[port].pos))
                # cont = True

    def get_port(self, mod, base_port):
        """returns the actual port to connect modules with when passed mod and the port to connect without rotation"""
        base_direcs = np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0],
                                [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, -1, 0]])
        direction = np.array(base_direcs[base_port])
        q = self.modules[mod].rotation
        rotation = np.array([[
            1 - 2 * (q[2]**2 + q[3]**2), 2 * (q[1] * q[2] - q[3] * q[0]),
            2 * (q[1] * q[3] + q[2] * q[0]), 0
        ],
                             [
                                 2 * (q[1] * q[2] + q[3] * q[0]),
                                 1 - 2 * (q[1]**2 + q[3]**2),
                                 2 * (q[2] * q[3] - q[1] * q[0]), 0
                             ],
                             [
                                 2 * (q[1] * q[3] - q[2] * q[0]),
                                 2 * (q[2] * q[3] + q[1] * q[0]),
                                 1 - 2 * (q[1]**2 + q[2]**2), 0
                             ], [0, 0, 0, 1]])
        rotated = np.round(base_direcs.dot(rotation))

        # now check which port has the same vector as the base port

        for index in range(len(base_direcs)):
            if np.array_equal(rotated[index], direction):
                return index
        raise ValueError(
            "Apperntly no ports point in that direction someone is wrong (blame the writer)"
        )

    def connect(self, mod_a, mod_a_port, mod_b, mod_b_port):
        """Connects the 2 passed modules with the specified ports
        as orientation is going to be considered in future code it takes both ports"""

        # checks the modules are not already connceted

        if self.modules[mod_a].cons[mod_a_port] == mod_b:
            if self.modules[mod_b].cons[mod_b_port] == mod_a:
                return

        # checks that the ports are not already in use
        try:
            if self.modules[mod_a].cons[mod_a_port] is not None:
                raise ValueError(
                    "The port %d on %s is already connected to %s" %
                    (mod_a_port, mod_a, self.modules[mod_a].cons[mod_a_port]))
        except IndexError:
            raise IndexError("Port %d does not exist in this dimension" %
                             (mod_a_port))

        try:
            if self.modules[mod_b].cons[mod_b_port] is not None:
                raise ValueError("The port %d on %s is already in use" %
                                 (mod_b_port, mod_b))
        except IndexError:
            raise IndexError("Port %d does not exist in this dimension" %
                             (mod_b_port))

        # give postitions to connected module

        if self.is_goal:
            self.modules[mod_a].pos = (0, 0, 0)
            self.modules[mod_b].pos = self.get_new_position(
                mod_a, mod_b, mod_a_port)
        elif (self.modules[mod_a].pos is not None) and (self.modules[mod_b].pos
                                                        is not None):
            # checks modules are next to each other

            if self.check_adjacency(mod_a, mod_b) is None:
                raise ValueError("Modules %s, %s are not adjecent" %
                                 (mod_a, mod_b))
        elif self.modules[mod_a].pos is not None:
            self.modules[mod_b].pos = self.get_new_position(
                mod_a, mod_b, mod_a_port)

        elif self.modules[mod_b].pos is not None:
            self.modules[mod_a].pos = self.get_new_position(
                mod_b, mod_a, mod_b_port)

        self.modules[mod_a].cons[mod_a_port] = mod_b
        self.modules[mod_b].cons[mod_b_port] = mod_a

        # move the cubes to the correct positions
        # won't move modules already in place
        # checks that modules should actually be moved

        if not self.is_goal:
            # move the modules into position and ensure they are there
            self.move_mod(mod_a, self.modules[mod_a].pos)
            self.move_mod(mod_b, self.modules[mod_b].pos)
        # links the modules together
        modCon.link(mod_a, mod_b)

    def connect_all(self, mod_id):
        """give a mod id, checks all adjacent positions and connects module to
        adjancent modules"""

        if self.modules[mod_id].pos is None:
            raise IndexError(
                "%s does not have a position so it not yet connected" %
                (mod_id))

        for mod in self.modules:
            if mod != mod_id:
                adja = self.check_adjacency(mod_id, mod)

                if adja is not None:
                    # use the returned port to get the actual ports to connect with and then connect the mods
                    mod_a_port = self.get_port(mod, adja)
                    # skips if the module is already connected at that port

                    if self.modules[mod_id].cons[mod_a_port] == mod:
                        continue

                    base_cons = [2, 3, 0, 1, 5, 4]
                    mod_b_port = self.get_port(mod, base_cons[adja])

                    self.connect(mod_id, mod_a_port, mod, mod_b_port)

    def disconnect(self, mod_id, port_id):
        """takes a module id and port number and disconnects that port"""

        if self.modules[mod_id].cons[port_id] is None:
            # will now just accept to allow for batch disconnects
            # raise ValueError("Port %d on module: %s is not connected" % (port_id, mod_id))

            return

        # disconnects port on other module
        modCon.unlink(mod_id, self.modules[mod_id].cons[port_id])

        for port in self.modules[self.modules[mod_id].cons[port_id]].cons:
            if port == mod_id:
                port = None
        self.modules[mod_id].cons[port_id] = None

    def disconnect_all(self, mod_id):
        """disconnects module from all connections"""
        # add a way to avoid disconnect from arm/tug

        for port_id in range(len(self.modules[mod_id].cons)):
            self.disconnect(mod_id, port_id)
        # remove position for module so it can be repositioned

    def get_isolated_mod(self, root):
        """gets unconnected module from root and path from root according to BFS"""

        to_visit = [[root]]
        visited = set()

        while to_visit:
            path = to_visit.pop(0)
            current_node = path[-1]

            to_return = True

            # checks if current_node is only connected by 1 link

            if sum(x is None for x in self.modules[current_node].cons) == 5:
                return current_node, path

            # add the children nodes in order
            elif current_node not in visited:
                for child in self.modules[current_node].cons:
                    if child is not None and child not in visited:
                        new_path = list(path)
                        new_path.append(child)
                        to_visit.append(new_path)
                        to_return = False

            if to_return is True:
                return current_node, visited
            visited.add(current_node)

    def get_goal_order(self):
        """return the goal order using BFS"""
        root, dump = self.goal.get_isolated_mod(next(iter(self.goal.modules)))
        to_visit = [root]
        visited = []

        while to_visit:
            current_node = to_visit[0]
            visited.append(current_node)

            for child in self.goal.modules[current_node].cons:
                # broken?

                if child is not None and child not in to_visit and child not in visited:
                    to_visit.append(child)

            to_visit.pop(0)

        return visited

    def get_mod_path(self, root, goal):
        """a dijkstra implementation
        returns path from root mod_id and goal mod_id as module ids"""
        to_visit = {root}
        est_cost = {root: 0}
        final_cost = {}
        visited = set()
        back_track = {}

        while to_visit:
            current_node = None
            current_score = None

            for mod in to_visit:
                if current_node is None or est_cost[mod] < current_score:
                    current_node = mod
                    current_score = est_cost[mod]
            # checks if reached goal

            if current_node == goal:
                path = [current_node]

                while current_node in back_track:
                    current_node = back_track[current_node]
                    path.append(current_node)
                # if goal[-self._mod_type:] == path[0][-self._mod_type:]:
                path.reverse()

                return path

            to_visit.remove(current_node)
            visited.add(current_node)

            for neighbour in self.goal.modules[current_node].cons:
                if neighbour in visited:
                    continue
                tmp_cost = est_cost[current_node] + 1

                if neighbour not in to_visit:
                    to_visit.add(neighbour)
                elif tmp_cost >= final_cost[neighbour]:
                    continue
                back_track[neighbour] = current_node
                final_cost[neighbour] = tmp_cost
                est_cost[neighbour] = final_cost[neighbour] + 1

    def import_from_file(self, file_name, goal=True):
        """pass json file to import design (have to redifine craft if importing)"""
        with open(file_name, 'r') as file:
            data = file.read().replace("\n", "")

        if goal is False:
            new_craft = pickler.decode(data)
            try:
                new_craft._mod_type
            except AttributeError:
                new_craft._mod_type = 3

            return new_craft
        else:
            self.goal = pickler.decode(data)

    def export_to_file(self, file_name):
        """export current spacecraft as a json file"""
        write_file = open(file_name + ".json", "w")
        write_file.write(pickler.encode(self))

    def get_coord_path(self, mod_path, final_port, clearance=None):
        """pass  a list of modules and the port the module will be connected to, returns a list of coordinates around the path
        doesn't take into account the orientation of the modules (will cause problems with different sized mods"""

        if clearance is None:
            clearance = self.precision

        mod_path = mod_path[::-1]
        moving_mod = mod_path[0]
        path = np.array([np.round(self.modules[moving_mod].pos, 2)])
        final_pos = self.get_new_position(mod_path[-1], moving_mod, final_port)
        moving_mod = self.modules[mod_path[0]]

        # get the direction of clearance to place the module clear of the structure
        # also ensures that the direction of movement is counter after 2nd connection
        # for j in range(2):
        # diff = np.round(list(map(op.sub, list(self.modules[mod_path[j]].pos), list(self.modules[mod_path[j+1]].pos))), 3)
        # for index in range(len(diff)):
        # if abs(diff[index]) >= 0.1:
        # axis_of_movement = index
        # if j != 0:
        # break
        # offset = np.round(clearance * np.sign(self.modules[mod_path[0]].pos[index] - self.modules[mod_path[1]].pos[index]), 4)

        diff = np.round(
            list(
                map(op.sub, list(self.modules[mod_path[0]].pos),
                    list(self.modules[mod_path[1]].pos))), 3)

        for index in range(len(diff)):
            if abs(diff[index]) >= 0.1:
                axis_of_movement = index
                offset = np.round(
                    clearance * np.sign(self.modules[mod_path[0]].pos[index] -
                                        self.modules[mod_path[1]].pos[index]),
                    4)

        if len(mod_path) > 2:
            diff = np.round(
                list(
                    map(op.sub, list(self.modules[mod_path[1]].pos),
                        list(self.modules[mod_path[2]].pos))), 3)

            for index in range(len(diff)):
                if abs(diff[index]) >= 0.1:
                    axis_of_movement = index

        # gets the corners in the path
        # still using 0.1 for module size needs to be altered to take into account of module dimension
        # also doesn't account for module rotation

        for index in range(2, len(mod_path)):
            diff = np.round(
                list(
                    map(op.sub, self.modules[mod_path[index - 1]].pos,
                        self.modules[mod_path[index]].pos)), 3)

            if abs(diff[axis_of_movement]) > 0.1:
                path = np.concatenate([
                    path,
                    np.array([
                        list(np.round(self.modules[mod_path[index - 1]].pos,
                                      2))
                    ])
                ])

                for index in range(len(diff)):
                    if abs(diff[index]) > clearance:
                        axis_of_movement = index

                        break

        # if a chain then add motions up and over the chain (not sure if necessary, chains don't seem to require it)

        if len(path) == 1:
            # creates 2 new modules to move the module around the chain
            # up = np.array([path[0]])
            over = np.array(np.array([final_pos]))
            # marks axis to use with value that will be rounded out later
            # up[0][(axis_of_movement+1) % 3] = 0.000001

            # path = np.concatenate((path, up))
            path = np.concatenate((path, over))

        else:
            # add the final destination to the path
            path = np.concatenate((path, np.array([final_pos])))

        # make the first movement to place the module clear of the structure
        path[0][axis_of_movement] += offset
        # offset = clearance + np.sign(clearance) * 0.1

        mod_coords = np.array([self.modules[x].pos for x in mod_path])
        # now with corners in mod_path, extrapolate external coordinates (seems to add a duplicate of the first movement)

        for i in range(1, len(path)):
            # take the previous offset to ensure that clearance is maintained in that axis
            dims = [0, 1, 2]
            path[i][axis_of_movement] = path[i - 1][axis_of_movement]
            dims.remove(axis_of_movement)

            for dim in dims:
                if np.round(path[i][dim], 2) == np.round(path[i - 1][dim], 2):
                    break
                axis_of_movement = dim

                # ensures that

                if i == len(path) - 1:
                    path[i][dim] += np.round(
                        clearance * np.sign(path[i][dim] - path[i - 1][dim]),
                        4)
                else:
                    try:
                        cur_mod = mod_path[np.where(
                            mod_coords.all() == path[i])[0][0]]
                    except IndexError:
                        print(
                            "%i coordinates don't appear to be related to another module in the path"
                            % (path[i]))
                    offset = np.round(
                        (clearance + self.modules[cur_mod].dim[dim] / 2 +
                         moving_mod.dim[dim] / 2) *
                        np.sign(path[i][dim] - path[i - 1][dim]), 4)
                    path[i][dim] += offset

        path = np.concatenate((path, np.array([final_pos])))

        # finally move the module around the last corner and onto the docking position

        for dim in range(len(path[-1])):
            if np.round(abs(path[-2][dim] - path[-1][dim]), 4) == clearance:
                path[-1][dim] = path[-2][dim]

                continue
            else:
                path[-1][dim] = final_pos[dim]

        path = np.concatenate((path, np.array([final_pos])))

        final_mod_path = np.array(path)

        return np.round(final_mod_path, 2)

    def move_mod(self, mod_id, dest, precision=None):
        """when called the program will only continue when the module has arrived at the passed position"""

        if precision is None:
            precision = self.precision
        cont = False

        while cont is False:
            modCon.setDest(mod_id=mod_id, x=dest[0], y=dest[1], z=dest[2])
            pose = modCon.getPose(mod_id)

            if dest[0] - precision <= pose["x"] <= dest[0] + precision:
                if dest[1] - precision <= pose["y"] <= dest[1] + precision:
                    if dest[2] - precision <= pose["z"] <= dest[2] + precision:
                        self.modules[mod_id].pos = tuple(dest)
                        cont = True

    def melt(self, root=None):
        """Places all modules in a line"""
        # get most extreme module or check passed module

        if root is None:
            root, dump_path = self.get_isolated_mod(next(iter(self.modules)))
        else:
            if root not in self.modules:
                raise ValueError("%s is not a valid module" % (root))
            good_root = False

            for port in self.modules[root].cons:
                if port is None:
                    good_root = True

            if good_root is False:
                raise ValueError("%s is not a valid root" % (root))

        # connect all modules together to ensure optimum paths

        for node in self.modules():
            self.connect_all(node)

        # find coords of free space next to root
        port_id = None

        for i in root.cons:
            if root.conncetions[i] is None:
                port_id = i

                break
        base_cons = [2, 3, 0, 1, 5, 4]
        # moves all modules into chain
        moved = []
        to_move = set(self.modules.keys())

        while len(to_move) != 0:
            # gets an isolated mod and the path of modules that connect it to the root
            current_node, current_path = self.get_isolated_mod(root)

            # gets the path of coordinates for the module to travel along
            coord_path = self.get_coord_path(current_path, base_cons[port_id])

            # disconnect the module and move it
            self.disconnect_all(current_node)

            # move current node over path by getting positions outside of modules

            for coords in coord_path:
                self.move_mod(current_node, coords)

            # connect module to chain (1 needs to be replaced to take account of modules need to be in certain orientations)
            self.connect(current_node, port_id, root,
                         self.get_port(base_cons[port_id]))
            moved.append(current_node)
            to_move.remove(current_node)
            root = current_node

        return moved

    def sort(self, current_order):
        """sorts the chain of modules"""

        if self.goal is None:
            raise TypeError("goal is not set and therefore cannot be achieved")

        # get order for goal then take only module types
        goal_order = self.get_goal_order()
        goal_order = [elem[-self.tag_len:] for elem in goal_order]

        final_places = {}

        if len(goal_order) != len(current_order):
            # handle this (write later)
            raise ValueError(
                "Goal and spacecraft contain different number of modules")

        tmp_order = current_order.copy()

        # finds where each module type need to be moved
        for pos in range(len(goal_order)):
            try:
                index = [
                    idx for idx, s in enumerate(tmp_order)

                    if goal_order[pos] in s
                ][0]
            except IndexError:
                raise IndexError("%s doesn't exist in craft" %
                                 (goal_order[pos]))
            final_places[tmp_order[index]] = pos
            del tmp_order[index]

        base_cons = [2, 3, 0, 1, 5, 4]

        # find the occupied ports and makes a list of the unused ones
        mid_mod = current_order[len(current_order) // 2]
        used = []

        for port_id in range(len(self.modules[mid_mod].cons)):
            if self.modules[mid_mod].cons[port_id] is not None:
                used.append(port_id)

        if len(used) != 2:
            raise IndexError("The modules are not in a chain")

        unused = [0, 1, 2, 3, 4, 5]
        unused.remove(used[0])
        unused.remove(used[1])

        print("\nSplitting in 2")

        # splits the row in 2
        current_order = [current_order]
        for i in range(len(current_order[0]) // 2):
            self.disconnect_all(current_order[0][0])

            popped_mod = current_order[0].pop(0)
            path = current_order[0][-i - 1::-1] + [popped_mod]

            if i == 0:
                current_order.append([popped_mod])
            else:
                current_order[1].insert(0, popped_mod)

            # moves the module to the new position
            # path currently moves the module towards nearest module (oops)
            path = self.get_coord_path(path, unused[0])
            print(popped_mod)

            for coord in path:
                print("moving to:", coord)
                self.move_mod(popped_mod, coord)
            final_pose = modCon.getPose(popped_mod)
            final_pose = [final_pose["x"]] + [final_pose["y"]] + [final_pose["z"]]
            final_pose = np.round(final_pose, 3)
            print("final pos:", final_pose)
            # connects to row above/below
            self.connect(popped_mod, unused[0], current_order[0][-i - 1], base_cons[unused[0]])
            # connect to modules on it's own rown
            self.connect_all(popped_mod)

        # remove the now used ports so that bubble sort only uses the remaining dimension
        unused.remove(base_cons[unused[0]])
        unused.remove(unused[0])

        print("beginning bubble")
        # bubble sort both rows

        # sort each row seperately (could run in parallel?)
        for sub_list in current_order:
            # sorts each row
            for i in range(len(sub_list) - 1):
                for j in range(0, len(sub_list) - i - 1):
                    if final_places[sub_list[j]] > final_places[sub_list[j+1]]:
                        # final positions of each module
                        pos1 = self.modules[sub_list[j]].pos
                        pos2 = self.modules[sub_list[j + 1]].pos
                        self.disconnect_all(sub_list[j + 1])


                        self.disconnect_all(sub_list[j])
                        self.move_mod(sub_list[j], )
                        # take first mod, get unused dimension
                        # move the first mod up and then ontop of the second module
                        # move the second mod along to pos of 1st
                        # move 1st mod down into position

                        self.connect_all(sub_list[j+1])
                        self.connect_all(sub_list[j])
                        sub_list[j], sub_list[j+1] = sub_list[j+1], sub_list[j]

        # connect structure together

        for key in self.modules:
            self.connect_all(key)

        # merge sorted rows

        if final_places[current_order[0][0]] < final_places[current_order[1]
                                                            [0]]:
            root = current_order[0][0]
            del current_order[0][0]
        else:
            root = current_order[1][0]
            del current_order[1][0]

        if final_places[current_order[0][-1]] > final_places[current_order[1]
                                                             [-1]]:
            self.disconnect_all(root)
            self.connect(current_order[0][-1], 2, root, 0)
        else:
            self.disconnect_all(root)
            self.connect(current_order[1][-1], 2, root, 0)
        final_order = [root]

        while len(current_order[0]) > 0 and len(current_order[1]) > 0:
            if final_places[current_order[0][0]] < final_places[
                    current_order[1][0]]:
                self.disconnect_all(current_order[0][0])
                self.connect(root, 2, current_order[0][0], 0)
                root = current_order[0][0]
                del current_order[0][0]
                final_order.append(root)
            else:
                self.disconnect_all(current_order[1][0])
                self.connect(root, 2, current_order[1][0], 0)
                root = current_order[1][0]
                del current_order[1][0]
                final_order.append(root)

        for mod in current_order[0]:
            self.disconnect_all(mod)
            self.connect(root, 2, mod, 0)
            root = mod
            final_order.append(root)

        for mod in current_order[1]:
            self.disconnect_all(mod)
            self.connect(root, 2, mod, 0)
            root = mod
            final_order.append(root)

        return final_order

    def grow(self, order):
        """moves the sorted module chain to form the goal structure"""

        for idx in range(len(order)):
            base_cons = [2, 3, 0, 1, 5, 4]
            mod_type = order[idx][-self.tag_len:]
            path = order[idx + 1:]

            if idx == 0:
                self.disconnect_all(order[idx])
                self.connect(order[-1], 2, order[idx], 0)
                # self.goal.modules[order[idx].replace("_", "-")] = self.goal.modules.pop(order[idx])
                # order[idx] = order[idx].replace("_", "-")

                continue

            path = path + self.get_mod_path(order[0], order[idx])
            sucess = False
            last_mod = path[-2]

            for port in range(len(self.goal.modules[last_mod].cons)):
                if self.goal.modules[last_mod].cons[port] is None:
                    continue
                elif self.goal.modules[last_mod].cons[port][
                        -self.tag_len:] == mod_type:
                    self.disconnect_all(order[idx])
                    self.connect(order[idx], base_cons[port], path[-1], port)
                    sucess = True

            self.display()

            if not sucess:
                raise ValueError("Growing failed. Sucess:", sucess)
