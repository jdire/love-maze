#!/usr/bin/env python3
"""
Love Maze - An 8-bit style maze game themed on love
Navigate through mazes to reach the heart endzone and progress to next level
"""

import pygame
import sys
from src.game import Game

def main():
    """Main entry point for Love Maze game"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Run game loop
    game.run()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
