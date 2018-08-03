'''
generateLevel.property

Generates the walls, food, and enemies of a level.

'''

import pygame
import levels
from wall import Wall

walls = []

level = levels.level1
x = 60
y = 60
for row in level:
    for col in row:
        if col == "W":
            walls.append(Wall((x, y)))

        x += 90
    y += 60
    x = 60
