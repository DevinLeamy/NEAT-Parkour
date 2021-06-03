import random

# Creates NN from genome and faciliates feedforward 
class Feedforward():
  '''
  nodes: Nodes of the NN
  '''
  def __init__(self, nodes):
    self.nodes = nodes
    self.generate_layers()

  # Compute output from input
  # inputs: int[] (not Input class)
  def feedforward(self, inputs):
    for node in self.nodes:
      node.reset()
      # Set input
      if node.is_input():
        # For input node, _id acts as index in input values list
        node.feed_input(inputs[node._id])

    # Preform feedforward over layers of NN 
    for layer in self.layers:
      node.activate()
    
    # Determine output (decision)
    output_nodes = self.layers[-1]

    # Find idx of output node with max value
    decision = 0
    max_val = out_nodes[0].out_val
    for idx, node in enumerate(output_nodes[1:]):
      if max_val < node.out_val:
        max_val = node.out_val
        decision = idx
    
    return decision

  # Check if network is full connected
  def fully_connected(self):
    for idx, layer in enumerate(self.layers[:-1]): # Excludes output layer
      # Maximum possible outgoing connections
      max_connections = len(self.layers[idx]) * len(self.layers[idx + 1]) 

      total_connections = 0
      for node in layer:
        total_connections += len(node.out_bound_edges) 
      
      assert total_connections <= max_connections
      if total_connections < max_connections:
        # Not fully connected 
        return False
    # Fully connected 
    return True
  
  # Get random compatible nodes (for forming connections)
  # Returns: (start_node, end_node)
  def get_random_compatible_nodes(self):
    # Collect nodes that can have inbound edges 
    potential_end = [] # (node, layer)
    for idx, layer in enumerate(self.layers[1:]): # Input node can't be have inbound edges 
      previous_layer_sz = len(self.layers[idx - 1])
      for node in layer:
        if len(node.in_bound_edges) != previous_layer_sz:
          # Has space
          potential_endpoints.append((node, idx))

    # Collect nodes that can have outbound edges 
    potential_start = [] # (node, layer)
    for idx, layer in enumerate(self.layers[:-1]): # Output node can't have outbound edges 
      next_layer_sz = len(self.layers[idx + 1])
      for node in layer:
        if len(node.out_bound_edges) != next_layer_sz:
          # Has space
          potential_start.append((node, idx))
    
    # Shuffle nodes to make selection random
    random.shuffle(potential_start)
    random.shuffle(potential_end)

    for start_node, start_layer in potential_start:
      for end_node, end_layer in potential_end:
        if start_layer >= end_layer: # Start node must be before end node
          continue
        if start_node.leads_to(end_node): # Nodes cannot be connected
          continue
        return (start_node, end_node)
    assert False # A pair should always be found
    
  # Create list of layers of nodes that can be evaluated in parallel
  def generate_layers(self):
    self.layers = []
    '''
    1. Find input nodes (some with not edges leading into them)
    2. Preform BFS, storing nodes at depth i in layers[i] 
    '''
    # Collect input nodes (first layer is input)
    layer = [node for node in self.nodes if node.is_input()]
    self.layers.append(layer)
    
    # BFS
    while (len(layer) != 0):
      new_layer = []
      for node in layer:
        for edge in node.out_bound_edges:
          new_node = edge.out_node
          # Avoid duplicates
          if not new_node in new_layer:
            new_layer.append(new_node)
      if len(new_layer) != 0:
        self.layers.append(new_layer)
      layer = new_layer


    
      

