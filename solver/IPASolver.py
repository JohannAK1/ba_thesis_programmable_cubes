from move_algorithms.Mover import Mover 
import numpy as np  # type: ignore
from move_algorithms.ManipulateMove import ManipulateMove
from utils.ConfigurationUtils import find_correct_cubes,movesToPositions,hasTwoEqualCoords
from ipa.SelectionHeuritsics import SelectionHeuristics
from benchmark.SequenceSaver import SequenceSaver
import time


class Solver: 
    def __init__(self, initialConfiguration, targetConfiguration, initialTypes, targetTypes, logProgress = False):
        self.targetConfiguration = np.copy(targetConfiguration)
        self.currentConfiguration = np.copy(initialConfiguration)
        self.initialTypes = initialTypes
        self.targetTypes = targetTypes
        self.lockedPositions = find_correct_cubes(initialConfiguration,targetConfiguration,initialTypes,targetTypes)
        self.moveSequence = []
        self.SH = SelectionHeuristics(self.currentConfiguration,self.targetConfiguration,self.initialTypes,self.targetTypes,self.lockedPositions)
        self.startTime = 0
        self.logProgress = logProgress
    
    def updateCurrentConfiguration(self, newMoves,cube):
        self.currentConfiguration = np.copy(movesToPositions(newMoves,self.currentConfiguration))
        if(cube != -1):
            self.lockedPositions.append(cube)
        self.SH = SelectionHeuristics(self.currentConfiguration,self.targetConfiguration,self.initialTypes,self.targetTypes,self.lockedPositions)
        self.moveSequence += newMoves

    def solve(self):
        self.startTime = time.time()
        oldProgress = len(self.lockedPositions)/len(self.currentConfiguration)
        while len(self.lockedPositions) != len(self.currentConfiguration): 
            
            currentProgress = len(self.lockedPositions)/len(self.currentConfiguration)
            if currentProgress > oldProgress + 0.02 and self.logProgress:
                print("Progress: " + str(currentProgress))
                SS = SequenceSaver(self.moveSequence,"enterprise","ipa")
                SS.saveSequenceToJson()
                oldProgress = currentProgress

            
            print("==================================")
            
            # returns all target positions that can be reached sorted by lowest x-coordinate
            targetPositions = self.SH.allTargetPositionsSortedCoord_N(5,0)
            
            if(len(targetPositions) == 0): 
                # returns all target positions
                targetPositions = self.SH.allTargetPositions()
            moveFound = False
            
            if len(targetPositions) == 0: 
                # returns call cubes that can move and are not on correct position
                movableCubes = self.SH.getAllMovableCubes()
                if(len(movableCubes) == 0):
                    print("No movable Cubes, select Remaining Cubes!")
                    # return all cubes that are on correct postion 
                    movableCubes = self.SH.getCubesNotLocked()
                print("Moveble Cubes: " + str(movableCubes))
                print("Num lockedCubes: " + str(len(self.lockedPositions)))
                for cube_id,_ in movableCubes:
                    moves = ManipulateMove(self.currentConfiguration,cube_id,[]).createTargetSpace(cube_id)
                    if(moves != None):
                        self.updateCurrentConfiguration(moves,-1)
                        print("New TargetPositons: " + str(targetPositions))
                        moveFound = True
                        break
                if(not moveFound): 
                    return self.moveSequence
            
            for tar_pos,tar_type in targetPositions:
                #returns all cubes of a type sorted that move storted by shortest distance.  
                movableCubes = self.SH.getTypeCubes_Distance_N(tar_type,tar_pos,5)
                
                print("#################################")
                print("Goal Position: " + str(tar_pos))

                for cube_id,_ in movableCubes:
                    
                    print("---------------------------------")
                    print("Check cube: " + str(cube_id))
                    

                    m = Mover(cube_id,self.currentConfiguration,tar_pos)
                    cubeMoves = m.moveCube()
                    
                    if cubeMoves == None and not hasTwoEqualCoords(tar_pos,self.currentConfiguration[cube_id]):
                        print("Path obstructed, trying to free target position")
                        freeSpaceMoves = ManipulateMove(self.currentConfiguration,cube_id,tar_pos).freeSpaceMove()
                        
                        if(freeSpaceMoves == None): 
                            print("No Goal Manipulation Possible")
                            break
                        else: 
                            self.updateCurrentConfiguration(freeSpaceMoves,cube_id)
                            moveFound = True
                            print("Cube moved with clear Landing: " + str(freeSpaceMoves))
                            break
                    elif cubeMoves == None:
                        print("Should not move this cube, not far from target")
                        continue
                    else:  
                            moveFound = True
                            self.updateCurrentConfiguration(cubeMoves,cube_id)
                            print("Cube moved: " + str(cube_id))
                            break  
                if(moveFound):
                    break  
            if (not moveFound and len(targetPositions) != 0):
                cubesNotFreeable = []
                print("Cube needs to be freed")
                for tar_pos,tar_type in targetPositions: 

                    # returns all cubes of a type sorted that are not on on the correct posiotn but cant move 
                    blockedCubes = self.SH.getTypeCubesNotLocked(tar_type)
                    for cube_id,_ in blockedCubes:
                        if cube_id not in cubesNotFreeable and not hasTwoEqualCoords(tar_pos,self.currentConfiguration[cube_id]):
                            print("Check cube: " + str(cube_id))
                            moves = ManipulateMove(self.currentConfiguration,cube_id,tar_pos).freeCubeAndSpaceMove()
                            if moves != None:                    
                                moveFound = True
                                self.updateCurrentConfiguration(moves,cube_id)
                                print("Cube freed and moved: " + str(cube_id))
                                cubesNotFreeable = []
                                break
                            else : 
                                cubesNotFreeable.append(cube_id)
                    if(moveFound):
                        break
                if(not moveFound): 
                    return self.moveSequence
        
        
        
        return self.moveSequence
    


