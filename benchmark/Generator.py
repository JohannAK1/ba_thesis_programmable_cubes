import numpy as np
import random
from utils.ConfigurationUtils import getAverageCubeNeighbours, overLappingCubes

class EnsembleGenerator:
    def __init__(self, cube_num, type_num, averageNeighbors=-1, overlap=-1):
        self.cube_num = cube_num - 1
        self.type_num = type_num - 1
        self.averageNeighbors = averageNeighbors  # Expected neighbor count (2-4.25) or -1 to ignore parameter
        self.overlap = overlap  # Expected overlap count (0-1) or -1 to ignore parameter
        self.initialConfiguration = []
        self.targetConfiguration = []
        self.initialTypes = []
        self.targetTypes = []


        self.possible_moves = [[1, 0, 0], [-1, 0, 0],
                          [0, 1, 0], [0, -1, 0],
                          [0, 0, 1], [0, 0, -1]]

        self.initNeighbours = []
        self.targetNeighbours = []

        self.createConfigs()

    def createConfigs(self):
        startDiv = 4
        init_pos = [self.cube_num // startDiv] * 3
        self.initialConfiguration.append(init_pos)
        self.targetConfiguration.append(init_pos)
        self.initialTypes.append(random.randint(0, self.type_num))

        self.initNeighbours.append(1)
        self.targetNeighbours.append(1)
    
    def generateEnsembleRandom(self):
        while len(self.initialConfiguration) < self.cube_num:
            self.addCubeRandom(self.initialConfiguration,self.initialTypes)
        
        while len(self.targetConfiguration) < self.cube_num:
            self.addCubeRandom(self.targetConfiguration,self.targetTypes)
        
        self.targetTypes = list.copy(self.initialTypes)
        random.shuffle(self.targetTypes)

    def generateEnsembleNeighbor(self):
        if(self.averageNeighbors == -1):
            print("Error: averageNeighbors parameter is not set")
            return
        
        while len(self.initialConfiguration) < self.cube_num:
            self.addCubeNeighbour(self.initialConfiguration,self.initialTypes)
        
        while len(self.targetConfiguration) < self.cube_num:
                self.addCubeNeighbour(self.targetConfiguration,self.targetTypes)
        
        self.targetTypes = list.copy(self.initialTypes)
        random.shuffle(self.targetTypes)

    def generateEnsembleOverlapCorrect(self):
        if(self.overlap == -1):
            print("Error: overlap parameter is not set")
            return
        
        overlappingCubes1 = {}

        overlappingCubes1[0] = self.initialTypes[0]

        while len(self.initialConfiguration) < self.cube_num:
            self.addCubeRandom(self.initialConfiguration,self.initialTypes)


        while len(self.targetConfiguration) < self.cube_num:
            overLap = self.addCubeOverlapDifferentType()
            if overLap != None:
                overlappingCubes1[overLap[1]] = self.initialTypes[overLap[0]]

        typeSum = {}

        for type in self.initialTypes:
            if type not in typeSum:
                typeSum[type] = 0
            typeSum[type] += 1


        self.targetTypes = [-1 for i in range(len(self.initialTypes))]
        print(len(overlappingCubes1)/len(self.initialTypes))

        # frist add to the array all overlapping cubes with same type

        for t_index in overlappingCubes1:
            new_type = overlappingCubes1[t_index]
            self.targetTypes[t_index] = new_type
            typeSum[new_type] -= 1

        # then add the rest of the cubes
        for i in range(len(self.initialTypes)):
            if self.targetTypes[i] == -1:
                for type in range(self.type_num+1):
                    if typeSum[type] > 0:
                        self.targetTypes[i] = type
                        typeSum[type] -= 1
                        break

    def generateEnsembleOverlapWrong(self):
        if(self.overlap == -1):
            print("Error: overlap parameter is not set")
            return
        
        overlappingCubes1 = {}

        while len(self.initialConfiguration) < self.cube_num:
            self.addCubeRandom(self.initialConfiguration,self.initialTypes)


        while len(self.targetConfiguration) < self.cube_num:
            overLap = self.addCubeOverlapDifferentType()
            if overLap != None:
                overlappingCubes1[overLap[1]] = self.initialTypes[overLap[0]]

        typeSum = {}

        for type in self.initialTypes:
            if type not in typeSum:
                typeSum[type] = 0
            typeSum[type] += 1

        print(typeSum)

        self.targetTypes = [-1 for i in range(len(self.initialTypes))]

        # frist add to the array all overlapping cubes with diffrent type

        for i in range(len(self.initialTypes)):
            if i in overlappingCubes1: 
                diffrentType = None
                for type in range(self.type_num+1):
                    if type != overlappingCubes1[i] and typeSum[type] > 0:
                        diffrentType = type
                        break
                self.targetTypes[i] = diffrentType
                typeSum[diffrentType] -= 1

        # then add the rest of the cubes
        for i in range(len(self.initialTypes)):
            if self.targetTypes[i] == -1:
                for type in range(self.type_num+1):
                    if typeSum[type] > 0:
                        self.targetTypes[i] = type
                        typeSum[type] -= 1
                        break

    def addCubeNeighbour(self,configuration,types):
        while True:
            element = random.choice(configuration)
            random.shuffle(self.possible_moves)
            for move in self.possible_moves:
                new_element = [element[i] + move[i] for i in range(3)]
                if new_element not in configuration:
                    newConfiguration = configuration + [new_element]
                    averageNeighbours = getAverageCubeNeighbours(newConfiguration)
                    # Add variability by adjusting the threshold with a random offset ±0.1
                    threshold = self.averageNeighbors + random.uniform(-0.1, 0.1)
                    if averageNeighbours <= threshold:
                        configuration.append(new_element)
                        types.append(random.randint(0, self.type_num))    
                        return
    
    def addCubeRandom(self,configuration,types):
        while True:
            element = random.choice(configuration)
            random.shuffle(self.possible_moves)
            for move in self.possible_moves:
                new_element = [element[i] + move[i] for i in range(3)]
                if new_element not in configuration:
                    configuration.append(new_element)
                    types.append(random.randint(0, self.type_num))    
                    return

    def addCubeOverlapDifferentType(self):
         while True:
            element = random.choice(self.targetConfiguration)
            random.shuffle(self.possible_moves)
            for move in self.possible_moves:
                new_element = [element[i] + move[i] for i in range(3)]
                curOverlap = overLappingCubes(self.initialConfiguration,self.targetConfiguration)
                if curOverlap <= self.overlap:
                    if new_element not in self.targetConfiguration and new_element in self.initialConfiguration:
                        initialIndex = self.initialConfiguration.index(new_element)
                        self.targetConfiguration.append(new_element)
                        targetIndex = len(self.targetConfiguration) - 1
                        return (initialIndex,targetIndex)
                else:
                    if new_element not in self.targetConfiguration and new_element not in self.initialConfiguration:
                        self.targetConfiguration.append(new_element)
                        return