from config import *
import pygame
import random
from enums import Move, Level

# Player 
class ParkourKing(pygame.sprite.Sprite):
  def __init__(self):
    super(ParkourKing, self).__init__()

    # Position
    self.LEFT_BUFFER = 3
    self.head_row = Level.GRND - 2 # Two blocks above ground level
        
    # Id: (frame-count, updates-per-frame)
    self.attacks = {1: [5, 4], 2: [6, 4], 3: [6, 4]}
    self.jumps = {1: [4, 2]}    
    self.falls = {1: [4, 2]}
    self.runs = {1: [6, 4]}
    self.slides = {1: [6, 4]}
    
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
    self.get_frame_increment = lambda updates_per_frame : 1 / updates_per_frame
    self.current_frame = 0.0
    self.updates_per_frame = self.runs[self.animation_id][1]

  # Jumps
  def jump(self):
    # Player is already in motion
    if not (self.animating == Move.RUN):
      return
    
    # Begins jumping
    self.animating = Move.JMP
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.jumps.keys()))
    self.updates_per_frame = self.jumps[self.animation_id][1]

  # Fall
  def fall(self):
    # Already falling 
    if self.animating == Move.FALL:
      return 
    if self.animating == Move.SLD:
      # Return to original height
      self.head_row -= 1

    # Begin falling
    self.animating = Move.FALL
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.falls.keys()))
    self.updates_per_frame = self.falls[self.animation_id][1]

  # Slide
  def slide(self):
    if not (self.animating == Move.RUN):
      return
    
    # Begins sliding
    self.head_row += 1
    self.animating = Move.SLD
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.slides.keys()))
    self.updates_per_frame = self.slides[self.animation_id][1]
  
  # Attack
  def attack(self, game_map):
    if not (self.animating == Move.RUN):
      return

    game_map[int(self.head_row)][self.LEFT_BUFFER + 3].break_block()
    game_map[int(self.head_row + 1)][self.LEFT_BUFFER + 3].break_block()
    game_map[int(self.head_row)][self.LEFT_BUFFER + 4].break_block()
    game_map[int(self.head_row + 1)][self.LEFT_BUFFER + 4].break_block()

    # Begins attacking
    self.animating = Move.ATK
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.attacks.keys()))
    self.updates_per_frame = self.attacks[self.animation_id][1]
  
  # Run
  def run(self):
    if self.animating == Move.RUN:
      return
    
    # Begins running 
    self.animating = Move.RUN
    self.current_frame = 0.0
    self.animation_id = random.choice(list(self.runs.keys()))
    self.updates_per_frame = self.runs[self.animation_id][1]
    
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
  
  # Increase speed 
  def increase_speed(self):
    for key in self.runs.keys():
      self.runs[key][1] = max(2, self.runs[key][1] - 1)
  
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

  # Shift player up an down
  def shift(self):
    if not self.animating == Move.JMP and not self.animating == Move.FALL:
      return
      
    # Determine total updates
    total_updates = self.updates_per_frame 
    if self.animating == Move.JMP:
      total_updates *= self.jumps[self.animation_id][0]
    elif self.animating == Move.FALL:
      total_updates *= self.falls[self.animation_id][0] 

    dist_shift = BLOCK_SZ / float(total_updates)
    row_shift = 1 / float(total_updates)

    cur_height = self.rect.topleft[1] 
    if self.animating == Move.JMP:
      # Shift upwards
      self.rect = self.rect.move(0, -1 * dist_shift)
      self.head_row += -1 * row_shift
      diff = abs(cur_height - self.rect.topleft[1])
      if diff < dist_shift and self.rect.topleft[1] % BLOCK_SZ != 0:
        self.rect = self.rect.move(0, -1)
    else:
      # Shift downwards
      self.rect = self.rect.move(0, dist_shift)
      self.head_row += row_shift
      diff = abs(cur_height - self.rect.topleft[1])
      if diff < dist_shift and self.rect.topleft[1] % BLOCK_SZ != 0:
        self.rect = self.rect.move(0, 1)

  # Update current frame 
  def update_current_frame(self):
    frame_increment = self.get_frame_increment(self.updates_per_frame)
    self.current_frame += frame_increment
    
    if (self.animating == Move.RUN):
      self.current_frame %= self.runs[self.animation_id][0]
    elif (self.animating == Move.JMP):
      self.current_frame %= self.jumps[self.animation_id][0]
      self.shift()
    elif (self.animating == Move.FALL):
      self.current_frame %= self.falls[self.animation_id][0]
      self.shift()
    elif (self.animating == Move.SLD):
      self.current_frame %= self.slides[self.animation_id][0]
    elif (self.animating == Move.ATK):
      self.current_frame %= self.attacks[self.animation_id][0]
    else:
      raise ValueError("Not animating a valid move")
    
    self.current_frame = round(self.current_frame, 2)
    # Animation is complete || Extra or is a hacky solution to handle floating point errors
    if self.current_frame == 0.0 or ((self.animating == Move.FALL or self.animating == Move.JMP) and self.rect.topleft[1] % BLOCK_SZ == 0):
      if (self.animating == Move.SLD):
        self.head_row -= 1 # Player stands
      self.run()

  # Move
  def move(self, move=Move.RUN, game_map=False):
    # Make move
    if (move == Move.RUN):
      pass
    elif (move == Move.JMP):
      self.jump()
    elif (move == Move.SLD):
      self.slide()
    elif (move == Move.ATK):
      assert not type(game_map) == bool
      self.attack(game_map)
    else:
      raise ValueError("Specified move is undefined")
  
  # Check if player on ground
  def on_ground(self, grid):
    # return True
    row = int(self.head_row)
    if self.animating == Move.SLD:
      # One tall 
      if grid[row + 1][self.LEFT_BUFFER].solid or grid[row + 1][self.LEFT_BUFFER + 1].solid:
        return True
    else:
      # Two tall 
      if grid[row + 2][self.LEFT_BUFFER + 1].solid or grid[row + 2][self.LEFT_BUFFER + 2].solid:

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

