'''
constants.py
'''
#CONSTANTS
import pygame
from neuralnet import Neural
import shelve

#dimensions
display_width = 1920
display_height = 1080
screen = pygame.display.set_mode((display_width, display_height))

#colours
black = (0, 0, 0)
white = (255, 255, 255)

#scores
score = 0
scores = []

frightenMode = False
chaseMode = True
scatterMode = False

wall_collide_number = 0

t = 0
added_previous_t = False
added_previous_t_two = False
randoming = False
movement = -1
random_movement_t = 0
closest_food = -1
max_movement_t = 0

shelf = shelve.open("objects")

if shelf["first_time"]:
    q_network = Neural()
    q_network.init_weights(31, 23, 23, 4)
    target_network = q_network
    print("Successfully initiated networks.")
    shelf.close()

else:
    try:
        q_network = shelf["q_network"]
        target_network = shelf["target_network"]
        print("Successfully restored networks.")
    finally:
        shelf.close()
