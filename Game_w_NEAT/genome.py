from edge import Edge
from node import Node
from feedforward import Feedforward
import random

class Genome():
  '''
  next_id: Id of next node created
  c1, c2, c3: Coefficients from compatibility function
  c_threshold: Compatibility threshold
  '''
  next_id = 0
  c1 = 1.0
  c2 = 1.0
  # c3 = 0.4
  c3 = 3.0 # For larger populations with room for more species
  c_threshold = 3.0
  '''
  in_nodes: Number of input nodes
  out_nodes: Number of output nodes
  '''
  def __init__(self, in_nodes_cnt=10, out_nodes_cnt=6, initialize_nodes=True):
    self.in_nodes_cnt = in_nodes_cnt
    self.out_nodes_cnt = out_nodes_cnt

    self.nodes = []
    self.edges = []

    if not initialize_nodes:
      return

    # Create input nodes
    in_nodes = []
    for i in range(self.in_nodes_cnt):
      in_nodes.append(Node(i)) # Input node ids remain the same
    
    # Create output nodes
    out_nodes = []
    for i in range(self.out_nodes_cnt):
      out_nodes.append(Node(self.in_nodes_cnt + i)) # Output node ids remain the same
    
    # Initialize edges
    for in_node in in_nodes:
      # Create edges between all output nodes
      for out_node in out_nodes:
        edge = Edge(in_node, out_node, True) # Note that these are references
        # Add edge to edges 
        self.edges.append(edge)

        # Add edge to endpoints (nodes)
        in_node.add_edge(edge) # The utility of list is shown in feedforward.py
        out_node.add_edge(edge)
    
    # Store input and output nodes
    self.nodes.extend(in_nodes)
    self.nodes.extend(out_nodes)
  
  # Determine if genome contains matching gene (edge)
  def has_matching(self, edge):
    for candidate in self.edges:
      if candidate.gene_matches(edge):
        return True
    return False
  
  # Retreive matching gene (edge), if it exists
  def get_matching(self, edge):
    for candidate in self.edges:
      if candidate.gene_matches(edge):
        return candidate
    # Edge has no match
    return None
  
  # Determine maximum innovation number among edges
  def max_inv(self):
    # There must be at least one edge
    assert len(self.edges) != 0

    max_inv = max([edge.inv for edge in self.edges])
    return max_inv
  
  # Add new node
  def add_node(self):
    edges = self.all_edges()
    assert len(edges) != 0

    # Select random edge 
    edge = random.choice(edges)
    in_node = edge.in_node
    out_node = edge.out_node
    weight = edge.weight

    '''
    1. Place new node in between edge endpoints
    2. Disable edge
    3. Create edges between new node and endpoints
    3.1 Edge leading into the new node has weight=1.0 
    3.2 Edge leading out fo the new node have weight=(previous edge's weight) 
    4. Add new edges to nodes
    '''

    # Disable existing edge
    edge.disable() 

    # Create new node
    new_node = Node(len(self.nodes)) # TODO: Explicit node_id should be removed in place of static Node variable

    # Create new edges - (names are to be read as relative to the new node)
    in_bound_edge = Edge(in_node, new_node, weight=1)
    out_bound_edge = Edge(new_node, in_node, weight=weight) 

    # Add edges to nodes and genome
    self.edges.append(in_bound_edge)
    self.edges.append(out_bound_edge)
    
    in_node.add_edge(in_bound_edge)
    out_node.add_edge(out_bound_edge)
    new_node.add_edge(in_bound_edge)
    new_node.add_edge(out_bound_edge)

  # Get all active edges in genome
  def all_edges(self):
    edges = []
    # Collect all outbound edges of all nodes - this collects all edges
    for node in self.nodes:
      for edge in node.out_bound_edges:
        if not edge.active: # Only active edges are included
          continue
        edges.append(edge)
    return edges
    

  # Add connection gene (edge) to genome
  def add_connection(self):
    # Create NN 
    feedforward = Feedforward(self.nodes)
    if feedforward.fully_connected():
      return
    # Find compatible nodes
    (start_node, end_node) = feedforward.get_random_compatible_nodes() 

    # Create new edge
    new_edge = Edge(in_node, out_node) 

    # Add edge to nodes and genome
    self.edges.append(new_edge)

    start_node.add_edge(new_edge)
    end_node.add_edge(new_edge)

  
  # TODO: Make probabilities configurable
  # Mutate genome 
  def mutate(self):
    '''
    - 80% chance weights are mutated 
    - 5%  chance connection is added
    - 3%  chance node is added
    '''

    # Mutate weights 
    rand = random.uniform(0, 1)
    if rand < 0.8:
      edges = self.all_edges()
      for edge in edges:
        edge.mutate()
    
    # Add connection
    rand = random.uniform(0, 1)
    if rand < 0.05:
      self.add_connection()
    
    # Add node
    rand = random.uniform(0, 1)
    if rand < 0.03:
      self.add_node()

  # Calculate compatibility of two genomes 
  @staticmethod
  def compatibility(genome_1, genome_2):
    edges_1 = genome_1.edges
    edges_2 = genome_2.edges

    # Max innovation numbers 
    max_1 = genome_1.max_inv()
    max_2 = genome_2.max_inv()

    # Normalizing factor
    N = max(len(edges_1), len(edges_2))
    if N <= 20:
      N = 1
    
    # Number of excess and disjoint genes between parents
    E = 0
    D = 0
    for edge in edges_1:
      if genome_2.has_matching(edge):
        continue 
      # Increment disjoint and excess
      if edge.inv <= max_2:
        D += 1 
      else:
        E += 1

    for edge in edges_2:
      if genome_1.has_matching(edge):
        continue
      # Increment disjoint and excess
      if edge.inv <= max_1:
        D += 1
      else:
        E += 1
    
    # Average weight distance
    W = Genome.average_weight_d(genome_1, genome_2)

    # Compatibility
    comp = (Genome.c1 * E) / N + (Genome.c2 * D) / N + (Genome.c3 * W)
    # print("E: %f, D: %f, W: %f, Compatibility: %f" % (E, D, W, comp))
    return comp

  # Set edges - for clarity
  def set_edges(self, new_edges):
    self.edges = new_edges
  
  # Set nodes - for clarity
  def set_nodes(self, new_nodes):
    self.nodes = new_nodes

  # Determine if genes are compatible - i.e. of the same species
  @staticmethod
  def compatible(gene_1, gene_2):
    return Genome.compatibility(gene_1, gene_2) <= Genome.c_threshold
   
  # Calculate average weight distance of matching genes
  @staticmethod
  def average_weight_d(genome_1, genome_2):
    # Total weight distance and matching genes count
    total_wd = 0.0
    total_mc = 0 
    for edge in genome_1.edges:
      matching_edge = genome_2.get_matching(edge)
      if matching_edge == None:
        # Does not exist
        continue
      total_wd += Edge.weight_distance(edge, matching_edge)
      total_mc += 1
    
    # Average weight distance 
    # W=100 in case of divide-by-zero
    W = total_wd / total_mc if total_mc != 0 else 100
    return W
  
  # Create crossover genome of two parents
  @staticmethod
  def crossover(parent_1, parent_2):
    # Make parent_1 the better preforming of the parents
    if parent_2.fitness > parent_1.fitness:
      # Swap
      parent_1, parent_2 = parent_2, parent_1
    
    # Get genomes
    genome_1 = parent_1.genome
    genome_2 = parent_2.genome
    
    # List of edge data - makes cloning easier
    # [[in_node_id, out_node_id, active, weight]]
    child_edges_data = []
    '''
    With genome_1 being that of the fitter of the two parents, crossover is defined as follows:
    - If both parents have a gene (edge), it is inherited from either parent with a 50% chance. 
    - If the edge was disabled in either parent, there is a 75% chance it will be disabled in the child. 
    - If genome_1 has excess or disjoint genes, they are also inherited.
    '''
    for edge in genome_1.edges:
      if genome_2.has_matching(edge):
        # Has matching edge
        matching_edge = genome_2.get_matching(edge) 

        # Randomly select parent to give edge
        rand = random.uniform(0, 1) 
        new_edge_data = Edge.data(edge) if rand > 0.5 else Edge.data(matching_edge) # See edge.py for format

        if not edge.active or not matching_edge.active:
          # Determine state of new edge
          rand = random.uniform(0, 1)
          # new_edge_data[2] holds edge state
          if rand < 0.75:
            new_edge_data[2] = False 
          else:
            new_edge_data[2] = True
        child_edges_data.append(new_edge_data)
      else:
        # Excess or disjoint gene
        new_edge_data = Edge.data(edge)
        child_edges_data.append(new_edge_data)
    
    # Create clone
    child = Genome.clone_from_edges_data(child_edges_data)
    return child
  
  # Deep copy of genome
  @staticmethod
  def clone(genome):
    # List of edge data - makes cloning easier
    # [[in_node_id, out_node_id, active, weight]]
    edges_data = []
    for edge in genome.edges:
      edge_data = Edge.data(edge)
      edges_data.append(edge_data) 

    clone = Genome.clone_from_edges_data(edges_data)
    return clone
  
  # Create genomes from edge data - listof [in_node_id, out_node_id, active, weight]
  @staticmethod
  def clone_from_edges_data(edges_data):
    clone = Genome(initialize_nodes=False)
    # Collect id's of all nodes used - edge_data[0]: in_node_id, edge_data[0]: out_node_id
    node_ids = set([edge_data[0] for edge_data in edges_data] + 
                   [edge_data[1] for edge_data in edges_data])
    # Create nodes
    nodes = [Node(_id) for _id in node_ids]

    # Create all edges and add edges to nodes
    edges = []
    for in_node_id, out_node_id, active, weight in edges_data:
      # Get nodes - O(n), can be improved
      in_node = next((node for node in nodes if node._id == in_node_id))
      out_node = next((node for node in nodes if node._id == out_node_id))

      # Create edge 
      edge = Edge(in_node, out_node, active, weight)

      # Add edge to nodes
      in_node.add_edge(edge)
      out_node.add_edge(edge)

      edges.append(edge)

    # Update child genome with edges and nodes 
    clone.set_edges(edges)
    clone.set_nodes(nodes)
    
    return clone 
