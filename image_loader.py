import pygame

# Image loader
class ImageLoader():
  def __init__(self):
    self.images = {}
  
  # Get loaded image
  def load_image(self, path, convert=True):
    if not path in self.images:
      if convert:      
        self.images[path] = pygame.image.load(path).convert()
      else:
        self.images[path] = pygame.image.load(path)
    return self.images[path]

