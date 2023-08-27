import numpy as np
import pygame

lightingDetail = 6

def generateLightMap(mapSize, worldMap, backgroundMap):
    lightMap = np.array([[1.0 for x in range(mapSize[0])] for y in range(mapSize[1])])
    for y in range(len(worldMap)):
        for x in range(len(worldMap[0])):
            if worldMap[y][x] != 0 or backgroundMap[y][x] != 0:
                lightMap[y][x] = 0.0
    

    newLight = lightMap
    for y in range(mapSize[1]):
        for x in range(mapSize[0]):
            if newLight[y][x] != 1.0:
                for i in range(1, lightingDetail):
                    detail = (lightingDetail - i)
                    cutout = lightMap[y-detail-1:y+detail+1, x-detail-1:x+detail+1]
                    if 1.0 in cutout:
                        newLight[y][x] = 1.0 - 1.0 / i
                        
    return newLight

def drawLightMap(map, mapSize):
    lightMapSurface = pygame.Surface((mapSize[0], mapSize[1]), pygame.SRCALPHA)
    for y in range(mapSize[0]):
        for x in range(mapSize[1]):
            if map[y][x] != 1.0:
                pygame.draw.rect(lightMapSurface, (0,0,0, 200 - map[y][x] * 150.0), (x, y, 1, 1))
    return lightMapSurface

def updateLightMap(position, lightMap, worldMap, backgroundMap):
    newLightMap = lightMap
    if worldMap[position[1]][position[0]] != 0 or backgroundMap[position[1]][position[0]] != 0:
        newLightMap[position[1]][position[0]] = 0.0
    else:
        newLightMap[position[1]][position[0]] = 1.0
    for y in range(position[1] - lightingDetail*2, position[1] + lightingDetail*2):
        for x in range(position[0] - lightingDetail*2, position[0] + lightingDetail*2):
            if newLightMap[y][x] != 1.0:
                for i in range(1, lightingDetail):
                    detail = (lightingDetail - i)
                    cutout = lightMap[y-detail-1:y+detail+1, x-detail-1:x+detail+1]
                    if 1.0 in cutout:
                        newLightMap[y][x] = 1.0 - 1.0 / i
    
    return newLightMap

def redrawLight(map, gridSize, lightMapSurface, pos):
    pygame.draw.rect(lightMapSurface, (0, 0, 0, 0), ((pos[0] - lightingDetail * 2) * gridSize, (pos[1] - lightingDetail * 2) * gridSize, lightingDetail * 4 * gridSize, lightingDetail * 4 * gridSize))
    for y in range(pos[1] - lightingDetail * 2, pos[1] + lightingDetail * 2):
        for x in range(pos[0] - lightingDetail * 2, pos[0] + lightingDetail * 2):
            if map[y][x] != 1.0:
                pygame.draw.rect(lightMapSurface, (0,0,0, 200 - map[y][x] * 150.0), (x * gridSize, y * gridSize, gridSize, gridSize))
    #pygame.draw.rect(lightMapSurface, (0,0,0, 200 - map[pos][x] * 150.0), (x * gridSize, y * gridSize, gridSize, gridSize))