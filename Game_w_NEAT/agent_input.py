# Class to hold the input structure of data
class Input():
  '''
    height: Head height [0, 1, 2]
    sliding: Sliding [0, 1]
    type1: Type of next block @ groud-height + 3
    type2: Type of next block @ groud-height + 2 
    type3: Type of next block @ groud-height + 1
    dist: Distance to the next block
  '''
  def __init__(self, height, sliding, type1, type2, type3, dist): 
    self.height = height
    self.sliding = sliding
    self.type1 = type1
    self.type2 = type2
    self.type3 = type3
    self.dist = dist

  # Return input as array
  def as_array(self):
    return [
      self.height,
      self.sliding,
      self.type1,
      self.type2,
      self.type3,
      self.dist
    ]
  