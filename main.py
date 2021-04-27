# Teaching Parkour... The Darwin Way
from enum import Enum
import random
import pygame 
pygame.init()

pygame.display.init()

# Create game window
W = 1000
H = 800
BLOCKS = 20
BLOCK_SZ = W / BLOCKS

SCN = pygame.display.set_mode((W, H))
pygame.display.flip()
pygame.display.set_caption("Teaching Parkour... The Darwin Way")

# Enums
class Level(Enum):
  GRND = 0
  MID = 1
  AIR = 2
  
class Move(Enum):
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
        
    # Id and frame count
    self.attacks = {1: 5, 2: 6, 3: 6}
    self.jumps = {1: 4}    
    self.runs = {1: 6}
    self.slides = {1: 2}
    
    # Generate image path
    self.get_attack_frame = lambda id, frame: "Adventurer/Sprites/adventurer-attack%d-0%d.png" % (id, frame)
    self.get_jump_frame = lambda id, frame: "Adventurer/Sprites/adventurer-jump-0%d.png" % (frame)
    self.get_run_frame = lambda id, frame: "Adventurer/Sprites/adventurer-run-0%d.png" % (frame) 
    self.get_slide_frame = lambda id, frame: "Adventurer/Sprites/adventurer-slide-0%d.png" % (frame)
    
    # Set image defaults
    self.image = pygame.image.load(self.get_run_frame(0, 0))
    self.scale_image()
    self.rect = self.image.get_rect()
    self.rect.topleft = [60, 60]
    
    # On the ground and not in motion
    self.level = Level.GRND
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
    self.level = Level.AIR
    self.animating = Move.JMP
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.jumps.keys()))

  # Slide
  def slide(self):
    if not (self.animating == Move.RUN):
      return
    
    # Begins sliding
    self.level = Level.GRND
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
    global BLOCK_SZ
    width, height = self.image.get_size()
#     self.image = pygame.transform.scale(self.image, (int(BLOCK_SZ), int(BLOCK_SZ / width * height)))
#     self.image = pygame.transform.scale(self.image, (int(BLOCK_SZ), int(BLOCK_SZ)))
    self.image = pygame.transform.scale(self.image, (100, 200))
    
  # Set sprite image
  def set_image(self):
    path = self.get_image_path()
    self.image = pygame.image.load(path)
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
    # Update player
    self.PK.update()

    self.draw()

  # Draw game state
  def draw(self):
    global SCN
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
    global BLOCKS

    # Create map (STATIC MAP - REMOVE)
    self.grid = []
    row = list()
    for i in range(BLOCKS):
      row.append(Block(i, 8, Tile.GRASS))
    self.grid.append(row)
    for i in range(BLOCKS):
      row = list()
      for j in range(1, BLOCKS - 9):
        row.append(Block(i, j + 8, Tile.DIRT))
      self.grid.append(row)

  # Returns block sprites
  def get_sprites(self):
    sprites = list()
    for row in self.grid:
      for block in row:
        sprites.append(block)
    return sprites
  
# Block
class Block(pygame.sprite.Sprite):
  def __init__(self, row, col, image_path=Tile.GRASS):
    global BLOCK_SZ
    super(Block, self).__init__()
    
    # Set sprite image
    self.image = pygame.image.load(image_path)
    self.image = pygame.transform.scale(self.image, (50, 50))
    # Scale image to BLOCK_SZ X BLOCK_SZ
    self.rect = self.image.get_rect()
    self.rect.topleft = [row * BLOCK_SZ, col * BLOCK_SZ]

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
#   CLK.tick(60)
  pygame.time.delay(20)
pygame.display.quit()