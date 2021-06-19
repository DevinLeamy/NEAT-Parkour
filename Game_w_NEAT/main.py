# Teaching Parkour... The Darwin Way
import pygame 
from game import Game
from config import *

# Pygame init
pygame.init()
pygame.display.init()
pygame.display.flip()
pygame.display.set_caption("Teaching Parkour... The Darwin Way")
SCN = pygame.display.set_mode((W, H)) # Screen
CLK = pygame.time.Clock() # Clock

# Initialize game
GAME = Game(SCN, CLK)

# Run
GAME.run_game()
GAME.run_highlights()