from player import Player
from agent_input import Input
from genome import Genome
from feedforward import Feedforward
from enums import Move
import random 

class Agent():
  def __init__(self):
    self.fitness = 0 
    self.player = Player() 
    self.genome = Genome()
  
  # Agent policy
  def policy(self):
    return random.choice(range(4)) # For testing
    # Collection inputs and convert to an array
    inputs = self.player.measure()
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
    move = self.policy()

    # Make move and update
    self.player.move(game_map, move)
    self.player.update(game_map)

    # Update fitness
    self.fitness = score
  
  # Deep copy of agent
  @staticmethod
  def deep_copy(agent):
    pass


