import time
from animation.Animation import CubeAnimation
from framework.programmable_cubes_UDP import ProgrammableCubes
import numpy as np
from csa.CommonConfigurator import CommonConfigurator
from csa.commonExtreme import CommonExtremeCubeConfigurator

class Solver:
    def __init__(self, initialConfiguration, targetConfiguration, initialTypes, targetTypes):
        self.initialConfiguration = np.copy(initialConfiguration)
        self.targetConfiguration = np.copy(targetConfiguration)
        self.initialTypes = np.copy(initialTypes)
        self.targetTypes = np.copy(targetTypes)
        self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}
        self.CECC = CommonExtremeCubeConfigurator(self.initialConfiguration,self.targetConfiguration)
        
        self.C_Configurator_Intial = CommonConfigurator(self.CECC.solvedInitialConfiguration,initialTypes)
        self.C_Configurator_Target = CommonConfigurator(self.CECC.solvedTargetConfiguration,targetTypes)

        self.initalMoves = self.CECC.movesInitial
        self.targetMoves = self.CECC.movesTarget
        self.typeNum = self.count_types()



    def solve(self,makeAnimation=False,step=1,interval=100,name='b-search_is'):
        start_time = time.time()
        line1,moves1 = self.C_Configurator_Intial.createCommonConfiguration()
        end_time = time.time()

        time1 = end_time - start_time
        
        start_time = time.time()
        line2,moves2 = self.C_Configurator_Target.createCommonConfiguration()
        end_time = time.time()

        time2 = end_time - start_time

        mapping = self.createCubeIdMapping(line1,line2)

        self.initalMoves += moves1
        self.targetMoves += moves2

        moves = self.combineMoveSequence(mapping)
        

        print("===============Statistic===============")
        print("------------Config1-Common-------------")
        print("Number of Moves: " + str(len(self.initalMoves)))
        print("Time to calculate: " + str(time1))
        print("------------Common-Config2-------------")
        print("Number of Moves: " + str(len(self.targetMoves)))
        print("Time to calculate: " + str(time2))
        return moves

    def count_types(self):
        element_counts = {}
        for element in self.initialTypes:
            if element in element_counts:
                element_counts[element] += 1
            else:
                element_counts[element] = 1
        return len(element_counts)
    
    def combineMoveSequence(self, mapping):
        initialMoveSequence = list.copy(self.initalMoves)
        targetMoveSequence = list.copy(self.targetMoves)
        
        combinedSequence = []

        combinedSequence += initialMoveSequence

        list.reverse(targetMoveSequence)

        combinedSequence.extend((mapping[cubeId], self.oppositeMove[moveId]) for cubeId, moveId in targetMoveSequence)

        return combinedSequence
    
    def createCubeIdMapping(self,line1,line2): 
        if(self.lineLength(line1) != self.lineLength(line2)): 
            print("No mapping possible lines not same dimensions")
            return []
        idMapping = {}
        for col in range(len(line2)): 
            for index in range(len(line2[col])): 
                id2 = line2[col][index]
                id1 =  line1[col][index]
                idMapping[id2] = id1
        return idMapping
    
    def lineLength(self,line):
        return sum(len(row) for row in line)