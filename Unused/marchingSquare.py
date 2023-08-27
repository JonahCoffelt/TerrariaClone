import numpy as np
import pygame

from Unused.SpriteSheet import processImageSheets 

GroundSheet = pygame.image.load(r'TerrariaLikeGrass.png')
tiles = processImageSheets(GroundSheet, "TerrariaLikeGrass")[0]

marchingSquare = {
    "0000" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "0001" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "0010" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "0011" : [[1, 0], [1, 1], [0, 1]],
    "0100" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "0101" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "0110" : [[0, 0], [1, 0], [0, 1]],
    "0111" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "1000" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "1001" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "1010" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "1011" : [[0, 0], [1, 0], [1, 1]],
    "1100" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "1101" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "1110" : [[0, 0], [1, 0], [1, 1], [0, 1]],
    "1111" : [[0, 0], [1, 0], [1, 1], [0, 1]]
}

#Top Right Bottom Left
tiles = [
    {
    "0000" : tiles[0],
    "0001" : tiles[1],
    "0010" : tiles[2],
    "0011" : tiles[3],
    "0100" : tiles[4],
    "0101" : tiles[5],
    "0110" : tiles[6],
    "0111" : tiles[7],
    "1000" : tiles[8],
    "1001" : tiles[9],
    "1010" : tiles[10],
    "1011" : tiles[11],
    "1100" : tiles[12],
    "1101" : tiles[13],
    "1110" : tiles[14],
    "1111" : tiles[15]
    }
]

def checkSurrounding(x, y, map):
    surrounding = ""
    if x < 498 and y < 298:
        if map[y - 1][x] != 0.0:
            surrounding += "1"
        else:
            surrounding += "0"

        if map[y][x + 1] != 0.0:
            surrounding += "1"
        else:
            surrounding += "0"
        
        if map[y + 1][x] != 0.0:
            surrounding += "1"
        else:
            surrounding += "0"
        
        if map[y][x - 1] != 0.0:
            surrounding += "1"
        else:
            surrounding += "0"
    else:
        return "0000"

    return surrounding

def getSquare(offset, drawX, drawY, x, y, map, gridSize):
    surrounding = checkSurrounding(x, y, map)
    square = marchingSquare[surrounding]
    newSquare = np.zeros_like(square)

    for point in range(len(square)):
        newSquare[point][0] = square[point][0] * gridSize + drawX * gridSize - offset[0]
        newSquare[point][1] = square[point][1] * gridSize + drawY * gridSize - offset[1]

    return newSquare

def getTileAsset(tileType, x, y, map):
    surrounding = checkSurrounding(x, y, map)

    return tiles[0][surrounding]
