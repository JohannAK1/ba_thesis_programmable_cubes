import numpy as np
from collections import Counter
import math
from csa.MoveOrder2 import MoveOrder
from framework.programmable_cubes_UDP import ProgrammableCubes
from csa.LineConfigurator import LineConfigurator
from move_algorithms.MoverAStart import MoverAStar as Mover
from move_algorithms.ManipulateMove import ManipulateMove
import sys
from csa.FreeCubeCSA import FreeCubeCSA
from ipa.LayerCubes import LayerCubes 

class CommonConfigurator:
    def __init__(self,configuration, types):
        
        #self.LL = LengthLogger()
        self.configuration = np.copy(configuration)
        self.types = np.copy(types)
        self.line = []
        self.movesMade = []
        self.extremeCube = self.findExtremeCube()
        self.extremePosition = configuration[self.extremeCube]
        self.rowLengths = self.calculateRowLengths()
        self.lineOrder = self.calculateLineOrder()
        
        self.M_Order = MoveOrder(configuration,self.extremeCube,types,self.lineOrder)
        self.LC = LineConfigurator(types)
        
        #self.moveOrder = M_Order.calculateMoveOrder()
        self.foundationOrder = self.M_Order.getFoundationOrder()

        self.currentConfiguration = np.copy(configuration)

        self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}

        self.correctCount = 0

        self.typeCount = self.count_types()

    def findExtremeCube(self):
        # Find the maximum x-coordinate
        max_x = np.max(self.configuration[:, 0])
        
        # Get the indices of the points with the maximum x-coordinate
        max_x_indices = np.where(self.configuration[:, 0] == max_x)[0]
        
        # Get the subset of points with the maximum x-coordinate
        max_x_points = self.configuration[max_x_indices]
        
        # Find the minimum z-coordinate among the subset
        min_z = np.min(max_x_points[:, 2])
        
        # Get the indices of the points with the maximum x-coordinate and minimum z-coordinate
        min_z_indices = np.where((max_x_points[:, 2] == min_z))[0]
        
        # Get the subset of points with the maximum x-coordinate and minimum z-coordinate
        min_z_points = max_x_points[min_z_indices]
        
        # Find the maximum y-coordinate among the subset
        max_y = np.max(min_z_points[:, 1])
        
        # Get the index of the point with the maximum x-coordinate, minimum z-coordinate, and maximum y-coordinate
        max_y_index = np.where((self.configuration[:, 0] == max_x) & (self.configuration[:, 2] == min_z) & (self.configuration[:, 1] == max_y))[0][0]
        
        return max_y_index
    
    def calculateRowLengths(self): 
        counter = Counter(self.types)
        result = {num: round(math.sqrt(count)) for num, count in counter.items()}
        return result
    
    def calculateLineOrder(self):
        count = Counter(self.types)
        sorted_items = sorted(count.items(), key=lambda x: (-x[1], x[0]))
        result = {item: index for index, (item, freq) in enumerate(sorted_items)}
        return result
    
    def createCommonConfiguration(self):
        print("=====Create Foundation=====")
        self.currentConfiguration = self.createFoundation2()

        print("=====Create Common=====")
        self.currentConfiguration = self.createCommon()

        print("=====Fix Foundation=====")
        #self.currentConfiguration = self.fixFoundation()

        return self.line,self.movesMade

    def createCommon(self):
        while self.correctCount != len(self.currentConfiguration):
            nextCube = self.M_Order.getNextCube(self.currentConfiguration)
            print("Next Cube to Move: ",nextCube)
            self.currentConfiguration = self.moveToAndUp(nextCube)
            self.correctCount += 1
        return self.currentConfiguration
    
    def createFoundation2(self): 
        curGPos = np.copy(self.extremePosition)
        curGPos[0] += 1
        print(self.foundationOrder)
        
        for cubeId,manipulate in self.foundationOrder:
            moves = None
            if(manipulate):
                LC = LayerCubes(self.currentConfiguration,cubeId)
                layer,cubesNeeded,_,bounds = LC.getCubesNeeded_Bounds_CSA()[0]
                movesNeeded = [0,1,2,3,4,5]
                FC = FreeCubeCSA(self.currentConfiguration,cubeId,layer,bounds,cubesNeeded,movesNeeded)
                moves = FC.freeCube()
                tempConfig = self.applyMoves(moves)
                moves += Mover(cubeId, tempConfig, curGPos).moveCube()
                print(moves)
            else:
                moves = self.moveCube(cubeId,curGPos,np.copy(self.currentConfiguration))
                print(moves)

            if moves != None and manipulate:
                self.movesMade += moves
                self.currentConfiguration = self.applyMoves(moves)
            elif moves == None: 
                print("Problem when creating foundation")
                print("Cube: ",cubeId)
                print("Manipulate: ",manipulate) 
                sys.exit()
            self.line.append([cubeId])
            
            self.correctCount += 1
            curGPos[0] += 1
        
        return self.currentConfiguration
    
    def fixFoundation(self): 
        layOver = np.copy(self.extremePosition)
        layOver[2] += 1
        
        for cube,newFoundationCube in self.moveOrder[2]: 
            if(newFoundationCube == -1): 
                self.currentConfiguration = self.moveToAndUp(cube)
            else:
                lineIndex = self.lineOrder[self.types[newFoundationCube]]
                curPos = np.copy(self.currentConfiguration[cube])

                self.moveCube(cube,layOver,np.copy(self.currentConfiguration))
                self.line[lineIndex].pop(0)
                print("cubeMoved to layover")
                self.currentConfiguration[cube] = np.copy(layOver)
                
                self.moveCube(newFoundationCube,curPos,np.copy(self.currentConfiguration))
                
                self.line[lineIndex].pop()
                self.line[lineIndex].insert(0,newFoundationCube)
                print("Cube Moved to start of line")
                
                self.currentConfiguration[newFoundationCube] = curPos
                self.currentConfiguration = self.moveToAndUp(cube)

        return self.currentConfiguration

    def moveCube(self, cubeId,gPos,stepConfiguration):
        numStates1,moves = Mover(cubeId,stepConfiguration,gPos).moveCubeEval()
        #numStates2,moves2 = BFS(cubeId,stepConfiguration,gPos).moveCubeEval()
        #distance = np.linalg.norm(stepConfiguration[cubeId] - gPos)
        #self.LL.log("AStar",distance,numStates1,len(moves))
        #self.LL.log("BFS",distance,numStates2,len(moves2))
        print(moves)
        if moves == None:
                print("Cube type: ",self.types[cubeId])
                print("CubePos ",stepConfiguration[cubeId])
                print("GoalPos ",gPos)
                print("No moves made by Mover!! ")
        else: 
            self.currentConfiguration = self.applyMoves(moves)
            self.movesMade += moves
        return moves
    
    def moveFreeCube(self, cubeId,gPos,stepConfiguration):
        moves = Mover(cubeId,stepConfiguration,gPos).moveCube()
        moves = ManipulateMove(stepConfiguration,cubeId,gPos).freeCubeAndSpaceMove()
        if moves != None:
            self.movesMade += moves
            self.currentConfiguration = self.applyMoves(moves)

    def moveToAndUp(self,nextCube):
        cubeType = self.types[nextCube]
        lineIndex = self.lineOrder[cubeType]
        extremLineCube = self.line[lineIndex][0]
        lineLength = len(self.line[lineIndex])
        rowLength = self.rowLengths[cubeType]

        gPos = np.array(self.currentConfiguration[extremLineCube])
       
        if lineLength < self.LC.breakPoints[cubeType][1]:
            gPos[2] = (gPos[2] + 1)
        else:
            gPos[1] = (gPos[1] - 1)
        
        self.moveCube(nextCube,gPos,np.copy(self.currentConfiguration))

        self.currentConfiguration[nextCube] = gPos
        
        self.currentConfiguration = self.moveCubeToLineEnd(nextCube)

        self.line[lineIndex].append(nextCube)
        return self.currentConfiguration
    
    def moveCubeToLineEnd(self,cubeId): 
        cubies = ProgrammableCubes(np.copy(self.currentConfiguration))
        move,moveCount = self.LC.moveToEnd(self.types[cubeId])

        for i in range(moveCount): 
            done = cubies.apply_single_update_step(cubeId,move)
            self.movesMade.append((cubeId,move))

        return np.copy(cubies.cube_position)
    
    def count_types(self):
        element_counts = {}
        for element in self.types:
            if element in element_counts:
                element_counts[element] += 1
            else:
                element_counts[element] = 1
        return element_counts

    def applyMoves(self,moves): 
        PC = ProgrammableCubes(np.copy(self.currentConfiguration))
        for c,m in moves:
            done = PC.apply_single_update_step(c,m)
            if not done: 
                print("Move could not be made")
                sys.exit()
            
        return np.copy(PC.cube_position)