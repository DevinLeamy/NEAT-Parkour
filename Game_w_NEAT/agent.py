from player import Player
from agent_input import Input
from genome import Genome
from feedforward import Feedforward
from enums import Move
import random 

class Agent():
  '''
  genome: Agent's genome
  '''
  def __init__(self, genome=None):
    self.genome = genome
    self.fitness = 0 
    self.adjusted_fitness = 0
    self.player = Player() 
    
    if self.genome == None:
      self.genome = Genome()
  
  # Agent policy
  def policy(self, game_map):
    # return random.choice(range(4)) # For testing
    # Collection inputs and convert to an array
    inputs = self.player.measure(game_map)
    input_arr = inputs.as_array()

    # Create NN (phenotype) based on nodes and edges (genotype)
    NN = Feedforward(self.genome.nodes)
    # Feed input
    move = NN.feedforward(input_arr)

    # Translate output to more degestible enums
    if move == 0:
      return Move.RUN 
    elif move == 1:
      return Move.JMP
    elif move == 2:
      return Move.SLD
    else:
      return Move.ATK

  # Update agent
  # game_map: Map.grid 
  def update(self, game_map, score):
    # Only active players must be updated
    if not self.player.alive:
      return 

    # Use genome-determined policy 
    move = self.policy(game_map)

    # Make move and update
    self.player.move(game_map, move)
    self.player.update(game_map)

    # Update fitness
    self.fitness = score
  
  # Update adjusted fitness
  # Assumes speciation has just taken place 
  # members_cnt: Number of members in the same species of self
  def update_adjusted_fitness(self, members_cnt):
    assert members_cnt != 0
    self.fitness /= members_cnt
  
  # Copy of agent - only genome is copied, remaining values are defaults
  @staticmethod
  def clone(agent):
    genome = Genome.clone(agent.genome)
    clone = Agent(genome)
    return clone


