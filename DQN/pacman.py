'''
pacman.py

Main File
'''
from wall import Wall
from ghost import Ghost
from player import Pacman
from neuralnet import Neural
import pygame
import sys
import player
import constants
import levels
import generateLevel
import dynamicPositions
import random
import featureExtraction
import shelve
import replay_buffer

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('arial', 50)

black = constants.black

pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()

gameOver = False
#Functions
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

def game(game_state, q_net):
    constants.score = 0
    constants.wall_collide_number = 0

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


    while not game_state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                changeGameState()
                game_state = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    changeGameState()
                    '''#FITNESS: update fitness - terminate the episode ---'''
                    q_net.fitness -= 500
                    #print("Final fitness: "  + str(q_net.fitness))
                    game_state = True #Set fitness to very negative number like -1000

        score_before_script = constants.score
        wall_collide_number_before_script = constants.wall_collide_number

        constants.screen.fill(black)

        generateLevel.drawWalls()
        generateLevel.drawCoins()

        label = font.render("Score: " + str(constants.score), 1, (255, 255, 255))
        constants.screen.blit(label, (constants.display_width * 0.02, constants.display_height * 0.9))

        label2 = font.render("Fitness: " + str(q_net.fitness), 1, (255, 255, 255))
        constants.screen.blit(label2, (constants.display_width * 0.02, constants.display_height * 0.85))

        label4 = font.render("Peak Fitness: " + str(q_net.peak_fitness), 1, (255, 255, 255))
        constants.screen.blit(label4, (constants.display_width * 0.02, constants.display_height * 0.80))

        label3 = font.render("Generation: " + str(generation) + "  Iteration: " + str(iteration), 1, (255, 255, 255))
        constants.screen.blit(label3, (constants.display_width * 0.02, constants.display_height * 0.01))

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
                q_net.fitness += 200
                if q_net.fitness > q_net.peak_fitness:
                    q_net.peak_fitness = q_net.fitness
                print(q_net.fitness)

            else: #lose the game
                changeGameState()
                '''#FITNESS: update fitness - losing the game'''
                q_net.fitness -= 500
                #print("Final fitness: "  + str(q_net.fitness))
                game_state = True
                pacmanMain.kill()
                blinky.kill()

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
        #wall_pos_2 = featureExtraction.check_tile(generateLevel.wallPositions, pacmanCurrentTile, 2, "wall", blinkyCurrentTile)
        distance_between = featureExtraction.distance_between((pacmanMain.rect.x, pacmanMain.rect.y), (blinky.rect.x, blinky.rect.y))

        inputVector = featureExtraction.extract(food_pos, enemy_pos, wall_pos, food_pos_2, enemy_pos_2, closest_food, distance_between, constants.frightenMode)

        pacmanMain.automate(q_net.process(inputVector))
        #print(q_net.process(inputVector))
        #print(q_net.show(inputVector))

        ''' ---- #FITNESS: Update fitness of network ---- '''
        score_after_script = constants.score
        wall_collide_number_after_script = constants.wall_collide_number

        if not game_state: #don't update score if game is over, -12 every second
            if time % 5 == 0: #time penalty
                q_net.fitness -= 1
                #print(q_net.fitness)

            if score_after_script - score_before_script == 1: #reward for eating a food/coin
                q_net.fitness += 10
                if q_net.fitness > q_net.peak_fitness:
                    q_net.peak_fitness = q_net.fitness
                #print(q_net.fitness)
            if wall_collide_number_after_script - wall_collide_number_before_script > 0: #penalty for hitting wall
                q_net.fitness -= 1

            if len(generateLevel.coinsObjects) == 0: #if pacman wins the game
                q_net.fitness += 500
                if q_net.fitness > q_net.peak_fitness:
                    q_net.peak_fitness = q_net.fitness
                #print(q_net.fitness)

            if q_net.fitness <= -50: #move to next network
                    changeGameState()
                    '''#FITNESS: update fitness - terminate the episode ---'''
                    #q_net.fitness -= 500
                    #print("Final fitness: "  + str(q_net.fitness))
                    game_state = True #Set fitness to very negative number like -1000
                    pacmanMain.kill()
                    blinky.kill()

        ''' ---- End update fitness of network ---- '''

        blinky.shortest_distance = []
        blinky.tileToMove = []
        blinky.futureMovementNumber = []

        pygame.display.update()
        clock.tick(60)


''' ---- DQN  ---- '''
replay_buffer_size = 10000
q_network = Neural()
q_network.init_weights(31, 23, 23, 4) ''' !!! CHECK OVER NUMBER OF FEATURE DIMENSIONS !!!'''
epislon = 1

while(True):
