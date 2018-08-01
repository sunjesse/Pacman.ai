'''
pacman.py

Main File
'''

import pygame
import sys
from player import Pacman
import constants
from wall import Wall
import levels

pygame.init()

black = constants.white

pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()

crashed = False


pacmanMain = Pacman()
pacmanGroup = pygame.sprite.Group(pacmanMain)

walls = []

level = levels.level
x = 60
y = 60
for row in level:
    for col in row:
        if col == "W":
            walls.append(Wall((x, y)))

        x += 90
    y += 60
    x = 60

#toggle = pygame.Rect(100, 100, 50, 50)
#toggleOn = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    mouse_pos = event.pos

        #    if toggle.collidepoint(mouse_pos):
        #        toggleOn = True

    #if toggleOn == False:
    keys = pygame.key.get_pressed() #TEMPORARY || WILL MAKE IT TOGGLE WHEN QLEARNING GETS IMPLEMENTED
    if keys[pygame.K_LEFT]:
        pacmanMain.x -= 0.006*constants.display_height
        pacmanMain.move_left = True
        pacmanMain.move_right = False

    elif keys[pygame.K_RIGHT]:
        pacmanMain.x += 0.006*constants.display_height
        pacmanMain.move_left = False
        pacmanMain.move_right = True

    elif keys[pygame.K_UP]:
        pacmanMain.y -= 0.006*constants.display_height

    elif keys[pygame.K_DOWN]:
        pacmanMain.y += 0.006*constants.display_height

    #print(str(pacmanMain.x) + " " + str(pacmanMain.y))
    #print(pacmanMain.move_left)

    #screen.blit(toggle, (100, 100))


    constants.screen.fill(black)
    for wall in walls:
        pygame.draw.rect(constants.screen, (0, 0, 0), wall.rect)
    pacmanGroup.update()
    pacmanGroup.draw(constants.screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
