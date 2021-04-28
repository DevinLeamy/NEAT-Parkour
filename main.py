# Teaching Parkour... The Darwin Way
import random
import pygame 
from image_loader import ImageLoader
pygame.init()

pygame.display.init()

# Constants
W = 1080
H = 800
BLOCKS = 18 
BLOCK_SZ = int(W / BLOCKS)
SCN = pygame.display.set_mode((W, H))
LOAD = ImageLoader()
DELAY = 20

# Pygame init
pygame.display.flip()
pygame.display.set_caption("Teaching Parkour... The Darwin Way")

# Enums
class Level():
  GRND = 8 
  
class Move():
  RUN = 0
  JMP = 1
  SLD = 2
  ATK = 3
  FALL = 4

class Color():
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  GREY = (230, 230, 230)

class Tile():
  GRASS = "TileSet2/Tiles/GrassMid.png"
  DIRT = "TileSet2/Tiles/Dirt.png"
  WALL = "TileSet/Objects/Crate.png"
  HARD = "TileSet/Tiles/stone.png"

class Ob():
  WALL = 0
  THARD = 1
  BHARD = 2

OBSTACLES = [Ob.WALL, Ob.THARD, Ob.BHARD]

# Player 
class ParkourKing(pygame.sprite.Sprite):
  def __init__(self):
    super(ParkourKing, self).__init__()
    self.updates_per_frame = 5.0 # Num of update before frame change
    self.frame_increment = 1 / self.updates_per_frame 

    # Position
    self.LEFT_BUFFER = 3
    self.head_row = Level.GRND - 2 # Two blocks above ground level
        
    # Id and frame count
    self.attacks = {1: 5, 2: 6, 3: 6}
    self.jumps = {1: 4}    
    self.falls = {1: 4}
    self.runs = {1: 6}
    self.slides = {1: 6}
    
    # Generate image path
    self.get_attack_frame = lambda id, frame: "Adventurer/Sprites/adventurer-attack%d-0%d.png" % (id, frame)
    self.get_jump_frame = lambda id, frame: "Adventurer/Sprites/adventurer-jump-0%d.png" % (frame)
    self.get_fall_frame = lambda id, frame: "Adventurer/Sprites/adventurer-smrslt-0%d.png" % (frame)
    self.get_run_frame = lambda id, frame: "Adventurer/Sprites/adventurer-run-0%d.png" % (frame) 
    self.get_slide_frame = lambda id, frame: "Adventurer/Sprites/adventurer-slide-0%d.png" % (frame)
    
    # Set image defaults
    self.image = LOAD.load_image(self.get_run_frame(0, 0), False)
    self.scale_image()
    self.rect = self.image.get_rect()

    # Set position
    self.rect.topleft = [self.LEFT_BUFFER * BLOCK_SZ, self.head_row * BLOCK_SZ]
    
    # On the ground and not in motion
    self.animating = Move.RUN
    
    # Current animation frame
    self.animation_id = random.choice(list(self.runs.keys()))
    self.current_frame = 0.0
    

  # Jumps
  def jump(self):
    # Player is already in motion
    if not (self.animating == Move.RUN):
      return
    
    # Begins jumping
    self.animating = Move.JMP
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.jumps.keys()))

  # Fall
  def fall(self):
    # Already falling 
    if self.animating == Move.FALL:
      return 

    # Begin falling
    self.animating = Move.FALL
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.falls.keys()))

  # Slide
  def slide(self):
    if not (self.animating == Move.RUN):
      return
    
    # Begins sliding
    self.head_row += 1
    self.animating = Move.SLD
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.slides.keys()))

  # Shift player up an down
  def shift(self):
    if not self.animating == Move.JMP and not self.animating == Move.FALL:
      return
    
    total_updates = self.updates_per_frame * self.jumps[self.animation_id]
    dist_shift = BLOCK_SZ / float(total_updates)
    row_shift = 1 / float(total_updates)
    
    if self.animating == Move.JMP:
      # Shift upwards
      self.rect = self.rect.move(0, -1 * dist_shift)
      self.head_row += -1 * row_shift
    else:
      # Shift downwards
      self.rect = self.rect.move(0, dist_shift)
      self.head_row += row_shift
    
  # Attack
  def attack(self):
    if not (self.animating == Move.RUN):
      return
    
    # Begins attacking
    self.animating = Move.ATK
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.attacks.keys()))
  
  # Run
  def run(self):
    if self.animating == Move.RUN:
      return
    
    # Begins running 
    self.animating = Move.RUN
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.runs.keys()))
    
  # Get image
  def get_image_path(self):
    if (self.animating == Move.RUN):
      return self.get_run_frame(self.animation_id, int(self.current_frame))
    elif (self.animating == Move.ATK):
      return self.get_attack_frame(self.animation_id, int(self.current_frame))
    elif (self.animating == Move.JMP):
      return self.get_jump_frame(self.animation_id, int(self.current_frame))
    elif (self.animating == Move.FALL):
      return self.get_fall_frame(self.animation_id, int(self.current_frame))
    elif (self.animating == Move.SLD):
      return self.get_slide_frame(self.animation_id, int(self.current_frame))
    else:
      raise ValueError("Not animating a valid move")
  
  # Scale image
  def scale_image(self):
    width, height = self.image.get_size()
    new_height = int(2 * BLOCK_SZ)
    new_width = int(width * (new_height / height))
    self.image = pygame.transform.scale(self.image, (new_width, new_height))
    
  # Set sprite image
  def set_image(self):
    path = self.get_image_path()
    self.image = LOAD.load_image(path, False)
    self.scale_image()
    
  # Update current frame 
  def update_current_frame(self):
    self.current_frame += self.frame_increment
    
    if (self.animating == Move.RUN):
      self.current_frame %= self.runs[self.animation_id]
    elif (self.animating == Move.JMP):
      self.current_frame %= self.jumps[self.animation_id]
      self.shift()
    elif (self.animating == Move.FALL):
      self.current_frame %= self.falls[self.animation_id]
      self.shift()
    elif (self.animating == Move.SLD):
      self.current_frame %= self.slides[self.animation_id]
    elif (self.animating == Move.ATK):
      self.current_frame %= self.attacks[self.animation_id]
    else:
      raise ValueError("Not animating a valid move")
    
    self.current_frame = round(self.current_frame, 2)
    # Animation is complete
    if self.current_frame == 0.0:
      if (self.animating == Move.SLD):
        self.head_row -= 1 # Player stands
      self.run()

  # Move
  def move(self, move=Move.RUN):
    # Make move
    if (move == Move.RUN):
      pass
    elif (move == Move.JMP):
      self.jump()
    elif (move == Move.SLD):
      self.slide()
    elif (move == Move.ATK):
      self.attack()
    else:
      raise ValueError("Specified move is undefined")
  
  # Check if player on ground
  def on_ground(self, grid):
    # return True
    row = int(self.head_row)
    # print(row)
    # print(type(grid[row + 2][self.LEFT_BUFFER]))
    # print(row)
    assert grid[row + 2][self.LEFT_BUFFER].row == row + 2 and grid[row + 2][self.LEFT_BUFFER].col == self.LEFT_BUFFER
    if self.animating == Move.SLD:
      # One tall 
      if grid[row + 1][self.LEFT_BUFFER].solid or grid[row + 1][self.LEFT_BUFFER + 1].solid:
        return True
    else:
      # Two tall 
      if grid[row + 2][self.LEFT_BUFFER].solid or grid[row + 2][self.LEFT_BUFFER + 1].solid:

        return True
    return False

  # Check for obstacle collisions
  def colliding(self, grid):
    return False
    row = int(self.head_row)
    if self.animating == Move.SLD:
      # Two wide
      if grid[row][self.LEFT_BUFFER].solid or grid[row][self.LEFT_BUFFER + 1].solid:
        return True
    else:
      # One wide
      if grid[row][self.LEFT_BUFFER].solid or grid[row + 1][self.LEFT_BUFFER].solid:
        return True 
    return False
      
  # Update player state
  def update(self, grid):
    # Check for collisions
    if (not self.on_ground(grid)) and (not self.animating == Move.JMP):
      self.fall()
    if self.colliding(grid):
      # Terminate the game / Return a score? 
      pass

    # Images
    self.set_image()
    self.update_current_frame()

