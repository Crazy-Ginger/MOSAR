#!/usr/bin/env python3
import operator as op

import numpy as np

modules = {"00": [None, "03", "01", None, "10", None],
           "01": ["00", "04", "02", None, "11", None],
           "02": ["01", "05", None, None, "12", None],
           "03": [None, "06", "04", "00", "13", None],
           "04": ["03", "07", "05", "02", "14", None],
           "05": ["04", "08", None, "02", "15", None],
           "06": [None, None, "07", "03", "16", None],
           "07": ["06", None, "08", "04", "17", None],
           "08": ["07", None, None, "05", "18", None],
           "10": [None, "13", "11", None, None, "00"],
           "11": ["10", "14", "12", None, None, "01"],
           "12": ["11", "15", None, None, None, "02"],
           "13": [None, "16", "14", "10", None, "03"],
           "14": ["13", "17", "15", "12", None, "04"],
           "15": ["14", "18", None, "12", None, "05"],
           "16": [None, None, "17", "13", None, "06"],
           "17": ["16", None, "18", "14", None, "07"],
           "18": ["17", None, None, "15", None, "08"]
          }

alt_modules = {"00": [None, None, None, None, None, None],
               "1": [None, None, None, None, None, None],
               "2": [None, None, None, None, None, None],
               "03": [None, None, None, None, None, None],
               "4": [None, None, None, None, None, None],
               "05": [None, None, None, None, None, None],
               "6": [None, None, None, None, None, None],
               "07": [None, None, None, None, None, None],
               "8": [None, None, None, None, None, None]
               }

pos = {"00": [0.0, 0.0, 0.0],
       "01": [0.0, 0.1, 0.0],
       "02": [0.0, 0.2, 0.0],
       "03": [0.1, 0.0, 0.0],
       "04": [0.1, 0.1, 0.0],
       "05": [0.1, 0.2, 0.0],
       "06": [0.2, 0.0, 0.0],
       "07": [0.2, 0.1, 0.0],
       "08": [0.2, 0.2, 0.0],
       "10": [0.0, 0.0, 0.1],
       "11": [0.0, 0.1, 0.1],
       "12": [0.0, 0.2, 0.1],
       "13": [0.1, 0.0, 0.1],
       "14": [0.1, 0.1, 0.1],
       "15": [0.1, 0.2, 0.1],
       "16": [0.2, 0.0, 0.1],
       "17": [0.2, 0.1, 0.1],
       "18": [0.2, 0.2, 0.1]
       }

alt_pos = {"00": [0.0, 0.0, 0.0],
           "01": [0.0, 0.1, 0.0],
           "02": [0.0, 0.2, 0.0],
           "03": [0.0, 0.3, 0.0],
           "04": [0.0, 0.4, 0.0],
           "05": [0.0, 0.5, 0.0],
           "06": [0.0, 0.6, 0.0],
           "07": [0.0, 0.7, 0.0],
           "08": [0.0, 0.8, 0.0]
           }


def path_to_isolated(root):
    to_visit = [[root]]
    visited = set()

    while to_visit:
        path = to_visit.pop(0)
        current_node = path[-1]
        if current_node in visited:
            continue

        visited.add(current_node)

        to_return = True

        # checks if current_node is only connected by 1 link
        if sum(x is None for x in modules[current_node]) == 5 and current_node != root:
            return path

        # add the children nodes in order
        for child in modules[current_node]:
            if child and child not in visited:
                to_return = False
                new_path = path.copy()
                new_path.append(child)
                to_visit.append(new_path)

        if to_return is True:
            return path


def get_new_position(fixed_mod, moving_mod, port_id):
    # first get x, y, z diffs to be added
    x_diff = 0.1
    y_diff = 0.1
    z_diff = 0.1

    # np.array allows port_id to index the correct offset
    ports = [
        [-x_diff, 0, 0],
        [0, y_diff, 0],
        [x_diff, 0, 0],
        [0, -y_diff, 0],
        [0, 0, z_diff],
        [0, 0, -z_diff],
    ]

    # convert quaternions to rotation matrix can be applied upon the ports
    q = [1] + [0] * 3
    rotation = np.array(
        [
            [
                1 - 2 * (q[2] ** 2 + q[3] ** 2),
                2 * (q[1] * q[2] - q[3] * q[0]),
                2 * (q[1] * q[3] + q[2] * q[0]),
                0,
            ],
            [
                2 * (q[1] * q[2] + q[3] * q[0]),
                1 - 2 * (q[1] ** 2 + q[3] ** 2),
                2 * (q[2] * q[3] - q[1] * q[0]),
                0,
            ],
            [
                2 * (q[1] * q[3] - q[2] * q[0]),
                2 * (q[2] * q[3] + q[1] * q[0]),
                1 - 2 * (q[1] ** 2 + q[2] ** 2),
                0,
            ],
            [0, 0, 0, 1],
        ]
    )

    # select the port from port_id
    diff = np.array(ports[port_id] + [0])

    # apply rotation matrix to get new direction of offset then add to fixed mod position
    return tuple(map(op.add, pos[fixed_mod], tuple(rotation.dot(diff))[:3]))


