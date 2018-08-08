'''
ghost.py

Ghost class

TO DO:
1. MAKE SURE GHOST DOES NOT GO BACK TO A TILE IT JUST CAME FROM.
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
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((960, 300))

        #state
        self.chase = True

        #movement number, 1 = up, 2 = right, 3 = down, 4 = left, 0 = no movement
        self.movementNumber = 5
        self.willMove = 0

        #movements
        self.move_up = False
        self.move_right = False
        self.move_down = False
        self.move_left = False

        #intersection decision making
        self.tileToMove = []
        self.shortest_distance = []
        self.futureMovementNumber = []

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

        for coordinate in self.tileToMove:
            self.shortest_distance.append(self.calculateDistance(coordinate[0], coordinate[1]))

        if len(self.shortest_distance) > 0:
            self.willMove = self.futureMovementNumber[self.shortest_distance.index(min(self.shortest_distance))]

            #Determine new direction of movement
            if self.willMove == 1 and self.willMove != self.movementNumber:
                self.move_up = True
                self.move_right = False
                self.move_down = False
                self.move_left = False
                self.movementNumber = self.willMove

            elif self.willMove == 2 and self.willMove != self.movementNumber:
                self.move_up = False
                self.move_right = True
                self.move_down = False
                self.move_left = False
                self.movementNumber = self.willMove

            elif self.willMove == 3 and self.willMove != self.movementNumber:
                self.move_up = False
                self.move_right = False
                self.move_down = True
                self.move_left = False
                self.movementNumber = self.willMove

            elif self.willMove == 4 and self.willMove != self.movementNumber:
                self.move_up = False
                self.move_right = False
                self.move_down = False
                self.move_left = True
                self.movementNumber = self.willMove

        #movements
        if self.move_up == True:
            self.rect.y -= 0.006*constants.display_height
        elif self.move_right == True:
            self.rect.x += 0.006*constants.display_height
        elif self.move_down == True:
            self.rect.y += 0.006*constants.display_height
        elif self.move_left == True:
            self.rect.x -= 0.006*constants.display_height

        if self.move_left == True:
            constants.screen.blit(pygame.transform.flip(self.image, True, False), (self.rect.x, self.rect.y))
        else:
            constants.screen.blit(self.image, (self.rect.x, self.rect.y))

        pygame.draw.circle(constants.screen, (255, 0, 0), (self.rect.x, self.rect.y), 4)


    def calculateDistance(self, x, y):
        return ((x - dynamicPositions.pacman[0])*(x - dynamicPositions.pacman[0]) + (y - dynamicPositions.pacman[1])*(y - dynamicPositions.pacman[1]))**(1/2)

    def checkCollision(self):
        for wall in walls:
            if self.rect.colliderect(wall.rect):

                if self.move_up == True:
                    self.rect.top = wall.rect.bottom

                if self.move_down == True:
                    self.rect.bottom = wall.rect.top

                if self.move_right == True:
                    self.rect.right = wall.rect.left

                if self.move_left == True:
                    self.rect.left = wall.rect.right
