from player import Player
from agent_input import Input
from genome import Genome

class Agent():
  # '''
  # player: Agents player, plays the game
  # genome: Agents player controller
  # fitness: Agents fitness
  # in_nodes: Number of input nodes
  # out_nodes: Number of output nodes
  # '''
  def __init__(self, genes=None, in_nodes=6, out_nodes=4):
    self.fitness = -1 
    self.player = Player() 
    self.genome = Genome(genes)
    self.in_nodes = in_nodes
    self.out_nodes = out_nodes
  
  # Determine agent fitness
  def fitness(self, recalculate=False):
    if not recalculate and not self.fitness == -1:
      return self.fitness
    # Calculate and return fitness
  
  # Agent policy
  def policy(self):
    inputs: Input = self.player.measure()



