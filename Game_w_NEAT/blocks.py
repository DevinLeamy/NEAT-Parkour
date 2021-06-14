from enums import Tile
from config import *
import pygame
from pygame import Rect

# Block
class Block(pygame.sprite.Sprite):
  SHIFT_SZ = 5
  def __init__(self, row, col, image_path=None):
    self.row = row 
    self.col = col

    # Used in single player
    self.solid = True 
    
    super(Block, self).__init__()
    
    if image_path != None:
      # Set sprite image
      self.image = LOAD.load_image(image_path)
      self.image = pygame.transform.scale(self.image, (BLOCK_SZ, BLOCK_SZ))
      # Scale image to BLOCK_SZ X BLOCK_SZ
      self.rect = self.image.get_rect()
    else:
      self.rect = pygame.Rect(0, 0, BLOCK_SZ, BLOCK_SZ)
    self.rect.topleft = [self.col * BLOCK_SZ, self.row * BLOCK_SZ]
  
  # Decrease col 
  def decrease_col(self):
    self.col -= 1
    self.rect.topleft = [self.col * BLOCK_SZ, self.row * BLOCK_SZ]

  # Shift block left 
  def shift(self):
    self.rect = self.rect.move(-1 * Block.SHIFT_SZ, 0)
  
  # Do nothing
  def break_block(self, player_id, single_player=False):
    return 
  
  # Does not collide, by default 
  def collide(self, player_id, single_player=False):
    return False
  
  # Increase speed
  @staticmethod
  def increase_shift():
    Block.SHIFT_SZ = min(15, Block.SHIFT_SZ + 1)

    # SHIFT_SZ must be a divisor of BLOCK_SZ
    while BLOCK_SZ % Block.SHIFT_SZ != 0:
      Block.SHIFT_SZ += 1
  
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
  
  # Reset block shift size
  @staticmethod
  def reset_shift():
    Block.SHIFT_SZ = 5


# Air block
class Air(Block):
  def __init__(self, row, col):
    super().__init__(row, col, None)
    self.row = row
    self.col = col

    self.solid = False

# Wall block
class WallBlock(Block):
  def __init__(self, row, col, image_path=Tile.WALL):
    super().__init__(row, col, image_path)
    self.solid = True
    
    # Ids for players that have broken the block
    self.broken = set() 
  
  # Breaks block
  def break_block(self, player_id, single_player=False):
    self.broken.add(player_id)

    if (single_player):
      # Update solid 
      self.solid = False

    # Set block to broken block - need a different sprite
    # Note: Although the block may appear to be Air, if will still act as a solid for 
    #       agents that have yet to break it 
    self.image = LOAD.load_image(Tile.AIR, False)
    self.image = pygame.transform.scale(self.image, (BLOCK_SZ, BLOCK_SZ))

  
  # Check for collision
  def collide(self, player_id, single_player=False):
    if single_player: 
      # Collide if solid, don't otherwise
      return self.solid

    # Collide if block has hot been broken by player_id
    if player_id in self.broken:
      return False
    return True

# Hard block
class HardBlock(Block):
  def __init__(self, row, col, image_path=Tile.HARD):
    super().__init__(row, col, image_path)
    self.solid = True
  
  def collide(self, player_id, single_player=False):
    # Always collide
    return True

