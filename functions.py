import EoN
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# globals, per day cases
birth_rate = 50
release_rate = 50
death_rate = 0.2 # % of recovered

def recalibrate_graph(G,recov_list,infect_list):
  G_new = add_nodes(remove_nodes(G))
  return G_new
  
def remove_nodes(G):
  # take all recovered and delete $death_rate$ fraction of them
  # take all nodes and delete $release_rate$ many of them
  return G

def add_nodes(G):
  for i in range(birth_rate): # assuming we're adding susceptible
    G.add_node()
  return G

def get_infected(data: EoN.Simulation_Investigation, end_time: int, state: char) -> List[int]:
  '''Returns list of infected nodes.'''
  return get_type_of_nodes(data, end_time, 'I')

def get_recovered(data: EoN.Simulation_Investigation, end_time: int, state: char) -> List[int]:
  '''Returns list of recovered nodes.'''
  return get_type_of_nodes(data, end_time, 'R')

def get_type_of_nodes(data: EoN.Simulation_Investigation, end_time: int, state: char) -> List[int]:
  '''Returns list of certain type of nodes.'''
  return [node for (node, state) in data.get_statuses(time=end_time).items() if state == state]


