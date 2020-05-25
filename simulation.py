import EoN
import random


def simulation(G, tau, gamma, initial_infected, max_time, release_time, release_number, birth_number, p):
    """Runs a simulation on SIR model.

    Args:
        G: Networkx graph
        tau: transmission rate
        gamma: recovery rate
        initial_infected: list of nodes that are initially infected
        max_time: # of time steps to run simulation
        release_time: time step at which to release inmates
        release_number: # of inmates to release
        birth_number: # of inmates added at each time step
        p: probability of contact between inmate and other inmates

    Returns:
        data_list: list of Simulation_Investigation objects from each time step of simulation
    """
    infected_list = initial_infected
    recovered_list = []
    data_list = []

    # Loop over time
    for i in range(max_time):
        # Run simulation
        data = EoN.fast_SIR(G, tau, gamma, initial_infecteds=infected_list, initial_recovereds=recovered_list, \
                            tmin=i, tmax=i + 1, return_full_data=True)
        data_list.append(data)

        # Update infected and recovered node lists
        infected_list, recovered_list = get_infected(data, i + 1), get_recovered(data, i + 1)

        # Add and remove nodes
        #     if len(infected_list) < number_of_infected_before_releases: # Only start inmate releases after some time
        #         r_n = 0
        #     else:
        #         r_n = release_number
        if i == release_time - 1:  # Only release inmates once, at release_time
            r_n = release_number
        else:
            r_n = 0
        G, infected_list, recovered_list = recalibrate_graph(G, infected_list, recovered_list, birth_number, r_n, p)

    return data_list


# Helper Functions
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





