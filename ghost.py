'''
ghost.py

Ghost class
'''

import random
import pygame
import constants

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super(Ghost, self).__init__()

        self.image = pygame.image.load("ghost.png")
        self.image = pygame.transform.scale(self.image, (int(constants.display_width*0.025), int(constants.display_height*0.045)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((900, 160))

    def update(self):
        constants.screen.blit(self.image, (self.rect.x, self.rect.y))
