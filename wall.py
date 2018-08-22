import pygame


class Wall():

    def __init__(self, pos):

        self.rect = pygame.Rect(pos[0], pos[1], 90, 60)
