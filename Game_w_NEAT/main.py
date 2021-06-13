# Teaching Parkour... The Darwin Way
import pygame 
from config import *
import random
random.seed(SEED)

pygame.init()

pygame.display.init()

# Constants
SCN = pygame.display.set_mode((W, H))

from enums import Color, Move, Ob, State
# from game import Game
# Pygame init
pygame.display.flip()
pygame.display.set_caption("Teaching Parkour... The Darwin Way")

running = True

from player import Player 
from game_map import Map
from population import Population


# Game  
class Game:
  def __init__(self):
    # State of game
    self.done = False

    # Create sprite group
    self.sprites = pygame.sprite.Group()

    self.population = Population(size=POPULATION) 

    # Add players to sprite group
    for agent in self.population.members:
      # Note: Agent is the NEAT class that wraps Player, the sprite that plays the game
      self.sprites.add(agent.player)

    # Create map and add block sprites
    self.game_map = Map()

    # Score
    self.updates = 0
    self.get_score = lambda : self.updates // 10 

    # Score display
    self.get_score_string = lambda score: "Score: %d" % (score)
    self.score_font = pygame.font.SysFont("couriernewttf", 25)

  # Update score 
  def display_score(self):
    # Display
    score_display = self.score_font.render(self.get_score_string(self.get_score()), True, Color.BLACK)
    score_rect = score_display.get_rect()
    score_rect.topleft = (0, 0)
    SCN.blit(score_display, score_rect)
  
  # Updates all game sprites
  def update(self):
    # Increment updates 
    self.updates += 1

    # Update population and map
    self.population.update(self.game_map.grid, self.get_score())
    self.game_map.update()

    self.display_score() 

    # Increase speed (Currently off to make the game easier)
    # if self.updates % 750 == 0:
    #   self.PK.increase_speed()
    #   self.game_map.ask_increase = True

    self.draw()

    # Update game status, game continues so long as the population has active members
    self.done = not self.population.has_active()
  
  # Reset for the next generation
  def next_generation(self):
    # Set defaults
    self.updates = 0
    self.game_map = Map()
    self.sprites = pygame.sprite.Group()

    # Update population 
    self.population.natural_selection()

    # Add players to sprite group
    for agent in self.population.members:
      # Note: Agent is the NEAT class that wraps Player, the sprite that plays the game
      self.sprites.add(agent.player)

  # Draw game state
  def draw(self):
    # Remove dead players from sprite group
    for agent in self.population.members:
      player = agent.player
      if not player.alive:
        # Note: Player may have already been removed
        self.sprites.remove(player)

    # Add block sprites 
    map_blocks = self.game_map.get_sprites()
    for block in map_blocks:
      self.sprites.add(block)

    # Draw sprites to screen
    self.sprites.draw(SCN)

CLK = pygame.time.Clock()

# Initialize game
game = Game()
state = State.RUNNING 

# 100 = number of generations
for gen in range(GENERATIONS):
  print("Generation: %d" % gen)
  # Game loop
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    
    # Displaying
    SCN.blit(LOAD.load_image("Tiles/Background.png"), (0, 0))
    game.update() 
    if game.done:
      # Game Over
      break
    pygame.display.update()

    # Set speed
    CLK.tick(DELAY)
  game.next_generation()

pygame.display.quit()