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
replay_buffer_size = 1000
q_network = Neural()
q_network.init_weights(31, 23, 23, 4)
target_network = q_network

epislon = 1
sample_epsilon = 0.8
gamma = 0.9
run = True
training = True
time_step = 0

while(training):
    pacman.game(run, target_network) #Inside this function, do sampling of experiences to put in buffer. Also calculate TD error and put in a parallel deque.

    #Sample from replay buffer
    if len(rb.replay_buffer) == replay_buffer_size:
        if time_step % 50 == 0:
            e = random.uniform(0, 1)
            i = 0
            if e > sample_epsilon: #greedy sample
                i = random.randint(0, replay_buffer_size)
            #calculate target q(s,a)
            q_t = target_network.process(rb.replay_buffer[i][0])
            q_t_plus_1 = target_network.process(rb.replay_buffer[i][3])
            t_index = q_t_plus_1.index(q_t_plus_1)
            q_value_target = rb.replay_buffer[i][2] + gamma*max(q_t_plus_1)
            for x in range(4):
                if x == t_index:
                    q_t_plus_1[x] = q_value_target
                else:
                    q_t_plus_1[x] = q_t[x]
            q_network.backpropagate(q_t_plus_1, q_t)
            rb.pop_experience(i)
