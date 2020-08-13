#!/usr/bin/env python3.5
import operator as op

import jsonpickle as pickler

import modControl as modCon

from math import asin, atan2, degrees


class Module:
    def __init__(self, mod_id, dimensions=(0.1, 0.1, 0.1)):
        self.cons = [None]*len(dimensions)*2
        self.rotation = [1] + [0]*3
        self.position = None
        self.type = None
        self.id = mod_id
        self.dimensions = dimensions

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


class Spacecraft:
    """A generic spacecraft class that contains a dictionary of modules and connections"""
    def __init__(self, tag_length=3):
        self._root = None
        self.modules = {}
        self.goal = None
        self.tag_len = tag_length

    def add_mod(self, new_id, size=(0.1, 0.1, 0.1), rotation=(1.0, 0., 0., 0.)):
        """Add an unconnected module to the craft dictionary"""
        new_mod = Module(new_id, size)
        new_mod.type = new_id[-self.tag_len:]
        if not self._root:
            new_mod.position = [0.0, 0.0, 0.0]
            self._root = new_mod
        new_mod.rotation = list(rotation)
        self.modules[str(new_id)] = new_mod

    def _get_position(self, fixed_mod, moved_mod, port_id):
        """returns the coordinates of the connected module based off the given module and port"""
        # detect cubiod modules here (changes offset)

        # first get x, y, z diffs to be added
        x_diff = (self.modules[fixed_mod].dimensions[0]/2) + (self.modules[moved_mod].dimensions[0]/2)
        y_diff = (self.modules[fixed_mod].dimensions[1]/2) + self.modules[moved_mod].dimensions[1]/2
        z_diff = self.modules[fixed_mod].dimensions[2]/2 + self.modules[moved_mod].dimensions[2]/2

        # array allows port_id to index the correct offset
        port_diff = [[-x_diff, 0, 0],
                     [0, y_diff, 0],
                     [x_diff, 0, 0],
                     [0, -y_diff, 0],
                     [0, 0, z_diff],
                     [0, 0, -z_diff]]

        # how to convert quaternion rotation to 1d matrix offset
        diff = port_diff[port_id]
        quat = self.modules[fixed_mod].rotation
        euler = [90*round(degrees(atan2(2*(quat[0]*quat[1]+quat[2]*quat[3]), 1-2*(quat[1]**2 + quat[2]**2)))/90),
                 90*round(degrees(asin(2*quat[0]*quat[2]-quat[3]*quat[1]))/90),
                 90*round(degrees(atan2(2*(quat[0]*quat[3]+quat[1]*quat[2]), 1-2*(quat[2]**2+quat[3]**2))/90))]

        # normalises coordinates so only positives are used
        for i in range(len(euler)):
            if euler[i] == -90:
                euler[i] == 270
            elif euluer[i] == 360:
                euler[i] == 0
        
        if euler[0] == 90:
            port_diff[1], port_diff[3], port_diff[4], port_diff[5] = port_diff[4], port_diff[5], port_diff[3], port_diff[1]
        elif euler[0] == 180:
            port_diff[1], port_diff[3], port_diff[4], port_diff[5] = port_diff[3], port_diff[1], port_diff[5], port_diff[4]
        elif euler[0] == 270:
            port_diff[1], port_diff[3], port_diff[4], port_diff[5] = port_diff[5], port_diff[4], port_diff[1], port_diff[3]
        else:
            raise ValueError("Euler[0]: %d is unexpected" % (euler[0]))

        if euler[1] == 90:
            port_diff[0], port_diff[1], port_diff[2], port_diff[3] = port_diff[3], port_diff[0], port_diff[1], port_diff[2]
        elif euler[1] == 180:
            port_diff[0], port_diff[1], port_diff[2], port_diff[3] = port_diff[2], port_diff[3], port_diff[0], port_diff[1]
        elif euler[1] == 270:
            port_diff[0], port_diff[1], port_diff[2], port_diff[3] = port_diff[1], port_diff[2], port_diff[3], port_diff[0]
        else:
            raise ValueError("euler[1]: %d is unexpected" % (euler[1]))

        if euler[2] == 90:
            port_diff[0], port_diff[2], port_diff[4], port_diff[5] = port_diff[4], port_diff[5], port_diff[2], port_diff[0]
        elif euler[2] == 180:
            port_diff[0], port_diff[2], port_diff[4], port_diff[5] = port_diff[2], port_diff[0], port_diff[5], port_diff[4]
        elif euler[2] == 270:
            port_diff[0], port_diff[2], port_diff[4], port_diff[5] = port_diff[5], port_diff[4], port_diff[0], port_diff[2]
        else:
            raise ValueError("euler[2]: %d is unexpected" % (euler[2]))

        return list(map(op.add, self.modules[fixed_mod].position, diff))

    def check_adjacency(self, mod_a, mod_b):
        """ returns true if mod_a and mod_b are next to each other (based on their positions)"""
        mod_a = self.modules[mod_a]
        mod_b = self.modules[mod_b]

        for i in range(len(mod_a.position)*2):
            if i % 2 == 0:
                mul = 1
            else:
                mul = -1
            difference = [0]*len(mod_a.position)
            difference[i % 3] = mul * ((mod_a.dimensions[i % 3]/2) + (mod_b.dimensions[i % 3]/2))
            if list(map(op.add, list(mod_a.position), difference)) == list(mod_b.position):
                return True
        return False

    def check_chain(self, mod):
        """returns max length of line originating on given module"""
        max_length = 0
        for port in self.modules[mod].connections:
            if port is not None:
                max_length += 1
                diff = list(map(op.sub, self.modules[mod].position, self.modules[port].position))
                cont = True

    def connect(self, mod_a, mod_a_port, mod_b, mod_b_port):
        """Connects the 2 passed modules with the specified ports
        as orientation is going to be considered in future code it takes both ports"""

        # checks that the ports are not already in use
        try:
            if self.modules[mod_a].cons[mod_a_port] is not None:
                raise ValueError("The port %d on %s is already in use" % (mod_a_port, mod_a))
        except IndexError:
            raise IndexError("Port %d does not exist in this dimension" % (mod_a_port))

        try:
            if self.modules[mod_b].cons[mod_b_port] is not None:
                raise ValueError("The port %d on %s is already in use" % (mod_b_port, mod_b))
        except IndexError:
            raise IndexError("Port %d does not exist in this dimension" % (mod_b_port))

        # give postitions to connected module
        if (self.modules[mod_a].position is not None) and (self.modules[mod_b].position is not None):
            # checks modules are next to each other
            if not self.check_adjacency(mod_a, mod_b):
                raise ValueError("Modules %s, %s are not adjecent" % (mod_a, mod_b))
        elif self.modules[mod_a].position is not None:
            self.modules[mod_b].position = self._get_position(mod_a, mod_b, mod_a_port)

        elif self.modules[mod_b].position is not None:
            self.modules[mod_a].position = self._get_position(mod_b, mod_a, mod_b_port)

        self.modules[mod_a].cons[mod_a_port] = mod_b
        self.modules[mod_b].cons[mod_b_port] = mod_a

        # move the cubes to the correct positions
        a_x = self.modules[mod_a].position[0]
        a_y = self.modules[mod_a].position[1]
        a_z = self.modules[mod_a].position[2]

        b_x = self.modules[mod_b].position[0]
        b_y = self.modules[mod_b].position[1]
        b_z = self.modules[mod_b].position[2]

        modCon.set_dest(mod_a, x=a_x, y=a_y, z=a_z)
        modCon.set_dest(mod_b, x=b_x, y=b_y, z=b_z)

    def connect_all(self, mod_id):
        """give a mod id, checks all adjacent positions and connects module to
        adjancent modules"""
        # this function requires knowing which ports to connect which means rotation
        if self.modules[mod_id].position is None:
            raise IndexError("%s does not have a position so it not yet connected" % (mod_id))

        # for mod in self.modules.keys():
        # if mod != mod_id and self.check_adjacency(mod_id, mod):
        # self.connect(mod_id,
        return

    def disconnect(self, mod_id, port_id):
        """takes a module id and port number and disconnects that port"""

        if self.modules[mod_id].conncetions[port_id] is None:
            # will now just accept to allow for batch disconnects
            # raise ValueError("Port %d on module: %s is not connected" % (port_id, mod_id))
            return

        # disconnects port on other module
        for port in self.modules[self.modules[mod_id].cons[port_id]]:
            if port == mod_id:
                port = None
        self.modules[mod_id].cons[port_id] = None

    def disconnect_all(self, mod_id):
        """disconnects module from all connections"""
        # add a way to avoid disconnect from arm/tug
        for port_id in range(len(self.modules[mod_id].connections)):
            self.disconnect(mod_id, port_id)
        # remove position for module so it can be repositioned

    def get_isolated_mod(self, root):
        """gets unconnected module from root and path from root to it"""

        to_visit = [root]
        visited = []
        while len(to_visit) != 0:
            current_node = to_visit[0]
            to_return = True
            if all(x is None for x in self.modules[current_node]):
                return current_node, visited

            for child in self.modules[current_node].connections:
                if child is not None and child not in visited:
                    to_visit = [child] + [to_visit[1:]]
                    to_return = False

            if to_return is True:
                return current_node, visited
            visited.append(current_node)

    def _get_goal_order(self):
        """return the goal order using bfs"""
        root, dump = self.goal.get_isolated_mod(next(iter(self.goal.modules)))
        to_visit = [root]
        visited = []

        while to_visit:
            current_node = to_visit[0]
            visited.append(current_node)

            for child in self.goal.modules[current_node].connections:
                # broken?
                if child is not None and child not in to_visit and child not in visited:
                    to_visit.append(child)

            to_visit.pop(0)
        return visited

    def get_path(self, root, goal):
        """returns path from root mod_id and goal mod_id"""
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
            # and current_node[-self._mod_type-1] != "-"
            # checks if reached goal
            if current_node == goal:
                path = [current_node]
                while current_node in back_track:
                    current_node = back_track[current_node]
                    path.append(current_node)
                # if goal[-self._mod_type:] == path[0][-self._mod_type:]:
                    # del path[0]
                path.reverse()
                # key = current_node
                # self.goal.modules[key.replace("_", "-")] = self.goal.modules.pop(current_node)
                return path

            to_visit.remove(current_node)
            visited.add(current_node)

            for neighbour in self.goal.modules[current_node].connections:
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
        write_file = open(file_name+".json", "w")
        write_file.write(pickler.encode(self))

    def melt(self, root=None):
        """Places all modules in a line"""
        # get most extreme module or check passed module
        if root is None:
            root, dump_path = self.get_isolated_mod(next(iter(self.modules)))
        else:
            if root not in self.modules:
                raise ValueError("%s is not a valid module" % (root))
            good_root = False
            for port in self.modules[root].connections:
                if port is None:
                    good_root = True
            if good_root is False:
                raise ValueError("%s is not a valid root" % (root))

        # find coords of free space next to root
        broke = False
        for i in range(2*self._dimensions):
            if i % 2 == 0:
                int_diff = 1
            else:
                int_diff = -1
            # get a tuple with +/-1 in one dimension to test free space round root
            difference = [0]*self._dimensions
            difference[i % self._dimensions] = int_diff
            difference = tuple(difference)
            destination = sum(tuple(map(op.add, self.modules[root].position, difference)))
            if destination not in self.positions:
                broke = True
                break
        if broke is False:
            raise ValueError("Did not find a free port around root: %s" % (root))

        # moves all modules into chain
        moved = []
        to_move = set(self.modules.keys())

        while len(to_move) != 0:
            current_node, current_path = self.get_isolated_mod(root)

            # move current node over path by getting positions outside of modules
            for node in current_path:
                self.modules[current_node].position = tuple(map(op.add, self.positions[root], difference))

            # disconnect the module and move it
            self.disconnect_all(current_node)

            # get the ports to connect
            if sum(difference) == 1:
                for i in range(len(difference)):
                    if difference[i] != 0:
                        axis = i
            else:
                for i in range(len(difference)):
                    if difference[i] != 0:
                        axis = i + 3
            axis_to_port = [[2, 1, 4, 0, 3, 5],
                            [0, 3, 5, 2, 1, 4]]
            # connect module to chain
            self.connect(current_node, axis_to_port[0][axis], root, axis_to_port[1][axis])
            moved.append(current_node)
            to_move.remove(current_node)
            root = current_node
        return moved

    def sort(self, current_order):
        """sorts the chain of modules"""
        if self.goal is None:
            raise TypeError("goal is not set and therefore cannot be achieved")

        # get order for goal then take only module types
        goal_order = self._get_goal_order()
        goal_order = [elem[-self._mod_type:] for elem in goal_order]

        final_places = {}

        if len(goal_order) != len(current_order):
            # handle this (write later)
            raise ValueError("Goal and spacecraft contain different number of modules")

        tmp_order = current_order.copy()
        # finds where each module type need to be moved
        for pos in range(len(goal_order)):
            try:
                index = [idx for idx, s in enumerate(tmp_order) if goal_order[pos] in s][0]
            except IndexError:
                raise IndexError("%s doesn't exist in craft" % (goal_order[pos]))
            final_places[tmp_order[index]] = pos
            del tmp_order[index]

        # find unoccupied dimension and sets the port to use
        for port_id in range(len(self.modules[current_order[len(current_order)//2]].connections)):
            if self.modules[current_order[len(current_order)//2]].cons[port_id] is not None:
                occupied = port_id
                break
        axis_to_port = [[2, 1, 4, 0, 3, 5],
                        [0, 3, 5, 2, 1, 4]]
        lower_port = axis_to_port[0][(occupied+1) % self._dimensions]

        current_order = [current_order]
        # splits the row in 2
        tmp_order = []
        for i in range(len(current_order[0]) // 2):
            tmp_order.insert(0, current_order[0][i])
            self.disconnect_all(current_order[0][i])
            self.connect(current_order[0][i], lower_port, current_order[0][(-i-1)], axis_to_port[1][lower_port])
            # self.connect_all(current_order[0][i])

        current_order.append(tmp_order)
        # removes from of row as it has been moved to below
        del current_order[0][:len(current_order[0])//2]

        # if sub-modules work could replace so arm just turns the modules over

        # bubble sort both rows
        for sub_list in current_order:
            for i in range(len(sub_list)-1):
                for j in range(0, len(sub_list)-i-1):
                    if final_places[sub_list[j]] > final_places[sub_list[j+1]]:
                        pos1 = self.positions[sub_list[j]]
                        pos2 = self.positions[sub_list[j+1]]
                        self.disconnect_all(sub_list[j+1])
                        self.disconnect_all(sub_list[j])
                        self.positions[sub_list[j]], self.positions[sub_list[j+1]] = pos2, pos1
                        # this will need rewriting for morse
                        # connect_all doesn't seem to work here
                        # self.connect_all(sub_list[j+1])
                        # self.connect_all(sub_list[j])
                        sub_list[j], sub_list[j+1] = sub_list[j+1], sub_list[j]

        # connect structure together
        # for key in self.modules:
            # self.connect_all(key)

        # merge sorted rows
        if final_places[current_order[0][0]] < final_places[current_order[1][0]]:
            root = current_order[0][0]
            del current_order[0][0]
        else:
            root = current_order[1][0]
            del current_order[1][0]

        if final_places[current_order[0][-1]] > final_places[current_order[1][-1]]:
            self.disconnect_all(root)
            self.connect(current_order[0][-1], 2, root, 0)
        else:
            self.disconnect_all(root)
            self.connect(current_order[1][-1], 2, root, 0)
        final_order = [root]
        while len(current_order[0]) > 0 and len(current_order[1]) > 0:
            if final_places[current_order[0][0]] < final_places[current_order[1][0]]:
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
        print(order)
        print()
        for idx in range(len(order)):
            port_finder = [2, 3, 0, 1, 5, 4]
            mod_type = order[idx][-self._mod_type:]
            path = order[idx+1:]

            if idx == 0:
                self.disconnect_all(order[idx])
                self.connect(order[-1], 2, order[idx], 0)
                # self.goal.modules[order[idx].replace("_", "-")] = self.goal.modules.pop(order[idx])
                # order[idx] = order[idx].replace("_", "-")
                print(path)
                continue

            path = path + self.get_path(order[0], order[idx])
            print(path)
            sucess = False
            last_mod = path[-2]
            for port in range(len(self.goal.modules[last_mod].connections)):
                if self.goal.modules[last_mod].cons[port] is None:
                    continue
                elif self.goal.modules[last_mod].cons[port][-self._mod_type:] == mod_type:
                    self.disconnect_all(order[idx])
                    self.connect(order[idx], port_finder[port], path[-1], port)
                    sucess = True

            self.display()
            if not sucess:
                raise ValueError("Didn't connect the module properly, rewrite it dipshit")
