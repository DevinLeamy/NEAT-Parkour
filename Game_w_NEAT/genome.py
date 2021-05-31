from gene import Gene 

'''
in_nodes: Number of input nodes
out_nodes: Number of output nodes
'''

class Genome():
  def __init__(self, in_nodes=6, out_nodes=6):
    self.in_nodes = in_nodes
    self.out_nodes = out_nodes

    # Initialize input nodes and output nodes
    

  # Get upper bound on genes innovation numbers
  # Used to determine whether genes are disjoint or excess
  # def get_max_inv(self):
  #   _max = 0
  #   for gene in self.genes:
  #     _max = max(_max, gene.inv)
  #   return _max

  # Determine if given gene has a matching gene 
  # def has_matching(self, gene: Gene):
  #   for self_gene in self.genes:
  #     if gene.match(self_gene):
  #       return True
  #   return False
  
  # # Find matching gene of given gene, if it exists
  # def get_matching(self, gene: Gene):
  #   for self_gene in self.genes:
  #     if gene.match(self_gene):
  #       return self_gene
  #   # Matching gene does not exist
  #   return None