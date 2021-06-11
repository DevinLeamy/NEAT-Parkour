import random
import math
from genome import Genome
from agent import Agent

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
    self.average_fitness = 0

    # Number of generations since last improvement 
    self.staleness = 0 

    # Select random member to be the representative
    self.representative = random.choice(self.members)

    # Select random agent to start as best
    self.best_agent = random.choice(self.members)
  
  # Add agent to species
  def add(self, agent):
    self.members.append(agent)
  
  # Update species fitness (called once every generation)
  def update_fitness(self): 
    assert len(self.members) != 0

    # Update best fitness
    previous_best = self.best_fitness
    self.best_fitness = max(self.best_fitness, max([agent.fitness for agent in self.members]))

    # Update best agent
    for agent in self.members:
      if agent.fitness == self.best_fitness:
        self.best_agent = Agent.clone(agent)
        break

    # Update staleness 
    if self.best_fitness > previous_best:
      # Improved
      self.staleness = 0
    else:
      self.staleness += 1
    
    # Fitness sharing 
    for agent in self.members:
      agent.update_adjusted_fitness(len(self.members))
      
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
    self.members.sort(key=lambda member : member.fitness, reverse=decreasing)
  
  # Removes the lowest preforming 50% - not sure whether this figure is comming from
  def cut_half(self):
    self.sort_members()
    half = math.ceil(len(self.members) / 2) # Rounded up
    self.members = self.members[:half]
  
  # Calculate the number of offspring to produce 
  # Modify?: https://github.com/CodeReclaimers/neat-python/blob/c2b79c88667a1798bfe33c00dd8e251ef8be41fa/neat/reproduction.py
  def offspring_cnt(self, pop_size, pop_average_sum):
    assert pop_average_sum != 0
    print(self.average_fitness / pop_average_sum, self.average_fitness, pop_size) # DEBUG
    # * 2 is for testing
    return int(self.average_fitness / pop_average_sum * pop_size) * 2

  # Produce offspring
  def offspring(self, pop_size, pop_average_sum):
    offspring = []
    if len(self.members) >= 5:
      # Fittest member move on unchanged
      offspring.append(Agent.clone(self.best_agent))

    # Produce offspring
    offspring_cnt = self.offspring_cnt(pop_size, pop_average_sum)
    '''
    Produce offspring
    - 25% result from mutation without crossover
    - 75% (the rest) result from the crossover from two random members of the species
    '''
    for i in range(offspring_cnt):
      rand = random.uniform(0, 1)
      if rand < 0.25:
        # Mutation without crossover
        child = Agent.clone(random.choice(self.members))
        child.genome.mutate()
        offspring.append(child)
        assert child.player.alive
      else:
        # Cross over - parents can be the same
        # Parents are not clones because their data does not change 
        parent_1 = random.choice(self.members)
        parent_2 = random.choice(self.members)

        child_genome = Genome.crossover(parent_1, parent_2) 
        child = Agent(genome=child_genome)
        offspring.append(child)
        assert child.player.alive

    return offspring




  
