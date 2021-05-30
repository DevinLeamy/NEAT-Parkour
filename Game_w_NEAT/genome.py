from gene import Gene 

class Genome():
  def __init__(self, genes=None):
    if (genes == None):
      self.genes = []
    else:
      self.genes = genes
  
  # Get upper bound on genes innovation numbers
  # Used to determine whether genes are disjoint or excess
  def get_max_inv(self):
    _max = 0
    for gene in self.genes:
      _max = max(_max, gene.inv)
    return _max

  # Determine if given gene has a matching gene 
  def has_matching(self, gene: Gene):
    for self_gene in self.genes:
      if gene.match(self_gene):
        return True
    return False
  
  # Find matching gene of given gene, if it exists
  def get_matching(self, gene: Gene):
    for self_gene in self.genes:
      if gene.match(self_gene):
        return self_gene
    # Matching gene does not exist
    return None