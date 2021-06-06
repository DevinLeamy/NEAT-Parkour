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
  
  # Divide the population into species by genetic similarity
  def speciate(self):
    # Reset species for speciation - see reset() in species.py 
    for species in self.species: 
      species.reset()
    
    # Divide members by genetic similarity
    for agent in self.members:
      found_comp = False
      for species in self.species:
        if species.member(agent):
          # Agent is compatible
          species.add(agent)
          found_comp = True
          break
      if not found_comp:
        # Create new species
        self.species.append(Species(self.generation, [agent]))
    
    # Update new species
    for species in self.species:
      species.cut_half()
      species.update_fitness()
    # Sort
    self.sort_species()


  # Natural selection - prepare for next generation
  # Assumes the fitness of all agents has been calculated
  def natural_selection(self):
    pass

  # Sort species by their average fitness 
  def sort_species(self, decreasing=True):
    self.species.sort(key=lambda species : species.fitness, reversed=decreasing)
  

