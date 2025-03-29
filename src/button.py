import pygame
from .constants import BLACK, WHITE

class Button:
    def __init__(self, x, y, width, height, text, color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont('Arial', 24)
        
    def draw(self, surface):
        # Draw button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, (220, 220, 220), self.rect)  # Lighter when hovered
        else:
            pygame.draw.rect(surface, self.color, self.rect)
            
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) 