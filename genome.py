from edge import Edge
from node import Node
from feedforward import Feedforward
from config import * 
import random

class Genome():
  # Id of next node created
  next_id = 0
  def __init__(self, initialize_nodes=True):
    self.in_nodes_cnt = INPUT_NODES
    self.out_nodes_cnt = OUTPUT_NODES 

    self.nodes = []
    self.edges = []

    # Create input nodes
    in_nodes = []
    for i in range(self.in_nodes_cnt):
      in_nodes.append(Node(i, _input=True)) # Input node ids remain the same
    
    # Create output nodes
    out_nodes = []
    for i in range(self.out_nodes_cnt):
      out_nodes.append(Node(self.in_nodes_cnt + i, output=True)) # Output node ids remain the same

    # Store input and output nodes
    self.nodes.extend(in_nodes)
    self.nodes.extend(out_nodes)

    if not initialize_nodes: 
      return
   
    # Initialize single edge 
    in_node = random.choice(in_nodes) # Random input
    out_node = random.choice(out_nodes) # Random output

    edge = Edge(in_node, out_node, True) 

    # Add edge to edges 
    self.edges.append(edge)

    # Add edge to endpoints (nodes)
    in_node.add_edge(edge) # The utility of list is shown in feedforward.py
    out_node.add_edge(edge)
    
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
    assert len(self.edges) != 0 # Requires at least one edge

    max_inv = max([edge.inv for edge in self.edges])
    return max_inv
  
  # Add new node
  def add_node(self):
    edges = self.all_edges()

    if len(edges) == 0: # Requires at least one edge
      return

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
    new_node = Node()
    self.nodes.append(new_node)

    # Create new edges (names are to be read as relative to the new node)
    in_bound_edge = Edge(in_node, new_node, weight=1)
    out_bound_edge = Edge(new_node, out_node, weight=weight) 

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
    (in_node, out_node) = feedforward.get_random_compatible_nodes() 

    # Create new edge
    new_edge = Edge(in_node, out_node) 

    # Add edge to nodes and genome
    self.edges.append(new_edge)

    in_node.add_edge(new_edge)
    out_node.add_edge(new_edge)

  # Set edges 
  def set_edges(self, new_edges):
    self.edges = new_edges
  
  # Set nodes 
  def set_nodes(self, new_nodes):
    for node in new_nodes:
      # Check if node with node._id exists
      if self.get_node(node._id) == None:
        self.nodes.append(node) # New node

  # Get node with _id
  def get_node(self, _id):
    for node in self.nodes:
      if node._id == _id:
        return node
    return None
  
  # Mutate genome 
  def mutate(self):
    # Mutate weights 
    rand = random.uniform(0, 100)
    if rand < PROB_MUTATE_WEIGHTS:
      edges = self.all_edges()
      for edge in edges:
        edge.mutate()
    
    # Add connection
    rand = random.uniform(0, 100)
    if rand < PROB_ADD_CONNECTION:
      self.add_connection()
    
    # Add node
    rand = random.uniform(0, 100)
    if rand < PROB_ADD_NODE:
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
    if N <= NORMALIZING_FACTOR_CUTOFF:
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
    comp = (C1 * E) / N + (C2 * D) / N + (C3 * W)
    return comp

  # Determine if genes are compatible - i.e. of the same species
  @staticmethod
  def compatible(gene_1, gene_2):
    return Genome.compatibility(gene_1, gene_2) <= C_THRESHOLD 
   
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
    # Collect id's of all nodes used - edge_data[0]: in_node_id, edge_data[1]: out_node_id
    node_ids = set([edge_data[0] for edge_data in edges_data] + 
                   [edge_data[1] for edge_data in edges_data])

    # Create and set nodes
    nodes = [Node(_id) for _id in node_ids] 
    clone.set_nodes(nodes)

    # Create all edges and add edges to nodes
    edges = []
    for in_node_id, out_node_id, active, weight in edges_data:
      in_node = clone.get_node(in_node_id) 
      out_node = clone.get_node(out_node_id) 

      # Create edge 
      edge = Edge(in_node, out_node, active, weight)

      # Add edge to nodes
      in_node.add_edge(edge)
      out_node.add_edge(edge)

      edges.append(edge)

    # Update child genome edges 
    clone.set_edges(edges)
    return clone 
