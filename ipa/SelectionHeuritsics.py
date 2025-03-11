import numpy as np
from framework.programmable_cubes_UDP import ProgrammableCubes
from utils.ConfigurationUtils import count_neighbours
from utils.CubeUtils import canMove,can_reach_n_positions, isCubeOnWrongTarget, can_reach_target_n, calcDistance

class SelectionHeuristics: 
    def __init__(self, currentConfiguration, targetConfiguration, initialTypes, targetTypes, lockedCubes):
        self.currentConfiguration = np.copy(currentConfiguration)
        self.targetConfiguration = np.copy(targetConfiguration)
        self.initialTypes = initialTypes
        self.targetTypes = targetTypes
        self.lockedCubes = lockedCubes

    def allTargetPositions(self):
        reachable_positions = []
        initial_positions = set(map(tuple, self.currentConfiguration))
        for i, target_pos in enumerate(self.targetConfiguration):
            if tuple(target_pos) not in initial_positions:
                adj_count = count_neighbours(target_pos, self.currentConfiguration)
                if adj_count > 0:
                    reachable_positions.append((target_pos, self.targetTypes[i]))
        return reachable_positions

    def getAllTargetPositionsReachableByN(self, n):
        allTargetPositions = self.allTargetPositions()
        return [tarPos for tarPos in allTargetPositions if can_reach_target_n(np.copy(tarPos[0]),self.currentConfiguration,n)]

    def allMovableCubesByType(self):
        movabelCubesByType = {}
        for id, cubePos in enumerate(self.currentConfiguration):
            if id not in self.lockedCubes and canMove(id,self.currentConfiguration):
                cubeType = self.initialTypes[id]
                if cubeType not in movabelCubesByType:
                    movabelCubesByType[cubeType] = []
                movabelCubesByType[cubeType].append((id,cubePos))
        return movabelCubesByType
    
    def getAllMovableCubes(self):
        movableCubes = []
        for id, cubePos in enumerate(self.currentConfiguration):
            if id not in self.lockedCubes and canMove(id,self.currentConfiguration):
                movableCubes.append((id,cubePos))
        return movableCubes
    
    def getAllCubesThatMoveN(self,n, type):
        movabelCubesByType = self.allMovableCubesByType()
        if(type not in movabelCubesByType):
            return []
        return [cube for cube in movabelCubesByType[type] if can_reach_n_positions(self.currentConfiguration,cube[0],n)]
    
    def getAllCubesOfTypeOnWrongTarget(self,type):
        movabelCubesByType = self.allMovableCubesByType()
        if(type not in movabelCubesByType):
            return []
        return [cube for cube in movabelCubesByType[type] if not isCubeOnWrongTarget(cube[1], type, self.targetConfiguration, self.targetTypes)]
    
    def getAllCubesOfTypeOnWrongTarget_N(self,n,type):
        cubes = self.getAllCubesThatMoveN(n,type)
        if len(cubes) == 0:
            return []
        return [cube for cube in cubes if not isCubeOnWrongTarget(cube[1], type, self.targetConfiguration, self.targetTypes)]

    def getTypeCubes_Distance_N(self,type,tarPos,n): 
        cubes = self.getAllCubesThatMoveN(n,type)
        return sorted(cubes, key=lambda x: calcDistance(x[1],tarPos))
    
    def getTypeCubes_Distance_Target_N(self,type,tarPos,n): 
        cubes = self.getAllCubesOfTypeOnWrongTarget_N(n,type)
        if len(cubes) == 0:
            return []
        return sorted(cubes, key=lambda x: calcDistance(x[1],tarPos))

    def getTypeCubesNotLocked(self,type): 
        notLockedCubes = []
        for id, cubePos in enumerate(self.currentConfiguration):
            cubeType = self.initialTypes[id]
            if id not in self.lockedCubes and cubeType == type:
                notLockedCubes.append((id,cubePos))
        return notLockedCubes
    
    def getCubesNotLocked(self): 
        notLockedCubes = []
        for id, cubePos in enumerate(self.currentConfiguration):
            if id not in self.lockedCubes:
                notLockedCubes.append((id,cubePos))
        return notLockedCubes
    
    def allTargetPositionsSortedNeighboursN(self,n):
        targetPositions = self.getAllTargetPositionsReachableByN(n)
        sorted(targetPositions, key=lambda x: count_neighbours(x[0], self.currentConfiguration))
        return targetPositions
    
    def allTargetPositionsSortedCoord_N(self,n,axis):
        targetPositions = self.getAllTargetPositionsReachableByN(n)
        return sorted(targetPositions, key=lambda x: x[0][axis])
    
    def getAllCubesType_Neighbours_N(self,type,n):
        cubes = self.getAllCubesThatMoveN(n,type)
        return sorted(cubes, key=lambda x: count_neighbours(x[1], self.currentConfiguration))