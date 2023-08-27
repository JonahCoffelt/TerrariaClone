import random, math
import numpy as np
from perlin_numpy import (
    generate_perlin_noise_2d
)


blockLevelData = [
    [(0, 2), 1], #Grass
    [(2, 5), 2], #Dirt
    [3], #Stone
    ]

biomeData = {
    "plains" :  {
        0 : 0,
        1 : 1,
        2 : 2,
        3 : 3,
        4 : 3
    },
    "desert" :  {
        0 : 0,
        1 : 4,
        2 : 4,
        3 : 4,
        4 : 5
    },
    "snow" :  {
        0 : 0,
        1 : 5,
        2 : 5,
        3 : 6,
        4 : 6
    }
    }

def generateBiomemap(mapSize):
    noiseBiome = generate_perlin_noise_2d((512, 512), (4, 4))

    biomeMap = np.array([[1.0 for x in range(mapSize[0])] for y in range(mapSize[1])])

    for y in range(0, mapSize[1]):
        for x  in range(0, mapSize[0]):
            biomeMap[y][x] = noiseBiome[x, y//5]
    
    return biomeMap

def getBiome(noiseValue):
    if noiseValue < -.25:
        return "desert"
    elif noiseValue < .25:
        return "plains"
    elif noiseValue >= .25:
        return "snow"
    return "plains"
 
def generateMap(mapSize):

    worldMap = np.array([[0 for x in range(mapSize[0])] for y in range(mapSize[1])])
    backgroundMap = np.array([[0 for x in range(mapSize[0])] for y in range(mapSize[1])])

    np.random.seed(random.randrange(0, 1000))
    noise = generate_perlin_noise_2d((512*2, 512*2), (8, 8))
    noiseCave = generate_perlin_noise_2d((512, 512), (8, 8))
    noiseCaveBig = generate_perlin_noise_2d((512, 512), (4, 4))

    biomeMap = generateBiomemap(mapSize)

    heightMap = []
    for x in range(0, mapSize[0]):
        heightMap.append(int(noise[0][x]*30) + int(((noise[100][int(x)]*2.9)**3)*7) + 100)

    for x in range(0, mapSize[0]):
        for blockLevels in blockLevelData[:-1]:
            for y in range(heightMap[x] + blockLevels[0][0], heightMap[x] + blockLevels[0][1]):
                worldMap[y][x] = blockLevels[1]
        for y in range(heightMap[x] + blockLevels[0][0], mapSize[1]):
            worldMap[y][x] = blockLevelData[-1][0]
    for y in range(0, mapSize[1]):
        for x in range(0, mapSize[0]):
            biome = getBiome(biomeMap[y][x])
            worldMap[y][x] = biomeData[biome][worldMap[y][x]]
            if y > heightMap[x] + 20:
                backgroundMap[y][x] = biomeData[biome][4]
            if abs(noiseCave[x][y]) < .05 + mapSize[1]/(y+1)/75:
                    worldMap[y][x] = 0
            if abs(noiseCaveBig[x][y]) < .08 + mapSize[1]/(y+1)/100  and y > mapSize[0] / 2:
                worldMap[y][x] = 0

    tree = 0
    for x in range(0, mapSize[0]):
        if tree > 7:
            if noise[x][50] > .1 and worldMap[heightMap[x]][x] != 0:
                treeHeight = random.randrange(2, 5)
                for y in range(heightMap[x] - treeHeight, heightMap[x]):
                    backgroundMap[y][x] = 4

            tree = 0
        tree += 1


    '''

    tree = 0
    for x in range(0, mapSize[0]):
        height = int(noise[0][x//7]*85) + int(noise[0][x]*45) + int(noise[2][int(x*1.5)]*30)+ 100
        if biomeMap[100][x] < -.3: #Desert
            for y in range(height, height+8):
                worldMap[y][x] = 4
            for y in range(height+8, mapSize[1]):
                worldMap[y][x] = 3
            for y in range(height+20, mapSize[1]):
                backgroundMap[y][x] = 5

            for y  in range(0, mapSize[1]):
                if abs(noiseCave[x][y]) < .05 + mapSize[1]/(y+1)/75:
                    worldMap[y][x] = 0

            if tree > 7:
                if noise[x][50] > .1 and worldMap[height][x] != 0:
                    treeHeight = random.randrange(2, 5)
                    for y in range(height - treeHeight, height):
                        backgroundMap[y][x] = 4

                tree = 0
            tree += 1
        
        elif biomeMap[100][x] < .3: #Plains
            for y in range(height, height+2):
                worldMap[y][x] = 1
            for y in range(height+2, height+5):
                worldMap[y][x] = 2
            for y in range(height+5, mapSize[1]):
                worldMap[y][x] = 3
            for y in range(height+20, mapSize[1]):
                backgroundMap[y][x] = 3

            for y  in range(0, mapSize[1]):
                if abs(noiseCave[x][y]) < .05 + mapSize[1]/(y+1)/75:
                    worldMap[y][x] = 0

            if tree > 7:
                if noise[x][50] > .1 and worldMap[height][x] != 0:
                    treeHeight = random.randrange(7, 14)
                    for leafx in range(x - random.randrange(2, 4), x + random.randrange(2, 4)): 
                        for leafy in range(height - treeHeight - random.randrange(2, 4), height - treeHeight + random.randrange(2, 4)):
                            backgroundMap[leafy][leafx] = 1
                    for y in range(height - treeHeight, height):
                        backgroundMap[y][x] = 2

                tree = 0
            tree += 1
        else: #Snow
            for y in range(height, height+8):
                worldMap[y][x] = 5
            for y in range(height+8, mapSize[1]):
                worldMap[y][x] = 6
            for y in range(height+20, mapSize[1]):
                backgroundMap[y][x] = 6

            for y  in range(0, mapSize[1]):
                if abs(noiseCave[x][y]) < .05 + mapSize[1]/(y+1)/75:
                    worldMap[y][x] = 0

            if tree > 7:
                if noise[x][50] > .1 and worldMap[height][x] != 0:
                    treeHeight = random.randrange(2, 5)
                    for y in range(height - treeHeight, height):
                        backgroundMap[y][x] = 4

                tree = 0
            tree += 1
    '''
    
    return worldMap, backgroundMap, biomeMap