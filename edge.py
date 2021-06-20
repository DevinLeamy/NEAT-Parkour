from node import Node
import random
from edge_history import EdgeHistory
from config import PROB_NEW_WEIGHT, WEIGHT_LOWER, WEIGHT_UPPER 

# Connection gene between two nodes
class Edge():
  '''
  in_node: Input node
  out_node: Output node
  active: State of the connection (active or not active)
  weight: Weight of the edge
  inv: Innovation number of the edge
  '''
  def __init__(self, in_node, out_node, active=True, weight=None):
    self.in_node = in_node
    self.out_node = out_node
    self.active = active
    self.weight = weight if weight != None else Edge.random_weight() 

    inv = EdgeHistory.get_innovation_number(in_node, out_node)
    if inv == -1:
      # New edge
      self.inv = EdgeHistory.add_edge(in_node, out_node)
    else:
      # Existing edge
      self.inv = inv 
  
  # Mutate weight 
  def mutate(self):
    rand = random.uniform(0, 100)

    # New random value 
    if (rand <= PROB_NEW_WEIGHT):
      self.weight = Edge.random_weight() 
    else:
      # Uniformly perturbed (slight change)
      self.weight = self.clamp(self.weight + random.gauss(0, 0.2))
  
  # Squeeze input between a range
  def clamp(self, x):
    return min(max(WEIGHT_LOWER, x), WEIGHT_UPPER)

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
  
  # Generate random new weight
  @staticmethod
  def random_weight():
    return random.uniform(WEIGHT_LOWER, WEIGHT_UPPER)
  
  # Calculate weight distance between edges
  @staticmethod
  def weight_distance(edge_1, edge_2):
    return abs(edge_1.weight - edge_2.weight)
  
  # High-level edge data as list - see genome.py crossover method for use
  # [in_node_id, out_node_id, active, weight]
  @staticmethod
  def data(edge):
    in_node_id = edge.in_node._id
    out_node_id = edge.out_node._id
    active = edge.active
    weight = edge.weight
    return [in_node_id, out_node_id, active, weight]
