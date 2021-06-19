from blocks import Block, HardBlock, WallBlock, Air
import random
from enums import Level, Tile, Ob
from config import *


# Map
class Map:
  def __init__(self):
    # Reseed random - makes the map predictable
    self.random = random.Random()
    self.random.seed(SEED)

    # Set buffer
    self.BUFFER = 5
    self.BUFFER_SZ = self.BUFFER * BLOCK_SZ
    self.current_buffer = self.BUFFER_SZ
    self.total_shift = 0

    self.cols = BLOCKS + self.BUFFER
    self.rows = BLOCKS
    self.grid = []
    self.initialize_map()

    # Increase at next chance
    self.ask_increase = False 

  # Create initial map config - Requires refactor
  def initialize_map(self):
    # Fill with Air
    self.grid = [[Air(i, j) for j in range(self.cols)] for i in range(self.rows)]

    # Add obstacle blocks
    for i in range(10, self.cols):
      if not i % 5 == 0:
        continue
      ob = self.random.choice(OBSTACLES)
      if ob == Ob.WALL:
        self.grid[Level.GRND - 2][i] = WallBlock(Level.GRND - 2, i)
        self.grid[Level.GRND - 1][i] = WallBlock(Level.GRND - 1, i)
      elif ob == Ob.BHARD:
        self.grid[Level.GRND - 1][i] = HardBlock(Level.GRND - 1, i)
      else:
        self.grid[Level.GRND - 2][i] = HardBlock(Level.GRND - 2, i)
 
    # Add ground blocks
    for i in range(self.cols):
      self.grid[Level.GRND][i] = Block(Level.GRND, i, Tile.GRASS)

    for i in range(Level.GRND + 1, self.rows):
      for j in range(self.cols):
        self.grid[i][j] = Block(i, j, Tile.DIRT)
 
  # Update blocks
  def update(self):
    # SHIFT_SZ might have changed
    self.current_buffer -= Block.SHIFT_SZ
    self.total_shift += Block.SHIFT_SZ
    for i in range(self.rows):
      for j in range(len(self.grid[i])):
        self.grid[i][j].shift()

    if self.total_shift == BLOCK_SZ:
      # Reset total shift
      self.total_shift = 0
      # Reset block shifts and remove left-most row
      for i in range(self.rows):
        # Col of first element should be 0
        self.grid[i].pop(0)
      for i in range(self.rows):
        for j in range(len(self.grid[0])):
          self.grid[i][j].decrease_col()  

    if self.current_buffer == 0:
      if self.ask_increase:
        self.ask_increase = False
        self.increase_speed()
      self.generate_buffer()

  # Increase speed
  def increase_speed(self):
    Block.increase_shift()

  # Returns block sprites
  def get_sprites(self):
    sprites = list()
    for row in self.grid:
      for block in row:
        # Check if block is empty
        if isinstance(block, Air):
          continue
        sprites.append(block)
    return sprites
  
  # Generate new buffer - Requires refactor
  def generate_buffer(self):
    new_cols = self.BUFFER

    for i in range(self.rows):
      self.grid[i].extend([Air(i, BLOCKS + j) for j in range(new_cols)])

    for i in range(self.rows):
      if i < Level.GRND - 2:
        continue
      elif i == Level.GRND - 2:
        # Make the number of obstacles a choice?
        pos = self.random.choice(range(3, self.BUFFER))
        ob = self.random.choice(OBSTACLES) 
        
        # Add row buffers
        for j in range(new_cols):
          if not j == pos:
            continue

          if ob == Ob.WALL:
            self.grid[i][BLOCKS + j] = WallBlock(i, BLOCKS + j)
            self.grid[i + 1][BLOCKS + j] = WallBlock(i + 1, BLOCKS + j)
          elif ob == Ob.BHARD:
            self.grid[i + 1][BLOCKS + j] = HardBlock(i + 1, BLOCKS + j)
          else:
            self.grid[i][BLOCKS + j] = HardBlock(i, BLOCKS + j)
      elif i == Level.GRND - 1:
        continue
      else:
        for j in range(new_cols):
          if i == Level.GRND:
            self.grid[i][BLOCKS + j] = Block(i, BLOCKS + j, Tile.GRASS) 
          else:
            self.grid[i][BLOCKS + j] = Block(i, BLOCKS + j, Tile.DIRT)
   
    # Reset buffer
    self.current_buffer = self.BUFFER_SZ

