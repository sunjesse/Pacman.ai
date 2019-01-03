import pacman
import random
import numpy as np
import replay_buffer as rb

'''
TO DO:
1. Create a file that stores data during training: q-values, loss, etc..
2. Seperate file that saves the current networks, current replay buffer, etc.
'''

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
    pacman.game(run, target_network) #Inside this function, do sampling of experiences to put in buffer. Also calculate TD error and put in a parallel deque.

    #Sample from replay buffer
    if time_step % 50 == 0:
