from config import *
from enums import Level, Tile

# Map
class Map:
  def __init__(self):
    # Set buffer
    self.BUFFER = 5
    self.BUFFER_SZ = self.BUFFER * BLOCK_SZ
    self.current_buffer = self.BUFFER_SZ
    self.total_shift = 0

    self.cols = BLOCKS + self.BUFFER
    self.rows = BLOCKS
    self.grid = []
    self.initialize_map()

  # Create initial map config - Requires refactor
  def initialize_map(self):
    # Fill with Air
    self.grid = [[Air(i, j) for j in range(self.cols)] for i in range(self.rows)]

    # Add obstacle blocks
    for i in range(self.cols):
      if not i % 5 == 0:
        continue
      ob = random.choice(OBSTACLES)
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
    self.current_buffer -= Block.SHIFT_SZ
    self.total_shift += Block.SHIFT_SZ
    for i in range(self.rows):
      for j in range(len(self.grid[i])):
        self.grid[i][j].shift()

    if self.total_shift == BLOCK_SZ:
      # Reset total shift
      self.total_shift = 0
      for i in range(self.rows):
        for j in range(len(self.grid[0])):
          self.grid[i][j].decrease_col()  

    if self.current_buffer == 0:
      # Might break something - be weary
      for i in range(self.rows):
        self.grid[i] = self.grid[i][5:]
      self.generate_buffer()

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
        pos = random.choice(range(2, self.BUFFER))
        ob = random.choice(OBSTACLES) 
        
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

