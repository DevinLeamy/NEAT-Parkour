from config import *

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

