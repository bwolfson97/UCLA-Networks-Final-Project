# globals, per day cases
birth_rate = 50
release_rate = 50
death_rate = 50

def recalibrate_graph(data):
  newdata = add_nodes(remove_nodes(data))
  return newdata
  
def remove_nodes(data):
  return data

def add_nodes(data):
  return data
