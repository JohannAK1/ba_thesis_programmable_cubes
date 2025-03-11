from framework.programmable_cubes_UDP import ProgrammableCubes
from move_algorithms.Mover import Mover 
import numpy as np  # type: ignore
import math 
from move_algorithms.ManipulateMove import ManipulateMove
from animation.Animation import CubeAnimation
from benchmark.SequenceSaver import SequenceSaver

class Solver: 
    def __init__(self, initialConfiguration, targetConfiguration, initialTypes, targetTypes):
        self.initalConfiguration =  initialConfiguration
        self.targetConfiguration = targetConfiguration
        self.initialTypes = initialTypes
        self.targetTypes = targetTypes
        self.currentConfiguration = np.copy(initialConfiguration)
        self.lockedPositions = self.find_common_positions_with_type()
        self.moveSequence = []
        self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}

    def is_adjacent(self,cube1, cube2):
        """
        Check if cube2 is adjacent to cube1
        """
        x1, y1, z1 = cube1
        x2, y2, z2 = cube2
        return (abs(x1 - x2) == 1 and y1 == y2 and z1 == z2) or \
            (x1 == x2 and abs(y1 - y2) == 1 and z1 == z2) or \
            (x1 == x2 and y1 == y2 and abs(z1 - z2) == 1)

    def count_adjacent(self,target_cube, initial_set):
        """
        Count how many cubes in initial_set are adjacent to target_cube
        """
        count = 0
        for initial_cube in initial_set:
            if self.is_adjacent(initial_cube, target_cube):
                count += 1
        return count

    def find_reachable_positions_sorted2(self):
        """
        Find indices in target that are reachable from initial positions and order by number of adjacent cubes
        """
        initial_set = set(map(tuple, self.currentConfiguration))
        reachable_positions = []

        for i, target_cube in enumerate(self.targetConfiguration):
            if tuple(target_cube) not in initial_set:
                adj_count = self.count_adjacent(target_cube, initial_set)
                if adj_count > 0:
                    reachable_positions.append((i, self.targetConfiguration[i], adj_count))

        sorted_positions = sorted(reachable_positions, key=lambda x: not self.isInReach(x[1]))
        
        return [(i, cube) for i, cube, _ in sorted_positions]

    def getNextCubeToMoveWithType(self, cubeType, targetPosition):
        sortedEnsemble = self.sort_by_num_neighbours()
        cubes = ProgrammableCubes(np.copy(self.currentConfiguration))
        movableCubes = []
        for cube_id in sortedEnsemble: 
            if(self.initialTypes[cube_id] == cubeType and cube_id not in self.lockedPositions): 
                for move in range(6):
                    done = cubes.checkIfMovePossible(cube_id, move)
                    if done == 1:
                        movableCubes.append(cube_id)
                        break
        sortedByDistance = sorted(movableCubes, key=lambda x: self.distance(x,targetPosition))
        return sortedByDistance

    def sort_by_num_neighbours(self):
        cubes = ProgrammableCubes(np.copy(self.currentConfiguration))
        # Get the lengths of each sub-array
        lengths = [len(sub_array) for sub_array in cubes.cube_neighbours]
        # Get the sorted indices based on lengths
        sorted_indices = np.argsort(lengths)       
        sorted_indices = sorted_indices[::-1]
        return sorted_indices

    def find_common_positions_with_type(self):
        """
        Find indices of positions in initial that are also in target and have the same type
        """
        target_dict = {tuple(pos): idx for idx, pos in enumerate(self.targetConfiguration)}
        common_indices = []

        for i, initial_cube in enumerate(self.initalConfiguration):
            initial_cube_tuple = tuple(initial_cube)
            if initial_cube_tuple in target_dict:
                target_idx = target_dict[initial_cube_tuple]
                if self.initialTypes[i] == self.targetTypes[target_idx]:
                    common_indices.append(i)
        return common_indices

    def updateCurrentConfiguration(self,cube,targetPosition, newMoves):
        self.lockedPositions.append(cube)
        self.currentConfiguration[cube] = targetPosition
        self.moveSequence += newMoves
  
    def getRemainingCubesofType(self,type): 
        notLocked = []
        for i in range(len(self.currentConfiguration)): 
            if(i not in self.lockedPositions and self.initialTypes[i] == type): 
                notLocked.append(i)
        return notLocked

    def sanityCheck(self,newMoves): 
        cubies = ProgrammableCubes(np.copy(self.currentConfiguration))
        smallStore = []
        for id,move in newMoves: 
            done = cubies.apply_single_update_step(id,move)
            if(not done):
                print("Move could not be made: " + str(move) + " for Cube: " + str(id))
                self.initialTypes[id] = 6
                #if(len(smallStore) != 0):
                    #CubeAnimation(smallStore,self.initialTypes,1,250,"CantMove: kkk").make_animation() 
                return False
            smallStore.append(np.copy(cubies.cube_position))
        return True
    
    def isInReach(self,gPos): 
        tempConfig = np.copy(self.currentConfiguration)
        tempConfig += gPos
        PC = ProgrammableCubes(tempConfig)
        lastCube = len(tempConfig)-1
        for m in range(6):
            if PC.checkIfMovePossible(lastCube,m): 
                return True
        return False

    def distance(self, cube, gPos): 
        cubePos = np.copy(self.currentConfiguration[cube])
        distance = np.linalg.norm(cubePos - gPos)
        return distance
    
    def isMovable(self,cube):
        PC = ProgrammableCubes(np.copy(self.currentConfiguration))
        for i in range(6):
            if PC.checkIfMovePossible(cube, i):
                return True
        return False
    
    def getMovableCubesNotLocked(self): 
        cubes = []
        for i in range (len(self.currentConfiguration)): 
            if i not in self.lockedPositions: 
                cubes.append(i)
        return cubes
    
    def applyMoves(self,moves):
        PC = ProgrammableCubes(np.copy(self.currentConfiguration))
        for c,m in moves:
            done = PC.apply_single_update_step(c,m)
            if not done: 
                print("Move could not be made: " + str(m) + " for Cube: " + str(c)) 
        return np.copy(PC.cube_position)
    
    def solve(self):
        size = len(self.initalConfiguration) 
        
        blackList = {}
        iteration_count = 0
        last_saved_percentage = 0

        possiblePossitions = self.find_reachable_positions_sorted2()

        while len(self.lockedPositions) != size: 
            print("==================================")
            percentage_done = (len(self.lockedPositions) / size) * 100
            print("Procent Done: " + str(percentage_done))

            if percentage_done - last_saved_percentage >= 5:
                SequenceSaver(movesSequence=self.moveSequence, problem='ISS', solverUsed='IPA_temp').saveSequenceToJson()
                last_saved_percentage = percentage_done

            moveFound = False
            
            possiblePossitions = self.find_reachable_positions_sorted2()
            
            if len(possiblePossitions) == 0: 
                print("No Cubes to move!!! Possible Postions empty")
                print("Moveble Cubes: " + str(self.getMovableCubesNotLocked()))
                for cube in self.getMovableCubesNotLocked():
                    moves = ManipulateMove(self.currentConfiguration,cube,[]).createTargetSpace(cube)
                    if(moves != None):
                        self.currentConfiguration = self.applyMoves(moves)
                        possiblePossitions = self.find_reachable_positions_sorted2()
                        self.moveSequence += moves
                        moveFound = True
                        break
                if(not moveFound): 
                    return self.moveSequence
            
            for targetCubeID,targetPosition in possiblePossitions: 
                targetType = self.targetTypes[targetCubeID]
                
                movableCubes = self.getNextCubeToMoveWithType(targetType,targetPosition)

                print("#################################")
                print("Goal Position: " + str(targetPosition))
                print("Cubes to Goal" + str(movableCubes))
                
                

                for cubeToMove in movableCubes:
                    if targetCubeID in blackList and blackList[targetCubeID] < iteration_count + 5:
                        print("There are more worlds than these, cube is on black list")
                        break
                    elif targetCubeID in blackList and blackList[targetCubeID] >= iteration_count + 5:
                        del blackList[targetCubeID]
                    
                    print("---------------------------------")
                    print("Check cube: " + str(cubeToMove))
                    

                    m = Mover(cubeToMove,self.currentConfiguration,targetPosition)
                    cubeMoves = m.moveCube()
                    
                    if(cubeMoves == None):
                        print("Path obstructed, trying to free target position")
                        
                        if targetCubeID != possiblePossitions[-1][0]:
                            print("There are more worlds than these")
                            blackList[targetCubeID] = iteration_count
                            break

                        freeSpaceMoves = ManipulateMove(self.currentConfiguration,cubeToMove,targetPosition).freeSpaceMove()
                        
                        

                        if(freeSpaceMoves == None): 
                            print("No Goal Manipulation Possible")
                            break
                        else: 
                            if(self.sanityCheck(freeSpaceMoves)):
                                self.updateCurrentConfiguration(cubeToMove,targetPosition,freeSpaceMoves)
                                moveFound = True
                                print("Cube moved with clear Landing: " + str(freeSpaceMoves))
                                break
                            else: 
                                print("Error with move sequence in clear landing")
                                print("Trying next Cube")
                                return []
                    else:  
                        if(self.sanityCheck(cubeMoves)):
                            moveFound = True
                            self.updateCurrentConfiguration(cubeToMove,targetPosition,cubeMoves)
                            print("Cube moved: " + str(cubeToMove))
                            break
                        else: 
                                print("Error with move sequence")
                                return []
                iteration_count += 1      
                
                if(moveFound):
                    break  
            if (not moveFound and len(possiblePossitions) != 0):
                print("IS NEEDED!!!!")
                for posPos in possiblePossitions: 
                    print(possiblePossitions)
                    gPos = posPos[1]
                    cubeToMove = self.getRemainingCubesofType(self.targetTypes[posPos[0]])
                    print(cubeToMove)
                    print("Goal Pos Solver: " + str(gPos))
                    moves = ManipulateMove(self.currentConfiguration,cubeToMove[0],gPos).freeCubeAndSpaceMove()
                    if moves != None: 
                        if(self.sanityCheck(moves)):
                            print("##########")
                            print("Moves made!!!!")
                            print("##########")
                            
                            moveFound = True
                            self.updateCurrentConfiguration(cubeToMove[0],gPos,moves)
                            break
                        else: 
                            print("Moves could not be made! Free Cube Space Move!")
                            return self.moveSequence 
                if(not moveFound): 
                    return self.moveSequence
        return self.moveSequence
    


