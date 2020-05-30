import EoN
import numpy as np


def simulation(G, tau, gamma, rho, max_time, number_infected_before_release, release_number, background_inmate_turnover,
               stop_inflow_at_intervention, p, death_rate, percent_infected, percent_recovered, social_distance,
               social_distance_tau, constant_patient_zero, patient_zero_numbers):
    """Runs a simulation on SIR model.

    Args:
        G: Networkx graph
        tau: transmission rate
        gamma: recovery rate
        rho: percent of inmates that are initially infected
        max_time: # of time steps to run simulation
        number_infected_before_release: number of infected at which to perform release on next integer time
        release_number: # of inmates to release at release intervention
        background_inmate_turnover: background # of inmates added/released at each time step
        stop_inflow_at_intervention: should we stop the background inflow of inmates at intervention time?
        p: probability of contact between inmate and other inmates
        death_rate: percent of recovered inmates that die
        percent_infected: percent of general population that is infected
        percent_recovered: percent of general population that is recovered
        social_distance: boolean flag, if we lower transmission rate after major release
        social_distance_tau: new transmission rate after major release
        constant_patient_zero: if True, then patient zero will be set to node patient_zero_number
        patient_zero_numbers: sets node number of patient zero (default is 0, this parameter is arbitrary)

    Returns:
        t: array of times at which events occur
        S: # of susceptible inmates at each time
        I: # of infected inmates at each time
        R: # of recovered inmates at each time
        D: # of dead inmates at each time step
    """
    print('Starting simulation...')
    release_occurred = False
    background_release_number = background_inmate_turnover
    data_list = []
    infected_list = []
    recovered_list = []
    delta_recovered_list = []

    if constant_patient_zero:
        infected_list.append(patient_zero_numbers)
    else:
        infected_list.append(np.random.sample(list(G.nodes), np.ceil(rho*len(G.nodes)), replace=False))

    # Loop over time
    for i in range(max_time):
        data = EoN.fast_SIR(G, tau, gamma, initial_infecteds=infected_list, initial_recovereds=recovered_list,
                                tmin=i, tmax=i + 1, return_full_data=True)
        data_list.append(data)

        # Update infected and recovered inmate lists
        infected_list, recovered_list = get_infected(data, i + 1), get_recovered(data, i + 1)

        # Check if release condition has been met
        if not release_occurred and len(infected_list) >= number_infected_before_release:
            print_release_intervention_info(i + 1, infected_list, release_number)
            r_n = background_release_number + release_number
            release_occurred = True

            # If we are stopping background inmate turnover at release intervention time
            if stop_inflow_at_intervention:
                print('\tStopping inmate inflow.')
                background_inmate_turnover = 0
            if social_distance:
                tau = social_distance_tau
        else:  # If not, use background release rate
            r_n = background_release_number

        # Add and release inmates
        G, infected_list, recovered_list, delta_recovered = recalibrate_graph(G, infected_list, recovered_list,
                                                                              background_inmate_turnover, r_n, p,
                                                                              percent_infected, percent_recovered,
                                                                              death_rate)

        # Track the number of recovered inmates added or released at each time step
        delta_recovered_list.append(delta_recovered)

    # Process raw data into t, S, I, R, D arrays
    t, S, I, R, D = process_data(data_list, delta_recovered_list, death_rate)

    print('Simulation completed.\n')
    return t, S, I, R, D


# Helper Functions
def recalibrate_graph(G, infected_list, recovered_list, birth_number, release_number, p,
                      percent_infected, percent_recovered, death_rate):
    """Updates graph by adding new inmates and removing released inmates.

    Args:
        G: a Networkx graph
        infected_list: list of infected nodes
        recovered_list: list of recovered nodes
        birth_number: # of inmates added at each time step
        release_number: # of inmates to release
        p: probability of contact between inmate and other inmates
        percent_infected: percent of general population that is infected
        percent_recovered: percent of general population that is recovered
        death_rate: percent of recovered inmates that die

    Returns:
        G: Networkx graph with new inmates added and released inmates removed
        infected_list: infected_list with released inmates removed
        recovered_list: recovered_list with released inmates removed
    """
    # Release inmates
    G, infected_list, recovered_list, num_recovered_released = remove_nodes(G, infected_list, recovered_list,
                                                                            release_number, death_rate)

    # Add new inmates
    G, num_recovered_added = add_nodes(G, infected_list, recovered_list, birth_number, p, percent_infected,
                                       percent_recovered)

    # Track how many recovered inmates were added and released
    delta_recovered = num_recovered_added - num_recovered_released

    return G, infected_list, recovered_list, delta_recovered


