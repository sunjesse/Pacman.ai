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

font = pygame.font.SysFont('arial', 50)

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

def reset():
    generateLevel.walls = []
    generateLevel.coins = []
    generateLevel.coinsObjects = []
    generateLevel.intersection = []
    generateLevel.allTiles = []
    generateLevel.frightenTiles = []
    constants.frightenMode = False
    constants.scatterMode = False
    constants.chaseMode = True

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

    networks = genetic.populate(1, 35, 26, 26, 4) #1 neural net, 5 input nodes, 4 hidden nodes

    while not game_state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                changeGameState()
                game_state = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    changeGameState()
                    '''#FITNESS: update fitness - terminate the episode ---'''
                    networks[0].fitness -= 500
                    print("Final fitness: "  + str(networks[0].fitness))
                    game_state = True #Set fitness to very negative number like -1000

        score_before_script = constants.score
        wall_collide_number_before_script = constants.wall_collide_number

        constants.screen.fill(black)

        generateLevel.drawWalls()
        generateLevel.drawCoins()

        label = font.render("Score: " + str(constants.score), 1, (255, 255, 255))
        constants.screen.blit(label, (constants.display_width * 0.02, constants.display_height * 0.9))

        label2 = font.render("Fitness: " + str(networks[0].fitness), 1, (255, 255, 255))
        constants.screen.blit(label2, (constants.display_width * 0.02, constants.display_height * 0.85))

        label2 = font.render("Generation: 1  Iteration: " + str(iteration), 1, (255, 255, 255))
        constants.screen.blit(label2, (constants.display_width * 0.02, constants.display_height * 0.01))

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

                '''#FITNESS: update fitness - for eating ghost'''
                networks[0].fitness += 200
                print(networks[0].fitness)

            else: #lose the game
                changeGameState()
                '''#FITNESS: update fitness - losing the game'''
                networks[0].fitness -= 500
                print("Final fitness: "  + str(networks[0].fitness))
                game_state = True

        if featureExtraction.on_current_tile((blinky.rect.x, blinky.rect.y), blinky) != blinkyCurrentTile: #blinky change tile
            blinkyCurrentTile = featureExtraction.on_current_tile((blinky.rect.x, blinky.rect.y), blinky)

        if featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain) != pacmanCurrentTile: #only do bfs when pacman changes tiles
            pacmanCurrentTile = featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)
            closest_food = featureExtraction.bfs([featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], [featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], 0, generateLevel.coins)

        #features
        food_pos = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 1, "food", blinkyCurrentTile)
        enemy_pos = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 1, "ghost", blinkyCurrentTile)
        wall_pos = featureExtraction.check_tile(generateLevel.wallPositions, pacmanCurrentTile, 1, "wall", blinkyCurrentTile)
        food_pos_2 = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 2, "food", blinkyCurrentTile)
        enemy_pos_2 = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 2, "ghost", blinkyCurrentTile)
        wall_pos_2 = featureExtraction.check_tile(generateLevel.wallPositions, pacmanCurrentTile, 2, "wall", blinkyCurrentTile)
        distance_between = featureExtraction.distance_between((pacmanMain.rect.x, pacmanMain.rect.y), (blinky.rect.x, blinky.rect.y))

        inputVector = featureExtraction.extract(food_pos, enemy_pos, wall_pos, food_pos_2, enemy_pos_2, wall_pos_2, closest_food, distance_between, constants.frightenMode)

        pacmanMain.automate(networks[0].process(inputVector))
        #print(networks[0].process(inputVector))
        #print(networks[0].show(inputVector))

        ''' ---- #FITNESS: Update fitness of network ---- '''
        score_after_script = constants.score
        wall_collide_number_after_script = constants.wall_collide_number

        if not game_state: #don't update score if game is over, -12 every second
            if time % 5 == 0: #time penalty
                networks[0].fitness -= 1
                #print(networks[0].fitness)

            if score_after_script - score_before_script == 1: #reward for eating a food/coin
                networks[0].fitness += 10
                #print(networks[0].fitness)
            if wall_collide_number_after_script - wall_collide_number_before_script > 0: #penalty for hitting wall
                networks[0].fitness -= 1

            if len(generateLevel.coinsObjects) == 0: #if pacman wins the game
                networks[0].fitness += 500
                #print(networks[0].fitness)

            if networks[0].fitness <= -50: #move to next network
                    changeGameState()
                    '''#FITNESS: update fitness - terminate the episode ---'''
                    #networks[0].fitness -= 500
                    print("Final fitness: "  + str(networks[0].fitness))
                    game_state = True #Set fitness to very negative number like -1000

        ''' ---- End update fitness of network ---- '''

        blinky.shortest_distance = []
        blinky.tileToMove = []
        blinky.futureMovementNumber = []

        pygame.display.update()
        clock.tick(60)

game(gameOver)
while gameOver == True:
    gameOver = False
    iteration += 1
    reset()
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
