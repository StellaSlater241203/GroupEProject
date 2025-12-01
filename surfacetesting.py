import pygame
import random
import math
from math import pi

pygame.init()

white = (255,255,255)
black = (0,0,0)

canvas = pygame.display.set_mode((256, 256))

def shape_gen_info(centreCoords, size, shape):
    coordList = [[0,0,24,12],[0,0,18,18],[0,0,18,18],[0,0,24,12],[0,0,24,0],[0,0,32,0],[0,0,18,18],[0,0,12,24],[0,0,24,12],[0,0,18,18,0,9,18,9],[0,0,12,24,0,12,12,12],[0,0,24,12,0,6,24,6],[0,16,18,16,9,0],[0,24,12,24,6,0],[0,10,28,10,14,0],[2,0,10,0,12,24,0,24],[4,0,20,0,24,12,0,12],[0,0,12,12,10,0,12,12,3,11,11,18,19,11,11,18],[9,1,11,7,18,7,12,11,14,17,9,14,4,17,6,7,0,7,7,7],[8,8,4,4,4,6,8,8,4,4,12,12,0,2,16,16,0,0,20,20,-4,-2,24,24]]
    rectList = [[-12,-6,24,12],[-9,-9,18,18],[-9,-9,18,18],[-12,-6,24,12],[-12,0,24,1],[-16,0,32,1],[-9,-4.5,18,18],[-6,-6,12,12],[-12,-3,24,6],[-9,-4.5,18,10],[-6,-6,12,13],[-12,-3,24,7],[-9,-8,19,17],[-6,-12,13,25],[-14,-5,29,11],[-6,-12,13,25],[-12,-6,25,13],[-11,-9,22,19],[-9,-9,19,19],[-10,-10,20,18]]
    x = centreCoords[0]
    y = centreCoords[1]
    coords = []

    for i in coordList[shape]:
        coord = round(i*size)
        coords.append(coord)

    rectCoords = [x + math.ceil(rectList[shape][0]*size), y + math.ceil(rectList[shape][1]*size), math.ceil(rectList[shape][2]*size), math.ceil(rectList[shape][3]*size)]
    return coords, rectCoords

def draw_shape(shapeInfo, rectInfo, shapeID):

    shapeSurfRect = pygame.Rect(rectInfo)
    shapeSurf = pygame.Surface(shapeSurfRect.size, pygame.SRCALPHA)

    if shapeID == 0 or shapeID == 1: # ovals and circles
        pygame.draw.ellipse(shapeSurf, black, shapeInfo, 1)
    elif shapeID == 2 or shapeID == 3: # squares and rectangles
        pygame.draw.rect(shapeSurf, black, shapeInfo, 1)
    elif shapeID == 4 or shapeID == 5: # lines and longer lines
        pygame.draw.line(shapeSurf, black, shapeInfo[0:2], shapeInfo[2:4], 1)
    elif shapeID == 6 or shapeID == 7 or shapeID == 8: # curved, deep curved and wide curved lines
        pygame.draw.arc(shapeSurf, black, shapeInfo, 0, pi, 1)
    elif shapeID == 9 or shapeID == 10 or shapeID == 11: # semi circle, vertical and horizontal semi oval
        pygame.draw.arc(shapeSurf, black, shapeInfo[0:4], 0, pi, 1)
        pygame.draw.line(shapeSurf, black, shapeInfo[4:6], shapeInfo[6:8], 1)
    elif shapeID == 12 or shapeID == 13 or shapeID == 14:# triangles
        pygame.draw.polygon(shapeSurf, black, (shapeInfo[0:2], shapeInfo[2:4], shapeInfo[4:6]), 1)
    elif shapeID == 15 or shapeID == 16: # trapeziums
        pygame.draw.polygon(shapeSurf, black, (shapeInfo[0:2], shapeInfo[2:4], shapeInfo[4:6], shapeInfo[6:8]), 1)
    elif shapeID == 18:# star
        pygame.draw.polygon(shapeSurf, black, (shapeInfo[0:2], shapeInfo[2:4], shapeInfo[4:6], shapeInfo[6:8], shapeInfo[8:10], shapeInfo[10:12], shapeInfo[12:14], shapeInfo[14:16], shapeInfo[16:18], shapeInfo[18:20]), 1)
    elif shapeID == 17: # heart
        pygame.draw.arc(shapeSurf, black, shapeInfo[0:4], (pi/4), (5*pi/4), 1)
        pygame.draw.arc(shapeSurf, black, shapeInfo[4:8], (7*pi/4), (3*pi/4), 1)
        pygame.draw.line(shapeSurf, black, shapeInfo[8:10], shapeInfo[10:12], 1)
        pygame.draw.line(shapeSurf, black, shapeInfo[12:14], shapeInfo[14:16], 1)
    elif shapeID == 19: # spiral
        pygame.draw.arc(shapeSurf, black, shapeInfo[0:4], 0, pi, 1)
        pygame.draw.arc(shapeSurf, black, shapeInfo[4:8], pi, 2*pi, 1)
        pygame.draw.arc(shapeSurf, black, shapeInfo[8:12], 0, pi, 1)
        pygame.draw.arc(shapeSurf, black, shapeInfo[12:16], pi, 2*pi, 1)
        pygame.draw.arc(shapeSurf, black, shapeInfo[16:20], 0, pi, 1)

    canvas.blit(shapeSurf, shapeSurf.get_rect(center=shapeSurfRect.center))

x = random.randint(52,204)
y = random.randint(32,224)
shapeInfo, rectInfo = shape_gen_info([x,y],0.8,0,)
canvas.fill(white)
draw_shape(shapeInfo, rectInfo, 0)
pygame.display.flip()

exit = False
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
pygame.quit()
