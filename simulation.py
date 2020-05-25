import networkx as nx
import EoN
import matplotlib.pyplot as plt
import numpy as np
from functions import *


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


def process_data(data_list, death_rate: float):
    """Processes raw simulation loop data list into plottable times, S, I, and R arrays.

    Args:
        data_list: list of Simulation_Investigation objects as output by simulation
        death_rate: percent of recovered inmates that actually die

    Returns:
        t: array of times at which events occur
        S: # of susceptible inmates at each time step
        I: # of infected inmates at each time step
        R: # of recovered inmates at each time step
        D: # of dead inmates at each time step
    """
    times_l = []
    susceptible_ll = []
    infected_ll = []
    recovered_ll = []

    # Get t, S, I, R data from data_list and correct them
    for data in data_list:
        times, dict_of_states = data.summary()

        # Append each time's data to appropriate list
        times_l.append(np.delete(times, 0))
        susceptible_ll.append(np.delete(dict_of_states['S'], 0))  # Deletes first element because of "recovered bug"
        infected_ll.append(np.delete(dict_of_states['I'], 0))
        recovered_ll.append(np.delete(dict_of_states['R'], 0))

    # Aggregate quantities into single lists
    t, S, I, R = aggregate_quantity(times_l), aggregate_quantity(susceptible_ll), \
                 aggregate_quantity(infected_ll), aggregate_quantity(recovered_ll)

    # Calculate deaths
    R, D = calculate_deaths(R, death_rate)

    return t, S, I, R, D
