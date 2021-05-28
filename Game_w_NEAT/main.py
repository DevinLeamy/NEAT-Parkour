# Teaching Parkour... The Darwin Way
import random
import pygame 
from config import *

pygame.init()

pygame.display.init()

# Constants
SCN = pygame.display.set_mode((W, H))
# BATCH = 20
# EPOCH = 100
BATCH = 1
EPOCH = 1

from enums import Color, Move, Ob, State
# from game import Game
# Pygame init
pygame.display.flip()
pygame.display.set_caption("Teaching Parkour... The Darwin Way")

running = True

from agent import Agent 
from game_map import Map


# Game  
class Game:
  def __init__(self):
    # Create sprite group
    self.sprites = pygame.sprite.Group()

    # Add player sprite
    self.PK = Agent()
    self.sprites.add(self.PK)

    # Create map and add block sprites
    self.game_map = Map()

    # Score
    self.updates = 0
    self.score = 0
    self.get_score = lambda updates:updates // 10 

    # Score display
    self.get_score_string = lambda score: "Score: %d" % (score)
    self.score_font = pygame.font.SysFont("couriernewttf", 25)

  # Update score
  def updates_and_display_score(self):
    # Update
    self.updates += 1
    self.score = self.get_score(self.updates)

    # Display
    score_display = self.score_font.render(self.get_score_string(self.score), True, Color.BLACK)
    score_rect = score_display.get_rect()
    score_rect.topleft = (0, 0)
    SCN.blit(score_display, score_rect)
  
  # Updates all game sprites
  def update(self):
    # Update player and map
    state = self.PK.update(self.game_map.grid)
    self.game_map.update()

    self.updates_and_display_score()

    # Increase speed
    if self.updates % 750 == 0:
      self.PK.increase_speed()
      self.game_map.ask_increase = True

    self.draw()

    if state == State.OVER:
      return self.score
    return State.RUNNING

  # Draw game state
  def draw(self):
    # Add block sprites 
    map_blocks = self.game_map.get_sprites()
    for block in map_blocks:
      self.sprites.add(block)

    # Draw sprites to screen
    self.sprites.draw(SCN)

CLK = pygame.time.Clock()

# Game loop
for batch in range(BATCH):
  for epoch in range(EPOCH):
    # Initialize game
    game = Game()
    state = State.RUNNING 

    agent_score = 0
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_w:
            game.PK.move(Move.JMP)
          elif event.key == pygame.K_s:
            game.PK.move(Move.SLD)
          elif event.key == pygame.K_SPACE:
            game.PK.move(Move.ATK, game.game_map.grid)

      # Displaying
      SCN.blit(LOAD.load_image("Tiles/Background.png"), (0, 0))
      state = game.update() 
      if not state == State.RUNNING: 
        agent_score = state
        print("You achieved a score of: %d" % (agent_score))
        break
      pygame.display.update()
    
      # Set speed
      CLK.tick(DELAY)
# pygame.display.quit()