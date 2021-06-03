# Records the history of new edges

class EdgeHistory():
  '''
  global_inv: Innovation number of the next new edge
  edges: Edges added in current generation update 
  '''
  global_inv = 0
  edges = [] # (in_node_id, out_node_id, innovation_number)

  # Clear edges (new generation) 
  @staticmethod
  def new_generation():
    EdgeHistory.edges = []
  
  # Get innovation number of new edge 
  # Returns -1 if new
  @staticmethod
  def get_innovation_number(in_node, out_node):
    in_node_id = in_node._id
    out_node_id = out_node._id
    for edge in EdgeHistory.edges:
      if edge[0] == in_node_id and edge[1] == out_node_id:
        # Return innovation number
        return edge[1] 
    # New edge
    return -1
  
  # Add new edge - stores information and increments global_inv
  # Returns previous global_inv (see edge.py for use)
  @staticmethod
  def add_edge(in_node, out_node):
    in_node_id = in_node._id
    out_node = out_node._id
    # Add edge
    EdgeHistory.edges.append([(in_node_id, out_node_id, EdgeHistory.global_inv)])
    # Increment global_inv
    EdgeHistory.global_inv += 1
    return EdgeHistory.global_inv - 1
