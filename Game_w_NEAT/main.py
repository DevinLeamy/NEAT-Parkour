# Teaching Parkour... The Darwin Way
import pygame 
from game import Game
from config import *

pygame.init()
pygame.display.init()

# Constants
SCN = pygame.display.set_mode((W, H))

# Pygame init
pygame.display.flip()
pygame.display.set_caption("Teaching Parkour... The Darwin Way")

running = True

CLK = pygame.time.Clock()
# Initialize game
game = Game(SCN)

# Launch game
def run():
  for gen in range(GENERATIONS):
    for batch in range(len(game.population.batches)):
      # Game loop
      while True:
        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            # Stop game (starting highlights) 
            return 
        game.update() # Update display
        if game.done: # Game over
          break
        pygame.display.update()
        CLK.tick(DELAY) # Set speed
      game.next_batch()
    game.next_generation()
    print("Best fitness: %d" % (game.population.get_best_fitness())) 

# Show highlights
def show_highlights():
  game.show_highlights()
  while not game.done:
    game.update() # Update display
    pygame.display.update()
    CLK.tick(DELAY) # Set speed

run()
show_highlights()