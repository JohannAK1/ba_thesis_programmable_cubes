from framework.programmable_cubes_UDP import ProgrammableCubes, programmable_cubes_UDP
import numpy as np
from PosSaver2 import SinglePositionSaver2

iss = programmable_cubes_UDP('ISS')


config1 = np.copy(iss.initial_cube_pos)
config2 = np.copy(iss.target_cube_positions)
type1 = np.copy(iss.initial_cube_types)
type2 = np.copy(iss.target_cube_types)

def is_adjacent(cube1, cube2):
        """
        Check if cube2 is adjacent to cube1
        """
        x1, y1, z1 = cube1
        x2, y2, z2 = cube2
        return (abs(x1 - x2) == 1 and y1 == y2 and z1 == z2) or \
            (x1 == x2 and abs(y1 - y2) == 1 and z1 == z2) or \
            (x1 == x2 and y1 == y2 and abs(z1 - z2) == 1)

def count_adjacent(target_cube, initial_set):
        """
        Count how many cubes in initial_set are adjacent to target_cube
        """
        count = 0
        for initial_cube in initial_set:
            if is_adjacent(initial_cube, target_cube):
                count += 1
        return count

def find_reachable_positions(config_ini, config_tar,type2):
    """
    Find indices in target that are reachable from initial positions and order by number of adjacent cubes
    """
    initial_set = set(map(tuple, config_ini))
    reachable_positions = []
    allPos = np.copy(config1)
    allTypes = np.copy(type1)

    for i, target_cube in enumerate(config_tar):
        if tuple(target_cube) not in initial_set:
            adj_count = count_adjacent(target_cube, initial_set)
            if adj_count > 0:
                allPos = np.vstack((allPos,config_tar[i]))
                allTypes = np.append(allTypes,type2[i])
                reachable_positions.append((config_tar[i]))
    
    return np.copy(allPos),np.copy(allTypes)



allPos1,allTypes1 = find_reachable_positions(config1,config2,type2)

"""
print(allPos1)
print(len(allPos1))
print(len(allTypes1))
print(len(config1))"""


SPS = SinglePositionSaver2(allPos1,allTypes1,"llssllslslsll")
SPS1 = SinglePositionSaver2(config1,type1,"llssllslslsll")
SPS2 = SinglePositionSaver2(config2,type2,"llssllslslsll")


#SPS.save_fixed_view_figure("zzzzz1",148)
SPS1.save_fixed_view_figure("iniPos",-200)
SPS2.save_fixed_view_figure("tarPos",-200)
