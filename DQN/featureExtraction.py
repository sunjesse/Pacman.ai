'''
#TO DO:
1. Get this bfs thing to work smh
'''
import dynamicPositions
import generateLevel
import constants
from collections import deque
from player import Pacman
#ghost_positions is a list of tuples (x,y) of each ghost's position
all_tiles = generateLevel.allTiles
walls = generateLevel.walls
food = generateLevel.coins

#shortest_path = []

def on_current_tile(position, player): #returns what tile (x,y) the agent is on
    for tile in all_tiles:
        if position[0] >= tile[0] - 45 and position[0] <= tile[0] + 45 and position[1] >= tile[1] - 30 and position[1] <= tile[1] + 30:
            return tile

    for wall in walls:
        if player.rect.colliderect(wall.rect):
            if player.move_up == True:
                return (wall.rect.centerx-15, wall.rect.centery+60)

            if player.move_down == True:
                return (wall.rect.centerx-15, wall.rect.centery-60)

            if player.move_right == True:
                return (wall.rect.centerx + 75, wall.rect.centery)

            if player.move_left == True:
                return (wall.rect.centerx - 105, wall.rect.centery)

    return (player.rect.x, player.rect.y)

def bfs(adjacent, visited, count, coins): #closest food algorithm
    adjacent_tiles = []
    coin_list = coins
    visited_tiles = visited
    path_length = count

    for i in adjacent:
        if i in all_tiles:
            if i in coins:
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

        else:
            return

    return bfs(adjacent_tiles, visited_tiles, path_length+1, coin_list)

def check_tile(item, position, steps_away, type, ghost_position):
    '''
    Item (list) is a member of [food].
    Position is the tile the pacman agent is currently on.
    Steps_away is num of tiles away from pacman agent that wishes to be checked.
    '''

    binary_return = [] # 1 if item present in tile, 0 if not. First index is up, then clockwise.

    x = 90
    y = 60

    if steps_away == 2:
        x = 180
        y = 120

    item_list = item

    if position != None:
        if type == "food" or type == "wall":
            if (position[0], position[1]-y) in item_list:
                binary_return.append(1)
            else:
                binary_return.append(0)

            if (position[0]+x, position[1]) in item_list:
                binary_return.append(1)
            else:
                binary_return.append(0)

            if (position[0], position[1]+y) in item_list:
                binary_return.append(1)
            else:
                binary_return.append(0)

            if (position[0]-x, position[1]) in item_list:
                binary_return.append(1)
            else:
                binary_return.append(0)

        elif type == "ghost":
            if (position[0], position[1]-y) == ghost_position:
                binary_return.append(1)
            else:
                binary_return.append(0)

            if (position[0]+x, position[1]) == ghost_position:
                binary_return.append(1)
            else:
                binary_return.append(0)

            if (position[0], position[1]+y) == ghost_position:
                binary_return.append(1)
            else:
                binary_return.append(0)

            if (position[0]-x, position[1]) == ghost_position:
                binary_return.append(1)
            else:
                binary_return.append(0)

    return binary_return

def distance_between(position_one, position_two):
    return (position_one[0] - position_two[0], position_one[1] - position_two[1])

def extract(food_pos, enemy_pos, wall_pos, food_pos_2, enemy_pos_2, food_closests, distance_between, ghost_scared):
    '''
    31 Features
    input_vector = food_pos[4], food_pos_2[4], enemy_pos[4], enemy_pos_2[4], enemy_scared_pos[4], enemy_scared_pos_2[4], wall_pos[4], food_closts int, delta x float, delta y float
    '''
    input_vector = []

    input_vector.extend(food_pos)
    input_vector.extend(food_pos_2)

    if ghost_scared == False:
        input_vector.extend(enemy_pos)
        input_vector.extend(enemy_pos_2)
        input_vector.extend([0, 0, 0, 0])
        input_vector.extend([0, 0, 0, 0])
    elif ghost_scared:
        input_vector.extend([0, 0, 0, 0])
        input_vector.extend([0, 0, 0, 0])
        input_vector.extend(enemy_pos)
        input_vector.extend(enemy_pos_2)

    input_vector.extend(wall_pos)
    input_vector.append(food_closests/10) #normalized this feature by dividng by 10.
    input_vector.append(distance_between[0]/constants.display_width)
    input_vector.append(distance_between[1]/constants.display_height)

    return input_vector
