import EoN
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# globals, per day cases
birth_number = 50
release_number = 50
death_rate = 0.2  # % of recovered


def recalibrate_graph(G, infect_list, recov_list):
    G_new, new_infect_list, new_recov_list = remove_nodes(G, infect_list, recov_list, release_number)
    G_new = add_nodes(G, birth_number)
    return G_new, new_infect_list, new_recov_list


def remove_nodes(G, infect_list, recov_list, release_number):
    release_list = random.sample(list(G.nodes), release_number)
    for x in release_list:
        G.remove_node(x)
        if x in recov_list:
            recov_list.remove(x)
        if x in infect_list:
            infect_list.remove(x)

    return G, infect_list, recov_list


def add_nodes(G, birth_number):
    for i in range(birth_number):  # assuming we're adding susceptible new nodes
        G.add_node((list(G.nodes)[-1]) + 1)
    return G


def get_infected(data: EoN.Simulation_Investigation, end_time: int):
    """Returns list of infected nodes."""
    return get_type_of_nodes(data, end_time, 'I')


def get_recovered(data: EoN.Simulation_Investigation, end_time: int):
    """Returns list of recovered nodes."""
    return get_type_of_nodes(data, end_time, 'R')


def get_type_of_nodes(data: EoN.Simulation_Investigation, end_time: int, state: str):
    """Returns list of certain type of nodes."""
    return [node for (node, s) in data.get_statuses(time=end_time).items() if s == state]
