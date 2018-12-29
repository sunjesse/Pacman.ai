import pacman
import random
import numpy as np



''' ---- Training ---- '''
replay_buffer_size = 10000
q_network = Neural()
q_network.init_weights(31, 23, 23, 4)
target_network = q_network

epislon = 1
run = True
training = True

while(training):
    pacman.game(run, target_network)
