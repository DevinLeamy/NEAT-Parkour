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


    
      

