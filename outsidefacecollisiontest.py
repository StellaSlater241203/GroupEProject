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

def detect_collision_mask(shape1, shape2): #from stack overflow
    surface1, pos1 = shape1
    surface2, pos2 = shape2
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    offset_x = pos2[0] - pos1[0]
    offset_y = pos2[1] - pos1[1]
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    return False

def check_inside_left_eye_region(x,y,xex=116,yex=122):
    xok = False
    yok = False
    if 68 < x < xex:
        xok = True
    if 74 < y < yex:
        yok = True
    rsq = ((x-116)**2)+((y-122)**2)
    if xok == True and yok == True and rsq < 2304:
        return True
    else:
        return False 

def check_inside_face(x,y):
    rsq = (((x-128)**2)/(76**2)) + (((y-128)**2)/(96**2))
    if rsq < 1:
        return True
    else:
        return False

def left_eye_boundary_box(xLeft = 68, xRight = 116, yTop = 74, yBottom = 122, surface = canvas):
    width = xRight - xLeft + 2 #find size of surface based on passed in size of allowed region
    height = yBottom - yTop + 2

    lEyeBoundaryRect = pygame.Rect(xLeft - 1, yTop - 1, width, height) #create a rectangle big enough to encompass boundary box
    lEyeBoundarySurface = pygame.Surface(lEyeBoundaryRect.size, pygame.SRCALPHA) #create a surface with the size of the rectangle

    pygame.draw.line(lEyeBoundarySurface, grey, (1, height-1), (width-1, height-1), 1)  # horizontal line
    pygame.draw.line(lEyeBoundarySurface, grey, (width-1, height-1), (width-1, 1), 1) # vertical line
    pygame.draw.arc(lEyeBoundarySurface, grey, (1, 1, 2*(width - 2), 2*(height - 2)), math.pi/2, math.pi, 1) # arc
    pygame.display.flip()
    
    surface.blit(lEyeBoundarySurface, lEyeBoundaryRect)
    lEyeBoundaryShape = [lEyeBoundarySurface, lEyeBoundaryRect]
    return lEyeBoundaryShape




boundary = left_eye_boundary_box()

counter = 0
gendFeats = []

for i in range(20):
    eyex = random.randint(52, 204)
    eyey = random.randint(32, 224)
    while not check_inside_face(eyex, eyey) or not check_inside_left_eye_region(eyex, eyey):
        eyex = random.randint(52, 204)
        eyey = random.randint(32, 224)

    eyeRect = pygame.Rect(eyex - 12, eyey - 6, 24, 12)
    eyeSurface = pygame.Surface(eyeRect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(eyeSurface, grey, (0, 0, *eyeRect.size), 1)
    eye = [eyeSurface, eyeRect]

    while detect_collision_mask(eye, boundary):
        counter += 1
        print(counter)

        eyex = random.randint(52, 204)
        eyey = random.randint(32, 224)

        for index, eye in enumerate(gendFeats):
            while not check_inside_face(eyex, eyey) or not check_inside_left_eye_region(eyex, eyey) or detect_collision_mask(eye, gendFeats[i]):
                eyex = random.randint(52, 204)
                eyey = random.randint(32, 224)

        eyeRect = pygame.Rect(eyex - 12, eyey - 6, 24, 12)
        eyeSurface = pygame.Surface(eyeRect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(eyeSurface, grey, (0, 0, *eyeRect.size), 1)
        eye = [eyeSurface, eyeRect]

    gendFeats.append(eye)
    canvas.blit(eyeSurface, eyeSurface.get_rect(center=eyeRect.center))
    pygame.display.flip()
    time.sleep(0.5)




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()