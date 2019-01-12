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
1. Maybe implement DeepMind's implementation of PER.
'''

''' ---- Training ---- '''
replay_buffer_size = 99
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
        shelf = shelve.open("objects", writeback = True)
        print("Saving training data...")

        try:
            shelf["q_network"] = constants.q_network
            shelf["target_network"] = constants.target_network
            shelf["replay_buffer"] = rb.replay_buffer
            shelf["replay_buffer_two"] = rb.replay_buffer_two
            shelf["count"] = rb.count
            shelf["count_two"] = rb.count_two
            print("Sucessfully saved objects and lists in objects.db.")
            if shelf["first_time"]:
                shelf["first_time"] = False
                print(shelf["first_time"])
        finally:
            shelf.close()

        try:
            with open('training_data.csv', 'w') as f:
                write = csv.writer(f)
                write.writerow(constants.scores)
                print("Successfully saved training data in training_data.csv")
        except:
            print("An error occured while saving the training data.")
        training = False

pygame.quit()
quit()
