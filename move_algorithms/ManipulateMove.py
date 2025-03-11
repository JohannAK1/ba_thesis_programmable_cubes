import numpy as np 
from ipa.LayerFreeCubeSpace import LayerFreeCubeSpace as LFCS
from ipa.LayerFreeCube import LayerFreeCube as LFC
from framework.programmable_cubes_UDP import ProgrammableCubes
from move_algorithms.Mover import Mover
from utils.ConfigurationUtils import ReachablePositions,movesToPositionsDebug

class ManipulateMove: 
    def __init__(self, configuration, cubeID, gPos):
          self.configuration = np.copy(configuration)
          self.cubeID = cubeID
          self.gPos = np.copy(gPos)
          print("SPos = " + str(self.configuration[self.cubeID]) + " GPos = " + str(self.gPos))
          self.initConfig = np.copy(configuration)
        
    def freeSpaceMove(self): 
        movesToFree = LFCS(self.configuration,self.cubeID,self.gPos).freeCubeSpace()
        print("moves to free Space: " + str(movesToFree))
        if movesToFree != None and self.sanityCheck(movesToFree,self.configuration):
            tempPosition = self.moves2Position2(movesToFree,self.configuration)
            if(tempPosition is None):
                return None
            movesToGoal = Mover(self.cubeID,tempPosition,self.gPos).moveCube()
    
            if(movesToGoal != None): 
                moves = []
                moves += movesToFree
                moves += movesToGoal
                moves += self.reverseMoves(movesToFree)
                print("Manipulator Moves: " + str(moves))
                if self.moves2Position2(moves,self.initConfig) is None:
                    print("ManipulateMove: Could not make moves!")
                    return None
                return moves
            else: 
                print("FreeSpaceMove: No path to Space found")
        else: 
                print("FreeSpaceMove: Space could not be freed")
        return None
    
    def freeSpaceMove2(self,config): 
        movesToFree = LFCS(config,self.cubeID,self.gPos).freeCubeSpace()
        print("moves to free Space: " + str(movesToFree))
        if movesToFree != None :
            tempPosition = self.moves2Position2(movesToFree,config)
            if tempPosition is None:
                return None
            movesToGoal = Mover(self.cubeID,tempPosition,self.gPos).moveCube()
            if(movesToGoal != None): 
                moves = []
                moves += movesToFree
                print("Free Space :" + str(self.sanityCheck(moves,config)))
                moves += movesToGoal
                moves += self.reverseMoves(movesToFree)
                print("Free Space and Move:" + str(self.sanityCheck(moves,config)))

                return moves
            else: 
                print("ManipulateMove: No path to Space found")
        else: 
                print("ManipulateMove: Space could not be freed")
        return None

    def freeCubeAndSpaceMove(self,debug=True):
        freeCubeMoves = self.freeCube()
        if(freeCubeMoves == None):
            print("Manipulate Move: Couldnt Free Cube!")
            return None
        print("Correct cube free moves: " + str(self.sanityCheck(freeCubeMoves,self.configuration)))
        config = self.moves2Position2(freeCubeMoves,self.configuration)
        if config is None:
            return None
        freeSpaceMoves = self.freeSpaceMove2(config)
        if(freeSpaceMoves == None):
            print("Couldnt Free Space and Moved!")
            return None
        moves = []
        moves += freeCubeMoves
        moves += freeSpaceMoves
        print("ManipulateMove: Sequence to free Space and Move: " + str(freeSpaceMoves))
        moves += self.reverseMoves(freeCubeMoves)
        print("ManipulateMove: Sequence for freCubeandMove: " + str(moves))
        if(debug):
            k = movesToPositionsDebug(moves,self.configuration,self.gPos,self.cubeID,"freeCubeAndSpaceMove")
            if k is None:
                return None
        return moves

    def freeCube(self): 
        movesToFree = LFC(self.configuration,self.cubeID,gPos=self.gPos).freeCube()
        if movesToFree != None :
            print("ManipulateMove: Moves to Free Cube: " + str(movesToFree))
            return movesToFree
        else:
            print("FreeCube: Cube could not be freed")
        return None
       
    def moves2Position2(self, moves,config): 
        cubes = ProgrammableCubes(np.copy(config))
        for cID, move in moves: 
            done = cubes.apply_single_update_step(cID, move)
            if not done: 
                print("Move could not be made to Pos PIPP")
                return None
        return np.copy(cubes.cube_position)
    
    def reverseMoves(self,moves):
        oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4} 
        revMoves = []
        list.reverse(moves)
        for c,m in moves: 
            revMoves.append((c,oppositeMove[m]))
        return revMoves
    
    def sanityCheck(self,newMoves, config): 
        cubies = ProgrammableCubes(np.copy(config))
        for id,move in newMoves: 
            done = cubies.apply_single_update_step(id,move)
            if(not done):
                print("Could not make move!!!!!!!!!!!")
                return False
        return True

    def getLayoverPos(self,cubeID, config): 
        reachablePositions = ReachablePositions(config, cubeID).getAllReachablePositions()
        cubePos = np.copy(config[cubeID])
        
        closest_pos = None
        min_distance = float('inf')
        
        for pos in reachablePositions:
            if pos[0] != cubePos[0] and pos[1] != cubePos[1] and pos[2] != cubePos[2]:
                distance = np.linalg.norm(pos - cubePos)
                if distance < min_distance and distance > 4:
                    min_distance = distance
                    closest_pos = pos
        return closest_pos
        
    def createTargetSpace(self, cubeOnTarget): 
        m1 = self.freeCube()
        if(m1 == None): 
            print("ManipulateMove: Couldnt Free Cube!")
            return None
        config1 = self.moves2Position2(m1,self.configuration)
        if config1 is None:
            return None
        layerOver = self.getLayoverPos(cubeOnTarget,config1)
        print("Layer Over: " + str(layerOver))
        m2 = Mover(cubeOnTarget,config1,layerOver).moveCube()
        print("Moves to Layer Over: " + str(m2))
        allMoves = []
        allMoves += m1
        allMoves += m2
        allMoves += self.reverseMoves(m1)
        print("All Moves: " + str(allMoves))
        return allMoves
        