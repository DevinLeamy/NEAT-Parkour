# Class to hold the input structure of data
class Input():
  '''
    height: Head height [1 - 3]
    sliding: Sliding [0 - 1]
    type1: Type of next block @ groud-height + 1 [1 - 4]
    type2: Type of next block @ groud-height + 2 [1 - 4]
    type3: Type of next-next block @ groud-height + 1 [1 - 4]
    type4: Type of next-next block @ groud-height + 2 [1 - 4]
    dist: Distance to the next block [185 - 240]
    shift_sz: Distance a block travels per update [5 - 15] 
  '''
  def __init__(self, height, sliding, type1, type2, type3, type4, dist, shift_sz):
    self.height = height
    self.height = Input.normalize(height, 1, 3) 
    self.sliding = Input.normalize(sliding, 0, 1)
    self.type1 = Input.normalize(type1, 1, 4) 
    self.type2 = Input.normalize(type2, 1, 4)
    self.type3 = Input.normalize(type3, 1, 4) 
    self.type4 = Input.normalize(type4, 1, 4)
    self.dist = Input.normalize(dist, 185, 240) 
    self.shift_sz = Input.normalize(shift_sz, 5, 15)

  # Return input as array
  def as_array(self):
    _input = [
      self.height,
      self.sliding,
      self.type1,
      self.type2,
      self.type3,
      self.type4,
      self.dist,
      # self.shift_sz
    ]
    # Assuming they're positive, all values are smaller than one
    assert sum(_input) <= len(_input)
    return _input
  
  # Normalize input into range [-1, 1]
  @staticmethod
  def normalize(x, minx, maxx):
    return 2 * (x - minx) / (maxx - minx) - 1
    