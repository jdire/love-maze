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
        self.font_tiny = pygame.font.Font(None, 18)
        
        # Volume control
        self.volume = 0.5  # 0.0 to 1.0
        self.muted = False
    
    def draw(self, screen, level, score, lives, game=None):
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
        
        # Draw volume controls in bottom left
        self.draw_volume_controls(screen)
        
        # Draw controls at bottom center - mobile friendly
        controls = self.font_small.render("Tap to move", True, GRAY)
        controls_rect = controls.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 8)
        screen.blit(controls, controls_rect)
    
    def draw_volume_controls(self, screen):
        """Draw mute button and volume slider"""
        y = SCREEN_HEIGHT - 35
        
        # Mute button
        mute_rect = pygame.Rect(10, y, 30, 25)
        color = RED if self.muted else PURPLE
        pygame.draw.rect(screen, color, mute_rect, border_radius=5)
        pygame.draw.rect(screen, DARK_PURPLE, mute_rect, 2, border_radius=5)
        
        # Speaker icon
        if self.muted:
            # X over speaker
            pygame.draw.line(screen, WHITE, (mute_rect.left + 5, mute_rect.top + 5), 
                           (mute_rect.right - 5, mute_rect.bottom - 5), 2)
            pygame.draw.line(screen, WHITE, (mute_rect.right - 5, mute_rect.top + 5), 
                           (mute_rect.left + 5, mute_rect.bottom - 5), 2)
        else:
            # Simple speaker icon
            pygame.draw.polygon(screen, WHITE, [
                (mute_rect.left + 8, mute_rect.centery - 3),
                (mute_rect.left + 8, mute_rect.centery + 3),
                (mute_rect.left + 13, mute_rect.centery + 6),
                (mute_rect.left + 13, mute_rect.centery - 6)
            ])
            # Sound waves
            for i in range(2):
                offset = 15 + i * 4
                pygame.draw.arc(screen, WHITE, 
                              (mute_rect.left + offset, mute_rect.centery - 8, 10, 16),
                              -0.5, 0.5, 2)
        
        # Volume slider
        slider_x = 50
        slider_width = 80
        slider_rect = pygame.Rect(slider_x, y + 8, slider_width, 8)
        pygame.draw.rect(screen, DARK_GRAY, slider_rect, border_radius=4)
        
        # Volume level
        if not self.muted:
            level_width = int(slider_width * self.volume)
            level_rect = pygame.Rect(slider_x, y + 8, level_width, 8)
            pygame.draw.rect(screen, HOT_PINK, level_rect, border_radius=4)
        
        # Volume handle
        handle_x = slider_x + int(slider_width * self.volume)
        handle_rect = pygame.Rect(handle_x - 4, y + 4, 8, 16)
        pygame.draw.rect(screen, PURPLE if not self.muted else GRAY, handle_rect, border_radius=3)
        pygame.draw.rect(screen, WHITE, handle_rect, 2, border_radius=3)
    
    def get_mute_button_rect(self):
        """Get the mute button clickable area"""
        y = SCREEN_HEIGHT - 35
        return pygame.Rect(10, y, 30, 25)
    
    def get_volume_slider_rect(self):
        """Get the volume slider clickable area"""
        y = SCREEN_HEIGHT - 35
        return pygame.Rect(50, y, 80, 25)
    
    def handle_volume_click(self, pos, game):
        """Handle clicks on volume controls"""
        # Check mute button
        if self.get_mute_button_rect().collidepoint(pos):
            self.muted = not self.muted
            if game and game.romantic_music:
                if self.muted:
                    game.romantic_music.set_volume(0)
                else:
                    game.romantic_music.set_volume(self.volume)
            return True
        
        # Check volume slider
        slider_rect = self.get_volume_slider_rect()
        if slider_rect.collidepoint(pos):
            # Calculate new volume based on click position
            relative_x = pos[0] - slider_rect.left
            self.volume = max(0.0, min(1.0, relative_x / slider_rect.width))
            
            if game and game.romantic_music and not self.muted:
                game.romantic_music.set_volume(self.volume)
            return True
        
        return False
    
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
