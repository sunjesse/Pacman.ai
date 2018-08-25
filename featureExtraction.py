'''
#TO DO:
1. Get this bfs thing to work smh
'''
import dynamicPositions
import generateLevel
import constants
from collections import deque

#ghost_positions is a list of tuples (x,y) of each ghost's position
all_tiles = generateLevel.allTiles
food = generateLevel.coins

#shortest_path = []

def on_current_tile(position): #returns what tile (x,y) the agent is on
    for tile in all_tiles:
        if position[0] >= tile[0] - 45 and position[0] <= tile[0] + 45 and position[1] >= tile[1] - 30 and position[1] <= tile[1] + 30:
            return tile

def bfs(adjacent, visited, count, coins): #closest food algorithm
    #global shortest_path
    adjacent_tiles = []
    coin_list = coins
    visited_tiles = visited
    path_length = count

    for i in adjacent:
        if i != None:
            if i in coins:
                #shortest_path.append(i)
                return path_length
            else:
                if (i[0], i[1]-60) not in visited_tiles and (i[0], i[1]-60) in all_tiles:
                    adjacent_tiles.append((i[0], i[1]-60))
                if (i[0]+90, i[1]) not in visited_tiles and (i[0]+90, i[1]) in all_tiles:
                    adjacent_tiles.append((i[0]+90, i[1]))
                if (i[0], i[1]+60) not in visited_tiles and (i[0], i[1]+60) in all_tiles:
                    adjacent_tiles.append((i[0], i[1]+60))
                if (i[0]-90, i[1]) not in visited_tiles and (i[0]-90, i[1]) in all_tiles:
                    adjacent_tiles.append((i[0]-90, i[1]))
                visited_tiles.append(i)

                #if shortest_path != []:
                    #shortest_path = []
        else:
            return

    return bfs(adjacent_tiles, visited_tiles, path_length+1, coin_list)

def check_tile(item, position, steps_away):
    '''
    Item (list) is a member of [food, wall].
    Position is the tile the pacman agent is currently on.
    Steps_away is num of tiles away from pacman agent that wishes to be checked.
    '''

    binary_return = [] # 1 if item present in tile, 0 if not. First index is up, then clockwise.

    x = 90
    y = 60

    if steps_away = 2:
        x = 180
        y = 120

    if (i[0], i[1]-y) in item:
        binary_return.append(1)
    else:
        binary_return.append(0)

    if (i[0]+x, i[1]) in item:
        binary_return.append(1)
    else:
        binary_return.append(0)

    if (i[0], i[1]+y) in item:
        binary_return.append(1)
    else:
        binary_return.append(0)

    if (i[0]-x, i[1]) in item:
        binary_return.append(1)
    else:
        binary_return.append(0)

    return binary_return

def extract(position, action, food, walls, ghost_positions):
    x = position[0]
    y = position[1]
