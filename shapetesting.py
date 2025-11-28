import pygame
import math
from math import pi
import random
import time
import os

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
glass = (180,210,255)
blue = (0, 0, 255)
green = (0, 255, 0)
purple = (255, 0, 255)
cyan = (0, 255, 255)
orange = (255, 127, 0)
yellow = (255, 255, 0)

colours = [black, red, blue, green, purple, cyan, orange, yellow]


# CREATING CANVAS
canvas = pygame.display.set_mode((256, 320))
canvas.fill(white)


# TITLE OF CANVAS
pygame.display.set_caption("Show Image")


coordList = [[-12,-6,24,12],[-9,-9,18,18],[-9,-9,18,18],[-12,-6,24,12],[-12,0,12,0],[-16,0,16,0],[-9,-4.5,18,18],[-6,-6,12,24],[-12,-3,24,12],[-9,-4.5,18,18,-9,4.5,9,4.5],[-6,-6,12,24,-6,6,6,6],[-12,-3,24,12,-12,3,12,3],[-9,6,9,6,0,-10],[-6,8,6,8,0,-16],[-14,5,14,5,0,-5],[-4,-12,4,-12,6,12,-6,12],[-8,-6,8,-6,12,6,-12,6],[-11,-8,13,13,0,-8,13,13,-9,2,0,10,9,2,0,10],[0,-9,2,-3,9,-3,3,1,5,7,0,4,-5,7,-3,1,-9,-3,-2,-3],[-2,-2,4,4,-6,-4,8,8,-6,-6,12,12,-10,-8,16,16,-10,-10,20,20,-14,-12,24,24]]
'''for i in range(len(coordList)):
    coordx = random.randint(20,236)
    coordy = random.randint(20,236)
    coords = [coordx + coordList[i][0], coordy + coordList[i][1], coordList[i][2], coordList[i][3]]
    if i == 0:
        pygame.draw.ellipse(canvas, black, pygame.Rect(coords), 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
    else:
        pygame.draw.rect(canvas, black, pygame.Rect(coords), 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
pygame.display.update()'''

coordx,coordy=32,32

