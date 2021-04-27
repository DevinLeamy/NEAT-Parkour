# Teaching Parkour... The Darwin Way
import random
import pygame 
from image_loader import ImageLoader
pygame.init()

pygame.display.init()

# Constants
W = 1000
H = 800
BLOCKS = 20
BLOCK_SZ = W / BLOCKS
SCN = pygame.display.set_mode((W, H))
LOAD = ImageLoader()

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

class Color():
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  GREY = (230, 230, 230)

class Tile():
  GRASS = "TileSet/Tiles/grass.png"
  DIRT = "TileSet/Tiles/dirt.png"

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
    self.runs = {1: 6}
    self.slides = {1: 4}
    
    # Generate image path
    self.get_attack_frame = lambda id, frame: "Adventurer/Sprites/adventurer-attack%d-0%d.png" % (id, frame)
    self.get_jump_frame = lambda id, frame: "Adventurer/Sprites/adventurer-jump-0%d.png" % (frame)
    self.get_run_frame = lambda id, frame: "Adventurer/Sprites/adventurer-run-0%d.png" % (frame) 
    self.get_slide_frame = lambda id, frame: "Adventurer/Sprites/adventurer-slide-0%d.png" % (frame)
    
    # Set image defaults
    self.image = LOAD.load_image(self.get_run_frame(0, 0))
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

  # Slide
  def slide(self):
    if not (self.animating == Move.RUN):
      return
    
    # Begins sliding
    self.animating = Move.SLD
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.slides.keys()))

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
    self.image = LOAD.load_image(path)
    self.scale_image()
    
  # Displays player
  def display(self):
    pass
  
  # Update current frame 
  def update_current_frame(self):
    self.current_frame += self.frame_increment
    
    if (self.animating == Move.RUN):
      self.current_frame %= self.runs[self.animation_id]
    elif (self.animating == Move.JMP):
      self.current_frame %= self.jumps[self.animation_id]
    elif (self.animating == Move.SLD):
      self.current_frame %= self.slides[self.animation_id]
    elif (self.animating == Move.ATK):
      self.current_frame %= self.attacks[self.animation_id]
    else:
      raise ValueError("Not animating a valid move")
    
    self.current_frame = round(self.current_frame, 2)
    # Animation is complete
    if self.current_frame == 0.0:
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
      
  # Update player state
  def update(self):
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
    self.PK.update()
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

    self.grid = []
    self.initialize_map()

  # Create initial map config
  def initialize_map(self):
    # Create map (STATIC MAP - REMOVE)
    self.grid = []
    row = list()
    for i in range(BLOCKS + self.BUFFER):
      row.append(Block(Level.GRND, i, Tile.GRASS))
    self.grid.append(row)

    for i in range(Level.GRND + 1, BLOCKS):
      row = list()
      for j in range(BLOCKS + self.BUFFER):
        row.append(Block(i, j, Tile.DIRT))  
      self.grid.append(row)

  # Update blocks
  def update(self):
    self.current_buffer -= Block.SHIFT_SZ
    self.total_shift += Block.SHIFT_SZ
    for row in self.grid:
      for block in row:
        block.shift()
    
    if self.total_shift == BLOCK_SZ:
      # Reset block shifts and remove left-most row
      for row in self.grid:
        # Col of first element should be 0
        assert(row[0].col == 0)
        row.pop(0)
      for row in self.grid:
        for block in row:
          block.decrease_col()  
      
      # Reset total shift
      self.total_shift = 0

    if self.current_buffer == 0:
      self.generate_buffer()

  # Returns block sprites
  def get_sprites(self):
    sprites = list()
    for row in self.grid:
      for block in row:
        sprites.append(block)
    return sprites
  
  # Generate new buffer
  def generate_buffer(self):
    # Add buffer to back
    for row in self.grid:
      image = Tile.DIRT
      if row[0].row == 8:
        image = Tile.GRASS
      row.extend([Block(row[0].row, BLOCKS + i, image) for i in range(self.BUFFER)])

      # Number of elements in a row, after gen, is fixed
      assert(len(row) == BLOCKS + self.BUFFER)

    self.current_buffer = self.BUFFER_SZ
  
# Block
class Block(pygame.sprite.Sprite):
  SHIFT_SZ = 5
  def __init__(self, row, col, image_path=Tile.GRASS):
    self.row = row 
    self.col = col
    
    super(Block, self).__init__()
    
    # Set sprite image
    self.image = LOAD.load_image(image_path)
    self.image = pygame.transform.scale(self.image, (50, 50))
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

# Wall block
class WallBlock(Block, ):
  def __init__(self):
    self.broken = False
  
  def break_block(self):
    self.broken = True
  
  def collide(self):
    if (self.broken):
      return True
    else:
      return False

# Hard block
class HardBlock(Block):
  def __init__(self):
    pass
  
  def collide(self):
    return True

running = True
CLK = pygame.time.Clock()

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
  SCN.fill(Color.GREY)  
  game.update()
  pygame.display.update()
  pygame.display.flip()
  
  # Clock delay
  # CLK.tick(60)
  pygame.time.delay(20)
pygame.display.quit()