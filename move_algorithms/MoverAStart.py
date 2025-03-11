import queue
import numpy as np
from framework.programmable_cubes_UDP import ProgrammableCubes

class MoverAStar:
    def __init__(self, cubeId, currentConfiguration, gPos):
        self.currentConfiguration = np.copy(currentConfiguration)
        self.cubeID = cubeId
        self.gPos = np.copy(gPos)
        self.sPos = np.copy(self.currentConfiguration[cubeId])
        self.oppositeMove = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}

    def moveCube(self):
        seenPositions = self.aStarSearch()
        if seenPositions is None:
            return None
        moves = self.retrace(seenPositions)
        if len(moves) == 0:
            print("Mover: Cube is on targetPosition: " + str(self.gPos))
        return moves
    
    def moveCubeEval(self):
        seenPositions = self.aStarSearch()
        if seenPositions is None:
            return None
        moves = self.retrace(seenPositions)
        if len(moves) == 0:
            print("Mover: Cube is on targetPosition: " + str(self.gPos))
        return (len(seenPositions),moves)

    def heuristic(self, pos):
        return np.linalg.norm(pos - self.gPos)

    def aStarSearch(self):
        q = queue.PriorityQueue()
        q.put((0, tuple(self.sPos)))
        seenPositions = {tuple(self.sPos): (-1, 0)}
        while not q.empty():
            _, curPos = q.get()
            self.currentConfiguration[self.cubeID] = np.array(curPos)
            if np.array_equal(curPos, self.gPos):
                return seenPositions
            for possiblePos, move in self.getPossiblePositions():
                new_cost = seenPositions[curPos][1] + 1
                possiblePosTuple = tuple(possiblePos)
                if possiblePosTuple not in seenPositions or new_cost < seenPositions[possiblePosTuple][1]:
                    priority = new_cost + self.heuristic(possiblePos)
                    q.put((priority, possiblePosTuple))
                    seenPositions[possiblePosTuple] = (move, new_cost)
        return None

    def retrace(self, seenPositions):
        curPos = tuple(self.gPos)
        gEnsemble = np.copy(self.currentConfiguration)
        gEnsemble[self.cubeID] = self.gPos
        cubies = ProgrammableCubes(gEnsemble)
        temp_movesMade = []

        while not np.array_equal(curPos, self.sPos):
            moveMade = self.findMove(seenPositions, curPos)
            temp_movesMade.append((self.cubeID, moveMade))
            backMove = self.findBackMove(seenPositions, curPos)
            cubies.apply_single_update_step(self.cubeID, backMove)
            curPos = tuple(cubies.cube_position[self.cubeID])

        temp_movesMade.reverse()
        return temp_movesMade

    def getPossiblePositions(self):
        possiblePositions = []
        cubies = ProgrammableCubes(self.currentConfiguration)
        for i in range(6):
            done = cubies.apply_single_update_step(self.cubeID, i)
            if done == 1:
                possiblePositions.append((np.copy(cubies.cube_position[self.cubeID]), i))
                cubies.apply_single_update_step(self.cubeID, self.oppositeMove[i])
        return possiblePositions

    def findBackMove(self, seenPositions, curPos):
        for pos, (move, _) in seenPositions.items():
            if np.array_equal(pos, curPos):
                return self.oppositeMove[move]

    def findMove(self, seenPositions, curPos):
        for pos, (move, _) in seenPositions.items():
            if np.array_equal(pos, curPos):
                return move