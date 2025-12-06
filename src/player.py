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
        # Draw player as ring character
        self.draw_heart_character(screen)
    
    def draw_heart_character(self, screen):
        """Draw player as a detailed 16-bit ring with diamond"""
        cx, cy = self.rect.center
        pixel = 2  # Smaller pixels for more detail
        
        # Ring pattern (16-bit style with shading)
        ring_pattern = [
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 2, 2, 2, 2, 2, 2, 1, 0, 0],
            [0, 1, 2, 3, 3, 3, 3, 3, 3, 2, 1, 0],
            [1, 2, 3, 3, 0, 0, 0, 0, 3, 3, 2, 1],
            [1, 2, 3, 0, 0, 0, 0, 0, 0, 3, 2, 1],
            [1, 2, 3, 0, 0, 0, 0, 0, 0, 3, 2, 1],
            [1, 2, 3, 0, 0, 0, 0, 0, 0, 3, 2, 1],
            [1, 2, 3, 3, 0, 0, 0, 0, 3, 3, 2, 1],
            [0, 1, 2, 3, 3, 3, 3, 3, 3, 2, 1, 0],
            [0, 0, 1, 2, 2, 2, 2, 2, 2, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        ]
        
        start_x = cx - (6 * pixel)
        start_y = cy - (5 * pixel)
        
        for row_idx, row in enumerate(ring_pattern):
            for col_idx, cell in enumerate(row):
                rect = pygame.Rect(
                    start_x + col_idx * pixel,
                    start_y + row_idx * pixel,
                    pixel, pixel
                )
                if cell == 1:
                    pygame.draw.rect(screen, DARK_GOLD, rect)  # Dark gold outline
                elif cell == 2:
                    pygame.draw.rect(screen, (218, 165, 32), rect)  # Medium gold
                elif cell == 3:
                    pygame.draw.rect(screen, GOLD, rect)  # Bright gold
        
        # Draw detailed diamond on top of ring
        diamond_pattern = [
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 2, 2, 1, 0, 0],
            [0, 1, 2, 3, 3, 2, 1, 0],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [0, 1, 2, 3, 3, 2, 1, 0],
            [0, 0, 1, 2, 2, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
        ]
        
        diamond_x = cx - (4 * pixel)
        diamond_y = cy - (10 * pixel)
        
        for row_idx, row in enumerate(diamond_pattern):
            for col_idx, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        diamond_x + col_idx * pixel,
                        diamond_y + row_idx * pixel,
                        pixel, pixel
                    )
                    if cell == 1:
                        pygame.draw.rect(screen, (70, 130, 180), rect)  # Steel blue
                    elif cell == 2:
                        pygame.draw.rect(screen, (135, 206, 250), rect)  # Light sky blue
                    elif cell == 3:
                        pygame.draw.rect(screen, (173, 216, 230), rect)  # Light blue
                    elif cell == 4:
                        pygame.draw.rect(screen, WHITE, rect)  # White sparkle
        
        # Add multiple sparkles on ring band
        sparkles = [
            (cx + 8, cy - 2),
            (cx - 8, cy + 2),
            (cx + 6, cy + 4)
        ]
        for sx, sy in sparkles:
            pygame.draw.rect(screen, WHITE, pygame.Rect(sx, sy, 2, 2))
            pygame.draw.rect(screen, (200, 200, 255), pygame.Rect(sx+1, sy+1, 1, 1))
