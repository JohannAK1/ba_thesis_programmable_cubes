from framework.programmable_cubes_UDP import ProgrammableCubes
import numpy as np
import queue

def canMove(CubeID,config): 
    cubes = ProgrammableCubes(config)
    for i in range(6): 
        done = cubes.checkIfMovePossible(CubeID,i)
        if done == 1: 
            return True
    return False

def can_reach_n_positions(current_configuration, cubeID,n ):
    """
    Returns all reachable positions for a cube given its id and current configuration.
    """
    sPos = np.copy(current_configuration[cubeID])
    opposite_move = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}

    def get_possible_positions(config):
        possible_positions = []
        cubies = ProgrammableCubes(config)
        for i in range(6):
            done = cubies.apply_single_update_step(cubeID, i)
            if done == 1:
                possible_positions.append((np.copy(cubies.cube_position[cubeID]), i))
                cubies.apply_single_update_step(cubeID, opposite_move[i])
        return possible_positions

    def breadth_search(config, start_pos):
        q = queue.Queue()
        q.put(start_pos)
        seen_positions = [(start_pos, -1)]
        while not q.empty():
            cur_pos = q.get()
            # Update the configuration for the cube under consideration.
            config[cubeID] = cur_pos
            for possible in get_possible_positions(config):
                pos = possible[0]
                if not any(np.array_equal(pos, seen) for seen, _ in seen_positions):
                    q.put(pos)
                    seen_positions.append(possible)
                    if(len(seen_positions) >= n):
                        return True
        return False

    return breadth_search(np.copy(current_configuration), sPos)

def isCubeOnWrongTarget(cubePos,cubeType, targetConfig, targetTypes): 
    for target_cube_id, target_pos in enumerate(targetConfig):
        if np.array_equal(cubePos, target_pos) and cubeType != targetTypes[target_cube_id]:
            return True
    return False

def can_reach_target_n(target_pos, config,n):
    tempConfig = np.append(np.copy(config), [target_pos], axis=0)
    tempCube = len(tempConfig)-1
    return can_reach_n_positions(tempConfig, tempCube ,n)


def calcDistance(cubePos, tarhetPos): 
    return np.linalg.norm(cubePos-tarhetPos)



def differInOneAxis(cubePos1, cubePos2):
    """
    Checks if two positions differ in exactly one axis.
    
    Args:
        cubePos1: First position [x, y, z]
        cubePos2: Second position [x, y, z]
        
    Returns:
        bool: True if positions differ in exactly one axis, False otherwise
    """
    differences = 0
    for i in range(3):  # Check x, y, z coordinates
        if cubePos1[i] != cubePos2[i]:
            differences += 1
    return differences == 1