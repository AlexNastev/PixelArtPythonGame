import time
import pygame
from .constants import GRID_SIZE, MESSAGE_DURATION
from .utils import get_random_position, get_door_position

class GameState:
    def __init__(self):
        self.reset_game()
        self.prev_keys = {pygame.K_w: False, pygame.K_s: False, pygame.K_a: False, pygame.K_d: False}
        self.message = ""
        self.message_timer = 0
        self.message_start_time = 0
        self.custom_player_image = None  # Store custom player image
        
    def set_custom_player_image(self, image):
        self.custom_player_image = image

    def reset_game(self):
        # Player position
        self.player_x = GRID_SIZE // 2
        self.player_y = GRID_SIZE // 2
        
        # Game objects positions
        self.chest_x, self.chest_y = get_random_position()
        self.key_x, self.key_y = get_random_position()
        self.enemy_x, self.enemy_y = get_random_position()
        self.door_x, self.door_y = get_door_position(
            (self.player_x, self.player_y),
            (self.chest_x, self.chest_y),
            (self.key_x, self.key_y),
            (self.enemy_x, self.enemy_y)
        )
        
        # Game state
        self.game_started = False
        self.game_over = False
        self.victory = False
        self.current_level = 1
        self.has_key = False
        self.has_grass_sword = False
        self.has_fire_sword = False
        self.has_water_sword = False
        self.chest_opened = False
        
        # Message system
        self.message = ""
        self.message_time = 0
    
    def next_level(self):
        # Reset player position
        self.player_x = GRID_SIZE // 2
        self.player_y = GRID_SIZE // 2
        
        # Reset items
        self.chest_x, self.chest_y = get_random_position()
        self.key_x, self.key_y = get_random_position()
        self.enemy_x, self.enemy_y = get_random_position()
        self.door_x, self.door_y = get_door_position(
            (self.player_x, self.player_y),
            (self.chest_x, self.chest_y),
            (self.key_x, self.key_y),
            (self.enemy_x, self.enemy_y)
        )
        
        # Reset level-specific state
        self.has_key = False
        self.chest_opened = False
        self.message = ""
        self.message_time = 0
        self.current_level += 1
    
    def show_message(self, message):
        self.message = message
        self.message_start_time = pygame.time.get_ticks()
    
    def is_message_active(self):
        if self.message_timer > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.message_start_time >= self.message_timer:
                self.message_timer = 0
                self.message = ""
                return False
            return True
        return False 