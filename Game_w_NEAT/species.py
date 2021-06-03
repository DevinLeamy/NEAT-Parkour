import random

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
      
    # Total sum of member fitnesses
    total_fitness = sum([agent.fitness for agent in self.members])

    # Update adjusted/average fitness
    self.average_fitness = total_fitness / len(self.members)
  
