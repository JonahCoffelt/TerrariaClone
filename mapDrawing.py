import pygame
#import tileData

def drawMap(map, mapSize, tileType):
    tiles = tileType
    mapSurface = pygame.Surface((mapSize[0], mapSize[1]), pygame.SRCALPHA)
    for y in range(mapSize[1]):
        for x in range(mapSize[0]):
            if map[y][x] != 0:
                pygame.draw.rect(mapSurface, (tiles[map[y][x]]), (x, y, 1, 1))
    return mapSurface

def drawLines(map, mapSize, gridSize):
    outlineWidth = 4
    lineSurface = pygame.Surface((mapSize[0] * gridSize, mapSize[1] * gridSize), pygame.SRCALPHA)
    for y in range(mapSize[1]):
        for x in range(mapSize[0]):
            if x < mapSize[0]-1 and y < mapSize[1]-1:
                if map[y][x] != 0:
                    if map[y - 1][x] == 0 and y > 1:
                        pygame.draw.line(lineSurface, "black", (x * gridSize - outlineWidth/2 + 1, y * gridSize), ((x+1) * gridSize + outlineWidth/2, y * gridSize), outlineWidth)
                    if map[y + 1][x] == 0 and y > 1:
                        pygame.draw.line(lineSurface, "black", (x * gridSize - outlineWidth/2 + 1, (y+1) * gridSize), ((x+1) * gridSize + outlineWidth/2, (y+1) * gridSize), outlineWidth)
                    if map[y][x - 1] == 0 and y > 1:
                        pygame.draw.line(lineSurface, "black", (x * gridSize, y * gridSize - outlineWidth/2 + 1), (x * gridSize, (y+1) * gridSize + outlineWidth/2), outlineWidth)
                    if map[y][x + 1] == 0 and y > 1:
                        pygame.draw.line(lineSurface, "black", ((x+1) * gridSize, y * gridSize - outlineWidth/2 + 1), ((x+1) * gridSize, (y+1) * gridSize + outlineWidth/2), outlineWidth)
    return lineSurface

def redrawLines(map, mapSize, gridSize, lineSurface, Pos):
    outlineWidth = 4
    pygame.draw.rect(lineSurface, (0, 0, 0, 0), (((Pos[0] - 1) * gridSize) + 1, ((Pos[1] - 1) * gridSize) + 1, gridSize * 3 - 1, gridSize * 3 - 1))
    for y in range(Pos[1] - 3, Pos[1] + 3):
        for x in range(Pos[0] - 3, Pos[0] + 3):
            if x < mapSize[0]-1 and y < mapSize[1]-1:
                if map[y][x] != 0:
                    if map[y - 1][x] == 0 and y > 1:
                        pygame.draw.line(lineSurface, "black", (x * gridSize - outlineWidth/2 + 1, y * gridSize), ((x+1) * gridSize + outlineWidth/2, y * gridSize), outlineWidth)
                    if map[y + 1][x] == 0 and y > 1:
                        pygame.draw.line(lineSurface, "black", (x * gridSize - outlineWidth/2 + 1, (y+1) * gridSize), ((x+1) * gridSize + outlineWidth/2, (y+1) * gridSize), outlineWidth)
                    if map[y][x - 1] == 0 and y > 1:
                        pygame.draw.line(lineSurface, "black", (x * gridSize, y * gridSize - outlineWidth/2 + 1), (x * gridSize, (y+1) * gridSize + outlineWidth/2), outlineWidth)
                    if map[y][x + 1] == 0 and y > 1:
                        pygame.draw.line(lineSurface, "black", ((x+1) * gridSize, y * gridSize - outlineWidth/2 + 1), ((x+1) * gridSize, (y+1) * gridSize + outlineWidth/2), outlineWidth)