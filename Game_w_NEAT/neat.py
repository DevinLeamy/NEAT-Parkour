from genome import Genome
from agent import Agent
from gene import Gene

# Responsible for training all the agents
class NEAT():
  '''
  agents: All the candidates 
  '''
  def __init__(self, c1=1, c2=1, c3=1):
    self.c1 = c1
    self.c2 = c2
    self.c3 = c3


  # Measures compatibility of different genomes
  def compatibility(self, parent1: Agent, parent2: Agent):
    genome1 = parent1.genome
    genome2 = parent2.genome
    
    # Normalizing factor 
    N = max(len(genome1.genes), len(genome2.genes))
    if N <= 20:
      N = 1

    max1 = genome1.get_max_inv()
    max2 = genome2.get_max_inv()

    # Number of excess and disjoint genes between parents
    E = 0
    D = 0
    for gene in genome1.genes:
      if genome1.has_matching(gene):
        pass
      if gene.inv <= max1:
        D += 1
      else:
        E += 1

    for gene in genome2.genes:
      if genome2.has_matching(gene):
        pass
      if gene.inv <= max1:
        D += 1
      else:
        E += 1

    # Calculate average weight distance of matching genes
    # Total weight distance and matching genes count
    total_wd = 0
    total_mc = 0
    for gene in genome1.genes:
      matching_gene = genome2.get_matching(gene)
      if matching_gene == None:
        continue
      total_mc += 1
      total_wd += abs(matching_gene.weight - gene.weight)
    
    # Average weight distance
    W = total_wd / total_mc
    
    # Compatibilty
    comp = (self.c1 * E) / N + (self.c2 * D) / N + (self.c3 * W)
    return comp 
    
  # Determine if a pair of genes are matching
  def match(self, gene1: Gene, gene2: Gene):
    # Check for matching innovation numbers
    return gene1.inv == gene2.inv
    