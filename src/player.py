"""Player character"""

import pygame
from src.constants import *

class Player:
    """Player character that navigates the maze"""
    
    def __init__(self, start_pos, maze=None):
        """Initialize player at start position"""
        offset_x = maze.offset_x if maze else MAZE_OFFSET_X
        offset_y = maze.offset_y if maze else MAZE_OFFSET_Y
        self.rect = pygame.Rect(
            start_pos[0] * TILE_SIZE + offset_x + 4,
            start_pos[1] * TILE_SIZE + offset_y + 4,
            TILE_SIZE - 8,
            TILE_SIZE - 8
        )
        self.color = RED
    
    def move(self, dx, dy, maze):
        """Move player if not colliding with walls"""
        # Try horizontal movement
        if dx != 0:
            new_rect = self.rect.copy()
            new_rect.x += dx
            
            # Check collision with maze walls
            if not self.collides_with_maze(new_rect, maze):
                self.rect.x += dx
        
        # Try vertical movement
        if dy != 0:
            new_rect = self.rect.copy()
            new_rect.y += dy
            
            # Check collision with maze walls
            if not self.collides_with_maze(new_rect, maze):
                self.rect.y += dy
    
    def collides_with_maze(self, rect, maze):
        """Check if rect collides with maze walls"""
        # Check corners and edges of player rect
        check_points = [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom),
            (rect.centerx, rect.top),
            (rect.centerx, rect.bottom),
            (rect.left, rect.centery),
            (rect.right, rect.centery),
        ]
        
        for x, y in check_points:
            if maze.is_wall(x, y):
                return True
        
        return False
    
    def draw(self, screen):
        """Draw player as a pixelated character"""
        # Draw player as animated heart character
        self.draw_heart_character(screen)
    
    def draw_heart_character(self, screen):
        """Draw player as a cute 8-bit heart character"""
        cx, cy = self.rect.center
        pixel = 3
        
        # Heart body
        heart_pattern = [
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 2, 2, 1, 1, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [0, 1, 2, 2, 2, 2, 1, 0],
            [0, 0, 1, 2, 2, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
        ]
        
        start_x = cx - (4 * pixel)
        start_y = cy - (3 * pixel)
        
        for row_idx, row in enumerate(heart_pattern):
            for col_idx, cell in enumerate(row):
                rect = pygame.Rect(
                    start_x + col_idx * pixel,
                    start_y + row_idx * pixel,
                    pixel, pixel
                )
                if cell == 1:
                    pygame.draw.rect(screen, DARK_RED, rect)
                elif cell == 2:
                    pygame.draw.rect(screen, RED, rect)
        
        # Draw eyes
        eye_color = WHITE
        left_eye = pygame.Rect(cx - 6, cy - 3, 2, 2)
        right_eye = pygame.Rect(cx + 4, cy - 3, 2, 2)
        pygame.draw.rect(screen, eye_color, left_eye)
        pygame.draw.rect(screen, eye_color, right_eye)
