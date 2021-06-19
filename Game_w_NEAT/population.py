from agent import Agent
from species import Species
import math
from config import MAX_STALENESS, BATCH_SZ, CHAMP_CUTOFF

# Controller of all members of the population
class Population():
  '''
  size: Initial population size
  generation: Generation the population was created
  '''
  def __init__(self, size):
    self.generation = 1 
    
    # Initialize population members
    self.members = []
    for i in range(size):
      self.members.append(Agent())
    
    # Initialize batches
    self.batches = []
    self.current_batch = 0
    self.batch()
    
    # Initialize species
    self.species = []

    # Player with the highest fitness
    self.best_agent = Agent.clone(self.members[0])
    # Best agent from each generation
    self.best_agents = [] 
    # Index of currently highlighted agent in best_agents
    self.highlight = 0 

    # Sum of all species average fitnesses
    self.species_average_sum = 0  
  
  # Update the players in the current batch
  def update(self, game_grid, score):
    for agent in self.get_batch():
      agent.update(game_grid, score)
  
  # Determine if current batch has active members
  def has_active(self):
    for agent in self.get_batch():
      if agent.player.alive:
        return True 
    # All members of the population are inactive 
    return False
  
  # Update best player
  def update_best_agent(self):
    assert len(self.species[0].members) != 0
    # Best agent in current generation
    generation_best = self.species[0].members[0] # Random member

    # Compare all agents
    for species in self.species:
      for agent in species.members:
        if agent.fitness > generation_best.fitness:
          generation_best = agent
    
    # Store generation best
    self.best_agents.append(Agent.clone(generation_best, copy_fitness=True))

    if generation_best .fitness > self.best_agent.fitness:
      # Replace current best agent 
      self.best_agent = Agent.clone(generation_best, copy_fitness=True)
  
  # Prune stale species
  def prune_stale_species(self):
    keep = lambda species: species.staleness < MAX_STALENESS
    self.species = [species for species in self.species if keep(species)]
  
  # Prune low preforming species - species that won't produce offspring
  def prune_low_preforming_species(self):
    pop_size = self.get_population_size()
    keep = lambda species: species.offspring_cnt(pop_size, self.species_average_sum) > 0
    self.species = [species for species in self.species if keep(species)] 
  
  # Prune empty species
  def prune_dead_species(self):
    keep = lambda species: len(species.members) > 0
    self.species = [species for species in self.species if keep(species)] 
  
  # Prune week species
  def prune_species(self):
    self.prune_low_preforming_species() 
    self.prune_stale_species()
    self.prune_dead_species()
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
    
    self.update_species_averages_sum()
    self.prune_species()
    self.update_species_averages_sum() # Average may have changed

    # Sort
    self.sort_species()

  # Natural selection - prepare for next generation
  # Assumes the fitness of all agents has been calculated
  def natural_selection(self):
    self.speciate()
    self.update_best_agent()
  
    # Agents for next generation
    offspring = []

    pop_size = self.get_population_size()
    for species in self.species:
      # if len(species.members) >= CHAMP_CUTOFF:
      #   # Fittest member moves on unchanged
      #   offspring.append(Agent.clone(species.best_agent))
      # Add offspring
      offspring.extend(species.offspring(pop_size, self.species_average_sum))
  
    # Replace population with offspring
    print("Number of offspring: %d" % len(offspring))
    self.members = offspring

    # Group members into training batches
    self.batch() 

    # Update generation
    self.generation += 1

  # Update species averages sum
  def update_species_averages_sum(self):
    self.species_average_sum = sum([species.average_fitness for species in self.species])
  
  # Calculate population size
  def get_population_size(self):
    return sum([len(species.members) for species in self.species]) 
  
  # Sort species by their average fitness 
  def sort_species(self, decreasing=True):
    self.species.sort(key=lambda species : species.best_fitness, reverse=decreasing)
  
  # Increase game speed for batch
  def increase_speed(self):
    for agent in self.get_batch():
      agent.player.increase_speed()
  
  # Get fitness of best agent
  def get_best_fitness(self):
    return self.best_agent.fitness
  
  # Distribute population into batchs
  def batch(self):
    # Group members into training batches
    batch_cnt = math.ceil(len(self.members) / BATCH_SZ) 
    self.batches = [[] for i in range(batch_cnt)]
    self.current_batch = 0

    # Distribute agents
    for idx, agent in enumerate(self.members):
      assert len(self.batches[idx % batch_cnt]) <= BATCH_SZ
      self.batches[idx % batch_cnt].append(agent)  

  # Get current batch
  def get_batch(self):
    if self.current_batch >= len(self.batches):
      # Out of range
      return []
    return self.batches[self.current_batch] 

  # Update current batch
  def update_batch(self):
    self.current_batch += 1
  
  # Update currently highlighted agent - return True if the game needs to reset
  def update_highlight(self, game_grid, game_score):
    agent = self.get_highlight()
    if not agent.alive():
      self.highlight += 1
      self.generation += 1 # Generation of current highlight
      return True

    if self.highlights_done():
      return False
    self.best_agents[self.highlight].update(game_grid, game_score)
    return False
  
  # Get currently highlighted agent 
  def get_highlight(self):
    if self.highlights_done():
      return False
    return self.best_agents[self.highlight]
  
  # Check if highlights are done
  def highlights_done(self):
    return self.highlight >= len(self.best_agents)
  
  # Reset generation
  def reset_generation(self):
    self.generation = 1