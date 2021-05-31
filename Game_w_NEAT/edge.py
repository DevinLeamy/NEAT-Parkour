from node import Node
import random

'''
TODO: Make the weight bounds (-1, 1) and mutation power (2) configurable
      hyperparameters
'''

# Connection gene between two nodes
class Edge():
  '''
  in_node: Input node
  out_node: Output node
  active: State of the connection (active or not active)
  weight: Weight of the edge
  inv: Innovation number of the edge
  '''
  def __init__(self, in_node, out_node, active, weight, inv):
    self.in_node = in_node
    self.out_node = out_node
    self.active = active
    self.weight = weight
    self.inv = inv
  
  # Mutate weight 
  def mutate(self):
    rand = random.uniform(0, 1)

    # New random value - 10% chance
    if (rand <= 0.1):
      # Bounds, (-1, 1), are arbitrary and may be subject to change
      self.weight = random.uniform(-1, 1) 
    else:
      # Uniformly perturbed (slight change) - 90% chance
      mutate_power = 2
      self.weight = self.clamp(random.gauss(0.0, 2))
    
  # Squeeze input between a range
  def clamp(self, x):
    return min(max(-1, x), 1)


  # Disable edge
  def disable(self):
    self.active = False 

  # Enable edge
  def enable(self):
    self.active = True
