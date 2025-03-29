import os
import pygame
import sys
from src.constants import (
    BROWN, WINDOW_SIZE, CELL_SIZE, GRID_SIZE,
    WHITE, BLACK, GRAY, YELLOW, GREEN, BLUE, ORANGE
)
from src.button import Button
from src.game_state import GameState
from src.utils import load_image
from src.screens import draw_start_screen, draw_game_over_screen, draw_message
from src.game_data import (
    get_monster_info, get_sword_info, get_item_info,
    get_monster_description, get_sword_description, get_defeat_message
)

# Initialize Pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("The Bad Elementals")

# Initialize fonts
game_font = pygame.font.SysFont('segoeuisymbol', CELL_SIZE)
title_font = pygame.font.SysFont('Arial', 48, bold=True)
message_font = pygame.font.SysFont('Arial', 24)
controls_font = pygame.font.SysFont('Arial', 20)

# Load images
def load_image(name, size=(CELL_SIZE, CELL_SIZE)):
    try:
        image = pygame.image.load(os.path.join('assets', name))
        return pygame.transform.scale(image, size)
    except:
        print(f"Error loading image: {name}")
        return None

# Load game assets
key_img = load_image('key.png')
grass_sword_img = load_image('Grass Sword.png')
fire_sword_img = load_image('Fire Sword.png')
water_sword_img = load_image('Water Sword.png')
grass_monster_img = load_image('Grass Monster.png')
fire_monster_img = load_image('Fire Monster.png')
water_monster_img = load_image('Water Monster.png')
player_img = load_image('Player.png')
chest_img = load_image('Chest.png')
door_img = load_image('Door.png')
floor_img = load_image('Floor.png')

# Create buttons
try_again_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 50, 200, 50, "Try Again", GRAY)
exit_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 120, 200, 50, "Exit", GRAY)
start_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 50, 200, 50, "Start Game", GRAY)
upload_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 120, 200, 50, "Upload Character", GRAY)

# Create game state
game_state = GameState()

# Game loop
running = True
clock = pygame.time.Clock()

