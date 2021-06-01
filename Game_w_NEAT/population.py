# Controller of all members of the population
class Population():
  '''
  size: Initial population size
  generation: Generation the population was created
  '''
  def __init__(self, size, generation=0):
    self.size = size
    self.generation = generation