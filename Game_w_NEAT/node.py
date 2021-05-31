# Single node in NN 
class Node():
  '''
  in_val: Input value 
  out_val: Output value 
  _id: Node identifier
  layer: Layer of node in the NN
  '''
  def __init__(self, _id, layer, in_val=0.0, out_val=0.0):
    self.in_val = in_val
    self.out_val = out_val
    self._id = _id
    self.layer = layer # Can the layer not increase??

  # Modified sigmoid function 
  def sigmoid(self, x):
    y = 1 / (1 + exp(-4.9 * x)) 
    return y