'''
pacman.py

Main File
'''

import pygame
import sys
from player import Pacman
import player
from ghost import Ghost
import constants
from wall import Wall
import levels
import generateLevel
import dynamicPositions
import random
import featureExtraction
import geneticAlgorithm as genetic


pygame.init()
pygame.font.init()

font = pygame.font.SysFont('arial', 100)

black = constants.black

pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()

gameOver = False

iteration = 1
#networks = genetic.populate(1, 27, 20, 20, 4) #generation one

def changeGameState():
    global gameOver
    if gameOver == True:
        gameOver = False
    elif gameOver == False:
        gameOver = True

def resetLists():
    generateLevel.walls = []
    generateLevel.coins = []
    generateLevel.coinsObjects = []
    generateLevel.intersection = []
    generateLevel.allTiles = []
    generateLevel.frightenTiles = []

def game(game_state):
    #global networks

    constants.score = 0
    generateLevel.createLevel()
    pacmanMain = Pacman()
    blinky = Ghost()
    walls = generateLevel.walls

    #initialize some feature variables
    pacmanCurrentTile = featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)
    blinkyCurrentTile = featureExtraction.on_current_tile((blinky.rect.x, blinky.rect.y), blinky)
    closest_food = featureExtraction.bfs([featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], [featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], 0, generateLevel.coins)


    crashCount = 1

    frightenModeCount = 0

    time = 0
    scatterModeCount = 0

    networks = genetic.populate(1, 27, 20, 20, 4) #1 neural net, 5 input nodes, 4 hidden nodes

    while not game_state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                changeGameState()
                game_state = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    changeGameState()
                    game_state = True #Set fitness to very negative number like -1000

        constants.screen.fill(black)

        generateLevel.drawWalls()
        generateLevel.drawCoins()

        label = font.render("Score: " + str(constants.score), 1, (255, 255, 255))
        constants.screen.blit(label, (constants.display_width * 0.02, constants.display_height * 0.9))

        #label2 = font.render("Generation: 1 Iteration:" + str(iteration), 1, (255, 255, 255))
        #constants.screen.blit(label2, (constants.display_width * 0.02, constants.display_height * 0.8))

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
                print(True)
            else:
                changeGameState()
                game_state = True

        if featureExtraction.on_current_tile((blinky.rect.x, blinky.rect.y), blinky) != blinkyCurrentTile: #blinky change tile
            blinkyCurrentTile = featureExtraction.on_current_tile((blinky.rect.x, blinky.rect.y), blinky)

        if featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain) != pacmanCurrentTile: #only do bfs when pacman changes tiles
            pacmanCurrentTile = featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)
            closest_food = featureExtraction.bfs([featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], [featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], 0, generateLevel.coins)
            print(pacmanCurrentTile)
        #features
        food_pos = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 1, "food", blinkyCurrentTile)
        enemy_pos = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 1, "ghost", blinkyCurrentTile)
        food_pos_2 = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 2, "food", blinkyCurrentTile)
        enemy_pos_2 = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 2, "ghost", blinkyCurrentTile)
        distance_between = featureExtraction.distance_between((pacmanMain.rect.x, pacmanMain.rect.y), (blinky.rect.x, blinky.rect.y))

        inputVector = featureExtraction.extract(food_pos, enemy_pos, food_pos_2, enemy_pos_2, closest_food, distance_between, constants.frightenMode)

        pacmanMain.automate(networks[0].process(inputVector))
        #print(networks[0].process(inputVector))
        #print(networks[0].show(inputVector))
        blinky.shortest_distance = []
        blinky.tileToMove = []
        blinky.futureMovementNumber = []

        pygame.display.update()
        clock.tick(60)

game(gameOver)
while gameOver == True:
    gameOver = False
    iteration += 1
    resetLists()
    game(gameOver)

pygame.quit()
quit()

'''
for i in range(len(networks)):
    print(i)
    game(gameOver, i)
    if gameOver == True:
        gameOver = False
        continue
'''
