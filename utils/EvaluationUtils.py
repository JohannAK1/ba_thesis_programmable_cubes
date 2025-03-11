import numpy as np
from utils.ConfigurationUtils import movesToPositions

def toList (config):
    listConfig = []
    for c in config:
        listConfig.append(list(c))
    return listConfig

def correctCubes2(solPos, tarPos, initTypes, tarTypes): 
    correctCubes1 = 0
    solPos = toList(solPos)
    tarPos = toList(tarPos)
    initTypes = list(initTypes)
    tarTypes = list(tarTypes)
    for id,cubePos in enumerate(solPos):
        if cubePos in tarPos: 
            if initTypes[id] == tarTypes[tarPos.index(cubePos)]:
                correctCubes1 += 1

    return correctCubes1/len(solPos)
    
    
