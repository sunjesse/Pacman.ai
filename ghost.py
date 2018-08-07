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
class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super(Ghost, self).__init__()

        self.image = pygame.image.load("ghost.png")
        self.image = pygame.transform.scale(self.image, (int(constants.display_width*0.025), int(constants.display_height*0.045)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((920, 300))

        #state
        self.chase = True

        #movement number
        self.movementNumber = 3

        #movements
        self.move_up = False
        self.move_right = False
        self.move_down = True
        self.move_left = False

        self.counter = 0
        #intersection decision making
        self.tileToMove = []
        self.short_distance = []

    def update(self):
        #movements

        if self.move_up == True:
            self.rect.y -= 0.006*constants.display_height
        elif self.move_right == True:
            self.rect.x += 0.006*constants.display_height
        elif self.move_down == True:
            self.rect.y += 0.006*constants.display_height
        elif self.move_left == True:
            self.rect.x -= 0.006*constants.display_height

        self.counter += 1
        ''' ---JUST HAVING FUN CODE--- TOO LAZY TO CODE ALGO RN'''
        if self.counter % 60 == 0:
            self.movementNumber = random.randint(1,4)

            if self.movementNumber == 1:
                self.move_up = True
                self.move_right = False
                self.move_down = False
                self.move_left = False

            elif self.movementNumber == 2:
                self.move_up = False
                self.move_right = True
                self.move_down = False
                self.move_left = False

            elif self.movementNumber == 3:
                self.move_up = False
                self.move_right = False
                self.move_down = True
                self.move_left = False

            elif self.movementNumber == 4:
                self.move_up = False
                self.move_right = False
                self.move_down = False
                self.move_left = True

            self.counter = 0
        ''' ---END OF MEME CODE--- '''

        constants.screen.blit(self.image, (self.rect.x, self.rect.y))


    def calculateDistance(self):
        return ((self.rect.x - dyanmicPositions.pacman[0])*(self.rect.x - dyanmicPositions.pacman[0]) + (self.rect.y - dyanmicPositions.pacman[1])*(self.rect.y - dyanmicPositions.pacman[1]))**(1/2)

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
