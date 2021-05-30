from player import Player
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
  
  def get_fitness(self, recalculate=False):
    if (recalculate or (not recalculate and self.fitness == -1)):
      # Calculate fitness
      pass




