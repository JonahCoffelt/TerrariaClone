import pygame
from PIL import Image

images = []

GroundSheet = pygame.image.load(r'GroundTileSheet.png')

def findBox(x, y, pixelMap):
    x1, y1 = x, y
    while pixelMap[x1, y1] != (0, 255, 0, 255): #find green
        x1 += 1
    while pixelMap[x1, y1] != (0, 0, 255, 255): #find blue
        y1 += 1
    return(x1, y1)

def SplitSheet(currentSheet, name):
    filename = "{}.png".format(name)
    filepath = f"{filename}"
    pixelMap = Image.open(filepath).load()
    for y in range(0, Image.open(filepath).size[1]):
        for x in range(0, Image.open(filepath).size[0]):
            #Red pixel found, will now search through to find green and blue
            if pixelMap[x, y] == (255, 0, 0, 255):
                #pixels found, creating new surface and storing it in images
                coords = findBox(x, y, pixelMap)
                surf = pygame.Surface((coords[0]-1 - x, coords[1] - y-1))
                surf.blit(currentSheet, (0, 0), (x + 1, y + 1, coords[0] - 1, coords[1] - 1))
                surf = pygame.transform.scale(surf, ((coords[0] - x) * 3, (coords[1] - y) * 3))
                surf.set_colorkey((0, 0, 0))
                images[len(images) - 1].append(surf)

def processImageSheets(sheet, name):
    images.append([])
    SplitSheet(sheet, name)
    return images

#To access images use:
#win.blit(images["Shotgun"], (100, 100))