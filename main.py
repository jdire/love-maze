#!/usr/bin/env python3
"""
Love Maze - An 8-bit style maze game themed on love
Navigate through mazes to reach the heart endzone and progress to next level
"""

import pygame
import sys
import asyncio
from src.game import Game

async def main():
    """Main entry point for Love Maze game"""
    print("Initializing pygame...")
    pygame.init()
    
    print("Creating game instance...")
    # Create game instance
    game = Game()
    
    print("Starting game loop...")
    # Run game loop with async support for web
    await game.run()
    
    # Cleanup
    pygame.quit()
    sys.exit()

# Start the game
asyncio.run(main())
