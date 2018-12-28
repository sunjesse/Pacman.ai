'''
pacman.py

Main File
'''
from wall import Wall
from ghost import Ghost
from player import Pacman
from simulatedannealing import SimulatedAnnealing
import pygame
import sys
import player
import constants
import levels
import generateLevel
import dynamicPositions
import random
import featureExtraction
import geneticAlgorithm as genetic
import shelve

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('arial', 50)

black = constants.black

pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()

#load training data
filename='database.db'
#filename = ''
shelf = shelve.open(filename)
try:
    current_gen = shelf["current_generation"]
finally:
    shelf.close()

gameOver = False
generation = current_gen #loaded from shelve.out

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

def generate_generation(generation):
    if generation == 1:
        networks = genetic.populate(5, 35, 26, 26, 4)
    else:
        networks = genetic.evolve(best_nets, 5)

def game(game_state):
    global networks
    global generation

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

    #networks = genetic.populate(1, 35, 26, 26, 4) #1 neural net, 5 input nodes, 4 hidden nodes

    while not game_state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                changeGameState()
                game_state = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    changeGameState()
                    '''#FITNESS: update fitness - terminate the episode ---'''
                    networks[i].fitness -= 500
                    #print("Final fitness: "  + str(networks[i].fitness))
                    game_state = True #Set fitness to very negative number like -1000

        score_before_script = constants.score
        wall_collide_number_before_script = constants.wall_collide_number

        constants.screen.fill(black)

        generateLevel.drawWalls()
        generateLevel.drawCoins()

        label = font.render("Score: " + str(constants.score), 1, (255, 255, 255))
        constants.screen.blit(label, (constants.display_width * 0.02, constants.display_height * 0.9))

        label2 = font.render("Fitness: " + str(networks[i].fitness), 1, (255, 255, 255))
        constants.screen.blit(label2, (constants.display_width * 0.02, constants.display_height * 0.85))

        label4 = font.render("Peak Fitness: " + str(networks[i].peak_fitness), 1, (255, 255, 255))
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
                networks[i].fitness += 200
                if networks[i].fitness > networks[i].peak_fitness:
                    networks[i].peak_fitness = networks[i].fitness
                print(networks[i].fitness)

            else: #lose the game
                changeGameState()
                '''#FITNESS: update fitness - losing the game'''
                networks[i].fitness -= 500
                #print("Final fitness: "  + str(networks[i].fitness))
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

        pacmanMain.automate(networks[i].process(inputVector))
        #print(networks[i].process(inputVector))
        #print(networks[i].show(inputVector))

        ''' ---- #FITNESS: Update fitness of network ---- '''
        score_after_script = constants.score
        wall_collide_number_after_script = constants.wall_collide_number

        if not game_state: #don't update score if game is over, -12 every second
            if time % 5 == 0: #time penalty
                networks[i].fitness -= 1
                #print(networks[i].fitness)

            if score_after_script - score_before_script == 1: #reward for eating a food/coin
                networks[i].fitness += 10
                if networks[i].fitness > networks[i].peak_fitness:
                    networks[i].peak_fitness = networks[i].fitness
                #print(networks[i].fitness)
            if wall_collide_number_after_script - wall_collide_number_before_script > 0: #penalty for hitting wall
                networks[i].fitness -= 1

            if len(generateLevel.coinsObjects) == 0: #if pacman wins the game
                networks[i].fitness += 500
                if networks[i].fitness > networks[i].peak_fitness:
                    networks[i].peak_fitness = networks[i].fitness
                #print(networks[i].fitness)

            if networks[i].fitness <= -50: #move to next network
                    changeGameState()
                    '''#FITNESS: update fitness - terminate the episode ---'''
                    #networks[i].fitness -= 500
                    #print("Final fitness: "  + str(networks[i].fitness))
                    game_state = True #Set fitness to very negative number like -1000
                    pacmanMain.kill()
                    blinky.kill()

        ''' ---- End update fitness of network ---- '''

        blinky.shortest_distance = []
        blinky.tileToMove = []
        blinky.futureMovementNumber = []

        pygame.display.update()
        clock.tick(60)

training = True

shelf = shelve.open(filename)
if shelf["current_generation"] == 1:
    best_nets = []
else:
    best_nets = shelf[str(generation-1)]

print(shelf["current_generation"])
shelf.close()

random_nets = []

while training:
    #generate a Generation
    iteration = 1

    minimum_peak_fitness = 10000000
    index_of_minimum = None

    if generation == 1:
        networks = genetic.populate(1000, 35, 26, 26, 4)
    else:
        networks = genetic.evolve(best_nets, 1000)
        best_nets = []

        #print(len(networks))

    for i in range(len(networks)): #goes through a generation
        #print(i)
        game(gameOver)

        if gameOver == True:
            if len(best_nets) < 10:
                best_nets.append((networks[i])) #append tuple (network, network's peak fitness)
                if networks[i].peak_fitness < minimum_peak_fitness:
                    minimum_peak_fitness = networks[i].peak_fitness
                    index_of_minimum = best_nets.index(networks[i])
                #print(index_of_minimum)

            else:
                if networks[i].peak_fitness > minimum_peak_fitness:
                    best_nets[index_of_minimum] = networks[i]
                    new_peak_min = 10000000
                    new_index = 0

                    iteration_counter = 0
                    for net in best_nets: #find the new minimum peak fitness value in the list
                        if net.peak_fitness < new_peak_min:
                            new_peak_min = net.peak_fitness
                            new_index = iteration_counter
                        iteration_counter += 1
                        print(net.peak_fitness)
                    minimum_peak_fitness = new_peak_min
                    index_of_minimum = new_index

            #randomly adds networks so they have a chance of being selected onto next generation.
            if random.randint(1, 100) == 1:
                random_nets.append(network[i])

            print("Min: "  + str(minimum_peak_fitness))
            #print(len(best_nets))
            gameOver = False
            iteration += 1
            reset()
            continue

    generation += 1 #move to next generation

    annealing = SimulatedAnnealing()

    for net in best_nets: #reset the fitness of the nets that will be used in the next generation.
        net.fitness = 0
        net.peak_fitness = 0

    shelf = shelve.open(filename)
    try:
        shelf["current_generation"] = generation #stores what generation we are on
        shelf[str(generation-1)] = best_nets #stores the best networks of the previous generation
        retrieve = str(generation-1) + " randomized"
        shelf[retrieve] = annealing.compute(random_nets, best_nets, 1)
        print("Successfully saved generation " + str(generation-1) + "'s best networks!'")
    finally:
        shelf.close()

    random_nets = []

''' ---OLD CODE USED TO RUN ONE ITERATION---
game(gameOver)
while gameOver == True:
    gameOver = False
    iteration += 1
    reset()
    game(gameOver)

pygame.quit()
quit()

'''
