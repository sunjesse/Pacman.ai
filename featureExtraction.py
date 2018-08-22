import dynamicPositions
import generateLevel
import constants
from collections import deque


#ghost_positions is a list of tuples (x,y) of each ghost's position
all_tiles = generateLevel.allTiles
food = generateLevel.coins

def on_current_tile(position): #returns what tile (x,y) the agent is on
    for tile in all_tiles:
        if position[0] >= tile[0] - 45 and position[0] <= tile[0] + 45 and position[1] >= tile[1] - 30 and position[1] <= tile[1] + 30:
            return tile

def bfs(position, visited, count): #closest food algorithm
    adjacent_tiles = []
    visited_tiles = visited
    path_length = count

    if (position[0], position[1]-60) not in visited_tiles and (position[0], position[1]-60) in all_tiles:
        adjacent_tiles.append((position[0], position[1]-60))
    if (position[0]+90, position[1]) not in visited_tiles and (position[0]+90, position[1]) in all_tiles:
        adjacent_tiles.append((position[0]+90, position[1]))
    if (position[0], position[1]+60) not in visited_tiles and (position[0], position[1]+60) in all_tiles:
        adjacent_tiles.append((position[0], position[1]+60))
    if (position[0]-90, position[1]) not in visited_tiles and (position[0]-90, position[1]) in all_tiles:
        adjacent_tiles.append((position[0]-90, position[1]))

    for i in adjacent_tiles:
        if i in food:
            return path_length
        else:
            visited_tiles.append(i)
            bfs(i, visited_tiles, path_length+1)


def extract(position, action, food, walls, ghost_positions):
    x = position[0]
    y = position[1]
