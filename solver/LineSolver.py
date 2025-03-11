import time
from framework.programmable_cubes_UDP import ProgrammableCubes
import numpy as np
from csa.CommonLineConfigurator import CommonLineConfigurator
from csa.commonExtreme import CommonExtremeCubeConfigurator

class LineSolver:
    def __init__(self, initialConfiguration, targetConfiguration, initialTypes, targetTypes):
        self.initialConfiguration = np.copy(initialConfiguration)
        self.targetConfiguration = np.copy(targetConfiguration)
        self.initialTypes = np.copy(initialTypes)
        self.targetTypes = np.copy(targetTypes)
        self.oppositeMove = {0:1,1:0,2:3,3:2,4:5,5:4}
        self.CECC = CommonExtremeCubeConfigurator(self.initialConfiguration,self.targetConfiguration)
        
        
        self.C_Configurator_Intial = CommonLineConfigurator(self.CECC.solvedInitialConfiguration,initialTypes)
        self.C_Configurator_Target = CommonLineConfigurator(self.CECC.solvedTargetConfiguration,targetTypes)
        
        
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
        print("------------Correckt Cubes-------------")
        #print("Percentage of correct Cubes: " + str(100*self.custom_fitness_function(storage[-1])) + "%")
        print("=======================================")

        #if(makeAnimation): 
            #animationMaker = CubeAnimation(storage,self.initialTypes,1,interval,name)
            #animationMaker = CubeAnimation([storage[len(self.initalMoves)],storage[len(self.initalMoves)-1]],self.initialTypes,1,interval,name) # For Testting 
           # animationMaker.make_animation()
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


    def createStorage(self,mapping,step):
        cubes = ProgrammableCubes(self.initialConfiguration)
        storage = []
        storage.append(np.copy(cubes.cube_position))
        counter = 0
        list.reverse(self.targetMoves)
        
        for cubeId,moveId in self.initalMoves: 
            counter += 1
            done = cubes.apply_single_update_step(cubeId,moveId)
            if(not done): 
                print("Move could not be made: " + str(moveId))
            if(counter % step == 0): 
                storage.append(np.copy(cubes.cube_position))
        
        for cubeId,moveId in self.targetMoves: 
            counter += 1
            cubes.apply_single_update_step(mapping[cubeId],self.oppositeMove[moveId])
            if(not done): 
                print("Move could not be made: " + str(self.oppositeMove[moveId]))
            if(counter % step == 0): 
                storage.append(np.copy(cubes.cube_position))
        
        return storage
    
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
    
    def custom_fitness_function(self,cube_ensemble):
        num_cube_types = self.typeNum
        init_cube_types = np.array(self.initialTypes)
        target_cube_types = np.array(self.targetTypes)
        target_cubes = self.targetConfiguration
        # Calculate cube overlap with target configuration
        num_correct_cubes = 0
        num_total_cubes = len(cube_ensemble)
        for types in range(num_cube_types):
            target_list = target_cubes[target_cube_types==types]
            final_list = cube_ensemble[init_cube_types==types]
            overlap = [cube in final_list for cube in target_list]
            num_correct_cubes += np.sum(overlap)
        cube_fraction = num_correct_cubes / num_total_cubes
        
        # calculate the score
        score = cube_fraction
        
        return score