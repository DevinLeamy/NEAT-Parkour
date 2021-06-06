import random
import math
from genome import Genome

# Controlles a species
class Species():
  '''
  gen_created: Generation when the species was created
  members: Initial members in the species
  '''
  def __init__(self, gen_created, members):
    # There must be at least one member
    assert len(members) != 0
 
    self.members = members
    # Fitness of the species
    self.best_fitness = 0 
 
    # Number of generations since last improvement 
    self.staleness = 0 

    # Select random member to be the representative
    self.representative = random.choice(self.members)
  
  # Add agent to species
  def add(self, agent):
    self.members.append(agent)
  
  # Update species fitness (called once every generation)
  def update_fitness(self): 
    assert len(self.members) != 0

    # Update best fitness
    previous_best = self.best_fitness
    self.best_fitness = max(self.best_fitness, max([agent.fitness for agent in self.members]))

    # Update stateless
    if self.best_fitness > previous_best:
      # Improved
      self.staleness = 0
    else:
      self.stateless += 1
    
    # Fitness sharing 
    for agent in self.members:
      agent.update_adjusted_fitness()
      
    # Total sum of member fitnesses
    total_fitness = sum([agent.fitness for agent in self.members])

    # Update adjusted/average fitness
    self.average_fitness = total_fitness / len(self.members)
  
  # Determine if given agent is a member of the species
  def member(self, agent):
    # Agent is member if they are compatible with the species representative
    return Genome.compatible(self.representative.genome, agent.genome)
  
  # Selects a random representative, clear all members and resets fitness
  def reset(self):
    # Select representative
    self.representative = random.choice(self.members)
    # Clear members and reset fitness
    self.members = []
  
  # Sort members by their average fitness 
  def sort_members(self, decreasing=True):
    self.members.sort(key=lambda member : member.fitness, reversed=decreasing)
  
  # Removes the lowest preforming 50% - not sure whether this figure is comming from
  def cut_half(self):
    self.sort_members()
    half = math.ceil(len(self.members) / 2) # Rounded up
    self.members = self.members[:half]


  
