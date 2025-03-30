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
from src.screens import (
    draw_start_screen,
    draw_game_over_screen,
    draw_message,
    draw_options_screen,
    get_key_name
)
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
wall_img = load_image('Wall.png')
button_img = load_image('Button.png')

# Create buttons
try_again_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 50, 200, 50, "Try Again", GRAY)
exit_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 120, 200, 50, "Exit", GRAY)
start_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 50, 200, 50, "Start Game", GRAY)
upload_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 120, 200, 50, "Upload Character", GRAY)
options_button = Button(WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 + 190, 200, 50, "Options", GRAY)

# Options screen buttons
back_button = Button(0, 0, 120, 30, "Back", GRAY)
volume_up_button = Button(0, 0, 30, 30, "+", GRAY)
volume_down_button = Button(0, 0, 30, 30, "-", GRAY)

# Key mapping buttons
key_buttons = [
    Button(0, 0, 160, 35, "Up: W", GRAY),
    Button(0, 0, 160, 35, "Down: S", GRAY),
    Button(0, 0, 160, 35, "Left: A", GRAY),
    Button(0, 0, 160, 35, "Right: D", GRAY)
]

# Initialize game state
game_state = GameState()
game_state.show_options = False
game_state.remapping_key = None

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

def handle_key_remap(event):
    if game_state.remapping_key:
        if event.key != pygame.K_ESCAPE:  # Don't allow ESC key
            game_state.remap_key(game_state.remapping_key, event.key)
            # Update button text
            key_name = get_key_name(event.key)
            for button in key_buttons:
                if button.text.startswith(game_state.remapping_key.capitalize()):
                    button.text = f"{game_state.remapping_key.capitalize()}: {key_name}"
                    break
        game_state.remapping_key = None

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state.show_options:
                if back_button.is_clicked(event.pos):
                    game_state.show_options = False
                elif volume_up_button.is_clicked(event.pos):
                    game_state.set_volume(min(1.0, game_state.volume + 0.1))
                elif volume_down_button.is_clicked(event.pos):
                    game_state.set_volume(max(0.0, game_state.volume - 0.1))
                else:
                    # Check key mapping buttons
                    for i, button in enumerate(key_buttons):
                        if button.is_clicked(event.pos):
                            game_state.remapping_key = ['up', 'down', 'left', 'right'][i]
                            button.text = f"{game_state.remapping_key.capitalize()}: Press any key..."
                            break
            elif game_state.game_started:
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
                elif options_button.is_clicked(event.pos):
                    game_state.show_options = True
        elif event.type == pygame.KEYDOWN and game_state.remapping_key:
            handle_key_remap(event)
    
    # Clear screen
    screen.fill(WHITE)

    if game_state.show_options:
        draw_options_screen(screen, back_button, volume_up_button, volume_down_button, key_buttons, title_font, message_font, game_state.volume, floor_img)
    elif not game_state.game_started:
        draw_start_screen(screen, start_button, upload_button, options_button, title_font, controls_font, floor_img)
    elif game_state.game_over:
        draw_game_over_screen(screen, game_state.victory, try_again_button, exit_button, floor_img, title_font, message_font)
    else:
        # Handle player movement with remapped keys
        keys = pygame.key.get_pressed()
        if keys[game_state.get_key_for_action('up')] and not game_state.prev_keys[game_state.get_key_for_action('up')]:
            game_state.player_y = max(0, game_state.player_y - 1)
        if keys[game_state.get_key_for_action('down')] and not game_state.prev_keys[game_state.get_key_for_action('down')]:
            game_state.player_y = min(GRID_SIZE - 1, game_state.player_y + 1)
        if keys[game_state.get_key_for_action('left')] and not game_state.prev_keys[game_state.get_key_for_action('left')]:
            game_state.player_x = max(0, game_state.player_x - 1)
        if keys[game_state.get_key_for_action('right')] and not game_state.prev_keys[game_state.get_key_for_action('right')]:
            game_state.player_x = min(GRID_SIZE - 1, game_state.player_x + 1)
        
        # Update previous key states
        game_state.prev_keys[game_state.get_key_for_action('up')] = keys[game_state.get_key_for_action('up')]
        game_state.prev_keys[game_state.get_key_for_action('down')] = keys[game_state.get_key_for_action('down')]
        game_state.prev_keys[game_state.get_key_for_action('left')] = keys[game_state.get_key_for_action('left')]
        game_state.prev_keys[game_state.get_key_for_action('right')] = keys[game_state.get_key_for_action('right')]
        
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
        
        # Draw floor tiles and grid
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if floor_img:
                    screen.blit(floor_img, (x * CELL_SIZE, y * CELL_SIZE))
                pygame.draw.rect(screen, GRAY, 
                               (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # Draw wall and button in level 2
        if game_state.current_level == 2:
            wall_x = GRID_SIZE // 2  # Center wall position

            # Draw button at its fixed position
            screen.blit(button_img, (game_state.button_x * CELL_SIZE, game_state.button_y * CELL_SIZE))
            
            # Check if player is on button
            if game_state.player_x == game_state.button_x and game_state.player_y == game_state.button_y:
                if game_state.wall_active:
                    game_state.wall_active = False
                    game_state.show_message("The wall disappears!")
                    game_state.message_timer = 2000
            
            # Draw wall if active
            if game_state.wall_active:
                # Draw vertical wall in center for entire height
                for y in range(GRID_SIZE):  # Full height wall
                    screen.blit(wall_img, (wall_x * CELL_SIZE, y * CELL_SIZE))
                    
                    # Block player movement through wall
                    if game_state.player_x == wall_x and game_state.player_y == y:
                        # Push player back to previous position
                        if game_state.player_x > game_state.prev_player_x:
                            game_state.player_x = game_state.prev_player_x
                        else:
                            game_state.player_x = game_state.prev_player_x

        # Draw maze walls in level 3
        elif game_state.current_level == 3:
            # Draw all maze walls
            for wall_x, wall_y in game_state.maze_walls:
                screen.blit(wall_img, (wall_x * CELL_SIZE, wall_y * CELL_SIZE))
                
                # Block player movement through maze walls
                if game_state.player_x == wall_x and game_state.player_y == wall_y:
                    # Push player back to previous position
                    game_state.player_x = game_state.prev_player_x
                    game_state.player_y = game_state.prev_player_y
                    game_state.show_message("You can't walk through walls!")
                    game_state.message_timer = 1000

        # Draw chest if not opened
        if not game_state.chest_opened:
            screen.blit(chest_img, (game_state.chest_x * CELL_SIZE, game_state.chest_y * CELL_SIZE))
        
        # Draw key if not collected
        if not game_state.has_key:
            screen.blit(key_img, (game_state.key_x * CELL_SIZE, game_state.key_y * CELL_SIZE))
        
        # Draw door
        screen.blit(door_img, (game_state.door_x * CELL_SIZE, game_state.door_y * CELL_SIZE))
        
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
        
        # Draw player
        player_img_to_use = game_state.custom_player_image if game_state.custom_player_image else player_img
        screen.blit(player_img_to_use, (game_state.player_x * CELL_SIZE, game_state.player_y * CELL_SIZE))
        
        # Store previous position for wall collision
        game_state.prev_player_x = game_state.player_x
        game_state.prev_player_y = game_state.player_y
        
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
    
    # Update display
    pygame.display.flip()
    
    # Check sound status
    game_state.check_sound_status()
    
    # Control frame rate
    clock.tick(60)

# Quit game
pygame.quit()
sys.exit() 