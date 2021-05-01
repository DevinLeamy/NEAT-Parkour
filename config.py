from enums import Ob

# Constants
W = 1080
H = 800
BLOCKS = 18 
BLOCK_SZ = int(W / BLOCKS)
DELAY = 30 
 
OBSTACLES = [Ob.WALL, Ob.THARD, Ob.BHARD]

from image_loader import ImageLoader
LOAD = ImageLoader()