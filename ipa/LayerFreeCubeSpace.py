import numpy as np
import queue
from framework.programmable_cubes_UDP import ProgrammableCubes
from ipa.LayerCubes import LayerCubes
import hashlib

class LayerFreeCubeSpace: 
    def __init__(self, configuration, cubeID, gPos):
        self.startConfiguration = np.copy(configuration)
        self.gPos = np.copy(gPos)
        self.goalConfiguration = np.copy(configuration)
        self.goalConfiguration[cubeID] = self.gPos
        self.cubeID = cubeID
        
        self.cubesNeeded = LayerCubes(self.goalConfiguration,self.cubeID).getCubesNeededSets()
        
        self.layer = self.cubesNeeded[0][0] 
        self.cubeLayerCoord = self.goalConfiguration[cubeID][self.layer]
        self.startLayerPositions = self.getLayerPositions(self.goalConfiguration)
        

        self.layer2moves = {
            0: [2,3],
            1: [4,5],
            2: [0,1]
        }
        
        self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}

        self.knownPositions = set()

    def updateLayer(self,layer):
        self.layer = layer
        self.cubeLayerCoord = self.goalConfiguration[self.cubeID][layer]
        self.startLayerPositions = self.getLayerPositions(self.goalConfiguration)

    def getLayerPositions(self, position): 
        return [coord for coord in position if coord[self.layer] == self.cubeLayerCoord]

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
        cubes = ProgrammableCubes(self.goalConfiguration)
        for cID, move in moves: 
            done = cubes.apply_single_update_step(cID, move)
            if not done: 
                print("Layer free Space: Move could not be made 2 pos")
        return cubes.cube_position
    
    def moves2SPosition(self, moves): 
        cubes = ProgrammableCubes(self.startConfiguration)
        for cID, move in moves: 
            done = cubes.apply_single_update_step(cID, move)
            if not done: 
                print("Layer free Space: Move could not be made 2 pos")
                print("Cube: " + str(cID) + " Move: " + str(move))
        return cubes.cube_position
    
    def getPossibleMoves(self, sPosition, gPosition, moveSequence, cubesNeeded): 
        possibleMoves = []
        moveChecker1 = ProgrammableCubes(sPosition)
        moveChecker2 = ProgrammableCubes(gPosition)
        for cube in cubesNeeded: 
            if cube == self.cubeID:
               for m in self.layer2moves[self.layer]:
                    if moveChecker2.checkIfMovePossible(cube, m): 
                            return [(cube, m)]
            for move in self.layer2moves[self.layer]: 
                if (cube,self.oppositeMove[move]) not in moveSequence:
                    if moveChecker2.checkIfMovePossible(cube, move) and moveChecker1.checkIfMovePossible(cube, move):
                        possibleMoves.append((cube, move))
        return possibleMoves

    def freeCubeSpace(self): 
        c = 0
        for layer,cubes,_ in self.cubesNeeded:
            if c > 3:
                return None
            c += 1
            self.updateLayer(layer)
            self.knownPositions = set()
        
            q = queue.Queue()
            initial_moves = self.getPossibleMoves(self.startConfiguration, self.goalConfiguration,[], cubes)
            for cubeMove in initial_moves:
                if cubeMove[0] == self.cubeID:
                    return [] # nothing to do space is free
                q.put([cubeMove])

            while not q.empty():
                move_sequence = q.get()

                goal_Position = self.moves2Position(move_sequence)
                
                if not self.isKnownPosition(goal_Position):
                    new_sPosition = self.moves2SPosition(move_sequence)
                    for cubeMove in self.getPossibleMoves(new_sPosition, goal_Position, move_sequence,cubes):
                        if cubeMove[0] == self.cubeID:
                            return move_sequence
                        new_sequence = move_sequence + [cubeMove]
                        q.put(new_sequence)
                if(len(self.knownPositions) > 1000):
                    print("LayerFreeCubeSpace: Too many known positions")
                    break
        return None
