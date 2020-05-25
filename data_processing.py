import numpy as np


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
    # Get t, S, I, R data from first time step
    first_time, first_dict_of_states = data_list[0].summary()
    times_ll = [first_time]
    susceptible_ll = [first_dict_of_states['S']]
    infected_ll = [first_dict_of_states['I']]
    recovered_ll = [first_dict_of_states['R']]

    # For next time steps, get data, but delete first element of each time step to fix "recovered bug"
    for data in data_list[1:]:
        times, dict_of_states = data.summary()

        # Append each time's data to appropriate list
        times_ll.append(np.delete(times, 0))
        susceptible_ll.append(np.delete(dict_of_states['S'], 0))  # Deletes first element because of "recovered bug"
        infected_ll.append(np.delete(dict_of_states['I'], 0))
        recovered_ll.append(np.delete(dict_of_states['R'], 0))

    # Aggregate quantities into single lists
    t, S, I, R = aggregate_quantity(times_ll), aggregate_quantity(susceptible_ll), \
                 aggregate_quantity(infected_ll), aggregate_quantity(recovered_ll)

    # Calculate deaths
    R, D = calculate_deaths(R, death_rate)

    return t, S, I, R, D


# Helper Functions
def aggregate_quantity(list_of_lists):
    """Concatenates list of numpy arrays."""
    return np.concatenate(list_of_lists)


def calculate_deaths(R, death_rate):
    """Says percent of recovered individuals at each time step actually die, and updates R."""
    D = R * death_rate
    R = R - D
    return R, D