def process_data(data_list, delta_recovered_list, death_rate: float):
    """Processes raw simulation loop data list into plottable times, S, I, and R arrays.

    Args:
        data_list: list of Simulation_Investigation objects as output by simulation
        delta_recovered_list: list of change in recovered inmates at each time step due to additions/releases
        death_rate: percent of recovered inmates that die

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
    t, S, I, R = np.concatenate(times_ll), np.concatenate(susceptible_ll), \
                 np.concatenate(infected_ll), np.concatenate(recovered_ll)

    # Calculate deaths
    R, D = calculate_deaths(t, R, delta_recovered_list, death_rate)

    return t, S, I, R, D


def remove_nodes(G, infected_list, recovered_list, release_number, death_rate):
    """Removes release_number inmates from G, selecting inmates of state proportional to the percentage of their
    state in the prison."""
    num_recovered_released = 0

    # Get list of susceptible inmates
    susceptible_list = list(np.setdiff1d(G.nodes, np.union1d(infected_list, recovered_list)))

    for i in range(release_number):
        # Calculate proportion of inmates that are susceptible, infected, or recovered (not dead)
        num_of_recovered_not_dead = np.floor(len(recovered_list) * (1 - death_rate))
        dm = len(susceptible_list) + len(infected_list) + num_of_recovered_not_dead

        # Prevent division by 0
        if dm == 0:
            raise Exception(
                'All inmates died or got released from prison :( Try turning down max_time or background '
                'turnover rate')

        # Proportion of state = # of inmates of state / # of alive inmates
        ps = len(susceptible_list) / dm
        pi = len(infected_list) / dm
        pr = num_of_recovered_not_dead / dm

        # Select state of inmate to remove according to their percentage of prison population
        state = np.random.choice(['S', 'I', 'R'], p=[ps, pi, pr])
        if state == 'S':
            removed_inmate = susceptible_list.pop()  # We assume lists of inmates are ordered randomly
        elif state == 'I':
            removed_inmate = infected_list.pop()
        else:
            removed_inmate = recovered_list.pop()
            num_recovered_released += 1
        G.remove_node(removed_inmate)

    return G, infected_list, recovered_list, num_recovered_released


def add_nodes(G, infected_list, recovered_list, birth_number, p, percent_infected, percent_recovered):
    """Adds birth_number inmates to G, with probability p of an edge forming between new node and each existing node."""
    num_recovered_added = 0

    # Add birth_number new inmates
    for i in range(birth_number):
        inmate_id = list(G.nodes)[-1] + 1  # Make sure node ID doesn't already exist
        G.add_node(inmate_id)

        # Set state of new inmate
        percent_susceptible = 1 - percent_infected - percent_recovered
        state = np.random.choice(['S', 'I', 'R'], p=[percent_susceptible, percent_infected, percent_recovered])
        if state == 'I':
            infected_list.append(inmate_id)
        elif state == 'R':
            recovered_list.append(inmate_id)
            num_recovered_added += 1

        # Connect inmate to existing inmates
        for other_inmate_id in G.nodes:
            # Do not allow self-edges
            if inmate_id == other_inmate_id:
                continue
            if np.random.rand() < p:  # add edge with certain probability (G(n,p) model edge generation for new node)
                G.add_edge(inmate_id, other_inmate_id)

    return G, num_recovered_added


def calculate_deaths(t, recovered_inmates_and_dead_inmates, delta_recovered_list, death_rate):
    """Says percent of recovered individuals at each time step actually die, and updates R."""
    # recovered_inmates_and_dead_inmates includes two groups:
    #   1) Inmates that we know are recovered
    #   2) Inmates that may be recovered or dead

    recovered_or_dead_inmates = recovered_inmates_and_dead_inmates.copy()
    # All added/released "recovered" inmates are not dead
    for i in range(1, len(delta_recovered_list)):
        # Check if any inmates changed state at the added/release time
        if np.where(t == i)[0].size != 0:
            # Find time index where additions/releases occurred
            time_idx = np.where(t == i)[0][0]

            # Adjust for added/released # recovered inmates
            recovered_or_dead_inmates[time_idx:] -= delta_recovered_list[i - 1]

    # Now we have the inmates that may be recovered or dead
    # Calculate the amount of these inmates that are dead
    D = np.ceil(recovered_or_dead_inmates * death_rate)

    # Subtract all the dead inmates from the original R
    R = recovered_inmates_and_dead_inmates - D

    return R, D


def print_release_intervention_info(time, infected_list, release_number):
    """Prints info when release intervention occurs."""
    print(f'Release intervention condition met:\n\tTime: {time}\n\t# of infected: {len(infected_list)}')
    print(f'\tReleasing {release_number} inmates.')


def get_infected(data: EoN.Simulation_Investigation, end_time: int):
    """Returns list of infected nodes."""
    return get_type_of_nodes(data, end_time, 'I')


def get_recovered(data: EoN.Simulation_Investigation, end_time: int):
    """Returns list of recovered nodes."""
    return get_type_of_nodes(data, end_time, 'R')


def get_type_of_nodes(data: EoN.Simulation_Investigation, end_time: int, state: str):
    """Returns list of certain type of nodes."""
    return [node for (node, s) in data.get_statuses(time=end_time).items() if s == state]
