from agent import Agent

# Controller of all members of the population
class Population():
  '''
  size: Initial population size
  generation: Generation the population was created
  '''
  def __init__(self, size=150, generation=0):
    self.size = size
    self.generation = generation
    
    # Initialize population members
    self.members = []
    for i in range(self.size):
      self.members.append(Agent())
    
    # Initialize species
    self.species = []
    # TODO: Initialize species

    # Player with the highest fitness
    self.best_agent = Agent.deep_copy(self.members[0])
  
  # Update the population (calls game update loop)
  def update(self, game_grid, score):
    for agent in self.members:
      agent.update(game_grid, score)
  
  # Determine if population has active members
  def has_active(self):
    for agent in self.members:
      if agent.player.alive:
        return True 
    # All members of the population are inactive 
    return False
  
  # Update best player
  def update_best_agent(self):
    # Best agent in current generation
    current_gen_best = self.members[0]
    for agent in self.members[1:]:
      if agent.fitness > current_gen_best.fitness:
        current_gen_best = agent
    
    if (current_gen_best.fitness > self.best_agent.fitness):
      # Replace current best agent 
      self.best_agent = Agent.deep_copy(current_gen_best)
  
  # Prune stale species
  def prune_stale_species(self):
    for species in self.species:
      if species.staleness >= 15: # TODO: Make this variable configurable
        # Remove species
        self.species.remove(species)
  

