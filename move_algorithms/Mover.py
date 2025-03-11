import queue
import numpy as np
from framework.programmable_cubes_UDP import ProgrammableCubes

class Mover:
    def __init__(self,cubeId, currentConfiguration, gPos):
          self.currentConfiguration = np.copy(currentConfiguration)
          self.cubeID = cubeId
          self.gPos = np.copy(gPos)
          self.sPos = np.copy(self.currentConfiguration[cubeId])
          self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}

    def moveCube(self):
            seenPositions = self.breadthSearch()
            if(seenPositions == None):
                return None
            moves = self.retrace(seenPositions)
            if len(moves) == 0:
                print("Mover: Cube is on targetPosition: " + str(self.gPos))
            return moves
    
    def moveCubeEval(self):
            seenPositions = self.breadthSearch()
            if(seenPositions == None):
                return None
            moves = self.retrace(seenPositions)
            if len(moves) == 0:
                print("Mover: Cube is on targetPosition: " + str(self.gPos))
            return (len(seenPositions),moves)

    def breadthSearch(self):
        q = queue.Queue()
        q.put(self.sPos)
        seenPositions = [(self.sPos, -1)]
        while (q.not_empty): 
            if(q.qsize() == 0): break
            curPos = q.get()
            self.currentConfiguration[self.cubeID] = curPos
            if(np.array_equal(curPos,self.gPos)):
                return seenPositions
            for possiblePos in self.getPossiblePositions():
                if not any(np.array_equal(possiblePos[0], seen_pos) for seen_pos,_ in seenPositions): 
                    q.put(possiblePos[0])
                    seenPositions.append(possiblePos)
        return None
        
    def retrace(self, seenPositions): 
        curPos = self.gPos
        gEnsemble = np.copy(self.currentConfiguration)
        gEnsemble[self.cubeID] = self.gPos
        cubies = ProgrammableCubes(gEnsemble)
        temp_movesMade = []
        
        while (not np.array_equal(curPos, self.sPos)):
            moveMade = self.findMove(seenPositions,curPos)
            temp_movesMade.append((self.cubeID,moveMade))
            backMove = self.findBackMove(seenPositions,curPos)
            cubies.apply_single_update_step(self.cubeID,backMove)
            curPos = cubies.cube_position[self.cubeID]
        
        list.reverse(temp_movesMade)
        return temp_movesMade

    def getPossiblePositions(self): 
        possiblePositions = []
        cubies = ProgrammableCubes(self.currentConfiguration)
        for i in range(6): 
            done = cubies.apply_single_update_step(self.cubeID,i)
            if(done == 1): 
                possiblePositions.append((np.copy(cubies.cube_position[self.cubeID]),i))
                cubies.apply_single_update_step(self.cubeID,self.oppositeMove[i])
        return possiblePositions

    def findBackMove(self,seenPositions, curPos): 
        for pos,move in seenPositions: 
            if(np.array_equal(pos, curPos)): return self.oppositeMove[move]

    def findMove(self,seenPositions, curPos): 
        for pos,move in seenPositions: 
            if(np.array_equal(pos, curPos)): return move