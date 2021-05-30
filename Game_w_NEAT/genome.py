from gene import Gene 

class Genome():
  def __init__(self, genes=None):
    if (genes == None):
      self.genes = []
    else:
      self.genes = genes