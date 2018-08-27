'''
player.py
'''

import pygame
import sys
import constants
import generateLevel

display_width = constants.display_width
display_height = constants.display_height
walls = generateLevel.walls
coins = generateLevel.coinsObjects
coinPos = generateLevel.coins

class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super(Pacman, self).__init__()
        self.frames = []
        self.frames.append(pygame.transform.scale(pygame.image.load("img/agent1x.png"), (int(display_width*0.0224), int(display_height*0.04))))
        self.frames.append(pygame.transform.scale(pygame.image.load("img/agent1frame2x.png"), (int(display_width*0.0224), int(display_height*0.04))))

        self.x = display_width * 0.49
        self.y = display_height * 0.45

        self.index = 0
        self.counter = 0
        self.image = self.frames[self.index]
        #self.image = pygame.image.load("agent1.png")
        #self.image = pygame.transform.scale(self.image,(int(display_width*0.03), int(display_height*0.0525)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((self.x, self.y))

        self.move_left = False
        self.move_right = True
        self.move_up = False
        self.move_down = False

        self.face_left = False
        self.face_right = True

    def update(self):

        self.moveAgent()
        #Animation
        if self.counter == 0:
            self.index += 1

        self.counter += 1

        if self.counter % 30 == 0:
            self.counter = 0

        elif self.counter % 15 == 0:
            self.index = 0

        self.image = self.frames[self.index]

        #Direction Vertical Flip
        if self.move_left == True:
            constants.screen.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        elif self.move_right == True:
            constants.screen.blit(self.image, (self.x, self.y))
        elif self.move_up == True:
            constants.screen.blit(pygame.transform.rotate(self.image, 90), (self.x, self.y))
        elif self.move_down == True:
            constants.screen.blit(pygame.transform.rotate(self.image, -90), (self.x, self.y))

        ''' ----DEBUGGING LINE---- DISPLAYS THE RECT.X and RECT.Y VALUES'''
        #pygame.draw.circle(constants.screen, (255, 0, 0), (self.rect.x, self.rect.y), 4)


    def moveAgent(self):
        keys = pygame.key.get_pressed() #TEMPORARY || WILL MAKE IT TOGGLE WHEN QLEARNING GETS IMPLEMENTED
        if keys[pygame.K_LEFT]:
            self.x -= 0.006*constants.display_height
            self.rect.x = self.x
            self.move_left = True
            self.move_right = False
            self.move_up = False
            self.move_down = False

            self.face_left = True
            self.face_right = False
            self.rect = self.rect.move(-0.006*constants.display_height, 0)

        elif keys[pygame.K_RIGHT]:
            self.x += 0.006*constants.display_height
            self.rect.x = self.x
            self.move_left = False
            self.move_right = True
            self.move_up = False
            self.move_down = False

            self.face_right = True
            self.face_left = False
            self.rect = self.rect.move(0.006*constants.display_height, 0)

        elif keys[pygame.K_UP]:
            self.y -= 0.006*constants.display_height
            self.rect.y = self.y
            self.rect = self.rect.move(0, -0.006*constants.display_height)
            self.move_up = True
            self.move_down = False
            self.move_right = False
            self.move_left = False

        elif keys[pygame.K_DOWN]:
            self.y += 0.006*constants.display_height
            self.rect.y = self.y
            self.rect = self.rect.move(0, 0.006*constants.display_height)
            self.move_up = False
            self.move_down = True
            self.move_right = False
            self.move_left = False

    def automate(self, movement):
        if movement == 0:
            self.y -= 0.006*constants.display_height
            self.rect.y = self.y
            self.rect = self.rect.move(0, -0.006*constants.display_height)
            self.move_up = True
            self.move_down = False
            self.move_right = False
            self.move_left = False

        elif movement == 1:
            self.x += 0.006*constants.display_height
            self.rect.x = self.x
            self.move_left = False
            self.move_right = True
            self.move_up = False
            self.move_down = False

            self.face_right = True
            self.face_left = False
            self.rect = self.rect.move(0.006*constants.display_height, 0)
        elif movement == 2:
            self.y += 0.006*constants.display_height
            self.rect.y = self.y
            self.rect = self.rect.move(0, 0.006*constants.display_height)
            self.move_up = False
            self.move_down = True
            self.move_right = False
            self.move_left = False
        elif movement == 3:
            self.x -= 0.006*constants.display_height
            self.rect.x = self.x
            self.move_left = True
            self.move_right = False
            self.move_up = False
            self.move_down = False

            self.face_left = True
            self.face_right = False
            self.rect = self.rect.move(-0.006*constants.display_height, 0)

    #Wall collisions
    def checkCollision(self):
        for wall in walls:
            if self.rect.colliderect(wall.rect):

                if self.move_up == True:
                    self.rect.top = wall.rect.bottom
                    self.y = wall.rect.bottom

                if self.move_down == True:
                    self.rect.bottom = wall.rect.top
                    self.y = wall.rect.top - constants.display_height * 0.04

                if self.move_right == True:
                    self.rect.right = wall.rect.left
                    self.x = wall.rect.left - constants.display_width * 0.0224

                if self.move_left == True:
                    self.rect.left = wall.rect.right
                    self.x = wall.rect.right

        for coin in coins:
            if self.rect.colliderect(coin):
                index = coins.index(coin)
                coins.remove(coin) #remove object
                if coinPos[index] in generateLevel.frightenTiles:
                    constants.frightenMode = True
                coinPos.pop(index) #remove (x,y) position of coin
                constants.score += 1
