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

    # Display highlights
    self.highlights = False

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
    # self.update_node_display()

  # Show generation highlights
  def show_highlights(self):
    self.highlights = True
    # Reset for highlights 
    self.population.reset_generation()
    self.reset_score()
    self.sprites = pygame.sprite.Group
    self.game_map = Map()
    self.sprites = pygame.sprite.Group()
    self.sprites.add(self.population.get_highlight().player)
    self.done = False
    Block.reset_shift()

  # Display score, generation, population size, and best-agent fitness  
  def update_main_display(self, display_highlights=False, display_score=True, display_generation=True, display_best_fitness=True, display_batch=True, display_population=True):
    # Display data
    score = self.get_score()
    generation = self.population.generation
    best_fitness = self.population.get_best_fitness()
    population_sz = self.population.get_population_size()
    # +1 because batch numbers of 0 indexed
    batch = self.population.current_batch + 1
    batches = len(self.population.batches)

    # Display strings
    display_str = []
    if display_highlights:
      display_str.append("Highlights!")
    if display_score:
      display_str.append(self.score_str(score)) 
    if display_generation:
      display_str.append(self.generation_str(generation))
    if display_population:
      display_str.append(self.population_str(population_sz))
    if display_best_fitness:
      display_str.append(self.fitness_str(best_fitness)) 
    if display_batch:
      display_str.append(self.batch_str(batch, batches))

    # Create and display 
    OFFSET = 10 # Left and top margin
    for idx, line in enumerate(display_str):
      display = self.font.render(line, True, Color.BLACK)
      display_rect = display.get_rect()
      display_rect.topleft = (OFFSET, OFFSET + idx * 30)

      # Display
      SCN.blit(display, display_rect)
  
  # Input display
  def update_node_display(self):
    font = pygame.font.SysFont("couriernewttf", 16)
    # Display strings
    display_str = [
      f"Inputs ({INPUT_NODES}):",
      "- Head height",
      "- Distance to head-height block",
      "- Distance to head-height - 1 block",
      "- Type of head-height block",
      "- Type of head-height - 1 block",
      "- Game speed",
      f"Outputs ({OUTPUT_NODES}):",
      "- Run",
      "- Jump",
      "- Slide",
      "- Attack"
    ]

     # Create and display 
    OFFSET_LEFT = 710 
    OFFSET_TOP = 525  

    for idx, line in enumerate(display_str):
      display = font.render(line, True, Color.BLACK)
      display_rect = display.get_rect()
      display_rect.topleft = (OFFSET_LEFT, OFFSET_TOP + idx * 20) 

      # Display
      SCN.blit(display, display_rect)
  
  # Display species information
  def update_species_display(self):
    font = pygame.font.SysFont("couriernewttf", 15)
    if len(self.population.species) == 0:
      return 
    OFFSET_LEFT = 10
    OFFSET_TOP = 525

    # Display strings
    display_str = ["Species (%d):" % (len(self.population.species))]
    for species in self.population.species:
      line = "- Members: %d, Best fitness: %d, Average fitness: %d" % (len(species.members), species.best_fitness, species.average_fitness) 
      display_str.append(line)

    for idx, line in enumerate(display_str):
      display = font.render(line, True, Color.BLACK)
      display_rect = display.get_rect()
      display_rect.topleft = (OFFSET_LEFT, OFFSET_TOP + idx * 20) 

      # Display
      SCN.blit(display, display_rect)
  
  # Update highlights display
  def update_highlights(self):
    # Update current highlight
    reset = self.population.update_highlight(self.game_map.grid, self.get_score())

    if self.population.highlights_done():
      self.game_over()
      return 

    if reset: 
      # Reset for next highlight 
      self.reset_score()
      self.sprites = pygame.sprite.Group
      self.game_map = Map()
      self.sprites = pygame.sprite.Group()
      self.sprites.add(self.population.get_highlight().player)
      Block.reset_shift()
    
    self.draw()

    # Update displays
    self.display_genome(self.population.get_highlight().genome)
    self.update_main_display(display_highlights=True, display_best_fitness=False, display_population=False, display_batch=False)
    # self.update_node_display()

    self.game_map.update()
    self.update_game_speed()
  
  # Update game speed 
  def update_game_speed(self):
    if self.updates % UPDATES_PER_INC == 0:
      # Increase speed
      self.population.increase_speed()
      self.game_map.ask_increase = True

  # Updates all game sprites
  def update(self):
    # Increment updates 
    self.updates += 1
  
    if self.highlights:
      self.update_highlights()
      return

    # Update population and map
    self.population.update(self.game_map.grid, self.get_score())
    self.game_map.update()
    self.update_game_speed()

    self.draw()

    # Update displays
    self.update_main_display() 
    self.update_species_display()
    # self.update_node_display()
    self.display_genome()

    # Update game status, game continues so long as the population has active members
    if not self.population.has_active():
      self.game_over()
  
  # Reset for the next generation
  def next_generation(self):
    # Set defaults
    self.reset_score()
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
    self.reset_score()
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
  
  # Reset game score
  def reset_score(self):
    self.updates = 0
  
  # End game
  def game_over(self):
    self.done = True
  
  # Display the genome of the current best agent
  def display_genome(self, genome=None):
    genome = self.population.best_agent.genome if genome == None else genome
    # Create network 
    network = Feedforward(genome.nodes)
    layers = network.layers

    GAP = 50 # Distance between nodes
    RAD = 11 # Radius of nodes
    LEFT_OFFSET = 800 # Right offset 
    TOP_OFFSET = 50 # Top offset 
    GENOME_WIDTH = 225 # Width of genome display 
    LINE_WIDTH = 5 # Max line width
    GET_LINE_WIDTH = lambda weight: max(1, int(abs(LINE_WIDTH * weight))) # Line width
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

    node_positions = dict() # Store position of node centers, by node
    outputs = []  # Output nodes

    # Display edge between two nodes
    def display_edge(edge):
      edge_color = COLORS["active_edge"] if edge.active else COLORS["disabled_edge"]
      line_width = GET_LINE_WIDTH(edge.weight) 
      try:
        pygame.draw.line(SCN, edge_color, node_positions[edge.in_node._id], node_positions[edge.out_node._id], line_width) 
      except Exception as err:
        print(edge.in_node._id)
        print(edge.out_node._id)
        print(str(err))

    # Input nodes
    for i, node in enumerate(layers[0]): 
      x_pos = LEFT_OFFSET + (i % 2) * NUDGE 
      y_pos = TOP_OFFSET + (MAX_LAYER - len(layers[0])) // 2 * GAP + i * GAP
      position = (x_pos, y_pos)
      node_positions[node._id] = position

    # Hidden nodes
    for i in range(1, len(layers)):
      layer = layers[i]
      for j, node in enumerate(layer):
        if node.is_output():
          outputs.append(node)
          continue
        x_pos = LEFT_OFFSET + i * GAP + (j % 2) * NUDGE 
        y_pos = TOP_OFFSET + (MAX_LAYER - len(layer)) // 2 * GAP + j * GAP
        position = (x_pos, y_pos) 
        node_positions[node._id] = position 
        # Display edges
        for edge in node.in_bound_edges:
          display_edge(edge)

    # Output nodes
    for i, node in enumerate(outputs):
      x_pos = LEFT_OFFSET + GENOME_WIDTH + (i % 2) * NUDGE
      y_pos = TOP_OFFSET + (MAX_LAYER - len(outputs)) // 2 * GAP + i * GAP
      position = (x_pos, y_pos)
      node_positions[node._id] = position
      # Display edges
      for edge in node.in_bound_edges:
        display_edge(edge)

    # Draw nodes - done after so they cover the lines
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
          # Stop game and play highlight reel
          game.show_highlights()
          break
      # Displaying
      SCN.blit(LOAD.load_image("Tiles/Background.png"), (0, 0))
      game.update() 
      if game.done: # Game over
        break
      pygame.display.update()
      # Set speed
      CLK.tick(DELAY)
    if game.highlights:
      break
    game.next_batch()
  if game.highlights:
    break
  game.next_generation()
  print("Best fitness: %d" % (game.population.get_best_fitness()))

# Show highlights
if not game.highlights:
  game.show_highlights()
while not game.done:
  # Displaying
  SCN.blit(LOAD.load_image("Tiles/Background.png"), (0, 0))
  game.update() 
  pygame.display.update()
  # Set speed
  CLK.tick(DELAY)

pygame.display.quit()