import numpy as np
from utils.ConfigurationUtils import movesToPositions

def correctCubes(moves, initPos, tarPos, initTypes, tarTypes): 
    solPos = movesToPositions(moves, initPos)
    
    cubeNum = len(solPos)
    targetDict = {}
    corCubes = 0

    for id, coords in enumerate(tarPos):
        targetDict[tuple(coords)] = tarTypes[id]  # Convert numpy array to tuple

    for id, coords in enumerate(solPos):
        if tuple(coords) in targetDict and targetDict[tuple(coords)] == initTypes[id]:  # Convert to tuple
            corCubes += 1

    return corCubes/cubeNum

def wrongCubes(solPos, tarPos, initTypes, tarTypes): 
    
    cubeNum = len(solPos)
    targetDict = {}
    corCubes = 0

    for id, coords in enumerate(tarPos):
        targetDict[tuple(coords)] = tarTypes[id]  # Convert numpy array to tuple

    for id, coords in enumerate(solPos):
        if tuple(coords) in targetDict and targetDict[tuple(coords)] != initTypes[id]:  # Convert to tuple
            corCubes += 1

    return corCubes/cubeNum

def wrongCubes2(solPos, tarPos, initTypes, tarTypes): 
    
    wrongCubes2 = 0

    for id,cubePos in enumerate(solPos):
        if cubePos in tarPos: 
            if initTypes[id] != tarTypes[tarPos.index(cubePos)]:
                wrongCubes2 += 1

    return wrongCubes2/len(solPos)


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
    
    
