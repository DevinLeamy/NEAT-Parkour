from main import BLOCK_SZ, LOAD, pygame
import random
from enums import Move, Level

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
    if self.animating == Move.SLD:
      # Return to original height
      self.head_row -= 1

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

