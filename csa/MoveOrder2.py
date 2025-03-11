from framework.programmable_cubes_UDP import ProgrammableCubes
import numpy as np
import math
from utils.CubeUtils import can_reach_n_positions

class MoveOrder:
    def __init__(self, ensemble, extremeCube, cubeTypes, lineOrder):
        self.ensemble = ensemble
        self.extremePos = ensemble[extremeCube]
        self.cubeTypes = cubeTypes
        self.lineOrder = lineOrder
        self.extremeCube = extremeCube
        self.cubes = ProgrammableCubes(np.copy(ensemble))
        self.cubeOrder = []
        self.cubeOrder.append(extremeCube)
        self.sortedEnsemble = self.sort_by_distance()
    
    def getFoundationOrder(self): 
        foundationCubes = []
        for cubeType in sorted(self.lineOrder, key=lambda k: self.lineOrder[k], reverse=False):
            nextCube = self.getNextCubeToMoveWithType(cubeType)
            foundationCubes.append(nextCube)
            self.cubeOrder.append(nextCube[0])
        return foundationCubes

    def getNextCubeToMoveWithType(self, cubeType): 
        for _,cube_id in self.sortedEnsemble: 
            if(self.cubeTypes[cube_id] == cubeType and cube_id not in self.cubeOrder): 
                if can_reach_n_positions(self.ensemble,cube_id,10):
                    # No Manipulation nessecary, therfore false
                    return (cube_id,False)
        
        for _,cube_id in self.sortedEnsemble: 
            if(self.cubeTypes[cube_id] == cubeType and cube_id): 
                # Manipulation nessecary, therfore true
                return (cube_id,True)

    def getNextCubeToMove(self):
        for _,cube_id in self.sortedEnsemble:
            if(cube_id not in self.cubeOrder):
                for move in range(6):
                    done = self.cubes.checkIfMovePossible(cube_id, move)
                    if done == 1:
                        return cube_id
        print("No moves found")
        return None

    def sort_by_distance(self):
        # Function to calculate Euclidean distance
        config = np.copy(self.ensemble)
        def euclidean_distance(coord1, coord2):
            return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2 + (coord1[2] - coord2[2]) ** 2)
        
        # Get the coordinate at the given index
        reference_coord = self.extremePos
        
        # Calculate the distances and store them along with the original coordinates and their indexes
        distances = [(coord, idx, euclidean_distance(coord, reference_coord)) for idx, coord in enumerate(config) if idx not in self.cubeOrder]
        
        # Sort by distance in descending order
        distances.sort(key=lambda x: x[2], reverse=True)
        
        # Extract the sorted coordinates with their original indexes
        sorted_coords_with_indexes = [(coord, idx) for coord, idx, dist in distances]
        
        return sorted_coords_with_indexes
    
    def getNextCube(self, currentConfig): 
        self.ensemble = np.copy(currentConfig)
        cubies = ProgrammableCubes(np.copy(currentConfig))
        sortedFilteredConfig = self.sort_by_distance()
        for _,cube_id in sortedFilteredConfig:
            for move in range(6):
                done = cubies.checkIfMovePossible(cube_id, move)
                if done == 1:
                    self.cubeOrder.append(cube_id)
                    return cube_id
        if(len(sortedFilteredConfig) == 0):
            return self.extremeCube
        
        return None