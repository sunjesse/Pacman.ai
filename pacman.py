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
import random
import featureExtraction

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('arial', 100)

black = constants.black

pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()

gameOver = False


def changeGameState():
    global gameOver
    if gameOver == True:
        gameOver = False
    elif gameOver == False:
        gameOver = True

def game(game_state):

    constants.score = 0
    generateLevel.createLevel()
    pacmanMain = Pacman()
    blinky = Ghost()
    walls = generateLevel.walls

    pacmanCurrentTile = featureExtraction.on_current_tile(dynamicPositions.pacman)
    crashCount = 1

    frightenModeCount = 0

    time = 0
    scatterModeCount = 0

    while not game_state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = True
                changeGameState()

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

        if blinky.reviveMode == False:
            blinky.update()

        elif blinky.reviveMode == True:
            if blinky.noMovementTime % 50 == 0: #idle time for 5/6th of a second.
                blinky.noMovementTime = 1
                blinky.reviveMode = False
            blinky.noMovementTime += 1
            if blinky.noMovementTime % 5 == 0: #shutter respawn effect.
                constants.screen.blit(blinky.image, (blinky.rect.x, blinky.rect.y))

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

        if time % 600 == 0: #every 10 seconds (including when game starts) it has 70% chance to scatter.
            if random.randint(1,100) >= 70:
                constants.scatterMode = True
                constants.chaseMode = False
            time = 0
        time += 1

        if blinky.rect.colliderect(pacmanMain.rect):
            if constants.frightenMode == True:
                blinky.rect.x = 960
                blinky.rect.y = 320
                constants.frightenMode = False
                blinky.reviveMode = True
                constants.score += 5
            else:
                changeGameState()
                game_state = True

        if featureExtraction.on_current_tile(dynamicPositions.pacman) != pacmanCurrentTile: #only do bfs when pacman changes tiles
            print(featureExtraction.bfs([featureExtraction.on_current_tile(dynamicPositions.pacman)], [featureExtraction.on_current_tile(dynamicPositions.pacman)], 0, generateLevel.coins))
            pacmanCurrentTile = featureExtraction.on_current_tile(dynamicPositions.pacman)
            #print(featureExtraction.shortest_path)
            #print(pacmanCurrentTile)

        blinky.shortest_distance = []
        blinky.tileToMove = []
        blinky.futureMovementNumber = []

        pygame.display.update()
        clock.tick(60)

game(gameOver)
while gameOver == True:
    gameOver = False
    game(gameOver)

pygame.quit()
quit()
