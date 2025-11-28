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
pygame.display.set_caption("Pygame Test 3 - Rough Face Shapes With Collision Detection")


# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Useful Variables
# center = (128, 128)
featureNumbers = [2, 1, 1] # eyes, nose, mouth
features = []

screen.fill(WHITE)

def face_outline(surface):
    rect = pygame.Rect(52, 31, 152, 192) # compute bounding rectangle for the ellipse
    pygame.draw.ellipse(surface, BLACK, rect, 1) # draw the ellipse outline
    

def draw_circle(surface, colour, center, radius):
    circle = pygame.draw.circle(surface, colour, center, radius, 1)

def draw_triangle(surface, colour, point1, point2, point3):
    nose = pygame.draw.polygon(surface, colour, [point1, point2, point3], 1)

def draw_mouth(surface, colour, center, width, height):
    mouth = (pygame.draw.line(surface, colour, (center[0] - width // 2, center[1]), (center[0] + width // 2, center[1]), 1), pygame.draw.circle(surface, colour, center, width // 2, 1, draw_top_right=False, draw_top_left=False, draw_bottom_right=True, draw_bottom_left=True))



def detect_collision_mask(surface1, pos1, surface2, pos2): #from stack overflow
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    offset_x = pos2[0] - pos1[0]
    offset_y = pos2[1] - pos1[1]
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    return False


def draw_face():
    collision_counter = 0
    surfaces_and_rects = [] #list to hold surfaces and rects of features
    feature_positions = [] #list to hold positions of features for collision detection
    mask_surfaces = []  # list to hold filled mask surfaces for collision detection
    
    # eyes
    for _ in range(featureNumbers[0]):
        r = 10
        #choose eye center in screen coords
        eye_cx = random.randint(52, 204)
        eye_cy = random.randint(32, 224)
        collision = True
        while collision:
            collision = False
            
            while (((eye_cx-128)**2)/(76**2)) + (((eye_cy-128)**2)/(96**2)) >= 1:
                print("regenerating")
                eye_cx = random.randint(52, 204)
                eye_cy = random.randint(32, 224)

            # filled mask surface for collision
            eye_mask_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(eye_mask_surf, BLACK, (r, r), r, 0)

            eye_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA) #eye bounding box
            draw_circle(eye_surf, BLACK, (r, r), r)#draw eye in centre of bounding box
            blit_pos = (eye_cx - r, eye_cy - r) #top-left position for blitting

            for j, (other_surf, other_rect) in enumerate(surfaces_and_rects): #check against already existing features
                other_pos = feature_positions[j]  # stored as top-left
                other_mask_surf = mask_surfaces[j]
                if detect_collision_mask(eye_mask_surf, blit_pos, other_mask_surf, other_pos):#check for collision, if so, try again
                    collision = True
                    collision_counter += 1
                    print("collision detected", collision_counter)
                    eye_cx = random.randint(52, 204)
                    eye_cy = random.randint(32, 224)
                    break

        rect = eye_surf.get_rect(topleft=blit_pos) #get rect for blitting
        surfaces_and_rects.append((eye_surf, rect)) #store surface and rect
        feature_positions.append(blit_pos) #store position for collision detection
        mask_surfaces.append(eye_mask_surf)

    for _ in range(featureNumbers[1]): # nose
        collision = True
        nose_cx = random.randint(96, 160)
        nose_cy = random.randint(80, 176)
        while (((nose_cx-128)**2)/(76**2)) + (((nose_cy-128)**2)/(96**2)) >= 1:
            print("regenerating")
            nose_cx = random.randint(96, 160)
            nose_cy = random.randint(80, 176)
        while collision:
            collision = False
            while (((nose_cx-128)**2)/(76**2)) + (((nose_cy-128)**2)/(96**2)) >= 1:
                print("regenerating")
                nose_cx = random.randint(96, 160)
                nose_cy = random.randint(80, 176)
            
            #triangle points in coords (pointing down)
            p1 = (nose_cx, nose_cy - 10)
            p2 = (nose_cx - 10, nose_cy + 10)
            p3 = (nose_cx + 10, nose_cy + 10)
            minx = min(p1[0], p2[0], p3[0])
            miny = min(p1[1], p2[1], p3[1])
            maxx = max(p1[0], p2[0], p3[0])
            maxy = max(p1[1], p2[1], p3[1])
            w = maxx - minx + 1
            h = maxy - miny + 1

            nose_surf = pygame.Surface((w, h), pygame.SRCALPHA) #nose bounding box
            lp1 = (p1[0] - minx, p1[1] - miny)
            lp2 = (p2[0] - minx, p2[1] - miny)
            lp3 = (p3[0] - minx, p3[1] - miny) #local points in nose_surf coords

            # filled mask surface for collision
            nose_mask_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.polygon(nose_mask_surf, BLACK, [lp1, lp2, lp3], 0)
            draw_triangle(nose_surf, BLACK, lp1, lp2, lp3)#draw nose in local coords

            blit_pos = (minx, miny)#top-left position for blitting

            for j, (other_surf, other_rect) in enumerate(surfaces_and_rects):#check against already existing features
                other_pos = feature_positions[j]
                other_mask_surf = mask_surfaces[j]
                if detect_collision_mask(nose_mask_surf, blit_pos, other_mask_surf, other_pos):#blah blah blah same as above
                    collision_counter += 1
                    print("collision detected", collision_counter)
                    collision = True
                    nose_cx = random.randint(96, 160)
                    nose_cy = random.randint(80, 176)
                    break
        
        rect = nose_surf.get_rect(topleft=blit_pos)#same as above
        pygame.transform.rotate(nose_surf, 30)

        surfaces_and_rects.append((nose_surf, rect))
        feature_positions.append(blit_pos)
        mask_surfaces.append(nose_mask_surf)

    for _ in range(featureNumbers[2]):#third times the charm (mouth)
        collision = True
        mouth_w = 60
        mouth_h = 60
        mouth_cx = random.randint(64, 192)
        mouth_cy = random.randint(128, 224)


        while collision:
            collision = False
            
            while (((mouth_cx-128)**2)/(76**2)) + (((mouth_cy-128)**2)/(96**2)) >= 1:
                print("regenerating mouth")
                mouth_cx = random.randint(96, 160)
                mouth_cy = random.randint(80, 176)

            # filled mask surface for collision
            mouth_mask_surf = pygame.Surface((mouth_w, mouth_h), pygame.SRCALPHA)
            pygame.draw.circle(mouth_mask_surf, BLACK, (mouth_w // 2, mouth_h // 2), mouth_w // 2, 0)

            mouth_surf = pygame.Surface((mouth_w, mouth_h), pygame.SRCALPHA) #mouth bounding box (who woulda seen it)
            draw_mouth(mouth_surf, BLACK, (mouth_w // 2, mouth_h // 2), mouth_w, mouth_h)
            rotated_mouth_surf = pygame.transform.rotate(mouth_surf, 30)
            mouth_surf.blit(rotated_mouth_surf, (50, 50))
            blit_pos = (mouth_cx - mouth_w // 2, mouth_cy - mouth_h // 2)

            for j, (other_surf, other_rect) in enumerate(surfaces_and_rects):#omg never guess what this does
                other_pos = feature_positions[j]
                other_mask_surf = mask_surfaces[j]
                if detect_collision_mask(mouth_mask_surf, blit_pos, other_mask_surf, other_pos):#pattern recognition test]
                    collision = True
                    collision_counter += 1
                    print("collision detected", collision_counter)
                    mouth_cx = random.randint(64, 192)
                    mouth_cy = random.randint(128, 224)
                    break

        rect = mouth_surf.get_rect(topleft=blit_pos)
        surfaces_and_rects.append((mouth_surf, rect)) 
        feature_positions.append(blit_pos)
        mask_surfaces.append(mouth_mask_surf)

    return surfaces_and_rects #return list of (surface, rect) tuples for blitting

def draw_ellipse_angle(surface, color, rect, angle, width=2):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

def draw_polygon_angle(surface, colour, rect, angle, width = 1):
    target_rect = pygame.Rect(rect)
    shape_surf1 = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf1, colour, ((5, 5), (15, 20), (10, 20), (5, 20)), width)
    rotated_surf = pygame.transform.rotate(shape_surf1, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))




draw_ellipse_angle(screen, BLACK, (20, 20, 20, 30), random.randint(5, 50))
draw_polygon_angle(screen, BLACK, (200, 220, 30, 30), random.randint(0, 360))


# Draw face outline
faces_list = []
for i in range(25):
    print("face: ", i)
    screen.fill(WHITE)
    face_outline(screen)
    #features_list = draw_face()
    #faces_list.append(features_list)
    draw_ellipse_angle(screen, BLACK, (20, 20, 20, 30), random.randint(0, 360))
    draw_polygon_angle(screen, BLACK, (200, 220, 30, 30), random.randint(0, 360))

    
    # Display this face immediately
    #for surface, rect in features_list:
        #screen.blit(surface, rect)
    pygame.display.flip()
    time.sleep(0.5)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
pygame.quit()