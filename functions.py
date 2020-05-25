import EoN
import numpy as np
import matplotlib as plt
import networkx as nx

# globals, per day cases
birth_rate = 50
release_rate = 50
death_rate = 0.2 # % of recovered

def recalibrate_graph(G):
  G_new = add_nodes(remove_nodes(G))
  return G_new
  
def remove_nodes(G):
  # take all recovered and delete $death_rate$ fraction of them
  # take all nodes and delete $release_rate$ many of them
  return G

def add_nodes(G):
  for i in range(birth_rate):
    G.add_node()
  return G

