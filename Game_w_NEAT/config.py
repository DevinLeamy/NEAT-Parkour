from enums import Ob

# Constants
W = 1080 # Widths of the screen in pixels
H = 800 # Height of the screen in pixels
BLOCKS = 18 # Number of blocks shown at once
BLOCK_SZ = int(W / BLOCKS) # Blocks width and height in pixels
DELAY = 30 # Millisecond delay between frames
GENERATIONS = 1000 # Number of generation
POPULATION = 1000 # Size of the population
SEED = 7 # Seem for random - to make training repeatable
INPUT_NODES = 6 # Number of input nodes
OUTPUT_NODES = 4 # Number of output nodes
MAX_STALENESS = 15 # Max number of generations a species can go without improvement
UPDATES_PER_INC = 30000 # Number of updates before a speed increase
 
OBSTACLES = [Ob.WALL, Ob.THARD, Ob.BHARD]

from image_loader import ImageLoader
LOAD = ImageLoader()