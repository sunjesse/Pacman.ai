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
import generateLevel

pygame.init()

black = constants.black

pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()

crashed = False


pacmanMain = Pacman()
#pacmanGroup = pygame.sprite.Group(pacmanMain)

walls = generateLevel.walls

#toggle = pygame.Rect(100, 100, 50, 50)
#toggleOn = False
i = 0
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
        pacmanMain.move_up = False
        pacmanMain.move_down = False

        pacmanMain.face_left = True
        pacmanMain.face_right = False
        pacmanMain.rect = pacmanMain.rect.move(-0.006*constants.display_height, 0)

    elif keys[pygame.K_RIGHT]:
        pacmanMain.x += 0.006*constants.display_height
        pacmanMain.move_left = False
        pacmanMain.move_right = True
        pacmanMain.move_up = False
        pacmanMain.move_down = False

        pacmanMain.face_right = True
        pacmanMain.face_left = False
        pacmanMain.rect = pacmanMain.rect.move(0.006*constants.display_height, 0)

    elif keys[pygame.K_UP]:
        pacmanMain.y -= 0.006*constants.display_height
        pacmanMain.rect = pacmanMain.rect.move(0, -0.006*constants.display_height)
        pacmanMain.move_up = True
        pacmanMain.move_down = False
        pacmanMain.move_right = False
        pacmanMain.move_left = False

    elif keys[pygame.K_DOWN]:
        pacmanMain.y += 0.006*constants.display_height
        pacmanMain.rect = pacmanMain.rect.move(0, 0.006*constants.display_height)
        pacmanMain.move_up = False
        pacmanMain.move_down = True
        pacmanMain.move_right = False
        pacmanMain.move_left = False
    #print(str(pacmanMain.x) + " " + str(pacmanMain.y))

    constants.screen.fill(black)

    #print(pacmanMain.rect)

    for wall in walls:
        pygame.draw.rect(constants.screen, (12, 0, 255), wall.rect)
        if pacmanMain.rect.colliderect(wall.rect):
            print(str(i) + " " + str(True))
            i += 1

            if pacmanMain.move_up == True:
                pacmanMain.rect.top = wall.rect.bottom
                pacmanMain.y = wall.rect.bottom

            if pacmanMain.move_down == True:
                pacmanMain.rect.bottom = wall.rect.top
                pacmanMain.y = wall.rect.top - constants.display_height*0.0525

            if pacmanMain.move_right == True:
                pacmanMain.rect.right = wall.rect.left
                pacmanMain.x = wall.rect.left - constants.display_width * 0.03

            if pacmanMain.move_left == True:
                pacmanMain.rect.left = wall.rect.right
                pacmanMain.x = wall.rect.right
    #pacmanGroup.update()
    pacmanMain.update()
    #pacmanMain.draw(constants.screen)
    #pacmanGroup.draw(constants.screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
