# Enums
class Level():
  GRND = 8 
  
class Move():
  RUN = 0
  JMP = 1
  SLD = 2
  ATK = 3
  FALL = 4

class Color():
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  GREY = (230, 230, 230)

class Tile():
  GRASS = "Tiles/GrassMid.png"
  DIRT = "Tiles/Dirt.png"
  WALL = "Tiles/Crate.png"
  HARD = "Tiles/Stone.png"
  AIR = "Tiles/Air.png"

  GRASS_ID = 0
  DIRT_ID = 1
  WALL_ID = 2
  HARD_ID = 3
  AIR_ID = 4

class Ob():
  WALL = 0
  THARD = 1
  BHARD = 2

class State():
  RUNNING = -1
  OVER = -2 
