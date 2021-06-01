# I believe this file can be deleted

from genome import Genome
from agent import Agent
from gene import Gene
import random

# Responsible for training all the agents
class NEAT():
  '''
  c1, c2, c3: From coefficents of compability function
  c_thresh: Compatibility threshold 
  species: List of all agents, seperated by species 
  initial_pop: In initial number of agents
  '''
  # Increase intial_pop to 1000 if it's not successful
  # Increase c3 to 3.0 to allow for finer distinctions between species base on weight differences
  # If c3 is increased, increase c_threshold to 4.0
  def __init__(self, c1=1.0, c2=1.0, c3=0.4, c_threshold=3.0, initial_pop=150): 
    self.c1 = c1
    self.c2 = c2
    self.c3 = c3
    self.c_threshold = c_threshold
    self.species = []

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
  
  # Determine if two agents are compatible - i.e. of the same species
  def compable(self, agent1: Agent, agent2: Agent):
    return self.compatibility(agent1, agent2) <= self.c_threshold
  
  # Update species
  def update_species(self, offspring):
    # Species representative agents 
    species_reps = [random.choice(species) for species in self.species]
    new_species = [[] for i in range(len(self.species))]
    for agent in offsping:
      found_match = False
      for idx, rep in enumerate(species_reps):
        if self.compable(agent, rep):
          found_match = True
          new_species[idx].append(agent)
      if not found_match:
        # Create new species and set representative
        species_reps.append(agent)
        new_species.append([agent])

      