import os
import math
import random
import pygame
from pygame import gfxdraw
import time

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

white = (255,255,255)
black = (0,0,0)

screen.fill(white)


coordx, coordy = 200, 200

coords = [[coordx, coordy, 36, 18]]

rect = pygame.Rect(coordx-38, coordy-20, 76, 40)
surf = pygame.Surface(rect.size, pygame.SRCALPHA)
pygame.gfxdraw.aaellipse(surf, 38, 20, coords[0][2], coords[0][3], black)
rotatedsurf = pygame.transform.rotate(surf, 60)
screen.blit(rotatedsurf, rotatedsurf.get_rect(center = rect.center))

coordx += 64
if coordx > 224:
    coordx = 32
    coordy += 64
pygame.display.update()

exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

pygame.quit()