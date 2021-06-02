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

