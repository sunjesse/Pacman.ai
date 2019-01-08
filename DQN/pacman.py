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
import shelve
import replay_buffer as rb

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

def game(game_state, q_net, gamma, sample_epsilon, replay_buffer_size):
    reward = 0

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

        if featureExtraction.on_current_tile(dynamicPositions.pacman, pacmanMain) != pacmanCurrentTile or constants.closest_food == None: #only do bfs when pacman changes tiles
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

        if constants.randoming == False:
            random_movement_epsilon = random.uniform(0, 1)

            if random_movement_epsilon < 0.1:
                action = random.randint(0, 3)
                constants.movement = action
            else:
                action = q_net.process(inputVector)
        else:
            action = constants.movement
            constants.random_movement_t += 1
            if(constants.random_movement_t % 30):
                constants.randoming = False

        if constants.added_previous_t:
            rb.replay_buffer[rb.count-1].append(action)
            constants.added_previous_t = False

        pacmanMain.automate(action)
        #print(q_net.process(inputVector))
        #print(q_net.show(inputVector))
        ''' ---- #FITNESS: Update fitness of network ---- '''
        score_after_script = constants.score
        wall_collide_number_after_script = constants.wall_collide_number

        if not game_state: #don't update score if game is over
            if score_after_script - score_before_script == 1: #reward for eating a food/coin
                reward += 1


        ''' ---- Saving memory into experience buffer ---- '''

        p = random.uniform(0, 1)
        if p < 0.02:  #~2 percent probability of remembering the current state.
            rb.replay_buffer.append([inputVector, action, reward])
            rb.count += 1
            constants.added_previous_t = True

        ''' ---- End of saving memory into experience buffer ---- '''

        blinky.shortest_distance = []
        blinky.tileToMove = []
        blinky.futureMovementNumber = []

        constants.t += 1 #increment a time-step
        #Sample from replay buffer every 100 timesteps
        if constants.t % 100 == 0:
            if len(rb.replay_buffer) == replay_buffer_size:
                if time_step % 50 == 0:
                    e = random.uniform(0, 1)
                    i = 0
                    if e > sample_epsilon: #sample stochastically rather than greedily.
                        i = random.randint(0, replay_buffer_size)
                    #calculate target q(s,a)
                    q_t = constants.constants.target_network.forward(rb.replay_buffer[i][0])
                    q_t_plus_1 = constants.target_network.forward(rb.replay_buffer[i][3])
                    t_index = q_t_plus_1.index(q_t_plus_1)
                    q_value_target = rb.replay_buffer[i][2] + gamma*max(q_t_plus_1)
                    for x in range(4):
                        if x == t_index:
                            q_t_plus_1[x] = q_value_target
                        else:
                            q_t_plus_1[x] = q_t[x]
                    constants.q_network.backpropagate(q_t_plus_1, q_t)
                    rb.pop_experience(i)
            constants.t = 0

        pygame.display.update()
        clock.tick(60)

game(gameOver, constants.target_network, 0.9, 0.8, 1000)
while gameOver == True:
    gameOver = False
    reset()
    print("restart")
    game(gameOver, constants.target_network, 0.9, 0.8, 1000)

pygame.quit()
quit()
