class Gene():
  '''
  in_node: Input node 
  out_node: Output node
  inv: Innovation number
  weight: Edge weight
  '''
  def __init__(self, in_node: int, out_node: int, inv: int, active: bool, weight=1):
    self.in_node = in_node
    self.out_node = out_node
    self.inv = inv
    self.active = active
    self.weight = weight
  
