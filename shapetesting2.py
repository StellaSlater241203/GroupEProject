import os
import math
import random
import pygame
import time

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shape Testing 2 - Collision Detection with screen wide/high surfaces")


# Colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

screen.fill(white)

def collision_detection(shape1, shape2):
    surface1, pos1 = shape1
    surface2, pos2 = shape2
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    offset_x = pos2[0] - pos1[0]
    offset_y = pos2[1] - pos1[1]
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    return False


def draw_randomly_placed_rectangle(surface, colour, x, y):
    rectRect = pygame.Rect(0, 0, 256, 256)
    surfRect = pygame.Surface(rectRect.size, pygame.SRCALPHA)
    pygame.draw.rect(surfRect, colour, (x, y, 20, 30), 1)
    rotatedsurf = pygame.transform.rotate(surfRect, 60)
    surface.blit(rotatedsurf, rotatedsurf.get_rect(center = rectRect.center))
    rectShape = [surfRect, rectRect]
    return rectShape

def face_outline(surface):
    faceRect = pygame.Rect(0, 0, 256, 256) # compute bounding rectangle for the ellipse
    faceSurface = pygame.Surface(faceRect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(faceSurface, black, (52, 32, 152, 192), 1) # draw the ellipse outline
    surface.blit(faceSurface, faceSurface.get_rect(center = faceRect.center))
    faceShape = [faceSurface, faceRect]
    return faceShape


j = 0
for i in range(1):
    faceShape = face_outline(screen)
    x, y = 30, 30 
    rectShape = draw_randomly_placed_rectangle(screen, black, x, y)
    pygame.display.flip()
    time.sleep(0.05)




running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()


pygame.quit()