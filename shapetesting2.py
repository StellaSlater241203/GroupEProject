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


def face_outline(surface):
    faceRect = pygame.Rect(0, 0, 256, 256) # compute bounding rectangle for the ellipse
    faceSurface = pygame.Surface(faceRect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(faceSurface, black, (52, 32, 192, 152), 1) # draw the ellipse outline
    surface.blit(faceSurface, faceSurface.get_rect(center = faceRect.center))

pygame.display.flip()