def get_coord_path(mod_path, final_port, clearance=None):
    if clearance is None:
        clearance = 0.05

    if type(mod_path) != list:
        mod_path = list(mod_path)

    # initial variables and conditions
    mod_path = mod_path[::-1]
    moving_mod = mod_path[0]
    final_pos = get_new_position(mod_path[-1], moving_mod, final_port)
    # moving_mod = modules[mod_path[0]]

    # get the directions and distance to move clear of structure
    diff = np.array(pos[moving_mod], dtype=np.float32)
    counter = 0
    for con_mod in modules[moving_mod]:
        if con_mod:
            diff += list(map(op.sub, pos[moving_mod], pos[con_mod]))
            counter += 1
            if counter > 3:
                raise ValueError("%s is not unconnected and free to move" % (moving_mod))
    if counter < 1:
        raise ValueError("%s is not connected at all" % (moving_mod))

    # add clearance to first motion
    for i in range(len(diff)):
        if diff[i] != pos[moving_mod][i]:
            diff[i] += np.sign(diff[i])*clearance
    diff = np.round(diff, 3)

    # path initiated with the first offset
    path = np.array([np.round(diff, 3)], dtype=np.float32)
    print("initial_move:\n", path[0])


    # if the path length is long enough ignores the first connection to find the next module
    if len(mod_path) > 2:
        diff = np.round(list(map(op.sub, list(pos[mod_path[1]]), list(pos[mod_path[2]]))), 3)

        for index in range(len(diff)):
            if abs(diff[index]) >= 0.1:
                axis_of_movement = index

    # gets the corners in the path
    # still using 0.1 for module size needs to be altered to take into account of module dimension
    # also doesn't account for module rotation
    for index in range(2, len(mod_path)):
        diff = np.round(list(map(op.sub, pos[mod_path[index - 1]], pos[mod_path[index]])), 3)

        if abs(diff[axis_of_movement]) > 0.1:
            path = np.concatenate([path, np.array([list(np.round(pos[mod_path[index - 1]], 2))])])

            for index in range(len(diff)):
                if abs(diff[index]) > clearance:
                    axis_of_movement = index
                    break

    # if a chain then add motions up and over the chain (not sure if necessary, chains don't seem to require it)
    if len(path) == 1:
        # creates 2 new modules to move the module around the chain
        over = np.array(np.array([final_pos]))
        path = np.concatenate((path, over))

    else:
        # add the final destination to the path
        path = np.concatenate((path, np.array([final_pos])))

    # make the first movement to place the module clear of the structure
    path[0][axis_of_movement] += offset
    mod_coords = np.array([pos[x] for x in mod_path])

    # now with corners in mod_path, extrapolate external coordinates (seems to add a duplicate of the first movement
    for i in range(1, len(path)):
        # take the previous offset to ensure that clearance is maintained in that axis
        dims = [0, 1, 2]
        path[i][axis_of_movement] = path[i - 1][axis_of_movement]
        dims.remove(axis_of_movement)

        for dim in dims:
            # if no change from previous axis skip it
            if np.round(path[i][dim], 2) == np.round(path[i - 1][dim], 2):
                break
            axis_of_movement = dim
            # checks if the module is the last and if so just add the offset
            if i == len(path) - 1:
                path[i][dim] += np.round(clearance * np.sign(path[i][dim] - path[i - 1][dim]), 4)
            # adds the clearance
            else:
                try:
                    cur_mod = mod_path[np.where(mod_coords.all() == path[i])[0][0]]
                except IndexError:
                    print("%i coordinates don't appear to be related to another module in the path" % (path[i]))
                offset = np.round((clearance + modules[cur_mod].dims[dim] / 2 + moving_mod.dims[dim] / 2) * np.sign(path[i][dim] - path[i - 1][dim]), 4)
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


def main():
    """     print("pos:")
    for key in pos.keys():
        print(key, ": ", pos[key]) """

    mod_path = path_to_isolated("00")
    current_mod = mod_path[-1]
    print("current_mod: ", current_mod)
    print("mod_path: ", mod_path)
    coord_path = get_coord_path(mod_path, 0)
    print("Coord_path:\n", coord_path)
    return

if __name__ == "__main__":
    main()
