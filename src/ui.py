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
        # Draw title at very top - mobile optimized
        title = self.font_medium.render("♥ LOVE MAZE ♥", True, DARK_RED)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, top=5)
        screen.blit(title, title_rect)
        
        # Draw level on left side
        level_text = self.font_small.render(f"Lvl {level}", True, PURPLE)
        screen.blit(level_text, (8, 40))
        
        # Draw score in center
        score_text = self.font_small.render(f"Score: {score}", True, PURPLE)
        score_rect = score_text.get_rect(centerx=SCREEN_WIDTH // 2, top=40)
        screen.blit(score_text, score_rect)
        
        # Draw lives as hearts in top right corner
        for i in range(lives):
            self.draw_life_heart(screen, SCREEN_WIDTH - 30 - (i * 28), 40)
        
        # Draw controls at bottom - mobile friendly
        controls = self.font_small.render("Tap to move", True, GRAY)
        controls_rect = controls.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 8)
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