for i in range(len(coordList)):
    if i == 4 or i == 5:
        coords = [[coordx + coordList[i][0], coordy + coordList[i][1]], [coordx + coordList[i][2], coordy + coordList[i][3]]]
    elif i == 9 or i == 10 or i == 11:
        coords = [[coordx + coordList[i][0], coordy + coordList[i][1], coordList[i][2], coordList[i][3]], [coordx + coordList[i][4], coordy + coordList[i][5]], [coordx + coordList[i][6], coordy + coordList[i][7]]]
    elif i == 12 or i == 13 or i == 14:
        coords = [[coordx + coordList[i][0], coordy + coordList[i][1]], [coordx + coordList[i][2], coordy + coordList[i][3]], [coordx + coordList[i][4], coordy + coordList[i][5]]]
    elif i == 15 or i == 16:
        coords = [[coordx + coordList[i][0], coordy + coordList[i][1]], [coordx + coordList[i][2], coordy + coordList[i][3]], [coordx + coordList[i][4], coordy + coordList[i][5]], [coordx + coordList[i][6], coordy + coordList[i][7]]]
    elif i == 18:
        coords = [[coordx + coordList[i][0], coordy + coordList[i][1]], [coordx + coordList[i][2], coordy + coordList[i][3]], [coordx + coordList[i][4], coordy + coordList[i][5]], [coordx + coordList[i][6], coordy + coordList[i][7]], [coordx + coordList[i][8], coordy + coordList[i][9]], [coordx + coordList[i][10], coordy + coordList[i][11]], [coordx + coordList[i][12], coordy + coordList[i][13]], [coordx + coordList[i][14], coordy + coordList[i][15]], [coordx + coordList[i][16], coordy + coordList[i][17]], [coordx + coordList[i][18], coordy + coordList[i][19]]]
    elif i == 17:
        coords = [[coordx + coordList[i][0], coordy + coordList[i][1], coordList[i][2], coordList[i][3]], [coordx + coordList[i][4], coordy + coordList[i][5], coordList[i][6], coordList[i][7]], [coordx + coordList[i][8], coordy + coordList[i][9]], [coordx + coordList[i][10], coordy + coordList[i][11]], [coordx + coordList[i][12], coordy + coordList[i][13]], [coordx + coordList[i][14], coordy + coordList[i][15]]]
    elif i == 19:
        coords = [[coordx + coordList[i][0], coordy + coordList[i][1], coordList[i][2], coordList[i][3]], [coordx + coordList[i][4], coordy + coordList[i][5], coordList[i][6], coordList[i][7]], [coordx + coordList[i][8], coordy + coordList[i][9], coordList[i][10], coordList[i][11]], [coordx + coordList[i][12], coordy + coordList[i][13], coordList[i][14], coordList[i][15]], [coordx + coordList[i][16], coordy + coordList[i][17], coordList[i][18], coordList[i][19]]]
    else:
        coords = [coordx + coordList[i][0], coordy + coordList[i][1], coordList[i][2], coordList[i][3]]
    if i == 0 or i == 1:
        pygame.draw.ellipse(canvas, black, coords, 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
    elif i == 2 or i == 3:
        pygame.draw.rect(canvas, black, coords, 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
    elif i == 4 or i == 5:
        pygame.draw.line(canvas, black, coords[0], coords[1], 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
    elif i == 6 or i == 7 or i == 8:
        pygame.draw.arc(canvas, black, coords, 0, pi, 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
    elif i == 9 or i == 10 or i == 11:
        pygame.draw.arc(canvas, black, coords[0], 0, pi, 1)
        pygame.draw.line(canvas, black, coords[1], coords[2], 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
    elif i == 12 or i == 13 or i == 14 or i == 15 or i == 16 or i == 18:
        pygame.draw.polygon(canvas, black, coords, 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
    elif i == 17:
        pygame.draw.arc(canvas, black, coords[0], (pi/4), (5*pi/4), 1)
        pygame.draw.arc(canvas, black, coords[1], (7*pi/4), (3*pi/4), 1)
        pygame.draw.line(canvas, black, coords[2], coords[3], 1)
        pygame.draw.line(canvas, black, coords[4], coords[5], 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))
    elif i == 19:
        pygame.draw.arc(canvas, black, coords[0], 0, pi, 1)
        pygame.draw.arc(canvas, black, coords[1], pi, 2*pi, 1)
        pygame.draw.arc(canvas, black, coords[2], 0, pi, 1)
        pygame.draw.arc(canvas, black, coords[3], pi, 2*pi, 1)
        pygame.draw.arc(canvas, black, coords[4], 0, pi, 1)
        pygame.draw.rect(canvas, red, pygame.Rect(coordx,coordy,1,1))


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


<<<<<<< Updated upstream
<<<<<<< Updated upstream
    for i in range (1, 500):
=======
=======
>>>>>>> Stashed changes

    '''for i in range (1, 20):
>>>>>>> Stashed changes
        randomcoloura = random.randint(0,255)
        randomcolourb = random.randint(0,255)
        randomcolourc = random.randint(0,255)
        randomcolour = (randomcoloura, randomcolourb, randomcolourc)
        pygame.draw.rect(canvas, randomcolour, pygame.Rect(52,64,152,120))
        pygame.draw.ellipse(canvas, randomcolour, pygame.Rect(52,32,152,64))
        pygame.draw.rect(canvas, randomcolour, pygame.Rect(52,184,60,60))
        pygame.draw.rect(canvas, randomcolour, pygame.Rect(144,184,60,60))
        pygame.draw.ellipse(canvas, randomcolour, pygame.Rect(30,80,44,90))
        pygame.draw.ellipse(canvas, glass, pygame.Rect(100,64,128,64))
        #pygame.draw.ellipse(canvas, black, pygame.Rect(52,32,))
        pygame.display.update()
        cwd = os.getcwd()
        filename = str("amongus" + str(i) + ".png")
<<<<<<< Updated upstream
        pygame.image.save(canvas, os.path.join(cwd, filename))
        time.sleep(0.00005)
pygame.quit()
=======
        pygame.image.save(canvas, filename)
        time.sleep(0.00005)'''
    
pygame.quit()
<<<<<<< Updated upstream
        
>>>>>>> Stashed changes
=======
        
>>>>>>> Stashed changes
