import EoN
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random


def recalibrate_graph(G, infected_list, recovered_list, birth_number, release_number, p):
    """Updates graph by adding new inmates and removing released inmates.

    Args:
        G: a Networkx graph
        infected_list: list of infected nodes
        recovered_list: list of recovered nodes
        birth_number: # of inmates added at each time step
        release_number: # of inmates to release
        p: probability of contact between inmate and other inmates

    Returns:
        G: Networkx graph with new inmates added and released inmates removed
        infected_list: infected_list with released inmates removed
        recovered_list: recovered_list with released inmates removed
    """
    G, infected_list, recovered_list = remove_nodes(G, infected_list, recovered_list, release_number)
    G = add_nodes(G, birth_number, p)
    return G, infected_list, recovered_list


def remove_nodes(G, infected_list, recovered_list, release_number):
    """Randomly removes release_number nodes from G and updated infected and recovered lists."""
    release_list = random.sample(list(G.nodes), release_number)
    for x in release_list:
        G.remove_node(x)

        # Remove released inmates from infected and recovered lists
        if x in infected_list:
            infected_list.remove(x)
        if x in recovered_list:
            recovered_list.remove(x)

    return G, infected_list, recovered_list


def add_nodes(G, birth_number, p):
    """Adds birth_number inmates to G, with probability p of an edge forming between new node and each existing node."""
    for i in range(birth_number):  # assuming we're adding susceptible new nodes
        G.add_node((list(G.nodes)[-1]) + 1)  # Make sure node ID doesn't already exist

        # Connect new node to existing nodes
        for x in G.nodes:
            if random.random() < p:  # add edge with certain probability (G(n,p) model edge generation for new node)
                G.add_edge(list(G.nodes)[-1], x)
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


def aggregate_quantity(list_of_lists):
    """Concatenates list of numpy arrays."""
    return np.concatenate(list_of_lists)


def calculate_deaths(R, death_rate):
    """Says percent of recovered individuals at each time step actually die, and updates R."""
    D = R * death_rate
    R = R - D
    return R, D
