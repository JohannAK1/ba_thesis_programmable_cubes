from framework.programmable_cubes_UDP import ProgrammableCubes
import numpy as np
from move_algorithms.Mover import Mover 
import math

class CommonExtremeCubeConfigurator:
    def __init__(self,initialConfiguration, targetConfiguration):
        self.initialConfiguration = np.copy(initialConfiguration)
        self.targetConfiguration = np.copy(targetConfiguration)
        result = self.createCommonExtremePos()
        self.solvedInitialConfiguration = result[0]
        self.movesInitial = result[1]
        self.solvedTargetConfiguration = result[2]
        self.movesTarget = result[3]

    def findExtremeCube(self,ensemble):
        # Find the maximum x-coordinate
        max_x = np.max(ensemble[:, 0])
        
        # Get the indices of the points with the maximum x-coordinate
        max_x_indices = np.where(ensemble[:, 0] == max_x)[0]
        
        # Get the subset of points with the maximum x-coordinate
        max_x_points = ensemble[max_x_indices]
        
        # Find the minimum z-coordinate among the subset
        min_z = np.min(max_x_points[:, 2])
        
        # Get the indices of the points with the maximum x-coordinate and minimum z-coordinate
        min_z_indices = np.where((max_x_points[:, 2] == min_z))[0]
        
        # Get the subset of points with the maximum x-coordinate and minimum z-coordinate
        min_z_points = max_x_points[min_z_indices]
        
        # Find the maximum y-coordinate among the subset
        max_y = np.max(min_z_points[:, 1])
        
        # Get the index of the point with the maximum x-coordinate, minimum z-coordinate, and maximum y-coordinate
        max_y_index = np.where((ensemble[:, 0] == max_x) & (ensemble[:, 2] == min_z) & (ensemble[:, 1] == max_y))[0][0]
        
        return ensemble[max_y_index]

    def getUnifiedExtremePosition(self,cube_pos1, cube_pos2):
        # Find the extreme positions in both ensembles
        extreme_pos1 = self.findExtremeCube(cube_pos1)
        extreme_pos2 = self.findExtremeCube(cube_pos2)
        
        # Determine the unified extreme position
        max_x = max(extreme_pos1[0], extreme_pos2[0])
        min_y = max(extreme_pos1[1], extreme_pos2[1])
        min_z = min(extreme_pos1[2], extreme_pos2[2])
        
        unified_extreme_pos = np.array([max_x, min_y, min_z])  # Assuming y-coordinate doesn't affect the criteria
        
        return unified_extreme_pos

    def calcPath(self,ensemble,commonExtreme):
        curExtreme = self.findExtremeCube(ensemble)
        neededPostions = []

        for cord in range(3):
            while curExtreme[cord] != commonExtreme[cord]: 
                if(curExtreme[cord] > commonExtreme[cord]):
                    curExtreme[cord] -= 1
                else:
                    curExtreme[cord] += 1 
                neededPostions.append(np.copy(curExtreme))

        return neededPostions

    def getNextCubeToMove(self,sortedEnsemble,blackList,ensemble):
        cubes = ProgrammableCubes(np.copy(ensemble))
        for _,cube_id in sortedEnsemble:
            if(cube_id not in blackList):
                for move in range(6):
                    done = cubes.checkIfMovePossible(cube_id, move)
                    if done == 1:
                        return cube_id
        print("No moves found")
        return None

    def sort_by_distance(self,ensemble,commonExtremePos):
            # Function to calculate Euclidean distance
            def euclidean_distance(coord1, coord2):
                return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2 + (coord1[2] - coord2[2]) ** 2)
            
            # Get the coordinate at the given index
            reference_coord = commonExtremePos
            
            # Calculate the distances and store them along with the original coordinates and their indexes
            distances = [(coord, idx, euclidean_distance(coord, reference_coord)) for idx, coord in enumerate(ensemble)]
            
            # Sort by distance in descending order
            distances.sort(key=lambda x: x[2], reverse=True)
            
            # Extract the sorted coordinates with their original indexes
            sorted_coords_with_indexes = [(coord, idx) for coord, idx, dist in distances]
            
            return sorted_coords_with_indexes

    def moveCubesToExtremePos(self,ensemble,path,commonExtremePos): 
    
        curEnsemble = np.copy(ensemble)
        blackList = []
        movesMade = []
        for position in path: 
            sortedEnsemble = self.sort_by_distance(np.copy(curEnsemble),commonExtremePos)
            nextCube = self.getNextCubeToMove(sortedEnsemble,blackList,curEnsemble)
            mover = Mover(nextCube,np.copy(curEnsemble),np.copy(position))
            movesMade += mover.moveCube()
            curEnsemble[nextCube] = position
            blackList.append(nextCube)

        return (curEnsemble,movesMade)

    def createCommonExtremePos(self): 

        commonExtremePos = self.getUnifiedExtremePosition(np.copy(self.initialConfiguration),np.copy(self.targetConfiguration))
        pathInitial = self.calcPath(np.copy(self.initialConfiguration),commonExtremePos)
        pathTarget = self.calcPath(np.copy(self.targetConfiguration),commonExtremePos)

        config1,moves1 = self.moveCubesToExtremePos(np.copy(self.initialConfiguration),pathInitial,commonExtremePos)
        config2,moves2 = self.moveCubesToExtremePos(np.copy(self.targetConfiguration),pathTarget,commonExtremePos)

        return (config1,moves1,config2,moves2)



        
    

    

