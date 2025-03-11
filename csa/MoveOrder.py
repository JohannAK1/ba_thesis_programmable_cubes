from framework.programmable_cubes_UDP import ProgrammableCubes
import numpy as np
import math

class MoveOrder:
    def __init__(self, ensemble, extremeCube, cubeTypes, lineOrder):
        self.ensemble = ensemble
        self.extremePos = ensemble[extremeCube]
        self.cubeTypes = cubeTypes
        self.lineOrder = lineOrder
        self.extremeCube = extremeCube
        self.cubes = ProgrammableCubes(np.copy(ensemble))
        self.sortedEnsemble = self.sort_by_distance()
        self.cubeOrder = []
        self.size = len(ensemble)
        self.curStoreLine = np.copy(self.extremePos)
        self.curStoreLine[0] += 1
        self.cubeOrder.append(extremeCube)
        self.curEnsemble = np.copy(ensemble)
        self.foundationProblems = []

    def updateCubes(self,nextCube): 
        self.curEnsemble[nextCube] = np.copy(self.curStoreLine)
        self.curStoreLine[0] += 1
        self.cubes = ProgrammableCubes(np.copy(self.curEnsemble))
    
    def getFoundationOrder(self): 
        foundationCubeOrder = []
        for cubeType in sorted(self.lineOrder, key=lambda k: self.lineOrder[k], reverse=False):
            nextCube = self.getNextCubeToMoveWithType(cubeType)
            if nextCube == None or nextCube in self.cubeOrder:
                print("Random Cube choosen!")
                nextCube = self.getNextCubeToMove()
                self.foundationProblems.append((cubeType,nextCube))
                
            self.cubeOrder.append(nextCube)    
            foundationCubeOrder.append(nextCube)
            self.updateCubes(nextCube)
        return foundationCubeOrder
    
    def getNextCubeToMoveWithType(self, cubeType): 
        for _,cube_id in self.sortedEnsemble: 
            if(self.cubeTypes[cube_id] == cubeType and cube_id not in self.cubeOrder): 
                for move in range(6):
                    done = self.cubes.checkIfMovePossible(cube_id, move)
                    if done == 1:
                        return cube_id
        print("No movable Cube with type: " + str(cubeType))
        return None

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
        def euclidean_distance(coord1, coord2):
            return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2 + (coord1[2] - coord2[2]) ** 2)
        
        # Get the coordinate at the given index
        reference_coord = self.extremePos
        
        # Calculate the distances and store them along with the original coordinates and their indexes
        distances = [(coord, idx, euclidean_distance(coord, reference_coord)) for idx, coord in enumerate(self.ensemble)]
        
        # Sort by distance in descending order
        distances.sort(key=lambda x: x[2], reverse=False)
        
        # Extract the sorted coordinates with their original indexes
        sorted_coords_with_indexes = [(coord, idx) for coord, idx, dist in distances]
        
        return sorted_coords_with_indexes

    def getToLineMoveOrder(self):
        lineCubeOrder = [] 
        while len(self.cubeOrder) < self.size: 
            nextCube = self.getNextCubeToMove()
            if(nextCube == None): 
                print("No movable Cube Found!")
                break
            else: 
                self.cubeOrder.append(nextCube)
                lineCubeOrder.append(nextCube)
            self.updateCubes(nextCube)
        return lineCubeOrder

    def findLastCubeFromType(self,lineCubeOrder,type): 
        list.reverse(lineCubeOrder)
        for id in lineCubeOrder: 
            if(self.cubeTypes[id] == type):
                return id

    def fixFoundation(self,lineCubeOrder):
        foundationFixOrder = []
        list.reverse(self.foundationProblems)

        for c_type,cube in self.foundationProblems: 
            newFoundationCube = self.findLastCubeFromType(list.copy(lineCubeOrder),c_type)
            foundationFixOrder.append((cube,newFoundationCube))
        foundationFixOrder.append((self.extremeCube,-1))
        return foundationFixOrder

    def calculateMoveOrder(self): 
        fco = self.getFoundationOrder()
        lco = self.getToLineMoveOrder()
        ffo = self.fixFoundation(lco)
        return (fco,lco,ffo)