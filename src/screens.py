import pygame
from .constants import (
    WINDOW_SIZE, BLACK, WHITE, GREEN, RED
)

def draw_start_screen(screen, start_button, upload_button, title_font, controls_font):
    # Draw title
    title_text = title_font.render("The Bad Elementals", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//4))
    screen.blit(title_text, title_rect)
    
    # Draw controls
    controls = [
        "Controls:",
        "WASD - Move",
        "Collect the key",
        "Open chest for sword",
        "Defeat the monster",
        "Reach the door"
    ]
    
    for i, text in enumerate(controls):
        text_surface = controls_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 3 + i * 30))
        screen.blit(text_surface, text_rect)
    
    # Draw buttons
    start_button.draw(screen)
    upload_button.draw(screen)

def draw_game_over_screen(screen, victory, try_again_button, exit_button, floor_img, title_font, message_font):
    # Fill background with floor tiles
    for x in range(10):
        for y in range(10):
            if floor_img:
                screen.blit(floor_img, (x * 50, y * 50))
            else:
                pygame.draw.rect(screen, WHITE, (x * 50, y * 50, 50, 50))
    
    # Create semi-transparent overlay
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)  # 50% transparency
    screen.blit(overlay, (0, 0))
    
    # Draw main text box
    box_width = 400
    box_height = 300
    box_x = (WINDOW_SIZE - box_width) // 2
    box_y = (WINDOW_SIZE - box_height) // 2
    
    # Draw box background
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 3)
    
    # Draw title
    if victory:
        title_text = title_font.render('Victory!', True, GREEN)
        subtitle_text = message_font.render('You have defeated all elemental monsters!', True, BLACK)
    else:
        title_text = title_font.render('Game Over', True, RED)
        subtitle_text = message_font.render('Better luck next time!', True, BLACK)
    
    title_rect = title_text.get_rect(center=(WINDOW_SIZE // 2, box_y + 60))
    subtitle_rect = subtitle_text.get_rect(center=(WINDOW_SIZE // 2, box_y + 100))
    
    screen.blit(title_text, title_rect)
    screen.blit(subtitle_text, subtitle_rect)
    
    # Update button positions
    try_again_button.rect.centerx = WINDOW_SIZE // 2
    try_again_button.rect.y = box_y + 160
    exit_button.rect.centerx = WINDOW_SIZE // 2
    exit_button.rect.y = box_y + 220
    
    # Draw buttons
    try_again_button.draw(screen)
    exit_button.draw(screen)

def draw_message(screen, message, message_font):
    if not message:
        return
    
    # Split long messages
    if len(message) > 30:  # If message is too long
        words = message.split()
        first_line = []
        second_line = []
        total_len = 0
        
        for word in words:
            if total_len + len(word) < 30:
                first_line.append(word)
                total_len += len(word) + 1
            else:
                second_line.append(word)
        
        first_line_text = ' '.join(first_line)
        second_line_text = ' '.join(second_line)
        
        # Render both lines
        line1_surface = message_font.render(first_line_text, True, BLACK)
        line2_surface = message_font.render(second_line_text, True, BLACK)
        
        # Position both lines
        line1_rect = line1_surface.get_rect(center=(WINDOW_SIZE // 2, 15))
        line2_rect = line2_surface.get_rect(center=(WINDOW_SIZE // 2, 35))
        
        # Draw background for both lines
        padding = 5
        combined_rect = pygame.Rect(
            min(line1_rect.left, line2_rect.left) - padding,
            line1_rect.top - padding,
            max(line1_rect.width, line2_rect.width) + (padding * 2),
            (line2_rect.bottom - line1_rect.top) + (padding * 2)
        )
        pygame.draw.rect(screen, WHITE, combined_rect)
        pygame.draw.rect(screen, BLACK, combined_rect, 2)
        
        # Draw both lines
        screen.blit(line1_surface, line1_rect)
        screen.blit(line2_surface, line2_rect)
    else:
        # Original single-line rendering
        message_surface = message_font.render(message, True, BLACK)
        message_rect = message_surface.get_rect(center=(WINDOW_SIZE // 2, 20))
        
        # Draw message background with smaller padding
        padding = 5
        bg_rect = message_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(screen, WHITE, bg_rect)
        pygame.draw.rect(screen, BLACK, bg_rect, 2)
        
        screen.blit(message_surface, message_rect) 