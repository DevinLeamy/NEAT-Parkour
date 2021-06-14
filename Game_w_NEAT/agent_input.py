# Class to hold the input structure of data
class Input():
  '''
    height: Head height [0, 1, 2]
    sliding: Sliding [0, 1]
    type1: Type of next block @ groud-height + 3
    type2: Type of next block @ groud-height + 2 
    type3: Type of next block @ groud-height + 1
    dist: Distance to the next block
    shift_sz: Distance a block travels per update 
  '''
  def __init__(self, height, sliding, type1, type2, type3, type4, dist, shift_sz,
                     max_height=40, max_sliding=1, max_type=4, max_dist=10, max_shift_sz=10): 
    # Normalize inputs || might be unnessecary
    self.height = height / max_height
    self.sliding = sliding / max_sliding
    self.type1 = type1 / max_type
    self.type2 = type2 / max_type 
    self.type3 = type3 / max_type
    self.type4 = type4 / max_type
    self.dist = dist / max_dist
    self.shift_sz = shift_sz / max_shift_sz


  # Return input as array
  def as_array(self):
    return [
      self.height,
      self.sliding,
      self.type1,
      self.type2,
      self.type3,
      self.type4,
      self.dist,
      self.shift_sz
    ]
  