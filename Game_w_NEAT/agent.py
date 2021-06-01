from player import Player
from agent_input import Input
from genome import Genome

class Agent():
  # '''
  # player: Agents player, plays the game
  # genome: Agents player controller
  # fitness: Agents fitness
  # '''
  def __init__(self, genes=None):
    self.fitness = -1 
    self.player = Player() 
    self.genome = Genome(genes)
  
  # Determine agent fitness
  def fitness(self, recalculate=False):
    if not recalculate and not self.fitness == -1:
      return self.fitness
    # Calculate and return fitness
  
  # Agent policy
  def policy(self):
    inputs: Input = self.player.measure()



