import pygame
import pygame.gfxdraw
import random, math
import numpy as np

from PIL import Image, ImageFilter

from tileData import tile, bgtile
import worldGeneration
import blockLighting
import mapDrawing
import player

clock = pygame.time.Clock()

winSize = (1500.0, 1000.0)
win = pygame.display.set_mode(winSize, pygame.RESIZABLE)

run = True
pygame.init()

pygame.font.init()
font = pygame.font.Font('Assets/PixelDigivolve-mOm9.ttf' , 18 , bold = True)

playerCharacters = [player.Player((63,150,200)), player.Player((255,255,255)), player.Player((205,133,63))]
playerCharacter = playerCharacters[0]

mapSize = (500, 500)
viewWindow = [60.0, 40.0]
gridSize = winSize[0]/60.0

cameraPos = [200.0, 50.0]
cameraSpeed = .01

lightMap = np.array([[0 for x in range(mapSize[0])] for y in range(mapSize[1])])

showFX = True

def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("red"))
    win.blit(fps_t,(1400,0))

def draw():
    win.fill("light blue")
    #offset = ((cameraPos[0] - int(cameraPos[0]))*gridSize, (cameraPos[1] - int(cameraPos[1])) * gridSize)
    win.blit(bgMapSurface, (0, -1), (cameraPos[0] * gridSize - viewWindow[0]* gridSize/2, cameraPos[1] * gridSize - viewWindow[1]*gridSize/2 - 1, 1500, 1001))
    win.blit(worldMapSurface, (0, -1), (cameraPos[0] * gridSize - viewWindow[0]* gridSize/2, cameraPos[1] * gridSize - viewWindow[1]*gridSize/2 - 1, 1500, 1001))
    if showFX:
        win.blit(lightMapSurface, (0, -1), (cameraPos[0] * gridSize - viewWindow[0]* gridSize/2, cameraPos[1] * gridSize - viewWindow[1]*gridSize/2 - 1, 1600, 1100))
        win.blit(lineSurface, (0, -1), (cameraPos[0] * gridSize - viewWindow[0]* gridSize/2, cameraPos[1] * gridSize - viewWindow[1]*gridSize/2 - 1, 1500, 1001))

    for chr in playerCharacters:
        chr.draw(win, gridSize, winSize, cameraPos)


def update():
    playerCharacter.update(worldMap, keys, dt)
    draw()
    playerCharacter.drawInv(win)
    fps_counter()
    pygame.display.flip()

worldMap, backgroundMap, biomeMap = worldGeneration.generateMap(mapSize)
lightMap = blockLighting.generateLightMap(mapSize, worldMap, backgroundMap)

worldMapSurface = mapDrawing.drawMap(worldMap, mapSize, tile)
worldMapSurface = pygame.transform.scale(worldMapSurface, (mapSize[0] * gridSize, mapSize[1] * gridSize))
bgMapSurface = mapDrawing.drawMap(backgroundMap, mapSize, bgtile)
bgMapSurface= pygame.transform.scale(bgMapSurface, (mapSize[0] * gridSize, mapSize[1] * gridSize))
lightMapSurface = blockLighting.drawLightMap(lightMap, mapSize)
lightMapSurface= pygame.transform.scale(lightMapSurface, (mapSize[0] * gridSize, mapSize[1] * gridSize))
lineSurface = mapDrawing.drawLines(worldMap, mapSize, gridSize)

while run:
    dt = clock.tick(120)
    if playerCharacter.pos[1] > mapSize[1]:
        playerCharacter.pos[1] = 10.0
        playerCharacter.speedVertical = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
        if event.type == pygame.VIDEORESIZE:
            width, height = event.size
            gridSize = width/60.0
            winSize = (width, height)
        if event.type == pygame.MOUSEWHEEL:
            if int(event.y) > 0:
                showFX = True
            else:
                showFX = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                playerCharacter.inputs(worldMap, "inv", dt)
            
            '''
            pass
            viewWindow[0] -= 15* int(event.y)
            viewWindow[1] -= 10 * int(event.y)
            gridSize = winSize[0]/viewWindow[0]
            worldMapSurface = pygame.transform.scale(worldMapSurface, (mapSize[0] * gridSize, mapSize[1] * gridSize))
            '''
    
    keys = pygame.key.get_pressed()
    mouseX, mouseY = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        offset = (cameraPos[0] - int(cameraPos[0]), cameraPos[1] - int(cameraPos[1]))

        mouseWorldX = int((mouseX + offset[0]*gridSize)//gridSize + int(cameraPos[0]) - viewWindow[0]//2)
        mouseWorldY = int((mouseY + offset[1]*gridSize)//gridSize + int(cameraPos[1]) - viewWindow[1]//2)

        if worldMap[mouseWorldY][mouseWorldX] != 2:
            pygame.draw.rect(worldMapSurface, tile[2], (mouseWorldX * gridSize, mouseWorldY * gridSize, gridSize, gridSize))
            worldMap[mouseWorldY][mouseWorldX] = 2

            pos = (mouseWorldX, mouseWorldY)
            mapDrawing.redrawLines(worldMap, mapSize, gridSize, lineSurface, pos)

            lightMap = blockLighting.updateLightMap((mouseWorldX, mouseWorldY), lightMap, worldMap, backgroundMap)
            blockLighting.redrawLight(lightMap, gridSize, lightMapSurface, pos)
    
    elif pygame.mouse.get_pressed()[2]:
        offset = (cameraPos[0] - int(cameraPos[0]), cameraPos[1] - int(cameraPos[1]))

        mouseWorldX = int((mouseX + offset[0]*gridSize)//gridSize + int(cameraPos[0]) - viewWindow[0]//2)
        mouseWorldY = int((mouseY + offset[1]*gridSize)//gridSize + int(cameraPos[1]) - viewWindow[1]//2)
        
        if worldMap[mouseWorldY][mouseWorldX] != 0:
            playerCharacter.addItem(worldMap[mouseWorldY][mouseWorldX])

            pygame.draw.rect(worldMapSurface, (0, 0, 0, 0), (mouseWorldX * gridSize, mouseWorldY * gridSize, gridSize, gridSize))
            worldMap[mouseWorldY][mouseWorldX] = 0

            pos = (mouseWorldX, mouseWorldY)
            mapDrawing.redrawLines(worldMap, mapSize, gridSize, lineSurface, pos)
            
            lightMap = blockLighting.updateLightMap((mouseWorldX, mouseWorldY), lightMap, worldMap, backgroundMap)
            blockLighting.redrawLight(lightMap, gridSize, lightMapSurface, pos)


    if keys[pygame.K_r]:
        cameraPos = [200.0, 50,0]
        playerCharacter.pos = [200.0, 50,0]

    if keys[pygame.K_d]:
        playerCharacter.inputs(worldMap, "right", dt)
    elif keys[pygame.K_a]:
        playerCharacter.inputs(worldMap, "left", dt)
    if keys[pygame.K_w]:
        playerCharacter.inputs(worldMap, "jump", dt)
    if keys[pygame.K_1]:
        playerCharacter = playerCharacters[0]
    if keys[pygame.K_2]:
        playerCharacter = playerCharacters[1]
    if keys[pygame.K_3]:
        playerCharacter = playerCharacters[2]

    cameraPos[0] = cameraPos[0] + (playerCharacter.pos[0] - cameraPos[0])/2 * cameraSpeed * dt
    cameraPos[1] = cameraPos[1] + (playerCharacter.pos[1] - cameraPos[1])/2 * cameraSpeed * dt

    update()