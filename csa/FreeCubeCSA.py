import numpy as np
import queue
from framework.programmable_cubes_UDP import ProgrammableCubes
import sys
import hashlib
from utils.ConfigurationUtils import movesToPositions


class FreeCubeCSA: 
    def __init__(self, configuration, cubeID, layer, bounds,cubesNeeded,movesNeeded):
        self.configuration = np.copy(configuration)
        self.cubeID = cubeID
        self.sPos = np.copy(self.configuration[self.cubeID])

        self.bounds = bounds
        self.layer = layer
        self.cubesNeeded = cubesNeeded
        self.movesNeeded = movesNeeded
        
        self.startLayerPositions = self.getLayerPositions(self.configuration)

        self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}

    def getLayerPositions(self, position): 
        return [coord for coord in position if self.isInBounds(coord)]

    def moves2Changes(self, newPos):
        newLayerPos = self.getLayerPositions(newPos)
        
        # Finde die Positionen in newLayerPos, die nicht in startLayerPositions sind
        addedPositions = [tuple(element) for element in newLayerPos if not any(np.array_equal(element, b_elem) for b_elem in self.startLayerPositions)]
        
        # Finde die Positionen in startLayerPositions, die nicht in newLayerPos sind
        removedPositions = [tuple(element) for element in self.startLayerPositions if not any(np.array_equal(element, b_elem) for b_elem in newLayerPos)]
        # Kombiniere hinzugefügte und entfernte Positionen
        changedPositions = addedPositions + removedPositions
        return tuple(sorted(changedPositions))

    def isKnownPosition(self, newPos):
        changedPositions = self.moves2Changes(newPos)
        state_hash = hashlib.md5(str(changedPositions).encode()).hexdigest()
        if state_hash in self.knownPositions:
            return True
        else:
            self.knownPositions.add(state_hash)
            return False

    def moves2Position(self, moves): 
        cubes = ProgrammableCubes(self.configuration)
        for cID, move in moves: 
            done = cubes.apply_single_update_step(cID, move)
            if not done: 
                print("Layer free Cube: Move could not be made")
                sys.exit()
        return cubes.cube_position

    def getPossibleMoves(self, position, moveSeuqence): 
        possibleMoves = []
        moveChecker = ProgrammableCubes(np.copy(position))

        for cube in self.cubesNeeded: 
            if cube == self.cubeID:
               for m in self.movesNeeded:
                    if moveChecker.checkIfMovePossible(cube, m): 
                            return [(cube, m)]
            for move in self.movesNeeded:
                if (cube,self.oppositeMove[move]) not in moveSeuqence and moveChecker.checkIfMovePossible(cube, move):
                    possibleMoves.append((cube, move))
        return possibleMoves

    def isInBounds(self,position):

        sPos = np.copy(self.sPos)

        lowerBound = []
        upperBound = []
        for i,offset in enumerate(self.bounds):
            if(offset == 2): 
                lowerBound.append(sPos[i]-1)
                upperBound.append(sPos[i]+1) 
            if offset == 1: 
                lowerBound.append(-50000)
                upperBound.append(sPos[i]+offset)
            if offset == -1:
                lowerBound.append(sPos[i]+offset)
                upperBound.append(50000)

        # Check if position is within bounds
        for i, coord in enumerate(position):
            if coord < lowerBound[i] or coord > upperBound[i]:
                return False
        
        return True

    def freeCube(self): 
        if(self.layer == -1):
            return None
        
        self.knownPositions = set()

        q = queue.Queue()
        initial_moves = self.getPossibleMoves(self.configuration, [])

        for cubeMove in initial_moves:
            if cubeMove[0] == self.cubeID:
                movesToPositions([cubeMove], self.configuration)
                return [cubeMove] # nothing to do, the cube is free
            q.put([cubeMove])

        while not q.empty():
            move_sequence = q.get()
            new_position = self.moves2Position(move_sequence)
            if not self.isKnownPosition(new_position):
                for cubeMove in self.getPossibleMoves(new_position, move_sequence):
                    if cubeMove[0] == self.cubeID:
                        new_sequence = move_sequence
                        print("___________")
                        print("Freeing Cube: " + str(self.cubeID))
                        print("Sequnce to free: " + str(new_sequence))
                        return new_sequence
                    else:
                        if(len(self.knownPositions) > 5000):
                            print("FreeCube: Could not free cube in quarter: " + str(self.cubesNeeded))
                            return None
                        new_sequence = move_sequence + [cubeMove]
                        q.put(new_sequence)
        return None
        
          