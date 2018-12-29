import pacman
import random
import numpy as np
import replay_buffer

''' ---- Training ---- '''
replay_buffer_size = 10000
q_network = Neural()
q_network.init_weights(31, 23, 23, 4)
target_network = q_network

epislon = 1
run = True
training = True
time_step = 0

while(training):
    pacman.game(run, target_network)
