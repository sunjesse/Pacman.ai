'''
ghost.py

Ghost class

'''

import random
import pygame
import constants
import dynamicPositions
import generateLevel

walls = generateLevel.walls
allTiles = generateLevel.allTiles

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super(Ghost, self).__init__()

        self.image = pygame.image.load("ghost.png")
        self.image = pygame.transform.scale(self.image, (int(constants.display_width*0.025), int(constants.display_height*0.045)))

        self.imageFrightened = pygame.image.load("ghostFrightened.png")
        self.imageFrightened = pygame.transform.scale(self.imageFrightened, (int(constants.display_width*0.025), int(constants.display_height*0.045)))

        self.rect = self.image.get_rect()
        self.rect = self.rect.move((960, 320))

        #state
        self.reviveMode = False
        self.noMovementTime = 1

        #movement number, 1 = up, 2 = right, 3 = down, 4 = left, 0 = no movement
        self.movementNumber = 5
        self.willMove = 0

        #movements
        self.move_up = False
        self.move_right = False
        self.move_down = True
        self.move_left = False

        self.face_left = False
        self.face_right = True

        self.speed = 0.00555*constants.display_height

        #intersection decision making
        self.tileToMove = []
        self.shortest_distance = []
        self.futureMovementNumber = []

        #wait
        self.wait = 0

    def update(self):

        for tile in generateLevel.intersection:
            if self.rect.colliderect(tile): #Find all neighbouring tiles that the ghost is allowed to move to and append to tileToMove list.

                if (tile.x, tile.y-60) in allTiles:
                    if (tile.x, tile.y-60) not in self.tileToMove:
                        self.tileToMove.append((tile.x, tile.y-60))
                        self.futureMovementNumber.append(1)

                if (tile.x+90, tile.y) in allTiles:
                    if (tile.x+90, tile.y) not in self.tileToMove:
                        self.tileToMove.append((tile.x+90, tile.y))
                        self.futureMovementNumber.append(2)

                if (tile.x, tile.y+60) in allTiles:
                    if (tile.x, tile.y+60) not in self.tileToMove:
                        self.tileToMove.append((tile.x, tile.y+60))
                        self.futureMovementNumber.append(3)

                if (tile.x-90, tile.y) in allTiles:
                    if (tile.x-90, tile.y) not in self.tileToMove:
                        self.tileToMove.append((tile.x-90, tile.y))
                        self.futureMovementNumber.append(4)

        #movement decision making based on mode.
        for coordinate in self.tileToMove:
            if constants.chaseMode == True or constants.frightenMode == True:
                self.shortest_distance.append(self.calculateDistance(coordinate[0], coordinate[1], dynamicPositions.pacman[0], dynamicPositions.pacman[1]))
            elif constants.scatterMode == True:
                self.shortest_distance.append(self.calculateDistance(coordinate[0], coordinate[1], 1920, 0))

        if len(self.shortest_distance) > 0:
            if constants.chaseMode == True or constants.scatterMode == True: #in chase mode or scatter, use shortest distance algorithm to reach target tile.
                self.willMove = self.futureMovementNumber[self.shortest_distance.index(min(self.shortest_distance))]
            if constants.frightenMode == True: #in frighten mode
                self.willMove = self.futureMovementNumber[random.randint(0, len(self.futureMovementNumber) - 1)]

            if self.wait % 8 == 0:
                #Determine new direction of movement
                if self.willMove == 1 and self.movementNumber != 3:
                    self.move_up = True
                    self.move_right = False
                    self.move_down = False
                    self.move_left = False
                    self.movementNumber = self.willMove

                elif self.willMove == 2 and self.movementNumber != 4:
                    self.move_up = False
                    self.move_right = True
                    self.move_down = False
                    self.move_left = False
                    self.movementNumber = self.willMove
                    self.face_right = True
                    self.face_left = False

                elif self.willMove == 3 and self.movementNumber != 1:
                    self.move_up = False
                    self.move_right = False
                    self.move_down = True
                    self.move_left = False
                    self.movementNumber = self.willMove

                elif self.willMove == 4 and self.movementNumber != 2:
                    self.move_up = False
                    self.move_right = False
                    self.move_down = False
                    self.move_left = True
                    self.movementNumber = self.willMove
                    self.face_left = True
                    self.face_right = False

                else: #find new movement number because it cannot go back from where it came from
                    self.willMove = self.futureMovementNumber[self.secondMinimumIndex(self.futureMovementNumber)]
                    self.movementNumber = 5

                self.wait = 0

            self.wait += 1

        #movements: if ghost rect wants to moves, then save its previous frame's position.
        if self.move_up == True:
            #self.frame_before_rect = self.rect
            self.rect.y -= self.speed
        elif self.move_right == True:
            #self.frame_before_rect = self.rect
            self.rect.x += self.speed
        elif self.move_down == True:
            #self.frame_before_rect = self.rect
            self.rect.y += self.speed
        elif self.move_left == True:
            #self.frame_before_rect = self.rect
            self.rect.x -= self.speed


        if constants.frightenMode == False:
            if self.face_left == True:
                constants.screen.blit(pygame.transform.flip(self.image, True, False), (self.rect.x, self.rect.y))
            else:
                constants.screen.blit(self.image, (self.rect.x, self.rect.y))

        elif constants.frightenMode == True:
            constants.screen.blit(self.imageFrightened, (self.rect.x, self.rect.y))
        #draw rect.x and rect.y positions
        #pygame.draw.circle(constants.screen, (255, 0, 0), (self.rect.x, self.rect.y), 4)


    def calculateDistance(self, x, y, x1, y1):
        return ((x - x1)*(x - x1) + (y - y1)*(y - y1))**(1/2)

    def checkCollision(self):
        for wall in walls:
            if self.rect.colliderect(wall.rect):

                if self.move_up == True:
                    self.rect.top = wall.rect.bottom
                    if (self.rect.left - wall.rect.right)**2 < (self.rect.left - wall.rect.left)**2: #moving to right side of wall
                        self.rect.left += self.speed
                    else:
                        self.rect.left -= self.speed

                if self.move_down == True:
                    self.rect.bottom = wall.rect.top
                    if (self.rect.left - wall.rect.right)**2 < (self.rect.left - wall.rect.left)**2: #moving to right side of wall
                        self.rect.left += self.speed
                    else:
                        self.rect.left -= self.speed

                if self.move_right == True:
                    self.rect.right = wall.rect.left
                    if (self.rect.top - wall.rect.bottom)**2 < (self.rect.top - wall.rect.top)**2:
                        self.rect.top += self.speed
                    else:
                        self.rect.top -= self.speed

                if self.move_left == True:
                    self.rect.left = wall.rect.right
                    if (self.rect.top - wall.rect.bottom)**2 < (self.rect.top - wall.rect.top)**2:
                        self.rect.top += self.speed
                    else:
                        self.rect.top -= self.speed

    def secondMinimumIndex(self, list): #returns the index of the second minimum distance tile. Used when the bot is stuck.
        self.reducedList = list
        self.indexOfFirstMin = self.reducedList.index(min(self.reducedList))
        self.reducedList.remove(min(self.reducedList))
        self.indexOfSecondMin = self.reducedList.index(min(self.reducedList))
        if self.indexOfSecondMin <= self.indexOfFirstMin:
            return self.indexOfSecondMin
        elif self.indexOfSecondMin > self.indexOfFirstMin:
            return self.indexOfSecondMin + 1
