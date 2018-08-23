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


def on_current_tile(position): #returns what tile (x,y) the agent is on
    for tile in all_tiles:
        if position[0] >= tile[0] - 45 and position[0] <= tile[0] + 45 and position[1] >= tile[1] - 30 and position[1] <= tile[1] + 30:
            return tile

def bfs(position, visited, count, coins): #closest food algorithm
    adjacent_tiles = []
    coin_list = coins
    visited_tiles = visited
    path_length = count

    lengths = []

    if position != None:
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
                lengths.append(path_length)
                #return path_length
            else:
                visited_tiles.append(i)
                return bfs(i, visited_tiles, path_length+1, coin_list)
        if len(lengths) > 0:
            return lengths
    else:
        return


def extract(position, action, food, walls, ghost_positions):
    x = position[0]
    y = position[1]

'''
path_length_list = []
def bfs(position, visited, count, coins): #closest food algorithm
    global path_length_list
    coin_list = coins
    #adjacent_tiles = []
    visited_tiles = visited
    path_length = count
    path_count = path_length

    if position != None:
        if (position[0], position[1]-60) not in visited_tiles and (position[0], position[1]-60) in all_tiles:
            if (position[0], position[1]-60) in coin_list:
                path_length_list.append(path_length)
                #return path_length
            else:
                visited_tiles.append((position[0], position[1]-60))
                return bfs((position[0], position[1]-60), visited_tiles, path_length + 1, coin_list)

        if (position[0]+90, position[1]) not in visited_tiles and (position[0]+90, position[1]) in all_tiles:
            if (position[0]+90, position[1]) in coin_list:
                path_length_list.append(path_length)
                #return path_length
            else:
                visited_tiles.append((position[0]+90, position[1]))
                return bfs((position[0]+90, position[1]), visited_tiles, path_length + 1, coin_list)

        if (position[0], position[1]+60) not in visited_tiles and (position[0], position[1]+60) in all_tiles:
            if (position[0], position[1]+60) in coin_list:
                path_length_list.append(path_length)
                #return path_length
            else:
                visited_tiles.append((position[0], position[1]+60))
                return bfs((position[0], position[1]+60), visited_tiles, path_length + 1, coin_list)

        if (position[0]-90, position[1]) not in visited_tiles and (position[0]-90, position[1]) in all_tiles:
            if (position[0]-90, position[1]) in coin_list:
                path_length_list.append(path_length)
                #return path_length
            else:
                visited_tiles.append((position[0]-90, position[1]))
                return bfs((position[0]-90, position[1]), visited_tiles, path_length + 1, coin_list)

        if path_length_list != []:
            copy = path_length_list
            path_length_list = []
            return copy

    else:
        return
'''
