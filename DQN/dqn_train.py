import pacman
import random
import numpy as np
import replay_buffer as rb

'''
TO DO:
1. Add sampling from pacman.game() in pacman.py into buffer
2. Add backprop after every forward pass into pacman.game() in pacman.py
3. Clearly define a reward system.
4. Sampling from replay_buffer should theoretically occur in pacman.game(), might have to transfer it over along ith time_step variable. Will increment it in pacman.game()
5. Try and except inside pacman.game() -> if game is closed via cmd+c or whatever, then save current progress.
6. Create a file that stores data during training: q-values, loss, etc..
7. Seperate file that saves the current networks, current replay buffer, etc.
8. Matplotlib // Maybe run a process displaying the data concurrently during training? Maybe idk.
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
            if e > sample_epsilon: #sample stochastically rather than greedily.
                i = random.randint(0, replay_buffer_size)
            #calculate target q(s,a)
            q_t = target_network.forward(rb.replay_buffer[i][0])
            q_t_plus_1 = target_network.forward(rb.replay_buffer[i][3])
            t_index = q_t_plus_1.index(q_t_plus_1)
            q_value_target = rb.replay_buffer[i][2] + gamma*max(q_t_plus_1)
            for x in range(4):
                if x == t_index:
                    q_t_plus_1[x] = q_value_target
                else:
                    q_t_plus_1[x] = q_t[x]
            q_network.backpropagate(q_t_plus_1, q_t)
            rb.pop_experience(i)
