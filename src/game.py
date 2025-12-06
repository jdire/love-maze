"""Main game class"""

import pygame
import asyncio
from src.constants import *
from src.maze import Maze
from src.player import Player
from src.ui import UI
from src.quiz import Quiz

class Game:
    """Main game controller"""
    
    def __init__(self):
        """Initialize game"""
        print("Setting up display...")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Love Maze ♥")
        self.clock = pygame.time.Clock()
        
        print("Initializing game state...")
        # Game state
        self.running = True
        self.level = 1
        self.score = 0
        self.lives = INITIAL_LIVES
        self.state = "playing"  # playing, quiz, game_over
        
        # Touch/swipe controls
        self.touch_start = None
        self.swipe_threshold = 50  # minimum distance for swipe
        self.tap_threshold = 10  # maximum movement for tap vs swipe
        self.tap_time_threshold = 0.3  # maximum time for tap (seconds)
        self.touch_start_time = 0
        
        # Pathfinding for tap movement
        self.target_path = []
        self.move_speed = 150  # pixels per second for smooth movement
        
        print("Creating maze and player...")
        # Game objects
        self.maze = Maze(self.level)
        self.player = Player(self.maze.start_pos, self.maze)
        self.ui = UI()
        self.quiz = Quiz()
        
        print("Game initialized successfully!")
        
        # Load and play background music
        try:
            import sys
            if sys.platform != "emscripten":
                # Only load music on desktop, not web
                pygame.mixer.music.load('assets/music/peppy_love_theme.wav')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)  # Loop forever
        except Exception as e:
            print(f"Could not load music: {e}")
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.state == "playing":
                    self.reset_level()
            # Touch/Mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.touch_start = event.pos
                self.touch_start_time = pygame.time.get_ticks() / 1000.0
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.touch_start:
                    touch_end = event.pos
                    touch_duration = (pygame.time.get_ticks() / 1000.0) - self.touch_start_time
                    distance = ((touch_end[0] - self.touch_start[0])**2 + 
                               (touch_end[1] - self.touch_start[1])**2)**0.5
                    
                    # Handle based on game state
                    if self.state == "quiz":
                        # Quiz screen - check for answer/continue click
                        if self.quiz.handle_click(touch_end):
                            if self.quiz.answered:
                                # Award points for correct answer
                                if self.quiz.correct:
                                    self.score += 50
                                # Move to next level
                                self.next_level()
                                self.state = "playing"
                    elif self.state == "playing":
                        # Game screen - handle tap/swipe
                        if distance < self.tap_threshold and touch_duration < self.tap_time_threshold:
                            self.handle_tap(touch_end)
                        else:
                            self.handle_swipe(self.touch_start, touch_end)
                    
                    self.touch_start = None
    
    def handle_swipe(self, start_pos, end_pos):
        """Handle swipe gesture for touch controls"""
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Check if swipe is significant enough
        if abs(dx) < self.swipe_threshold and abs(dy) < self.swipe_threshold:
            return
        
        # Determine swipe direction
        if abs(dx) > abs(dy):
            # Horizontal swipe
            if dx > 0:
                # Swipe right
                self.player.move(PLAYER_SPEED * 3, 0, self.maze)
            else:
                # Swipe left
                self.player.move(-PLAYER_SPEED * 3, 0, self.maze)
        else:
            # Vertical swipe
            if dy > 0:
                # Swipe down
                self.player.move(0, PLAYER_SPEED * 3, self.maze)
            else:
                # Swipe up
                self.player.move(0, -PLAYER_SPEED * 3, self.maze)
        
        # Check for hearts and end after swipe movement
        hearts_collected = self.maze.check_heart_collision(self.player.rect)
        if hearts_collected:
            self.score += hearts_collected * 10
    def handle_tap(self, tap_pos):
        """Handle tap/click to move ring to location with line of sight"""
        # Convert screen position to grid position
        grid_x = (tap_pos[0] - self.maze.offset_x) // TILE_SIZE
        grid_y = (tap_pos[1] - self.maze.offset_y) // TILE_SIZE
        
        # Get player's current grid position
        player_grid_x = (self.player.rect.centerx - self.maze.offset_x) // TILE_SIZE
        player_grid_y = (self.player.rect.centery - self.maze.offset_y) // TILE_SIZE
        
        # Check if tap is within maze bounds
        if not (0 <= grid_x < self.maze.width and 0 <= grid_y < self.maze.height):
            return
        
        # Check if target tile is walkable
        from src.constants import WALL
        if self.maze.grid[grid_y][grid_x] == WALL:
            return
        
        # Check line of sight and get path
        path = self.get_line_path(player_grid_x, player_grid_y, grid_x, grid_y)
        if path:
            # Convert grid path to pixel coordinates
            self.target_path = []
            for px, py in path:
                pixel_x = px * TILE_SIZE + self.maze.offset_x + TILE_SIZE // 2
                pixel_y = py * TILE_SIZE + self.maze.offset_y + TILE_SIZE // 2
                self.target_path.append((pixel_x, pixel_y))
    
    def get_line_path(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
    def get_line_path(self, x0, y0, x1, y1):
        """Get path along line of sight using Bresenham's line algorithm"""
        from src.constants import WALL
        path = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        x_inc = 1 if x1 > x0 else -1
        y_inc = 1 if y1 > y0 else -1
        
        if dx > dy:
            error = dx / 2
            while x != x1:
                # Check if current tile is a wall
                if 0 <= y < self.maze.height and 0 <= x < self.maze.width:
                    tile = self.maze.grid[y][x]
                    if tile == WALL:
                        return None  # No line of sight
                    path.append((x, y))
                
                error -= dy
                if error < 0:
                    y += y_inc
                    error += dx
                x += x_inc
        else:
            error = dy / 2
            while y != y1:
                # Check if current tile is a wall
                if 0 <= y < self.maze.height and 0 <= x < self.maze.width:
                    tile = self.maze.grid[y][x]
                    if tile == WALL:
                        return None  # No line of sight
                    path.append((x, y))
                
                error -= dx
                if error < 0:
                    x += x_inc
                    error += dy
                y += y_inc
        
        # Add final position
        path.append((x1, y1))
        return path
    
    def update(self, dt):
        """Update game state"""
        # Handle pathfinding movement if there's a target path
        if self.target_path:
            target = self.target_path[0]
            current_x = self.player.rect.centerx
            current_y = self.player.rect.centery
            
            # Calculate direction to target
            dx = target[0] - current_x
            dy = target[1] - current_y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 3:  # Close enough to target waypoint
                # Move to next waypoint
                self.target_path.pop(0)
                
                # Check for collectibles when reaching waypoint
                hearts_collected = self.maze.check_heart_collision(self.player.rect)
                if hearts_collected:
                    self.score += hearts_collected * 10
                
                if self.maze.check_end_collision(self.player.rect):
                    self.next_level()
                    self.target_path = []
            else:
                # Move towards target
                move_distance = self.move_speed * dt
                if move_distance > distance:
                    move_distance = distance
                
                # Normalize and apply movement
                dx = (dx / distance) * move_distance
                dy = (dy / distance) * move_distance
                
                self.player.rect.centerx += dx
                self.player.rect.centery += dy
        else:
            # Get keyboard input
            keys = pygame.key.get_pressed()
            dx = 0
            dy = 0
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = PLAYER_SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -PLAYER_SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = PLAYER_SPEED
            
            # Update player position
            self.player.move(dx, dy, self.maze)
        
        # Check if player collected hearts (for keyboard movement)
        if not self.target_path:
            hearts_collected = self.maze.check_heart_collision(self.player.rect)
            if hearts_collected:
                self.score += hearts_collected * 10
            
            # Check if player reached endzone
            if self.maze.check_end_collision(self.player.rect):
                # Start quiz before next level
                self.state = "quiz"
                self.quiz.start_quiz()
                self.target_path = []  # Clear movement path
    
    def update(self, dt):
        """Update game state"""
        # Only update game objects when in playing state
        if self.state != "playing":
            return
        
        # Handle pathfinding movement if there's a target path
        if self.target_path:
            target = self.target_path[0]
            current_x = self.player.rect.centerx
            current_y = self.player.rect.centery
            
            # Calculate direction to target
            dx = target[0] - current_x
            dy = target[1] - current_y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 3:  # Close enough to target waypoint
                # Move to next waypoint
                self.target_path.pop(0)
                
                # Check for collectibles when reaching waypoint
                hearts_collected = self.maze.check_heart_collision(self.player.rect)
                if hearts_collected:
                    self.score += hearts_collected * 10
                
                if self.maze.check_end_collision(self.player.rect):
                    self.next_level()
                    self.target_path = []
            else:
                # Move towards target
                move_distance = self.move_speed * dt
                if move_distance > distance:
                    move_distance = distance
                
                # Normalize and apply movement
                dx = (dx / distance) * move_distance
                dy = (dy / distance) * move_distance
                
                self.player.rect.centerx += dx
                self.player.rect.centery += dy
        else:
            # Get keyboard input
            keys = pygame.key.get_pressed()
            dx = 0
            dy = 0
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = PLAYER_SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -PLAYER_SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = PLAYER_SPEED
            
            # Update player position
            self.player.move(dx, dy, self.maze)
        
        # Check if player collected hearts (for keyboard movement)
        if not self.target_path:
            hearts_collected = self.maze.check_heart_collision(self.player.rect)
            if hearts_collected:
                self.score += hearts_collected * 10
            
            # Check if player reached endzone
            if self.maze.check_end_collision(self.player.rect):
                # Start quiz before next level
                self.state = "quiz"
                self.quiz.start_quiz()
    
    def next_level(self):
        """Progress to next level (called after quiz)"""
        self.level += 1
        self.score += 50  # Bonus for completing level
        self.maze = Maze(self.level)
        self.player = Player(self.maze.start_pos, self.maze)
        self.target_path = []  # Clear any movement path
    
    def reset_level(self):
        """Reset current level"""
        self.maze = Maze(self.level)
        self.player = Player(self.maze.start_pos, self.maze)
    
    def render(self):
        """Render game"""
        # Clear screen with love theme background
        self.screen.fill(LIGHT_PINK)
        
        if self.state == "quiz":
            # Draw quiz screen
            self.quiz.draw(self.screen)
        else:
            # Draw game screen
            # Draw maze
            self.maze.draw(self.screen)
            
            # Draw player
            self.player.draw(self.screen)
            
            # Draw UI
            self.ui.draw(self.screen, self.level, self.score, self.lives)
        
        # Update display
        pygame.display.flip()
    
    async def run(self):
        """Main game loop with async support for web"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
            
            # Yield control for web platform
            await asyncio.sleep(0)
