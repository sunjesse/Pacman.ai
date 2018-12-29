'''
generateLevel.property

Generates the walls, food, and enemies of a level.

'''

import pygame
import levels
from wall import Wall
import constants
#import player

walls = []
wallPositions = [] #in terms of tile positions
coins = []
coinsObjects = []
intersection = []
allTiles = []
frightenTiles = [] #contains center coordinates of all tiles on the level.

def createLevel():
    level = levels.level1
    x = 60
    y = 60

    for row in level:
        for col in row:
            if col == "W":
                wall = Wall((x,y))
                walls.append(wall)
                wallPositions.append((wall.rect.centerx-15, wall.rect.centery))
            elif col == " " or col == "I" or col == "F":
                coins.append((x+30, y+30))
                coinsObjects.append(pygame.Rect(x+30, y+30, \
                16, 16))
                allTiles.append((x+30, y+30))
                if col =="I":
                    intersection.append(pygame.Rect(x+30, y+30, \
                    14, 14))
                elif col == "F":
                    frightenTiles.append((x+30, y+30))
            x += 90
        y += 60
        x = 60

#    player.coins = coinsObjects
#    player.coinPos = coins

def drawWalls():
    for wall in walls:
        pygame.draw.rect(constants.screen, (12, 0, 255), wall.rect)

def drawCoins():
    for pos in coins:
        if pos in frightenTiles:
            pygame.draw.circle(constants.screen, (255, 255, 255), pos, int((14/constants.display_height)*constants.display_height))
        else:
            pygame.draw.circle(constants.screen, (255, 255, 255), pos, int((8/constants.display_height)*constants.display_height))
