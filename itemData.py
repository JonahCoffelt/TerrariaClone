import pygame

itemData = {
    0 : ((25, 50, 255), ((0, 0), (1, 0), (1, 1), (0, 1))), #Air
    1 : ((55, 225, 45), ((0, 0), (1, 0), (1, 1), (0, 1))), #Grass
    2 : ((110, 75, 40), ((0, 0), (1, 0), (1, 1), (0, 1))), #Dirt
    3 : ((100, 100, 105), ((0, 0), (1, 0), (1, 1), (0, 1))), #Stone
    4 : ((255,255,102), ((0, 0), (1, 0), (1, 1), (0, 1))),  #Sand
    5 : ((180,230,255), ((0, 0), (1, 0), (1, 1), (0, 1))), #Snow
    6 : ((55,150,200), ((0, 0), (1, 0), (1, 1), (0, 1))) #Ice
}

def drawItem(win, item, pos, scale):
    #positions = [(x, y) for x, y in itemData[item][1]]
    pygame.draw.polygon(win, itemData[item][0], [(x * scale + pos[0], y * scale + pos[1]) for x, y in itemData[item][1]])
    pygame.draw.polygon(win, "black", [(x * scale + pos[0], y * scale + pos[1]) for x, y in itemData[item][1]], 2)