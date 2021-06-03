from node import Node
import random
from edge_history import EdgeHistory

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
  def __init__(self, in_node, out_node, active=True, weight=random.uniform(-1, 1)):
    self.in_node = in_node
    self.out_node = out_node
    self.active = active
    self.weight = weight
    
    inv = EdgeHistory.get_innovation_number(in_node, out_node)
    if inv == -1:
      # New edge
      self.inv = EdgeHistory.add_edge(in_node, out_node)
    else:
      # Existing edge
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

  # Determine if edge matched self
  def edge_matches(self, new_edge_in_node, new_edge_out_node):
    # Input nodes must match
    if new_edge_in_node._id != self.in_node._id:
      return False
    # Output nodes must match
    if new_edge_out_node._id != self.out_node._id:
      return False
    return True
  
  # Determine if edge represents the same gene as self
  def gene_matches(self, edge):
    # Compare innovation numbers
    return edge.inv == self.inv
  
  # Calculate weight distance between edges
  @staticmethod
  def weight_distance(edge_1, edge_2):
    return abs(edge_1.weight - edge_2.weight)
