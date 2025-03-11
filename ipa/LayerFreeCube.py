import numpy as np
import queue
from framework.programmable_cubes_UDP import ProgrammableCubes
from ipa.LayerCubes import LayerCubes
import sys
import hashlib
from utils.CubeUtils import can_reach_n_positions


class LayerFreeCube: 
    def __init__(self, configuration, cubeID, gPos=[-500,-500,-500]):
        self.configuration = np.copy(configuration)
        self.cubeID = cubeID

        self.sPos = np.copy(self.configuration[self.cubeID])

        self.quarterCubesNeeded = LayerCubes(self.configuration,self.cubeID).getCubesNeededSetsDependend_Bounds()   
        print("QuarterCubesNeeded (Free Cube): " + str(self.quarterCubesNeeded))


        if(len(self.quarterCubesNeeded) == 0):
            self.layer = -1
            self.bounds = []
        else:
            self.layer = self.quarterCubesNeeded[0][0] 
            self.bounds = self.quarterCubesNeeded[0][3]
        self.cubeLayerCoord = self.configuration[cubeID][self.layer]
        self.startLayerPositions = self.getLayerPositions(self.configuration)

        if(len(gPos) == 0):
            self.gPos = [-500,-500,-500]
        else:
            self.gPos = np.copy(gPos)

        self.layer2xyz= {
            0: [1,2],
            1: [0,2],
            2: [0,1]
        }

        self.layer2moves = {
            0: [2,3],
            1: [4,5],
            2: [0,1]
        }

        self.cubesNeeded = []

        self.knownPositions = set()

        self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}

    def updateLayer(self,layer,bounds):
        self.layer = layer
        self.bounds = bounds
        self.cubeLayerCoord = self.configuration[self.cubeID][layer]
        self.startLayerPositions = self.getLayerPositions(self.configuration)


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
        cubes = ProgrammableCubes(self.configuration)
        for cID, move in moves: 
            done = cubes.apply_single_update_step(cID, move)
            if not done: 
                print("Layer free Cube: Move could not be made")
                sys.exit()
        return cubes.cube_position

    def getLayerCubes(self, position): 
        return [i for i, coord in enumerate(position) if coord[self.layer] == self.cubeLayerCoord]
    
    def getPossibleMoves(self, position, moveSeuqence,cubesNeeded): 
        possibleMoves = []
        moveChecker = ProgrammableCubes(np.copy(position))
        for cube in cubesNeeded: 
            if cube == self.cubeID:
               for m in self.layer2moves[self.layer]:
                    if moveChecker.checkIfMovePossible(cube, m): 
                            return [(cube, m)]
            for move in self.layer2moves[self.layer]:
                if (cube,self.oppositeMove[move]) not in moveSeuqence:
                    if moveChecker.apply_single_update_step(cube, move):
                        tempGoal = np.copy(moveChecker.cube_position)
                        if self.isOnBounds(tempGoal[cube]):
                            tempGoal[self.cubeID] = self.gPos
                            moverChecker2 = ProgrammableCubes(tempGoal)
                            if (moverChecker2.checkIfMovePossible(cube, self.oppositeMove[move])):
                                possibleMoves.append((cube, move))
                        moveChecker.apply_single_update_step(cube,self.oppositeMove[move])
        return possibleMoves

    def isOnBounds(self, position):
        fst_coord = self.bounds[0]
        snd_coord = self.bounds[1]

        sPos = np.copy(self.sPos)

        fst_C_coord = sPos[fst_coord[0]] + fst_coord[1]
        snd_C_coord = sPos[snd_coord[0]] + snd_coord[1]

        fst_P_coord = position[fst_coord[0]]
        snd_P_coord = position[snd_coord[0]]

        check1 = fst_coord[1] == 1 and fst_P_coord <= fst_C_coord or fst_coord[1] == -1 and fst_P_coord >= fst_C_coord
        check2 = snd_coord[1] == 1 and snd_P_coord <= snd_C_coord or snd_coord[1] == -1 and snd_P_coord >= snd_C_coord
        #if not check1 and check2: 
            #print("Is not in bounds: " + str(position))
            #print("Bounds: " + str(self.bounds))
            #print("Start Position: " + str(self.sPos))
        return check1 and check2

    def freeCube(self): 
        if(self.layer == -1):
            return None
        for layer,cubes,_,bounds in self.quarterCubesNeeded:

            self.updateLayer(layer,bounds)
            self.knownPositions = set()

            q = queue.Queue()
            initial_moves = self.getPossibleMoves(self.configuration, [], cubes)

            for cubeMove in initial_moves:
                if cubeMove[0] == self.cubeID:
                    return [] # nothing to do, the cube is free
                q.put([cubeMove])

            exceeded_limit = False
            while not q.empty() and not exceeded_limit:
                move_sequence = q.get()
                new_position = self.moves2Position(move_sequence)
                if not self.isKnownPosition(new_position):
                    for cubeMove in self.getPossibleMoves(new_position, move_sequence, cubes):
                        if cubeMove[0] == self.cubeID:
                            new_sequence = move_sequence
                            print("___________")
                            print("Freeing Cube: " + str(self.cubeID))
                            print("Sequnce to free: " + str(new_sequence))
                            return new_sequence
                        else:
                            if(len(self.knownPositions) > 1000):
                                print("FreeCube: Could not free cube in quarter: " + str(cubes))
                                exceeded_limit = True
                                break
                            new_sequence = move_sequence + [cubeMove]
                            q.put(new_sequence)
                    if exceeded_limit:
                        break
            print("FreeCube: Could not free cube in quarter: " + str(cubes))
        return None