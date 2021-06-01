from edge import Edge
from node import Node

class Genome():
  '''
  next_id: Id of next node created
  c1, c2, c3: Coefficients from compatibility function
  c_threshold: Compatibility threshold
  '''
  next_id = 0
  c1 = 1.0
  c2 = 1.0
  c3 = 0.4
  c_threshold = 3.0
  '''
  in_nodes: Number of input nodes
  out_nodes: Number of output nodes
  '''
  def __init__(self, in_nodes=6, out_nodes=6, c1=1.0, c2=1.0, c3=0.4, c_threshold=3.0):
    self.in_nodes = in_nodes
    self.out_nodes = out_nodes
    self.nodes = []
    self.edges = []

    # Create input nodes
    for i in range(self.in_nodes):
      self.nodes.append(Node(Genome.next_id))
      Genome.next_id += 1
    
    # Create output nodes
    for i in range(self.out_nodes):
      self.nodes.append(Node(Genome.next_id))
      Genome.next_id += 1
    
    # TODO: Edges also have to be initialized
  
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

  # Calculate compatibility of two genomes 
  @staticmethod
  def compatibility(genome_1, genome_2):
    edges_1 = genome_1.edges
    edges_2 = genome_2.edges

    # Get max innovation numbers 
    max_1 = genome_1.get_max_inv()
    max_2 = genome_2.get_max_inv()

    # Normalizing factor
    N = max(len(edges_1), len(edges_2))
    if N <= 20:
      N = 1

    # Number of excess and disjoint genes between parents
    E = 0
    D = 0
    for edge in edges_1:
      if genome_1.has_matching(edge):
        continue 
      # Increment disjoint and excess
      if edge.inv <= max_2:
        D += 1 
      else:
        E += 1

    for edge in edges_2:
      if genome_2.has_matching(edge):
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
    return comp
  
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