# Game  
class Game:
  def __init__(self):
    # Add player sprite
    self.PK = ParkourKing()

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
    # Create sprite group
    sprites = pygame.sprite.Group()

    # Add player sprite
    sprites.add(self.PK)

    # Add block sprites 
    map_blocks = self.game_map.get_sprites()
    for block in map_blocks:
      sprites.add(block)

    # Draw sprites to screen
    sprites.draw(SCN)

    
# Map
class Map:
  def __init__(self):
    # Set buffer
    self.BUFFER = 5
    self.BUFFER_SZ = self.BUFFER * BLOCK_SZ
    self.current_buffer = self.BUFFER_SZ
    self.total_shift = 0

    self.rows = BLOCKS + self.BUFFER
    self.cols = BLOCKS
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
        assert ob == Ob.THARD
        self.grid[Level.GRND - 2][i] = HardBlock(Level.GRND - 2, i)
 
    # Add ground blocks
    for i in range(self.cols):
      self.grid[Level.GRND][i] = Block(Level.GRND, i, Tile.GRASS)

    for i in range(Level.GRND + 1, self.rows):
      for j in range(self.cols):
        self.grid[i][j] = Block(i, j, Tile.DIRT)
 
    # Tests
    for row in self.grid:
      assert len(row) == self.cols
    for i in range(BLOCKS):
      for j in range(cols):
        assert self.grid[i][j].row == i and self.grid[i][j].col == j
      
  # Update blocks
  def update(self):
    self.current_buffer -= Block.SHIFT_SZ
    self.total_shift += Block.SHIFT_SZ
    for i in range(self.rows):
      for j in range(self.cols):
        self.grid[i][j].shift()
    
    if self.total_shift == BLOCK_SZ:
      # Reset block shifts and remove left-most row
      for row in self.grid:
        # Col of first element should be 0
        assert(row[0].col == 0)
        row.pop(0)
      for row in self.grid:
        for block in row:
          block.decrease_col()  

    for i in range(len(self.grid)):
      for j in range(len(self.grid[0])):
        assert self.grid[i][j].row == i and self.grid[i][j].col == j
      
      # Reset total shift
      self.total_shift = 0

    if self.current_buffer == 0:
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
    rows = BLOCKS
    new_cols = self.BUFFER

    for i in range(rows):
      if i < Level.GRND - 2:
        self.grid[i].extend([Air(i, BLOCKS + j) for j in range(new_cols)])
      elif i == Level.GRND - 2:
        # Fill with Air
        self.grid[i].extend([Air(i, BLOCKS + j) for j in range(new_cols)])
        self.grid[i + 1].extend([Air(i + 1, BLOCKS + j) for j in range(new_cols)])

        # Make the number of obstacles a choice?
        pos = random.choice(range(2, self.BUFFER + 1))
        ob = random.choice(OBSTACLES) 
    
        # Add row buffers
        for j in range(new_cols):
          if not j == pos:
            continue

          if ob == Ob.WALL:
            self.grid[i][j] = WallBlock(i, BLOCKS + j)
            self.grid[i + 1][j] = WallBlock(i + 1, BLOCKS + j)
          elif ob == Ob.BHARD:
            self.grid[i + 1][j] = HardBlock(i + 1, BLOCKS + j)
          else:
            assert ob == Ob.THARD
            self.grid[i][j] = HardBlock(i, BLOCKS + j)
        assert len(self.grid[i]) == BLOCKS + self.BUFFER and len(self.grid[i + 1]) == BLOCKS + self.BUFFER
      elif i == Level.GRND - 1:
        continue
      elif i == Level.GRND:
        self.grid[i].extend([Block(i, BLOCKS + j, Tile.GRASS) for j in range(new_cols)])
      else:
        self.grid[i].extend([Block(i, BLOCKS + j, Tile.DIRT) for j in range(new_cols)])
   
    # Reset buffer
    self.current_buffer = self.BUFFER_SZ

    # Tests
    for row in self.grid:
      print(len(row))
      assert len(row) == BLOCKS + self.BUFFER
    for i in range(rows):
      for j in range(BLOCKS + self.BUFFER):
        assert self.grid[i][j].row == i and self.grid[i][j].col == j
  
