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
    self.best_agent = Agent.clone(self.members[0])

    # Sum of all species average fitnesses
    self.species_average_sum = 0  
  
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
    current_gen_best = self.species[0].members[0] # Random member

    # Compare all agents
    for species in self.species:
      for agent in species.members:
        if agent.fitness > current_gen_best.fitness:
          current_gen_best = agent
    
    if (current_gen_best.fitness > self.best_agent.fitness):
      # Replace current best agent 
      self.best_agent = Agent.clone(current_gen_best)
  
  # Prune stale species
  def prune_stale_species(self):
    for species in self.species:
      if species.staleness >= 15: # TODO: Make this variable configurable
        # Remove species
        self.species.remove(species)
  
  # Prune low preforming species - species that won't produce offspring
  def prune_low_preforming_species(self):
    pop_size = self.get_population_size()
    for species in self.species:
      if species.calculate_offstring_count(pop_size, self.species_average_sum) == 0:
        # No offspring
        self.species.remove(species)
  
  # Prune week species
  def prune_species(self):
    self.prune_stale_species()
    self.prune_low_preforming_species()
    # Average sum may have changed
    self.update_species_averages_sum()
  
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
    self.update_species_averages_sum()

  # Natural selection - prepare for next generation
  # Assumes the fitness of all agents has been calculated
  def natural_selection(self):
    self.speciate()
    self.prune_species()
    self.update_best_agent()
  
    # Agents for next generation
    offspring = []

    for species in self.species:
      if len(species.members) >= 5:
        # Fitest member moves on unchanged
        offspring.append(species.best_agent)
      
      pop_size = self.get_population_size()
      # Add offspring
      offspring.extend(species.offspring(pop_size, self.species_average_sum))
  
    # Replace population with offspring
    self.members = offspring

  # Update species averages sum
  def update_species_averages_sum(self):
    self.species_average_sum = sum([species.average_fitness for species in self.species])
  
  # Calculate population size
  # Note: len(self.members) may not be correct because some agents in self.members 
  #       have been either cut from their species or belong to a species that no longer exists
  def get_population_size(self):
    return sum([len(species.members) for species in self.species]) 
  
  # Sort species by their average fitness 
  def sort_species(self, decreasing=True):
    self.species.sort(key=lambda species : species.fitness, reversed=decreasing)
  

