import os
import math
import random
import pygame

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Test 3 - Rough Face Shapes With Collision Detection")

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Useful Coordinates
center = (128, 128)


def face_outline(surface, color, center, size):

    a = 76 # horizontal radius
    b = 96 # vertical radius
    rect = pygame.Rect(center[0] - a, center[1] - b, 2*a, 2*b) # compute bounding rectangle for the ellipse
    pygame.draw.ellipse(surface, color, rect, 1) # draw the ellipse outline
    






screen.fill(WHITE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw face outline
    face_outline(screen, BLACK, (128, 128), (152, 192))
    
    pygame.display.flip()
    
pygame.quit()