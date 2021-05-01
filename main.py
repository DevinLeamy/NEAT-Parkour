# Teaching Parkour... The Darwin Way
import random
import pygame 
from config import *

pygame.init()

pygame.display.init()

# Constants
SCN = pygame.display.set_mode((W, H))

from enums import Color, Move, Ob
# from game import Game
# Pygame init
pygame.display.flip()
pygame.display.set_caption("Teaching Parkour... The Darwin Way")

running = True

from player import ParkourKing
from game_map import Map


# Game  
class Game:
  def __init__(self):
    # Create sprite group
    self.sprites = pygame.sprite.Group()

    # Add player sprite
    self.PK = ParkourKing()
    self.sprites.add(self.PK)

    # Create map and add block sprites
    self.game_map = Map()
  
  # Updates all game sprites
  def update(self):
    # Update player and map
    self.PK.update(self.game_map.grid)
    self.game_map.update()

    self.draw()

  # Draw game state
  def draw(self):
    # Add block sprites 
    map_blocks = self.game_map.get_sprites()
    for block in map_blocks:
      self.sprites.add(block)

    # Draw sprites to screen
    self.sprites.draw(SCN)

# Initialize game
game = Game()

CLK = pygame.time.Clock()
# Game loop
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w:
        game.PK.move(Move.JMP)
      elif event.key == pygame.K_s:
        game.PK.move(Move.SLD)
      elif event.key == pygame.K_SPACE:
        game.PK.move(Move.ATK)

  # Displaying
  SCN.blit(LOAD.load_image("TileSet2/Background/Background.png"), (0, 0))
  game.update()
  pygame.display.update()
  pygame.display.flip()
  
  # Set speed
  CLK.tick(DELAY)
  # pygame.time.delay(DELAY)
pygame.display.quit()