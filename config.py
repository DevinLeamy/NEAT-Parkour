from enums import Ob

# Pygame
W = 1080 # Widths of the screen in pixels
H = 800 # Height of the screen in pixels

# Game
BLOCKS = 18 # Number of blocks shown at once
BLOCK_SZ = int(W / BLOCKS) # Blocks width and height in pixels
DELAY = 30 # Millisecond delay between frames
UPDATES_PER_SCORE = 10 # Number of updates per +1 score
UPDATES_PER_INC = 1000 # Number of updates before a speed increase
OBSTACLES = [Ob.WALL, Ob.THARD, Ob.BHARD] # Types of game obsticles

# NEAT
GENERATIONS = 1000 # Number of generation
POPULATION = 1000 # Size of the population
BATCH_SZ = 150 # Max number of agents in one training batch

INPUT_NODES = 6 # Number of input nodes
OUTPUT_NODES = 4 # Number of output nodes

MAX_STALENESS = 15 # Max number of generations a species can go without improvement

WEIGHT_UPPER = 1 # Max value of a weight
WEIGHT_LOWER = -1 # Minimum value of a weight

PROB_NEW_WEIGHT = 10 # Probability of generating a new weight when mutating edge
PROB_MUTATE_WEIGHTS = 80 # Probability of mutating weights 
PROB_ADD_CONNECTION = 20 # Probability of adding a connection
PROB_ADD_NODE = 3 # Probability of adding a new node
PROB_MUTATION_WITHOUT_CROSSOVER = 25 # Probability of mutation without crossover

C1 = 1.0 # Compatibility function coefficient # 1
C2 = 1.0 # Compatibility function coefficient # 2
C3 = 3.0 # Compatibility function coefficient # 3
C_THRESHOLD = 4.0 # Compatibility threshold

NORMALIZING_FACTOR_CUTOFF = 20 # Number of edges required before applying normalizing factor
CHAMP_CUTOFF = 5 # Number of members a species must have before the champ is carried over without mutation 


# Other
SEED = 1077 # Seed for random 
 

from image_loader import ImageLoader
LOAD = ImageLoader()
