import pygame


class Wall():

    def __init__(self, pos):

        #pacman.walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 90, 60)

'''
        super(Wall, self).__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(blue)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
'''
