import pygame

def setupOutlineMap(worldMap, outlineMap, surface, mapSize):
    for y in AHHHHHHHHHHHH:
        if worldMap[y - 1][x] == 0 and y > 1:
            pygame.draw.line(outlineSurface, "black", (drawX * gridSize - outlineWidth/2 + 1, drawY * gridSize), ((drawX+1) * gridSize + outlineWidth/2, drawY * gridSize), outlineWidth)
        if worldMap[y + 1][x] == 0 and y > 1:
            pygame.draw.line(outlineSurface, "black", (drawX * gridSize - outlineWidth/2 + 1, (drawY+1) * gridSize), ((drawX+1) * gridSize + outlineWidth/2, (drawY+1) * gridSize), outlineWidth)
        if worldMap[y][x - 1] == 0 and y > 1:
            pygame.draw.line(outlineSurface, "black", (drawX * gridSize, drawY * gridSize - outlineWidth/2 + 1), (drawX * gridSize, (drawY+1) * gridSize + outlineWidth/2), outlineWidth)
        if worldMap[y][x + 1] == 0 and y > 1:
            pygame.draw.line(outlineSurface, "black", ((drawX+1) * gridSize, drawY * gridSize - outlineWidth/2 + 1), ((drawX+1) * gridSize, (drawY+1) * gridSize + outlineWidth/2), outlineWidth)
        