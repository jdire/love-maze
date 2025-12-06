"""UI rendering"""

import pygame
from src.constants import *

class UI:
    """User interface renderer"""
    
    def __init__(self):
        """Initialize UI"""
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def draw(self, screen, level, score, lives):
        """Draw UI elements"""
        # Draw title
        title = self.font_large.render("♥ LOVE MAZE ♥", True, DARK_RED)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, top=10)
        screen.blit(title, title_rect)
        
        # Draw level
        level_text = self.font_medium.render(f"Level: {level}", True, PURPLE)
        screen.blit(level_text, (20, 20))
        
        # Draw score
        score_text = self.font_medium.render(f"Score: {score}", True, PURPLE)
        screen.blit(score_text, (20, 60))
        
        # Draw lives as hearts
        for i in range(lives):
            self.draw_life_heart(screen, SCREEN_WIDTH - 40 - (i * 35), 30)
        
        # Draw controls
        controls = self.font_small.render("Arrow Keys/WASD/Swipe: Move  |  R: Reset  |  ESC: Quit", True, GRAY)
        controls_rect = controls.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 10)
        screen.blit(controls, controls_rect)
    
    def draw_life_heart(self, screen, x, y):
        """Draw a small heart for lives display"""
        pixel = 2
        heart_pattern = [
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
        ]
        
        for row_idx, row in enumerate(heart_pattern):
            for col_idx, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(x + col_idx * pixel, y + row_idx * pixel, pixel, pixel)
                    pygame.draw.rect(screen, RED, rect)
