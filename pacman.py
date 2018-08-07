'''
pacman.py

Main File

SATURDAY TO DO:
1. Find better method of detect wall collision, for loop is not efficient and fast.

'''

import pygame
import sys
from player import Pacman
from ghost import Ghost
import constants
from wall import Wall
import levels
import generateLevel
import dynamicPositions

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('arial', 100)

black = constants.black

pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()

crashed = False


pacmanMain = Pacman()
#pacmanGroup = pygame.sprite.Group(pacmanMain)

blinky = Ghost()

walls = generateLevel.walls

crashCount = 1

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True


    constants.screen.fill(black)

    generateLevel.drawWalls()
    generateLevel.drawCoins()

    label = font.render("Score: " + str(constants.score), 1, (255, 255, 255))
    constants.screen.blit(label, (constants.display_width * 0.02, constants.display_height * 0.9))

    ''' ---DEBUGGING CODE ---- WALL COLLISION DETECTION'''
    #for wall in walls: #DEBUGGING CODE
    #    if pacmanMain.rect.colliderect(wall.rect):
    #        print(crashCount)
    #        crashCount += 1


    pacmanMain.checkCollision()
    blinky.checkCollision()
    blinky.update()
    pacmanMain.update()

    print(blinky.counter)

    #Update (x, y) position value of pacman in the global variables file dynamicPositions.py
    dynamicPositions.pacman = (pacmanMain.x, pacmanMain.y)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
