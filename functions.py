import EoN
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# globals, per day cases
birth_rate = 50
release_number = 50
death_rate = 0.2  # % of recovered


def recalibrate_graph(G, recov_list, infect_list):
    G_new, new_recov_list, new_infect_list = remove_nodes(G, recov_list, infect_list)
    G_new = add_nodes(G)
    return G_new, new_recov_list, new_infect_list


def remove_nodes(G, recov_list, infect_list):
    deaths = len(recov_list) * death_rate  # deaths
    death_list = random.sample(recov_list, deaths)
    for x in death_list:
        G.remove_node(x)
        recov_list.remove(x)

    release_list = random.sample(list(G.nodes), release_number)
    for x in release_list:
        G.remove_node(x)
        if x in recov_list:
            recov_list.remove(x)
        if x in infect_list:
            infect_list.remove(x)

    return G, recov_list, infect_list


def add_nodes(G):
    for i in range(birth_rate):  # assuming we're adding susceptible new nodes
        G.add_node((list(G.nodes)[-1]) + 1)


def get_infected(data: EoN.Simulation_Investigation, end_time: int):
    """Returns list of infected nodes."""
    return get_type_of_nodes(data, end_time, 'I')


def get_recovered(data: EoN.Simulation_Investigation, end_time: int):
    """Returns list of recovered nodes."""
    return get_type_of_nodes(data, end_time, 'R')


def get_type_of_nodes(data: EoN.Simulation_Investigation, end_time: int, state: str):
    """Returns list of certain type of nodes."""
    return [node for (node, s) in data.get_statuses(time=end_time).items() if s == state]
