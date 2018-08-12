'''
pacman.py

Main File

To Do:
1. Pacman and ghost collision implement.
2. Add animation of ghost travelling back to base when eliminated.
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
import random

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

time = 0
scatterModeCount = 0

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
        if constants.scatterMode == True or constants.chaseMode == True:
            constants.scatterMode = False
            constants.chaseMode = False
        frightenModeCount += 1
        if frightenModeCount % 150 == 0: #2.5 second frighten mode
            constants.frightenMode = False
            frightenModeCount = 0

    if constants.scatterMode == True:
        if constants.chaseMode or constants.frightenMode:
            constants.frightenMode = False
            constants.chaseMode = False
        scatterModeCount += 1
        if scatterModeCount % 180 == 0: #scatter lasts for 3 seconds
            constants.scatterMode = False
            scatterModeCount = 0


    if constants.chaseMode == False and constants.frightenMode == False and constants.scatterMode == False:
        constants.chaseMode = True

    if time % 600 == 0: #every 10 seconds (including when game starts) it has 50% chance to scatter.
        if random.randint(1,100) >= 50:
            constants.scatterMode = True
            constants.chaseMode = False
        time = 0
    time += 1

    #print(str(blinky.willMove) + " " + str(constants.scatterMode) + " " + str(constants.chaseMode) + " " + str(constants.frightenMode) + " " + str(frightenModeCount))
    print(blinky.shortest_distance)
    print(blinky.willMove)



    blinky.shortest_distance = []
    blinky.tileToMove = []
    blinky.futureMovementNumber = []




    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
