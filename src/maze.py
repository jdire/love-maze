"""Maze generation and rendering"""

import pygame
import random
from src.constants import *

class Maze:
    """Maze generator and manager"""
    
    def __init__(self, level):
        """Initialize maze for given level"""
        self.level = level
        # Limit maze size to fit on screen (max 19x15)
        self.width = min(15 + level, 19)
        self.height = min(13 + level, 15)
        
        # Generate maze
        self.grid = self.generate_maze()
        
        # Set start and end positions
        self.start_pos = (1, 1)
        self.end_pos = (self.width - 2, self.height - 2)
        
        self.grid[self.start_pos[1]][self.start_pos[0]] = START
        self.grid[self.end_pos[1]][self.end_pos[0]] = END
        
        # Calculate offset to center maze on screen
        maze_pixel_width = self.width * TILE_SIZE
        maze_pixel_height = self.height * TILE_SIZE
        self.offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        self.offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2 + 30
        
        # Place collectible hearts
        self.hearts = self.place_hearts()
    
    def generate_maze(self):
        """Generate maze using recursive backtracking"""
        # Initialize grid with all walls
        grid = [[WALL for _ in range(self.width)] for _ in range(self.height)]
        
        # Recursive backtracking maze generation
        def carve_path(x, y):
            grid[y][x] = PATH
            
            # Randomize directions
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if grid[ny][nx] == WALL:
                        # Carve wall between cells
                        grid[y + dy // 2][x + dx // 2] = PATH
                        carve_path(nx, ny)
        
        # Start carving from (1, 1)
        carve_path(1, 1)
        
        # Ensure end position is carved (make it reachable)
        end_x = self.width - 2
        end_y = self.height - 2
        grid[end_y][end_x] = PATH
        
        # Carve a path to the end if it's isolated
        if end_x > 1:
            grid[end_y][end_x - 1] = PATH
        if end_y > 1:
            grid[end_y - 1][end_x] = PATH
        
        return grid
    
    def place_hearts(self):
        """Place collectible hearts in maze"""
        hearts = []
        num_hearts = 3 + self.level
        
        # Find valid positions for hearts
        valid_positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == PATH:
                    pos = (x * TILE_SIZE + self.offset_x, y * TILE_SIZE + self.offset_y)
                    if pos != (self.start_pos[0] * TILE_SIZE + self.offset_x, 
                              self.start_pos[1] * TILE_SIZE + self.offset_y):
                        valid_positions.append(pos)
        
        # Randomly select heart positions
        if len(valid_positions) > num_hearts:
            hearts = random.sample(valid_positions, num_hearts)
        else:
            hearts = valid_positions
        
        return [pygame.Rect(x, y, TILE_SIZE - 4, TILE_SIZE - 4) for x, y in hearts]
    
    def check_heart_collision(self, player_rect):
        """Check if player collects hearts"""
        collected = 0
        remaining_hearts = []
        
        for heart in self.hearts:
            if player_rect.colliderect(heart):
                collected += 1
            else:
                remaining_hearts.append(heart)
        
        self.hearts = remaining_hearts
        return collected
    
    def check_end_collision(self, player_rect):
        """Check if player reached end zone"""
        end_rect = pygame.Rect(
            self.end_pos[0] * TILE_SIZE + self.offset_x,
            self.end_pos[1] * TILE_SIZE + self.offset_y,
            TILE_SIZE, TILE_SIZE
        )
        return player_rect.colliderect(end_rect)
    
    def is_wall(self, x, y):
        """Check if position is a wall"""
        grid_x = (x - self.offset_x) // TILE_SIZE
        grid_y = (y - self.offset_y) // TILE_SIZE
        
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            return self.grid[grid_y][grid_x] == WALL
        return True
    
    def draw(self, screen):
        """Draw the maze"""
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                rect = pygame.Rect(
                    x * TILE_SIZE + self.offset_x,
                    y * TILE_SIZE + self.offset_y,
                    TILE_SIZE, TILE_SIZE
                )
                
                # Draw based on tile type
                if tile == WALL:
                    pygame.draw.rect(screen, PURPLE, rect)
                    pygame.draw.rect(screen, DARK_GRAY, rect, 2)
                elif tile == PATH:
                    pygame.draw.rect(screen, WHITE, rect)
                elif tile == START:
                    pygame.draw.rect(screen, PINK, rect)
                    # Draw small heart
                    self.draw_pixel_heart(screen, rect.centerx, rect.centery, 8, RED)
                elif tile == END:
                    pygame.draw.rect(screen, GOLD, rect)
                    # Draw big heart
                    self.draw_pixel_heart(screen, rect.centerx, rect.centery, 12, RED)
        
        # Draw collectible hearts
        for heart in self.hearts:
            self.draw_pixel_heart(screen, heart.centerx, heart.centery, 10, PINK)
    
    def draw_pixel_heart(self, screen, cx, cy, size, color):
        """Draw a pixelated 8-bit heart"""
        pixel = size // 4
        
        # Simple 8-bit heart pattern
        heart_pattern = [
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        
        start_x = cx - (4 * pixel)
        start_y = cy - (3 * pixel)
        
        for row_idx, row in enumerate(heart_pattern):
            for col_idx, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        start_x + col_idx * pixel,
                        start_y + row_idx * pixel,
                        pixel, pixel
                    )
                    pygame.draw.rect(screen, color, rect)
