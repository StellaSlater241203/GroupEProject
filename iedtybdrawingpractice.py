import pygame
import math

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Test 4 - Iedtyb Drawing")


# Colours
black = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

canvas.fill(WHITE)

def face_outline(surface):
    faceRect = pygame.Rect(52, 32, 152, 192) # compute bounding rectangle for the ellipse
    faceSurface = pygame.Surface(faceRect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(faceSurface, black, (0, 0, *faceRect.size), 1) # draw the ellipse outline
    surface.blit(faceSurface, faceSurface.get_rect(center = faceRect.center))

def left_eye_boundary_box(xLeft = 68, xRight = 116, yTop = 74, yBottom = 122, surface = canvas):
    width = xRight - xLeft + 2#find size of surface based on passed in size of allowed region
    height = yBottom - yTop + 2

    lEyeBoundaryRect = pygame.Rect(xLeft - 1, yTop - 1, width, height) #create a rectangle big enough to encompass boundary box
    lEyeSurface = pygame.Surface(lEyeBoundaryRect.size, pygame.SRCALPHA) #create a surface with the size of the rectangle

    pygame.draw.line(lEyeSurface, black, (1, height-1), (width-1, height-1), 1)  # horizontal line
    pygame.draw.line(lEyeSurface, black, (width-1, height-1), (width-1, 1), 1) # vertical line
    pygame.draw.arc(lEyeSurface, black, (1, 1, 2*(width - 2), 2*(height - 2)), math.pi/2, math.pi, 1) # arc

    surface.blit(lEyeSurface, lEyeBoundaryRect)

def right_eye_boundary_box(xLeft = 140, xRight = 188, yTop = 74, yBottom = 122, surface = canvas):
    width = xRight - xLeft + 2 #find size of surface based on passed in size of allowed region
    height = yBottom - yTop + 2
    
    rEyeBoundaryRect = pygame.Rect(xLeft - 1, yTop - 1, width, height) #create a rectangle big enough to encompass boundary box
    rEyeSurface = pygame.Surface(rEyeBoundaryRect.size, pygame.SRCALPHA) #create a surface with the size of the rectangle
    
    pygame.draw.line(rEyeSurface, black, (1, height-1), (width-1, height-1), 1)  # horizontal line
    pygame.draw.line(rEyeSurface, black, (1, height-1), (1, 1), 1) # vertical line
    pygame.draw.arc(rEyeSurface, black, (-46, 1, 2*(width - 2), 2*(height - 2)), math.pi, (math.pi/2), 1) # arc
    
    surface.blit(rEyeSurface, rEyeBoundaryRect)
    return [rEyeSurface, rEyeBoundaryRect]

def nose_boundary_box(xLeft = 100, xRight = 156, yTop = 96, yBottom = 146, surface = canvas):
    width = xRight - xLeft
    height = yBottom - yTop
    
    noseBoundaryRect = pygame.Rect(xLeft, yTop, width, height)
    noseSurface = pygame.Surface(noseBoundaryRect.size, pygame.SRCALPHA)
    
    pygame.draw.rect(noseSurface, GREEN, (0, 0, width, height), 1)
    
    surface.blit(noseSurface, noseBoundaryRect)
    return [noseSurface, noseBoundaryRect]

def mouth_boundary_box(xLeft = 100, xRight = 156, yTop = 132, yBottom = 198, surface = canvas):
    width = xRight - xLeft
    height = yBottom - yTop
    
    mouthBoundaryRect = pygame.Rect(xLeft, yTop, width, height)
    mouthSurface = pygame.Surface(mouthBoundaryRect.size, pygame.SRCALPHA)
    
    pygame.draw.rect(mouthSurface, RED, (0, 0, width, height), 1)
    
    surface.blit(mouthSurface, mouthBoundaryRect)
    return [mouthSurface, mouthBoundaryRect]


face_outline(canvas)
left_eye_boundary_box()
right_eye_boundary_box()
nose_boundary_box()
mouth_boundary_box()

pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
pygame.quit()