'''
pacman.py

Main File
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

frightenModeCount = 0

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True


    constants.screen.fill(black)

    generateLevel.drawWalls()
    generateLevel.drawCoins()

    label = font.render("Score: " + str(constants.score), 1, (255, 255, 255))
    constants.screen.blit(label, (constants.display_width * 0.02, constants.display_height * 0.9))

    pacmanMain.checkCollision()
    blinky.checkCollision()
    pacmanMain.update()
    #Update (x, y) position value of pacman in the global variables file dynamicPositions.py
    dynamicPositions.pacman = (pacmanMain.x, pacmanMain.y)

    blinky.update()

    if constants.frightenMode == True:
        frightenModeCount += 1
        if frightenModeCount % 150 == 0: #2.5 second frighten mode
            constants.frightenMode = False
            frightenModeCount = 0

    print(blinky.shortest_distance)
    print(blinky.willMove)

    blinky.shortest_distance = []
    blinky.tileToMove = []
    blinky.futureMovementNumber = []




    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
