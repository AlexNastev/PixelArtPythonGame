import os
import pygame
import random
from .constants import CELL_SIZE, GRID_SIZE

def load_image(name, size=(CELL_SIZE, CELL_SIZE)):
    try:
        image = pygame.image.load(os.path.join('assets', name))
        return pygame.transform.scale(image, size)
    except:
        print(f"Error loading image: {name}")
        return None

def get_random_position():
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        # Make sure not spawning on player's starting position
        if x != GRID_SIZE // 2 or y != GRID_SIZE // 2:
            return x, y

def get_door_position(player_pos, chest_pos, key_pos, enemy_pos):
    while True:
        # Randomly choose a side (0: top, 1: right, 2: bottom, 3: left)
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, GRID_SIZE - 1)
            y = 0
        elif side == 1:  # Right
            x = GRID_SIZE - 1
            y = random.randint(0, GRID_SIZE - 1)
        elif side == 2:  # Bottom
            x = random.randint(0, GRID_SIZE - 1)
            y = GRID_SIZE - 1
        else:  # Left
            x = 0
            y = random.randint(0, GRID_SIZE - 1)
        
        # Check if position is free
        if (x, y) != player_pos and \
           (x, y) != chest_pos and \
           (x, y) != key_pos and \
           (x, y) != enemy_pos:
            return x, y 