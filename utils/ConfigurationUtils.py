import queue
import numpy as np
from framework.programmable_cubes_UDP import ProgrammableCubes
import sys 
from debug.ipaDebug import saveErrorConfig


class ReachablePositions:
    def __init__(self, currentConfiguration,cubeID):
          self.currentConfiguration = np.copy(currentConfiguration)
          self.cubeID = cubeID
          self.sPos = np.copy(self.currentConfiguration[cubeID])
          self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}

    def getAllReachablePositions(self):
        seenPositions = self.breadthSearch()
        return [pos for pos,_ in seenPositions]    

    def breadthSearch(self):
        q = queue.Queue()
        q.put(self.sPos)
        seenPositions = [(self.sPos, -1)]
        while (q.not_empty): 
            if(q.qsize() == 0): break
            curPos = q.get()
            self.currentConfiguration[self.cubeID] = curPos
            for possiblePos in self.getPossiblePositions():
                if not any(np.array_equal(possiblePos[0], seen_pos) for seen_pos,_ in seenPositions): 
                    q.put(possiblePos[0])
                    seenPositions.append(possiblePos)
        return seenPositions

    def getPossiblePositions(self): 
        possiblePositions = []
        cubies = ProgrammableCubes(self.currentConfiguration)
        for i in range(6): 
            done = cubies.apply_single_update_step(self.cubeID,i)
            if(done == 1): 
                possiblePositions.append((np.copy(cubies.cube_position[self.cubeID]),i))
                cubies.apply_single_update_step(self.cubeID,self.oppositeMove[i])
        return possiblePositions


def get_all_reachable_positions(current_configuration, cubeID):
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
        return seen_positions

    seen = breadth_search(np.copy(current_configuration), sPos)
    # Return only the positions (not the move indices)
    return [pos for pos, _ in seen]

def movesToPositions(moves, initPos):
    cubes = ProgrammableCubes(np.copy(initPos))
    for cID, move in moves: 
        done = cubes.apply_single_update_step(cID, move)
        if not done: 
            print("Move could not be made")
            print("Moves: " + str(moves))
            print("Cube ID: " + str(cID))
            print("Move: " + str(move))
            sys.exit()
    return np.copy(cubes.cube_position)


def movesToPositionsDebug(moves, initPos, gPos, cubeID, method):
    cubes = ProgrammableCubes(np.copy(initPos))
    for cID, move in moves: 
        done = cubes.apply_single_update_step(cID, move)
        if not done: 
            print("Move could not be made")
            print("Moves: " + str(moves))
            print("Cube ID: " + str(cID))
            print("Move: " + str(move))
            saveErrorConfig(np.copy(initPos), cubeID, gPos, method)
            return None

    return np.copy(cubes.cube_position)

def getAverageCubeNeighbours(config):
    """
    Returns the density of the cubes in the configuration.
    """
    cubes = ProgrammableCubes(config)
    sum = 0
    for cube in cubes.cube_neighbours:
        sum += len(cube)
    return sum / len(cubes.cube_neighbours)

def overLappingCubes(intialConfig, TargetConfig):
    sum = 0
    for pos in intialConfig:
        if pos in TargetConfig:
            sum += 1
    return sum/len(intialConfig) 

def isNeighbour(cube1_pos, cube2_pos):
    x1, y1, z1 = cube1_pos
    x2, y2, z2 = cube2_pos
    return (abs(x1 - x2) == 1 and y1 == y2 and z1 == z2) or \
           (x1 == x2 and abs(y1 - y2) == 1 and z1 == z2) or \
           (x1 == x2 and y1 == y2 and abs(z1 - z2) == 1)

def count_neighbours(target_pos,config):
        count = 0
        for cubePos in config:
            if isNeighbour(cubePos, target_pos):
                count += 1
        return count

def find_correct_cubes(initialConfiguration, targetConfiguration, initialTypes, targetTypes):
    """
    Find indices of positions in initial that are also in target and have the same type
    """
    target_dict = {tuple(pos): idx for idx, pos in enumerate(targetConfiguration)}
    common_indices = []

    for i, initial_cube in enumerate(initialConfiguration):
        initial_cube_tuple = tuple(initial_cube)
        if initial_cube_tuple in target_dict:
            target_idx = target_dict[initial_cube_tuple]
            if initialTypes[i] == targetTypes[target_idx]:
                common_indices.append(i)
    return common_indices

def getAllCubesOfType(type, typeList): 
    return [cubeID for cubeID,cube_type in enumerate(typeList) if cube_type == type]


def hasTwoEqualCoords(pos1, pos2):
    return np.sum(pos1 == pos2) == 2