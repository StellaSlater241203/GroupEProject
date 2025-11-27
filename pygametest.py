import pygame
import random
import os

# --- Collision Detection Functions (Kept for initial placement logic) ---

def detect_oval_collision_mask(rect1, rect2):
    surface1 = pygame.Surface((rect1.width, rect1.height), pygame.SRCALPHA)
    surface2 = pygame.Surface((rect2.width, rect2.height), pygame.SRCALPHA)
    pygame.draw.ellipse(surface1, (255, 255, 255), (0, 0, rect1.width, rect1.height))
    pygame.draw.ellipse(surface2, (255, 255, 255), (0, 0, rect2.width, rect2.height))
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    offset_x = rect2.x - rect1.x
    offset_y = rect2.y - rect1.y
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    return False

# --- Pygame Setup and Test Implementation ---

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Static Ovals")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define the ovals using pygame.Rect for position and size
oval1_rect = pygame.Rect(125, 200, 100, 80)

# Oval 2 (Setup function)
def get_new_random_rect():
    # Keep sizes somewhat contained to fit in the window better
    w = random.randint(10, 110)
    h = random.randint(10, 110)
    x = random.randint(0, SCREEN_WIDTH - w)
    y = random.randint(0, SCREEN_HEIGHT - h)
    return pygame.Rect(x, y, w, h)

oval2_rect = get_new_random_rect()
oval1_rect = get_new_random_rect()

# --- Initial Placement Logic ---

# Ensure oval2_rect is placed in a non-colliding spot ONCE before drawing
'''while detect_oval_collision_mask(oval1_rect, oval2_rect):
    oval2_rect = get_new_random_rect()'''

# --- Drawing Logic (Done only ONCE) ---

screen.fill(BLACK) # Clear screen once

# Draw the ovals in their final static positions
pygame.draw.ellipse(screen, GREEN, oval1_rect)
pygame.draw.ellipse(screen, RED, oval2_rect)

# Update the display once so the user sees the final drawing
pygame.display.flip()


filename = "static_ovals.png"
try:
    # The file format (PNG or JPEG) is determined by the filename extension.
    pygame.image.save(screen, filename) 
    print(f"Successfully saved window content to {os.path.abspath(filename)}")
except pygame.error as e:
    print(f"Failed to save image: {e}")

# --- Event Loop (Keeps window open, no updates) ---

running = True
# This loop now ONLY listens for the QUIT event
while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # This breaks the while loop and closes the window
        

pygame.quit()
