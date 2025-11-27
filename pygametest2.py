import os
import random
import pygame
import math

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Test 2 - With Face Shapes")


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_oval(surface, color, rect):
    pygame.draw.ellipse(surface, color, rect, 1)

def draw_triangle(surface, color, point1, point2, point3):
    pygame.draw.polygon(surface, color, [point1, point2, point3], 1)
    
def draw_semioval(surface, color, rect):
    pygame.draw.ellipse(surface, color, rect, 1)
    pygame.draw.rect(surface, BLACK, (rect.x, rect.y, rect.width, rect.height // 2))
    
def draw_star(surface, color, center, size):
    points = []
    for i in range(5):
        angle = i * (4 * 3.14159 / 5) - 3.14159 / 2
        x = center[0] + size * 0.5 * math.cos(angle)
        y = center[1] + size * 0.5 * math.sin(angle)
        points.append((x, y))
        angle += (2 * 3.14159 / 5)
        x = center[0] + size * 0.2 * math.cos(angle)
        y = center[1] + size * 0.2 * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, 1)


def get_random_position(size):
    x = random.randint(0, SCREEN_WIDTH - size[0])
    y = random.randint(0, SCREEN_HEIGHT - size[1])
    return (x, y)

def detect_collision_mask(rect1, rect2):
    surface1 = pygame.Surface((rect1.width, rect1.height), pygame.SRCALPHA)
    surface2 = pygame.Surface((rect2.width, rect2.height), pygame.SRCALPHA)
    pygame.draw.rect(surface1, (255, 255, 255), (0, 0, rect1.width, rect1.height))
    pygame.draw.rect(surface2, (255, 255, 255), (0, 0, rect2.width, rect2.height))
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    offset_x = rect2.x - rect1.x
    offset_y = rect2.y - rect1.y
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    return False

screen.fill(WHITE)

# Draw random shapes for testing
for j in range (50):
    shapes = ["oval", "triangle", "semioval", "star"]
    for i in shapes:
        size = (random.randint(30, 80), random.randint(30, 80))
        pos = get_random_position(size)
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        color = BLACK
        
        if i == "oval":
            draw_oval(screen, color, rect)
        elif i == "triangle":
            point1 = (rect.x + rect.width // 2, rect.y)
            point2 = (rect.x, rect.y + rect.height)
            point3 = (rect.x + rect.width, rect.y + rect.height)
            draw_triangle(screen, color, point1, point2, point3)
        elif i == "semioval":
            draw_semioval(screen, color, rect)
        elif i == "star":
            center = (rect.x + rect.width // 2, rect.y + rect.height // 2)
            draw_star(screen, color, center, min(size))
            
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    print("Running...")

# This code is only reached when 'running' becomes False
pygame.quit()
