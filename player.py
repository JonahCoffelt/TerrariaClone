import pygame

import itemData

worldGravity = -.0005

invSlotSize = 50

pygame.font.init()
font = pygame.font.Font('Assets/PixelDigivolve-mOm9.ttf' , 18 , bold = True)

class Player(object):
    def __init__(self, skin) -> None:
        self.skin = skin

        self.inv = [[0, 1] for i in range(54)]
        self.showInv = False

        self.pos = [200.0, 50.0]
        self.maxMovementSpeed = .1
        self.movementAcceleration = .008
        self.speedHorizontal = 0.0
        self.speedVertical = 0.0

    def update(self, map, keys, dt):
        #Gravity
        if self.collide(map, (self.pos[0], self.pos[1] + 1.5 + (self.speedVertical * .1 * dt))) or self.collide(map, (self.pos[0] - .7, self.pos[1] + 1.5 + (self.speedVertical * .1 * dt))) or self.collide(map, (self.pos[0] + .7, self.pos[1] + 1.5 + (self.speedVertical * .1 * dt))):
            self.pos[1] = int(self.pos[1]) + .5
            self.speedVertical = 0.0
        else:
            self.speedVertical -= worldGravity * dt

        projectedPosition = (self.pos[0] + (self.speedHorizontal * .1 * dt), self.pos[1] + (self.speedVertical * .1 * dt))

        #slow down
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            if abs(self.speedHorizontal) >= 0.002:
                self.speedHorizontal -= self.speedHorizontal * self.movementAcceleration * dt * 5
            else:
                self.speedHorizontal = 0.0

        #move horizontal
        if self.speedHorizontal > 0:
            if self.collide(map, (projectedPosition[0] + .75, self.pos[1] - 1.4)) or self.collide(map, (projectedPosition[0] + .75, self.pos[1] - 1)) or self.collide(map, (projectedPosition[0] + .75, self.pos[1] - .5)):
                self.speedHorizontal = 0.0
                self.pos[0] = int(self.pos[0]) + .25
            else:
                if self.collide(map, (projectedPosition[0] + .75, self.pos[1] + 1.4)):
                    if not self.collide(map, (projectedPosition[0], self.pos[1] - 1.6)):
                        if self.speedVertical == 0:
                            self.pos[1] = int(self.pos[1]) - .5
                            self.pos[0] = projectedPosition[0]
                    else:
                        self.speedHorizontal = 0.0
                        self.pos[0] = int(self.pos[0]) + .25
                else:
                    self.pos[0] = projectedPosition[0]
        if self.speedHorizontal < 0:
            if self.collide(map, (projectedPosition[0] - .75, self.pos[1] - 1.4)) or self.collide(map, (projectedPosition[0] - .75, self.pos[1] - 1)) or self.collide(map, (projectedPosition[0] - .75, self.pos[1] - .5)):
                self.speedHorizontal = 0.0
                self.pos[0] = int(self.pos[0]) + .75
            else:
                if self.collide(map, (projectedPosition[0] - .75, self.pos[1] + 1.4)):
                    if not self.collide(map, (projectedPosition[0], self.pos[1] - 1.6)):
                        if self.speedVertical == 0:
                            self.pos[1] = int(self.pos[1]) - .5
                            self.pos[0] = projectedPosition[0]
                    else:
                        self.speedHorizontal = 0.0
                        self.pos[0] = int(self.pos[0]) + .75
                else:
                    self.pos[0] = projectedPosition[0]
        #move vertical
        if self.speedVertical > 0:
            self.pos[1] = projectedPosition[1]
        elif self.speedVertical < 0:
            if self.collide(map, (self.pos[0], projectedPosition[1] - 1.5)) or self.collide(map, (self.pos[0] + .7, projectedPosition[1] - 1.5)) or self.collide(map, (self.pos[0] -.7, projectedPosition[1] - 1.5)):
                self.speedVertical = 0.01
            else:
                self.pos[1] = projectedPosition[1]
                
    def draw(self, win, gridSize, winSize, cameraPos):
        pygame.draw.rect(win, self.skin, (winSize[0]/2 - gridSize * .75 + gridSize*(self.pos[0] - cameraPos[0]), gridSize*45/2 - gridSize*2.5 - gridSize * 1.5 + gridSize*(self.pos[1] - cameraPos[1]), gridSize * 1.5, gridSize * 3))
        
    def drawInv(self, win):
        if self.showInv:
            levels = 6
        else:
            levels = 1
        for invLevel in range(levels):
            for slot in range(9):
                pygame.draw.rect(win, (0, 0, 0), (invSlotSize * slot * 1.15 + 10, invSlotSize * invLevel * 1.15 + 10, invSlotSize, invSlotSize), 5)
                if self.inv[invLevel * 8 + slot][0] != 0:
                    itemData.drawItem(win, self.inv[invLevel * 9 + slot][0], (invSlotSize * slot * 1.15 + 10, invSlotSize * invLevel * 1.15 + 10), invSlotSize * .8)
                    itemQuantity = font.render(str(self.inv[invLevel * 9 + slot][1]) , 1, pygame.Color("grey"))
                    win.blit(itemQuantity,(invSlotSize * slot * 1.15 + 10, invSlotSize * invLevel * 1.15 + 10))

    def collide(self, map, collisionPoint):
        if map[int(collisionPoint[1])][int(collisionPoint[0])] != 0:
            return True
        else:
            return False

    def addItem(self, itemID):
        location = 999
        for item in range(len(self.inv)):
            if itemID == self.inv[item][0]:
                location = item
            elif location == 999 and self.inv[item][0] == 0:
                location = item
        self.inv[location][0] = itemID
        self.inv[location][1] += 1

    def inputs(self, map, input, dt):
        if input == "jump":
            if self.collide(map, (self.pos[0], self.pos[1] + 1.6)) or self.collide(map, (self.pos[0] - .7, self.pos[1] + 1.6)) or self.collide(map, (self.pos[0] + .7, self.pos[1] + 1.6)):
                self.speedVertical = -.25
        if input == "right":
            if self.speedHorizontal < self.maxMovementSpeed:
                self.speedHorizontal += .1 * self.movementAcceleration * dt
        if input == "left":
            if self.speedHorizontal > self.maxMovementSpeed*-1:
                self.speedHorizontal -= .1 * self.movementAcceleration * dt
        if input == "inv":
            print("s")
            self.showInv = not self.showInv