def handle_image_upload():
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Create and hide the main tkinter window
        root = tk.Tk()
        root.withdraw()
        
        # Open file dialog for PNG files
        file_path = filedialog.askopenfilename(
            title="Select Character Image",
            filetypes=[("PNG files", "*.png")]
        )
        
        if file_path:
            # Load and scale the image
            custom_image = load_image(file_path)
            if custom_image:
                game_state.set_custom_player_image(custom_image)
                game_state.show_message("Custom character image loaded successfully!")
                game_state.message_timer = 2000
            else:
                game_state.show_message("Failed to load custom image. Using default character.")
                game_state.message_timer = 2000
    except Exception as e:
        game_state.show_message("Error loading custom image. Using default character.")
        game_state.message_timer = 2000

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state.game_started:
                if game_state.game_over:
                    if try_again_button.is_clicked(event.pos):
                        game_state.reset_game()
                    elif exit_button.is_clicked(event.pos):
                        running = False
            else:
                if start_button.is_clicked(event.pos):
                    game_state.game_started = True
                elif upload_button.is_clicked(event.pos):
                    handle_image_upload()
    
    # Clear screen with floor tiles
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if floor_img:
                screen.blit(floor_img, (x * CELL_SIZE, y * CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    if not game_state.game_started:
        draw_start_screen(screen, start_button, upload_button, title_font, controls_font)
    elif not game_state.game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        
        # Check each movement key
        if keys[pygame.K_w] and not game_state.prev_keys[pygame.K_w] and game_state.player_y > 0:
            game_state.player_y -= 1
        if keys[pygame.K_s] and not game_state.prev_keys[pygame.K_s] and game_state.player_y < GRID_SIZE - 1:
            game_state.player_y += 1
        if keys[pygame.K_a] and not game_state.prev_keys[pygame.K_a] and game_state.player_x > 0:
            game_state.player_x -= 1
        if keys[pygame.K_d] and not game_state.prev_keys[pygame.K_d] and game_state.player_x < GRID_SIZE - 1:
            game_state.player_x += 1
        
        # Update previous key states
        game_state.prev_keys[pygame.K_w] = keys[pygame.K_w]
        game_state.prev_keys[pygame.K_s] = keys[pygame.K_s]
        game_state.prev_keys[pygame.K_a] = keys[pygame.K_a]
        game_state.prev_keys[pygame.K_d] = keys[pygame.K_d]
        
        # Check if player collects key
        if not game_state.has_key and game_state.player_x == game_state.key_x and game_state.player_y == game_state.key_y:
            key_info = get_item_info('key')
            game_state.has_key = True
            game_state.key_x = -1  # Remove key from map
            game_state.show_message(f"You found the {key_info['name']}! {key_info['description']}")
            game_state.message_timer = 3000  # Set message display time to 3 seconds

        # Check if player opens chest
        if not game_state.chest_opened and game_state.player_x == game_state.chest_x and game_state.player_y == game_state.chest_y:
            chest_info = get_item_info('chest')
            if not game_state.has_key:
                game_state.show_message(f"You need a key to open the {chest_info['name']}!")
                game_state.message_timer = 2000  # Set message display time to 2 seconds
            else:
                game_state.chest_opened = True
                if game_state.current_level == 1:
                    game_state.has_grass_sword = True
                    sword_info = get_sword_info('grass_sword')
                    game_state.show_message(f"You got the {sword_info['name']}! {sword_info['description']}")
                elif game_state.current_level == 2:
                    game_state.has_fire_sword = True
                    sword_info = get_sword_info('fire_sword')
                    game_state.show_message(f"You got the {sword_info['name']}! {sword_info['description']}")
                else:
                    game_state.has_water_sword = True
                    sword_info = get_sword_info('water_sword')
                    game_state.show_message(f"You got the {sword_info['name']}! {sword_info['description']}")
                game_state.message_timer = 3000  # Set message display time to 3 seconds
        
        # Check if player encounters enemy
        if game_state.player_x == game_state.enemy_x and game_state.player_y == game_state.enemy_y:
            monster_info = get_monster_info(game_state.current_level)
            if game_state.current_level == 1:  # Grass monster
                if not game_state.has_grass_sword:
                    game_state.show_message(f"{monster_info['description']}. You need the right sword!")
                    game_state.message_timer = 2000
                    game_state.game_over = True
                    game_state.victory = False
                else:
                    game_state.enemy_x = -1  # Remove enemy when defeated
                    game_state.show_message(monster_info['defeat_message'])
                    game_state.message_timer = 2000
            elif game_state.current_level == 2:  # Fire monster
                if not game_state.has_fire_sword:
                    game_state.show_message(f"{monster_info['description']}. Your grass sword is ineffective!")
                    game_state.message_timer = 2000
                    game_state.game_over = True
                    game_state.victory = False
                else:
                    game_state.enemy_x = -1
                    game_state.show_message(monster_info['defeat_message'])
                    game_state.message_timer = 2000
            else:  # Water monster
                if not game_state.has_water_sword:
                    game_state.show_message(f"{monster_info['description']}. Find the water sword!")
                    game_state.message_timer = 2000
                    game_state.game_over = True
                    game_state.victory = False
                else:
                    game_state.enemy_x = -1
                    game_state.show_message(monster_info['defeat_message'])
                    game_state.message_timer = 2000
                    game_state.show_message("Good Job! You have defeated all 3 elemental monsters! GG!")
                    game_state.message_timer = 2000
                    game_state.game_over = True
                    game_state.victory = True
        
        # Check if player reaches the door
        if game_state.player_x == game_state.door_x and game_state.player_y == game_state.door_y:
            door_info = get_item_info('door')
            if game_state.enemy_x >= 0:  # Enemy still alive
                game_state.show_message(f"Defeat the monster before using the {door_info['name']}!")
                game_state.message_timer = 2000
            else:  # Enemy defeated
                game_state.show_message(f"{door_info['name']} activated! {door_info['description']}")
                game_state.message_timer = 3000
                game_state.next_level()
        
        # Draw grid lines
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                pygame.draw.rect(screen, GRAY, 
                               (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw chest if not opened
        if not game_state.chest_opened:
            if chest_img:
                screen.blit(chest_img, (game_state.chest_x * CELL_SIZE, game_state.chest_y * CELL_SIZE))
            else:
                chest_text = game_font.render('📦', True, BROWN)
                screen.blit(chest_text, (game_state.chest_x * CELL_SIZE, game_state.chest_y * CELL_SIZE))
        
        # Draw key if not collected
        if not game_state.has_key and game_state.key_x >= 0:
            if key_img:
                screen.blit(key_img, (game_state.key_x * CELL_SIZE, game_state.key_y * CELL_SIZE))
            else:
                key_text = game_font.render('🔑', True, YELLOW)
                screen.blit(key_text, (game_state.key_x * CELL_SIZE, game_state.key_y * CELL_SIZE))
        
        # Draw enemy if not defeated
        if game_state.enemy_x >= 0:
            if game_state.current_level == 1:
                if grass_monster_img:
                    screen.blit(grass_monster_img, (game_state.enemy_x * CELL_SIZE, game_state.enemy_y * CELL_SIZE))
                else:
                    enemy_text = game_font.render('🌿', True, GREEN)
                    screen.blit(enemy_text, (game_state.enemy_x * CELL_SIZE, game_state.enemy_y * CELL_SIZE))
            elif game_state.current_level == 2:
                if fire_monster_img:
                    screen.blit(fire_monster_img, (game_state.enemy_x * CELL_SIZE, game_state.enemy_y * CELL_SIZE))
                else:
                    enemy_text = game_font.render('🔥', True, ORANGE)
                    screen.blit(enemy_text, (game_state.enemy_x * CELL_SIZE, game_state.enemy_y * CELL_SIZE))
            else:
                if water_monster_img:
                    screen.blit(water_monster_img, (game_state.enemy_x * CELL_SIZE, game_state.enemy_y * CELL_SIZE))
                else:
                    enemy_text = game_font.render('💧', True, BLUE)
                    screen.blit(enemy_text, (game_state.enemy_x * CELL_SIZE, game_state.enemy_y * CELL_SIZE))
        
        # Draw door (only on levels 1 and 2)
        if game_state.current_level < 3:
            if door_img:
                screen.blit(door_img, (game_state.door_x * CELL_SIZE, game_state.door_y * CELL_SIZE))
            else:
                door_text = game_font.render('🚪', True, BLUE)
                screen.blit(door_text, (game_state.door_x * CELL_SIZE, game_state.door_y * CELL_SIZE))
        
        # Draw player
        player_img = game_state.custom_player_image if game_state.custom_player_image else player_img
        screen.blit(player_img, (game_state.player_x * CELL_SIZE, game_state.player_y * CELL_SIZE))
        
        # Draw inventory
        inventory_x = 10
        if game_state.has_key:
            if key_img:
                scaled_key = pygame.transform.scale(key_img, (30, 30))
                screen.blit(scaled_key, (inventory_x, 10))
            else:
                inventory_text = game_font.render('🔑', True, YELLOW)
                screen.blit(inventory_text, (inventory_x, 10))
            inventory_x += 40
        
        # Draw swords in inventory
        if game_state.has_grass_sword:
            if grass_sword_img:
                scaled_sword = pygame.transform.scale(grass_sword_img, (30, 30))
                screen.blit(scaled_sword, (inventory_x, 10))
            else:
                sword_text = game_font.render('🌿', True, GREEN)
                screen.blit(sword_text, (inventory_x, 10))
            inventory_x += 40
        
        if game_state.has_fire_sword:
            if fire_sword_img:
                scaled_sword = pygame.transform.scale(fire_sword_img, (30, 30))
                screen.blit(scaled_sword, (inventory_x, 10))
            else:
                sword_text = game_font.render('🔥', True, ORANGE)
                screen.blit(sword_text, (inventory_x, 10))
            inventory_x += 40
        
        if game_state.has_water_sword:
            if water_sword_img:
                scaled_sword = pygame.transform.scale(water_sword_img, (30, 30))
                screen.blit(scaled_sword, (inventory_x, 10))
            else:
                sword_text = game_font.render('💧', True, BLUE)
                screen.blit(sword_text, (inventory_x, 10))
        
        # Draw level number
        level_text = controls_font.render(f'Level {game_state.current_level}', True, BLACK)
        screen.blit(level_text, (WINDOW_SIZE - 80, 10))
        
        # Draw message if active
        if game_state.is_message_active():
            draw_message(screen, game_state.message, message_font)
    else:
        draw_game_over_screen(screen, game_state.victory, try_again_button, exit_button, floor_img, title_font, message_font)
    
    # Update display
    pygame.display.flip()
    
    # Control game speed
    clock.tick(60)

# Quit game
pygame.quit()
sys.exit() 