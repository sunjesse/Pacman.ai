'''
player.py
'''

import pygame
import sys
import constants

display_width = constants.display_width
display_height = constants.display_height

class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super(Pacman, self).__init__()
        self.frames = []
        self.frames.append(pygame.transform.scale(pygame.image.load("agent1.png"), (int(display_width*0.03), int(display_height*0.0525))))
        self.frames.append(pygame.transform.scale(pygame.image.load("agent1frame2.png"), (int(display_width*0.03), int(display_height*0.0525))))

        self.x = display_width * 0.5
        self.y = display_height * 0.5

        self.index = 0
        self.counter = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((self.x,self.y))

        self.move_left = False
        self.move_right = True

    def update(self):

        if self.counter == 0:
            self.index += 1

        self.counter += 1

        if self.counter % 30 == 0:
            self.counter = 0

        elif self.counter % 15 == 0:
            self.index = 0

        self.image = self.frames[self.index]
        self.rect = self.rect.move((self.x,self.y))

        if self.move_left == True:
            constants.screen.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        else:
            constants.screen.blit(self.image, (self.x, self.y))
