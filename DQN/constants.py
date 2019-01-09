'''
constants.py
'''
#CONSTANTS
import pygame
from neuralnet import Neural

#dimensions
display_width = 1920
display_height = 1080
screen = pygame.display.set_mode((display_width, display_height))


#colours
black = (0, 0, 0)
white = (255, 255, 255)
score = 0

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

q_network = Neural()
q_network.init_weights(31, 23, 23, 4)
target_network = q_network

closest_food = None
