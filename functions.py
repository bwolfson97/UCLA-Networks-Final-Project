import EoN
import numpy as np
import matplotlib as plt

# globals, per day cases
birth_rate = 50
release_rate = 50
death_rate = 0.2 # % of recovered

def recalibrate_graph(data):
  newdata = add_nodes(remove_nodes(data))
  return newdata
  
def remove_nodes(data):
  # take all recovered and delete $death_rate$ fraction of them
  # take all nodes and delete $release_rate$ many of them
  return data

def add_nodes(data):
  # add $birth_rate$ many susceptible nodes
  return data

