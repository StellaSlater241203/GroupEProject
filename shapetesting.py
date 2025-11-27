import pygame
import math
import random
import time

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
canvas = pygame.display.set_mode((256, 256))

# TITLE OF CANVAS
pygame.display.set_caption("Show Image")

exit = False

while not exit:
    canvas.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True


    '''for i in range (1, 20):
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
        filename = str("amongus" + str(i) + ".png")
        pygame.image.save(canvas, filename)
        time.sleep(0.00005)'''
    
    
        