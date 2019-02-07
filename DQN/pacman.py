'''
pacman.py

Main File
'''
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
import replay_buffer as rb
import numpy as np
import csv

pygame.init()
pygame.font.init()

#np.set_printoptions(threshold=np.nan)

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

def game(game_state, q_net, gamma, sample_epsilon, replay_buffer_size):
    global constants

    constants.score = 0
    constants.wall_collide_number = 0

    generateLevel.createLevel()
    pacmanMain = Pacman()
    blinky = Ghost()
    walls = generateLevel.walls

    #initialize some feature variables
    pacmanCurrentTile = featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)
    blinkyCurrentTile = featureExtraction.on_current_tile((blinky.rect.x, blinky.rect.y), blinky)
    #closest_food = featureExtraction.bfs([featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], [featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], 0, generateLevel.coins)

    crashCount = 1

    frightenModeCount = 0

    time = 0
    scatterModeCount = 0

    while not game_state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                constants.added_previous_t = False
                changeGameState()
                game_state = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    constants.added_previous_t = False
                    changeGameState()
                    game_state = True

        reward = 0
        score_before_script = constants.score
        wall_collide_number_before_script = constants.wall_collide_number

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

                '''#FITNESS: update fitness - for eating ghost'''
                reward += 10

            else: #lose the game
                constants.scores.append(constants.score)
                changeGameState()
                '''#FITNESS: update fitness - losing the game'''
                reward -= 10
                constants.added_previous_t = False
                game_state = True
                pacmanMain.kill()
                blinky.kill()
                break

        if featureExtraction.on_current_tile((blinky.rect.x, blinky.rect.y), blinky) != blinkyCurrentTile: #blinky change tile
            blinkyCurrentTile = featureExtraction.on_current_tile((blinky.rect.x, blinky.rect.y), blinky)

        #only do bfs when pacman changes tiles
        if featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain) != pacmanCurrentTile or constants.closest_food == None:
            pacmanCurrentTile = featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)
            constants.closest_food = featureExtraction.bfs([featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], [featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain)], 0, generateLevel.coins)
        #features
        food_pos = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 1, "food", blinkyCurrentTile)
        enemy_pos = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 1, "ghost", blinkyCurrentTile)
        wall_pos = featureExtraction.check_tile(generateLevel.wallPositions, pacmanCurrentTile, 1, "wall", blinkyCurrentTile)
        food_pos_2 = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 2, "food", blinkyCurrentTile)
        enemy_pos_2 = featureExtraction.check_tile(generateLevel.coins, pacmanCurrentTile, 2, "ghost", blinkyCurrentTile)
        distance_between = featureExtraction.distance_between((pacmanMain.rect.x, pacmanMain.rect.y), (blinky.rect.x, blinky.rect.y))

        inputVector = featureExtraction.extract(food_pos, enemy_pos, wall_pos, food_pos_2, enemy_pos_2, constants.closest_food, distance_between, constants.frightenMode)
        #print(inputVector)
        if constants.randoming == False:
            random_movement_epsilon = random.uniform(0, 1)
            if random_movement_epsilon < 0:
                constants.randoming = True
                action = random.randint(0, 3)
                constants.movement = action
                constants.max_movement_t = int(np.random.normal(32, 10))
                print("Randoming with movement time: " + str(constants.max_movement_t))

            else:
                if constants.target_network.apply_softmax:
                    probability = constants.target_network.process(inputVector)
                    action = np.random.choice(np.array([0,1,2,3]), p=probability) # Sample from softmax probability distribution.
                    constants.randoming = True
                    constants.movement = action
                    constants.max_movement_t = int(np.random.normal(15, 4))
                    print(probability)
                else:
                    action = constants.target_network.process(inputVector)
        else:
            action = constants.movement
            constants.random_movement_t += 1
            if(constants.random_movement_t % constants.max_movement_t == 0):
                constants.random_movement_t = 0
                constants.randoming = False

        #Adding state on time step "t+1" into the transition at time step t
        if constants.added_previous_t:
            rb.replay_buffer[rb.count-1].append(inputVector)
            #print(rb.replay_buffer[rb.count-1])
            constants.added_previous_t = False
        elif constants.added_previous_t_two:
            rb.replay_buffer_two[rb.count_two-1].append(inputVector)
            constants.added_previous_t_two = False

        pacmanMain.automate(action)
        #print(q_net.process(inputVector))
        #print(q_net.show(inputVector))

        score_after_script = constants.score
        wall_collide_number_after_script = constants.wall_collide_number

        if not game_state: #don't update score if game is over
            if score_after_script - score_before_script == 1: #reward for eating a food/coin
                reward += 1


        ''' ---- Saving memory into experience buffer ---- '''

        if(reward > 0): #remember states where reward is earned
            if rb.count<=replay_buffer_size:
                rb.replay_buffer.append([inputVector, action, reward])
                rb.count += 1
                constants.added_previous_t = True
                print("Added to replay_buffer. Transition count: "+ str(rb.count))

        p = random.uniform(0, 1)
        if p < 0.04 and reward <= 0:  #~4 percent probability of remembering the current state.
            if rb.count_two <= replay_buffer_size:
                rb.replay_buffer_two.append([inputVector, action, reward])
                rb.count_two += 1
                constants.added_previous_t_two = True
                print("Added to replay_buffer_two. Transition count: "+ str(rb.count_two))


        ''' ---- End of saving memory into experience buffer ---- '''

        blinky.shortest_distance = []
        blinky.tileToMove = []
        blinky.futureMovementNumber = []

        constants.t += 1 #increment a time-step
        #Sample from replay buffer every 20 timesteps
        if constants.t % 5 == 0:
            if random.randint(0, 100) < 60: #sample from first replay buffer
                if rb.count >= replay_buffer_size:
                    print("Sampling from replay buffer one.")
                #if time_step % 50 == 0:
                    e = random.uniform(0, 1)
                    i = 0
                    if e > sample_epsilon: #sample stochastically rather than greedily.
                        i = random.randint(0, replay_buffer_size-1)
                    #calculate target q(s,a)
                    if len(rb.replay_buffer[i]) == 4: #s(t+1) may not have been added to the transition yet, so check if it has then proceed.
                        q_t = constants.q_network.forward(rb.replay_buffer[i][0])
                        q_t_plus_1 = constants.target_network.forward(rb.replay_buffer[i][3])
                        t_index = list(q_t_plus_1).index(max(q_t_plus_1))
                        q_value_target = rb.replay_buffer[i][2] + gamma*max(q_t_plus_1)
                        print(q_value_target - max(q_t))
                        for x in range(4):
                            if x == t_index:
                                q_t_plus_1[x] = q_value_target
                            else:
                                q_t_plus_1[x] = q_t[x]
                        constants.q_network.backpropagate(q_t_plus_1, q_t)
                        rb.count -= 1
                        rb.pop_experience(i, 1)

            else: #sample from second replay buffer
                if rb.count_two >= replay_buffer_size:
                    print("Sampling from replay buffer two.")
                    e = random.uniform(0, 1)
                    i = 0
                    if e > sample_epsilon: #sample stochastically rather than greedily.
                        i = random.randint(0, replay_buffer_size-1)
                    #calculate target q(s,a)
                    if len(rb.replay_buffer[i]) == 4: #s(t+1) may not have been added to the transition yet, so check if it has then proceed.
                        q_t = constants.q_network.forward(rb.replay_buffer_two[i][0])
                        q_t_plus_1 = constants.target_network.forward(rb.replay_buffer_two[i][3])
                        t_index = list(q_t_plus_1).index(max(q_t_plus_1))
                        q_value_target = rb.replay_buffer_two[i][2] + gamma*max(q_t_plus_1)
                        print(q_value_target - max(q_t))
                        for x in range(4):
                            if x == t_index:
                                q_t_plus_1[x] = q_value_target
                            else:
                                q_t_plus_1[x] = q_t[x]
                        constants.q_network.backpropagate(q_t_plus_1, q_t)
                        rb.count_two -= 1
                        rb.pop_experience(i, 2)

        #Freeze interval of 100000 time steps, update the target_network with the weights of the q_network.
        if constants.t % 1200 == 0:
            constants.target_network = constants.q_network
            constants.t = 0
            print("Target network is now up-to-date with Q network.")

        #if constants.t % 10 == 0:
        #    rgbArray = pygame.surfarray.array_colorkey(constants.screen)
        #    print("hallo")

        pygame.display.update()
        clock.tick(60)
