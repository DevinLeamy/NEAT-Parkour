from enums import Ob

# Constants
W = 1080 # Widths of the screen in pixels
H = 800 # Height of the screen in pixels
BLOCKS = 18 # Number of blocks shown at once
BLOCK_SZ = int(W / BLOCKS) # Blocks width and height in pixels
DELAY = 30 # Millisecond delay between frames
GENERATIONS = 100 # Number of generation
POPULATION = 200 # Size of the population
SEED = 103 # Seem for random - to make training repeatable
 
OBSTACLES = [Ob.WALL, Ob.THARD, Ob.BHARD]

from image_loader import ImageLoader
LOAD = ImageLoader()