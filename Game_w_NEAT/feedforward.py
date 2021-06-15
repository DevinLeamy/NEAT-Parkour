import random

# Creates NN from genome and faciliates feedforward 
class Feedforward():
  '''
  nodes: Nodes of the NN
  '''
  def __init__(self, nodes):
    self.nodes = nodes
    self.generate_layers()
    # print(len(nodes))
    # print(sum([1 for node in nodes if node.is_output()]))

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
      for node in layer:
        node.activate()
    
    # Determine output (decision)
    out_nodes = [node for node in self.nodes if node.is_output()]

    # Find idx of output node with max value
    decision = [0]
    max_val = out_nodes[0].out_val
    for idx, node in enumerate(out_nodes):
      if max_val < node.out_val:
        max_val = node.out_val
        decision = [idx]
      elif max_val == node.out_val:
        decision.append(idx)
    # If outputs are tied, choose a random one
    return random.choice(decision)

  # Check if network is full connected
  def fully_connected(self):
    for i, layer in enumerate(self.layers[:-1]): 
      # Exclude output nodes
      nodes = [node for node in layer if not node.is_output()]

      # Calculate the number of nodes in all layers after i
      nodes_infront = 0
      for next_layer in self.layers[i + 1:]:
        nodes_infront += len(next_layer)

      # Maximum possible outgoing connections
      max_connections = len(nodes) * nodes_infront

      total_connections = 0
      for node in nodes:
        total_connections += len(node.out_bound_edges) 
      
      assert total_connections <= max_connections
      if total_connections < max_connections:
        # Not fully connected 
        return False

    print("Fully connected")
    # Fully connected 
    return True
  
  # Get random compatible nodes (for forming connections)
  # Returns: (start_node, end_node)
  def get_random_compatible_nodes(self):
    # Collect nodes that can have inbound edges 
    potential_end = [] # (node, layer)
    # Number of nodes in previous layers
    previous_nodes = len(self.layers[0])

    for idx in range(1, len(self.layers)): # Input node can't be have inbound edges 
      layer = self.layers[idx]
      for node in layer:
        if len(node.in_bound_edges) < previous_nodes:
          # Has space
          potential_end.append((node, idx))
      previous_nodes += len(layer)

    # Collect nodes that can have outbound edges 
    potential_start = [] # (node, layer)

    # Number of nodes in following layers
    next_nodes = len([node for node in self.nodes if node.is_output()]) # Number of output nodes

    # Output node can't have outbound edges 
    # Fancy range: Iterates is reversed order, ignoring the last layer
    for idx in range(len(self.layers) - 2, -1, -1): 
      layer = self.layers[idx]
      non_output_nodes = [node for node in layer if not node.is_output()]
      for node in non_output_nodes: # Exclude output nodes
        if len(node.out_bound_edges) != next_nodes:
          # Has space
          potential_start.append((node, idx))
      next_nodes += len(non_output_nodes)
    
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

    # Set of node _ids that have been visited
    seen = set() 
    # BFS
    while (len(layer) != 0):
      new_layer = []
      for node in layer:
        for edge in node.out_bound_edges:
          if not edge.active: # Only active edges participate in feedforward 
            continue
          new_node = edge.out_node
          # Avoid duplicates
          if not new_node in new_layer and not new_node._id in seen: 
            new_layer.append(new_node)
            # Node has been seen
            seen.add(new_node._id) 
      if len(new_layer) != 0:
        self.layers.append(new_layer)
      layer = new_layer
    
    # Outputs never visited
    outputs = [node for node in self.nodes if node.is_output() and not node._id in seen]

    # for idx, layer in enumerate(self.layers):
    #   print("IDX %d" % (idx), len(layer))
    
    # Add outputs to last layer
    self.layers[-1].extend(outputs)


    
      

