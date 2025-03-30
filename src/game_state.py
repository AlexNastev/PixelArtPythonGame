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
        self.volume = 0.2  # Changed from 1.0 to 0.2 (20%)
        self.key_mappings = {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d
        }
        self.soundtrack = None
        self.wall_active = True  # Track if the wall is present
        self.button_pressed = False  # Track if button is pressed
        self.prev_player_x = 0
        self.prev_player_y = 4
        self.button_x = 0  # Add button position state
        self.button_y = 0
        self.maze_walls = []  # List to store maze wall positions
        self.initialize_sound()
        
    def initialize_sound(self):
        try:
            pygame.mixer.init()
            self.soundtrack = pygame.mixer.Sound('assets/soundTrack.MP3')
            self.soundtrack.set_volume(self.volume)
            # Start playing with infinite loops (-1)
            self.soundtrack.play(-1)
        except Exception as e:
            print(f"Error loading soundtrack: {e}")

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
        if self.soundtrack:
            self.soundtrack.set_volume(self.volume)

    def check_sound_status(self):
        if self.soundtrack and not pygame.mixer.get_busy():
            # If sound stopped, restart it
            self.soundtrack.play(-1)

    def remap_key(self, action, new_key):
        self.key_mappings[action] = new_key

    def get_key_for_action(self, action):
        return self.key_mappings.get(action)

    def set_custom_player_image(self, image):
        self.custom_player_image = image

    def reset_game(self):
        # Reset all game state variables
        self.player_x = 0
        self.player_y = 4
        self.prev_player_x = 0
        self.prev_player_y = 4
        self.enemy_x = 8
        self.enemy_y = 4
        self.key_x = 2
        self.key_y = 2
        self.chest_x = 4
        self.chest_y = 7
        self.door_x = 9
        self.door_y = 4
        self.button_x = 0
        self.button_y = 0
        self.maze_walls = []  # Reset maze walls
        self.has_key = False
        self.chest_opened = False
        self.has_grass_sword = False
        self.has_fire_sword = False
        self.has_water_sword = False
        self.current_level = 1
        self.game_over = False
        self.victory = False
        self.game_started = False
        self.wall_active = True
        self.button_pressed = False
        
        # Message system
        self.message = ""
        self.message_time = 0
    
    def next_level(self):
        self.current_level += 1
        # Clear inventory when changing levels
        self.has_key = False
        self.chest_opened = False
        self.has_grass_sword = False
        self.has_fire_sword = False
        self.has_water_sword = False
        self.wall_active = True
        self.button_pressed = False
        self.maze_walls = []  # Clear maze walls
        
        if self.current_level == 2:
            # Level 2 setup - Fire level with wall and button
            import random
            wall_x = 5  # Center wall position
            left_side = random.choice([True, False])  # Randomly choose left or right side
            
            if left_side:
                self.player_x = 0  # Left side
                self.enemy_x = 8   # Enemy on right side
                self.key_x = 2     # Key on left side
                self.chest_x = 7   # Chest on right side
                self.button_x = 3  # Button on left side
            else:
                self.player_x = 9  # Right side
                self.enemy_x = 1   # Enemy on left side
                self.key_x = 7     # Key on right side
                self.chest_x = 2   # Chest on left side
                self.button_x = 7  # Button on right side
            
            self.player_y = 4  # Middle height
            self.enemy_y = 4   # Middle height
            self.key_y = 2
            self.chest_y = 6
            self.button_y = 8  # Button near bottom
            self.door_x = 9 if left_side else 0  # Door opposite to player
            self.door_y = 4
        
        elif self.current_level == 3:
            # Level 3 setup - Water level with maze
            # Player starts at bottom left (10,1)
            self.player_x = 9  # 10-1 for 0-based
            self.player_y = 0  # 1-1 for 0-based
            
            # Enemy position (2,9)
            self.enemy_x = 1   # 2-1 for 0-based
            self.enemy_y = 8   # 9-1 for 0-based
            
            # Key position (6,2)
            self.key_x = 5    # 6-1 for 0-based
            self.key_y = 1    # 2-1 for 0-based
            
            # Chest position (5,8)
            self.chest_x = 4   # 5-1 for 0-based
            self.chest_y = 7   # 8-1 for 0-based
            
            # No door on final level
            self.door_x = -1
            self.door_y = -1
            
            # Define maze walls based on provided coordinates (converted to 0-based grid)
            self.maze_walls = []
            
            # 1,1 - 1,6
            for y in range(0, 6):
                self.maze_walls.append((0, y))  # x=0 for 1-1
            
            # 2,1 - 9,1
            for x in range(1, 9):  # 2-1 to 9-1
                self.maze_walls.append((x, 0))  # y=0 for 1-1
            
            # 8,1 - 8,8
            for y in range(0, 8):
                self.maze_walls.append((7, y))  # x=7 for 8-1
            
            # 9,1 - 9,8 (excluding 9,4)
            for y in range(0, 8):
                if y != 3:  # Skip 4th position
                    self.maze_walls.append((8, y))  # x=8 for 9-1
            
            # 10,10 - 6,10
            for x in range(9, 4, -1):  # 10-1 to 6-1
                self.maze_walls.append((x, 9))  # y=9 for 10-1
            
            # 6,10 - 6,3
            for y in range(9, 2, -1):  # 10-1 to 3-1
                self.maze_walls.append((5, y))  # x=5 for 6-1
            
            # 6,3 - 2,3
            for x in range(5, 4, -1):  # Stop before 5 (5,3)
                self.maze_walls.append((x, 2))  # y=2 for 3-1
            for x in range(2, 0, -1):  # Start after 5 (5,3)
                self.maze_walls.append((x, 2))  # y=2 for 3-1
            
            # 2,4 - 5,4
            for x in range(1, 4):  # Stop at 4 (5-1) to skip position 5,4
                self.maze_walls.append((x, 3))  # y=3 for 4-1
            
            # 5,4 - 4,10
            for y in range(5, 8):  # Start from 6-1 and stop before 9 to skip 4,9
                self.maze_walls.append((3, y))  # x=3 for 4-1
            self.maze_walls.append((3, 9))  # Add back the wall at 4,10
            
            # 4,10 - 1,10
            for x in range(3, -1, -1):  # 4-1 to 1-1
                self.maze_walls.append((x, 9))  # y=9 for 10-1
            
            # 1,6 - 3,6
            for x in range(0, 3):  # 1-1 to 3-1
                self.maze_walls.append((x, 5))  # y=5 for 6-1
            
            # 3,6 - 3,8
            for y in range(5, 8):  # 6-1 to 8-1
                self.maze_walls.append((2, y))  # x=2 for 3-1
            
            # 3,8 - 1,8
            for x in range(2, -1, -1):  # 3-1 to 1-1
                self.maze_walls.append((x, 7))  # y=7 for 8-1
        
        self.message = ""
        self.message_time = 0
    
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