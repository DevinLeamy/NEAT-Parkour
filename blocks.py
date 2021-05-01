from enums import Tile
from config import *
import pygame

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