# Block
class Block(pygame.sprite.Sprite):
  SHIFT_SZ = 5
  def __init__(self, row, col, image_path=Tile.GRASS):
    self.row = row 
    self.col = col

    self.solid = True 
    self.can_break = False
    
    super(Block, self).__init__()
    
    # Set sprite image
    self.image = LOAD.load_image(image_path)
    self.image = pygame.transform.scale(self.image, (BLOCK_SZ, BLOCK_SZ))
    # Scale image to BLOCK_SZ X BLOCK_SZ
    self.rect = self.image.get_rect()
    self.rect.topleft = [self.col * BLOCK_SZ, self.row * BLOCK_SZ]
  
  # Decrease col 
  def decrease_col(self):
    self.col -= 1
    self.rect.topleft = [self.col * BLOCK_SZ, self.row * BLOCK_SZ]

  # Shift block left 
  def shift(self):
    self.rect = self.rect.move(-1 * self.SHIFT_SZ, 0)

# Air block
class Air(Block):
  def __init__(self, row, col):
    self.row = row
    self.col = col

    self.solid = False 
    self.can_break = False
  
  # Override Block methods
  # Decrease col
  def decrease_col(self):
    self.col -= 1 

  # Do nothing 
  def shift(self):
    return 

# Wall block
class WallBlock(Block):
  def __init__(self, row, col, image_path=Tile.WALL):
    super().__init__(row, col, image_path)
    self.solid = True
    self.can_break = True
  
  # Breaks block
  def break_block(self):
    self.solid = False 
  
  # Check for collision
  def collide(self):
    if (self.solid):
      return True
    else:
      return False

# Hard block
class HardBlock(Block):
  def __init__(self, row, col, image_path=Tile.HARD):
    super().__init__(row, col, image_path)
    self.can_break = False
    self.solid = True
  
  def collide(self):
    return True

running = True

# Initialize game
game = Game()

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
  pygame.time.delay(DELAY)
pygame.display.quit()