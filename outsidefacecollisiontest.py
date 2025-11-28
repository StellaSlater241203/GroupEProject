import pygame
import math
import random
import time

pygame.init()

grey = (10,10,15)
white = (255,255,255)

canvas = pygame.display.set_mode((256,256))
canvas.fill(white)

#draw face and add to surface for collision
faceTopLeft = [52,32]
faceRect = pygame.Rect(52, 32, 152, 192)
faceSurface = pygame.Surface(faceRect.size, pygame.SRCALPHA)
pygame.draw.ellipse(faceSurface, grey, (0, 0, *faceRect.size), 1)
canvas.blit(faceSurface, faceSurface.get_rect(center = faceRect.center))

def detect_collision_mask(surface1, pos1, surface2, pos2): #from stack overflow
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    offset_x = pos2[0] - pos1[0]
    offset_y = pos2[1] - pos1[1]
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    return False

for i in range(0,500):
    eyex = random.randint(52,204)
    eyey = random.randint(32,224)
    while ((((eyex)-128)**2)/(76**2)) + ((((eyey)-128)**2)/(96**2)) >= 1:
        eyex = random.randint(52,204)
        eyey = random.randint(32,224)
    eyeRect = pygame.Rect(eyex-12, eyey-6, 24, 12)
    eyeSurface = pygame.Surface(eyeRect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(eyeSurface, grey, (0, 0, *eyeRect.size), 1)
    canvas.blit(eyeSurface, eyeSurface.get_rect(center = eyeRect.center))
    print(detect_collision_mask(faceSurface, faceTopLeft, eyeSurface, [eyex-12, eyey-6]))
    pygame.display.flip()
    time.sleep(0.05)




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()