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

class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super(Pacman, self).__init__()
        self.frames = []
        self.frames.append(pygame.transform.scale(pygame.image.load("agent1.png"), (int(display_width*0.03), int(display_height*0.0525))))
        self.frames.append(pygame.transform.scale(pygame.image.load("agent1frame2.png"), (int(display_width*0.03), int(display_height*0.0525))))

        self.x = display_width * 0.49
        self.y = display_height * 0.446

        self.index = 0
        self.counter = 0
        self.image = self.frames[self.index]
        #self.image = pygame.image.load("agent1.png")
        self.image = pygame.transform.scale(self.image,(int(display_width*0.03), int(display_height*0.0525)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((self.x,self.y))

        self.move_left = False
        self.move_right = True
        self.move_up = False
        self.move_down = False

        self.face_left = False
        self.face_right = True

    def update(self):
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
        if self.face_left == True:
            constants.screen.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        else:
            constants.screen.blit(self.image, (self.x, self.y))

        #Wall Collisions

        for wall in walls:
            if self.rect.colliderect(wall.rect):

                if self.move_up == True:
                    self.rect.top = wall.rect.bottom
                    self.y = wall.rect.bottom

                if self.move_down == True:
                    self.rect.bottom = wall.rect.top
                    self.y = wall.rect.top - constants.display_height*0.0525

                if self.move_right == True:
                    self.rect.right = wall.rect.left
                    self.x = wall.rect.left - constants.display_width * 0.03

                if self.move_left == True:
                    self.rect.left = wall.rect.right
                    self.x = wall.rect.right
