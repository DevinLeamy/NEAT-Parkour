from enums import Tile
from config import *
import pygame
from pygame import Rect

SHIFT_SZ = 5
# Block
class Block(pygame.sprite.Sprite):
  def __init__(self, row, col, image_path=Tile.GRASS):
    self.row = row 
    self.col = col

    self.solid = True 
    
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
    self.rect = self.rect.move(-1 * SHIFT_SZ, 0)
  
  # Do nothing
  def break_block(self):
    return 
  
  # Increase speed
  @staticmethod
  def increase_shift():
    global SHIFT_SZ
    SHIFT_SZ = min(15, SHIFT_SZ + 1)

    # SHIFT_SZ must be a divisor of BLOCK_SZ
    while BLOCK_SZ % SHIFT_SZ != 0:
      SHIFT_SZ += 1
    assert BLOCK_SZ % SHIFT_SZ == 0
  
  # Returns block type Id 
  def get_block_type(self):
    if isinstance(self, HardBlock):
      return Tile.HARD_ID
    elif isinstance(self, WallBlock):
      return Tile.WALL_ID
    else:
      return Tile.AIR_ID
  
  # Get location of left side of block
  def get_block_start(self):
    return self.rect.left

# Air block
class Air(Block):
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.solid = False 

  # Block Override: Decrease col
  def decrease_col(self):
    self.col -= 1 

  # Block Override: Do nothing 
  def shift(self):
    return
  
  # Block Override: Does not have left
  def get_block_start(self):
    return 0

# Wall block
class WallBlock(Block):
  def __init__(self, row, col, image_path=Tile.WALL):
    super().__init__(row, col, image_path)
    self.solid = True
  
  # Breaks block
  def break_block(self):
    if not self.solid:
      return self
    self.solid = False 

    # Set block to broken block - need a different sprite
    self.image = LOAD.load_image(Tile.AIR, False)
    self.image = pygame.transform.scale(self.image, (BLOCK_SZ, BLOCK_SZ))

  
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
    self.solid = True
  
  def collide(self):
    return True

