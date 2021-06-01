import random

# Controlles a species
class Species():
  '''
  gen_created: Generation when the species was created
  members: Initial members in the species
  '''
  def __init__(self, gen_created, members):
    # There must be at least one member
    assert len(members) != 0
 
    self.gen_created = gen_created
    self.members = members
      # Fitness of the species
    self.fitness = None
    self.adjusted_fitness = None
 
    self.gen_last_improved = self.gen_created

    # Select random member to be the representative
    self.representative = random.choice(self.members)