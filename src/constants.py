"""Game constants and configuration"""

# Display settings (optimized for mobile portrait 9:16)
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 32  # Optimized for mobile screens

# Colors (16-bit palette with more shades)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
RED = (220, 20, 60)
DARK_RED = (139, 0, 0)
LIGHT_PINK = (255, 182, 193)
PURPLE = (138, 43, 226)
DARK_PURPLE = (75, 0, 130)
GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
DEEP_PINK = (255, 20, 147)
HOT_PINK = (255, 69, 180)

# Game settings
PLAYER_SPEED = 4
INITIAL_LIVES = 3

# Maze settings
MAZE_OFFSET_X = 100
MAZE_OFFSET_Y = 50

# Tile types
WALL = 1
PATH = 0
START = 2
END = 3
HEART = 4
