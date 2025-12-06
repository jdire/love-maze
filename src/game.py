"""Main game class"""

import pygame
from src.constants import *
from src.maze import Maze
from src.player import Player
from src.ui import UI

class Game:
    """Main game controller"""
    
    def __init__(self):
        """Initialize game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Love Maze ♥")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.level = 1
        self.score = 0
        self.lives = INITIAL_LIVES
        
        # Touch/swipe controls
        self.touch_start = None
        self.swipe_threshold = 50  # minimum distance for swipe
        
        # Game objects
        self.maze = Maze(self.level)
        self.player = Player(self.maze.start_pos, self.maze)
        self.ui = UI()
        
        # Load and play background music
        try:
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
                elif event.key == pygame.K_r:
                    self.reset_level()
            # Touch/Mouse events for swipe controls
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.touch_start = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.touch_start:
                    self.handle_swipe(self.touch_start, event.pos)
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
        
        if self.maze.check_end_collision(self.player.rect):
            self.next_level()
    
    def update(self, dt):
        """Update game state"""
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
        
        # Check if player collected hearts
        hearts_collected = self.maze.check_heart_collision(self.player.rect)
        if hearts_collected:
            self.score += hearts_collected * 10
        
        # Check if player reached endzone
        if self.maze.check_end_collision(self.player.rect):
            self.next_level()
    
    def next_level(self):
        """Progress to next level"""
        self.level += 1
        self.score += 50  # Bonus for completing level
        self.maze = Maze(self.level)
        self.player = Player(self.maze.start_pos, self.maze)
    
    def reset_level(self):
        """Reset current level"""
        self.maze = Maze(self.level)
        self.player = Player(self.maze.start_pos, self.maze)
    
    def render(self):
        """Render game"""
        # Clear screen with love theme background
        self.screen.fill(LIGHT_PINK)
        
        # Draw maze
        self.maze.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.ui.draw(self.screen, self.level, self.score, self.lives)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
