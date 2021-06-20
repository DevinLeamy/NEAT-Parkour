# Class to hold the input structure of data
class Input():
  '''
    height: Head height [1 - 3]
    sliding: Sliding [0 - 1]
    dist1: Distance to next .solid block @ groud-height + 1 [125 - 900]
    dist2: Distance to next .solid block @ groud-height + 1 [125 - 900]
    type1: Type of next .solid block @ ground-height + 1 (1 - unbreakable, otherwise 2) [1, 2]
    type2: Type of next .solid block @ ground-height + 2 (1 - unbreakable, otherwise 2) [1, 2]
    shift_sz: Distance a block travels per update [5 - 15] 
  '''
  def __init__(self, height, dist1, dist2, type1, type2, shift_sz):
    self.height = Input.normalize(height, 1, 3) 
    self.dist1 = Input.normalize(dist1, 125, 900)
    self.dist2 = Input.normalize(dist2, 125, 900)
    self.type1 = Input.normalize(type1, 1, 2)
    self.type2 = Input.normalize(type2, 1, 2)
    self.shift_sz = Input.normalize(shift_sz, 5, 15)

  # Return input as array
  def as_array(self):
    _input = [
      self.height,
      self.dist1,
      self.dist2,
      self.type1,
      self.type2,
      self.shift_sz
    ]
    return _input
  
  # Normalize input into range [-1, 1]
  @staticmethod
  def normalize(x, minx, maxx):
    return 2.0 * (x - minx) / (maxx - minx) - 1.0
    