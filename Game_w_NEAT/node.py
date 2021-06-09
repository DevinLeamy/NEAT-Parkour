import math

# Single node in NN 
class Node():
  '''
  _id: Node identifier
  in_val: Input value or sum of input values
  out_val: Output value 
  '''
  def __init__(self, _id, in_val=0.0, out_val=0.0):
    self._id = _id # Id should be set by a static Node.global_id variable
    self.in_val = in_val
    self.out_val = out_val
    # Edges leading into and out of the node
    self.out_bound_edges = [] 
    self.in_bound_edges = []

  # Modified sigmoid function 
  def sigmoid(self, x):
    y = 1 / (1 + math.exp(-4.9 * x)) 
    return y
  
  # Call activation function and set result
  # Is is assumed that the node has received input from all in bound edges 
  def activate(self):
    # Active with sigmoid, unless node is an input node
    self.out_val = self.sigmoid(self.in_val) if not self.is_input() else self.in_val

    # Relay output through edges
    for edge in self.out_bound_edges:
      next_node = edge.out_node
      next_node.feed_input(self.out_val * edge.weight)
  
  # Increase input
  def feed_input(self, increase):
    self.in_val += increase

  # Add edge 
  def add_edge(self, edge):
    in_node_id = edge.in_node._id
    out_node_id = edge.out_node._id
    if self._id == in_node_id:
      # Edge leads out of node
      self.out_bound_edges.append(edge)
    else:
      # Edge leads into node
      self.in_bound_edges.append(edge)
  
  # Reset input value
  def reset(self):
    self.in_val = 0
  
  # Determine if node is input node
  def is_input(self):
    # No edges lead into input nodes
    if len(self.in_bound_edges) == 0:
      return True
    return False
  
  # Determine if self has edge leading to a given node
  def leads_to(self, node):
    node_id = node._id
    for edge in self.out_bound_edges:
      if edge.out_node._id == node_id:
        # self is connected to node by an outbound edge
        return True
    # self is not connected to node
    return False
  
  # Determine if node is output node
  def is_output(self):
    # No edges lead out of output nodes
    if len(self.out_bound_edges) == 0:
      return True
    return False