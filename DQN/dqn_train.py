import pacman
import pygame
import random
import numpy as np
import constants
import shelve
import replay_buffer as rb
import csv

'''
TO DO:

'''

''' ---- Training ---- '''
replay_buffer_size = 500
epislon = 1
sample_epsilon = 0.8
gamma = 0.9
gameOver = False
training = True
outer_time_step = 0

while(training):
    try:
        pacman.game(gameOver, constants.target_network, gamma, sample_epsilon, replay_buffer_size) #calculate TD error and put in a parallel deque.
        gameOver = False
        pacman.reset()
    except KeyboardInterrupt:
        print("Saving training data...")

        shelf = shelve.open(constants.filename)
        try:
            shelf["q_network"] = constants.q_network
            shelf["target_network"] = constants.target_network
            shelf["replay_buffer"] = rb.replay_buffer
            shelf["replay_buffer_two"] = rb.replay_buffer_two
            shelf["P"] = rb.P
            shelf["P_two"] = rb.P_two
            print("Sucessfully saved objects and lists in " + constants.filename + ".db.")
            #if shelf["first_time"]:
            #    shelf["first_time"] = False
        finally:
            shelf.close()

        try:
            with open('training_data.csv', 'wb', newline = '') as f:
                write = f.writer(f)
                write.writerow(constants.scores)
                print("Successfully saved training data in training_data.csv")
        except:
            print("An error occured while saving the training data.")
        break

pygame.quit()
quit()
