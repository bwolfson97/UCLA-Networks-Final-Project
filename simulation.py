import networkx as nx
import EoN
import matplotlib.pyplot as plt
import numpy as np
from functions import *


def process_data(data_list, death_rate):
    """Processes raw simulation loop data list into plottable times, S, I, and R arrays."""
    times_l = []
    susceptible_ll = []
    infected_ll = []
    recovered_ll = []

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
