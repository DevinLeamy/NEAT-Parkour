# Teaching Parkour... The Darwin Way
import pygame 
from config import *

pygame.init()
pygame.display.init()

# Constants
SCN = pygame.display.set_mode((W, H))

from enums import Color, Move, Ob, State

# Pygame init
pygame.display.flip()
pygame.display.set_caption("Teaching Parkour... The Darwin Way")

running = True

from player import Player 
from game_map import Map
from population import Population
from blocks import Block
from feedforward import Feedforward

# Game  
class Game:
  def __init__(self):
    # State of game
    self.done = False

    # Create sprite group
    self.sprites = pygame.sprite.Group()

    self.population = Population(size=POPULATION) 

    # Add batch to sprite group 
    for agent in self.population.get_batch():
      self.sprites.add(agent.player)

    # Create map and add block sprites
    self.game_map = Map()

    # Score
    self.updates = 0
    self.get_score = lambda : self.updates // 10 

    # Display strings 
    self.score_str = lambda score: "Score: %d" % (score)
    self.generation_str = lambda generation: "Generation: %d" % (generation)
    self.fitness_str = lambda fitness: "Best fitness: %d" % (fitness)
    self.population_str = lambda population: "Population size: %d" % (population)
    self.batch_str = lambda batch, batches: "Batch: %d of %d" % (batch, batches)

    # Font
    self.font = pygame.font.SysFont("couriernewttf", 17)

    # Display best agent genome
    self.display_genome()

  # Display score, generation, population size, and best-agent fitness  
  def update_main_display(self):
    # Display data
    score = self.get_score()
    generation = self.population.generation
    best_fitness = self.population.get_best_fitness()
    population_sz = self.population.get_population_size()
    # +1 because batch numbers of 0 indexed
    batch = self.population.current_batch + 1
    batches = len(self.population.batches)


    # Display strings
    display_str = [
      self.score_str(score), 
      self.generation_str(generation), 
      self.population_str(population_sz), 
      self.fitness_str(best_fitness), 
      self.batch_str(batch, batches)
    ]

    # Create and display 
    OFFSET = 10 # Left and top margin
    for idx, line in enumerate(display_str):
      display = self.font.render(line, True, Color.BLACK)
      display_rect = display.get_rect()
      display_rect.topleft = (OFFSET, OFFSET + idx * 30)

      # Display
      SCN.blit(display, display_rect)
  
  # Display species information
  def update_species_display(self):
    OFFSET_LEFT = 10
    OFFSET_TOP = 525

    # Display strings
    display_str = ["Species (%d):" % (len(self.population.species))]
    for species in self.population.species:
      line = "- Members: %d, Best fitness: %d, Average fitness: %d" % (len(species.members), species.best_fitness, species.average_fitness) 
      display_str.append(line)

    for idx, line in enumerate(display_str):
      display = self.font.render(line, True, Color.BLACK)
      display_rect = display.get_rect()
      display_rect.topleft = (OFFSET_LEFT, OFFSET_TOP + idx * 30) 

      # Display
      SCN.blit(display, display_rect)

  # Updates all game sprites
  def update(self):
    # Increment updates 
    self.updates += 1

    # Update population and map
    self.population.update(self.game_map.grid, self.get_score())
    self.game_map.update()

    # Increase speed 
    if self.updates % UPDATES_PER_INC == 0:
      self.population.increase_speed()
      self.game_map.ask_increase = True

    self.draw()

    # Update displays
    self.update_main_display() 
    self.update_species_display()
    self.display_genome()

    # Update game status, game continues so long as the population has active members
    self.done = not self.population.has_active()
  
  # Reset for the next generation
  def next_generation(self):
    # Set defaults
    self.updates = 0
    self.game_map = Map()
    self.sprites = pygame.sprite.Group()
    Block.reset_shift()

    # Update population 
    self.population.natural_selection()

    # Add players to sprite group
    for agent in self.population.get_batch():
      # Note: Agent is the NEAT class that wraps Player, the sprite that plays the game
      self.sprites.add(agent.player)
  
  # Reset of the next batch
  def next_batch(self):
    self.population.update_batch()

    # Set defaults
    self.done = False
    self.updates = 0
    self.game_map = Map()
    self.sprites = pygame.sprite.Group()
    Block.reset_shift()

    # Add batch to sprite group 
    for agent in self.population.get_batch():
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
  
  # Display the genome of the current best agent
  def display_genome(self, genome=None, display=True):
    genome = self.population.best_agent.genome if genome == None else genome
    # Create network 
    network = Feedforward(genome.nodes)
    layers = network.layers

    GAP = 50 # Distance between nodes
    RAD = 11 # Radius of nodes
    RIGHT_OFFSET = 800 # Right offset 
    TOP_OFFSET = 50 # Top offset 
    WIDTH = 5 # Line width
    NUDGE = 10 # Horizontal nudge
    MAX_LAYER = 7 # Max nodes we can expect in one layer

    # Colors
    COLORS = {
      "active_edge": (0, 200, 0),
      "disabled_edge": (200, 0, 0),
      "node": (50, 50, 50),
      "input_node": (0, 0, 150),
      "output_node": (150, 0, 0)
    }

    # Store position of node centers, by node
    node_positions = dict()
    for i, layer in enumerate(layers):
      for j, node in enumerate(layer):
        position = (RIGHT_OFFSET + i * GAP + j * NUDGE, j * GAP + TOP_OFFSET +(MAX_LAYER - len(layer))//2 * GAP)
        # Store position
        node_positions[node._id] = position 
        for edge in node.in_bound_edges:
          edge_color = COLORS["active_edge"] if edge.active else COLORS["disabled_edge"]
          if not display:
            continue
          # Line width depends on edge width - width increased with magnitude 
          pygame.draw.line(SCN, edge_color, 
                          node_positions[edge.in_node._id], 
                          node_positions[edge.out_node._id], max(1, int(abs(WIDTH * edge.weight))))

    # Draw nodes - done after so they cover the lines
    if not display:
      return
    for node_id, position in node_positions.items():
      color = COLORS["node"]
      node = genome.get_node(node_id)
      if node.is_input():
        color = COLORS["input_node"]
      if node.is_output():
        color = COLORS["output_node"]
      pygame.draw.circle(SCN, color, position, RAD)

CLK = pygame.time.Clock()
# Initialize game
game = Game()
state = State.RUNNING 

# 100 = number of generations
for gen in range(GENERATIONS):
  for batch in range(len(game.population.batches)):
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
    game.next_batch()
  game.next_generation()
  print("Best fitness: %d" % (game.population.get_best_fitness()))

pygame.display.quit()