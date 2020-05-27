import EoN
import numpy as np


def simulation(G, tau, gamma, rho, max_time, release_time, release_number, birth_number,
               p, death_rate, percent_infected, percent_recovered):
    """Runs a simulation on SIR model.

    Args:
        G: Networkx graph
        tau: transmission rate
        gamma: recovery rate
        rho: percent of inmates that are initially infected
        max_time: # of time steps to run simulation
        release_time: time step at which to release inmates
        release_number: # of inmates to release
        birth_number: # of inmates added at each time step
        p: probability of contact between inmate and other inmates
        death_rate: percent of recovered inmates that die
        percent_infected: percent of general population that is infected
        percent_recovered: percent of general population that is recovered

    Returns:
        t: array of times at which events occur
        S: # of susceptible inmates at each time step
        I: # of infected inmates at each time step
        R: # of recovered inmates at each time step
        D: # of dead inmates at each time step
    """
    data_list = []
    infected_list = []
    recovered_list = []

    # Loop over time
    for i in range(max_time):
        # Use rho for first time step of simulation
        if i == 0:
            data = EoN.fast_SIR(G, tau, gamma, rho=rho, tmax=1, return_full_data=True)
        else:
            data = EoN.fast_SIR(G, tau, gamma, initial_infecteds=infected_list, initial_recovereds=recovered_list,
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
            r_n = birth_number + release_number
        else:  # Release the same amount of inmates coming in to prison
            r_n = birth_number
        G, infected_list, recovered_list = recalibrate_graph(G, infected_list, recovered_list, birth_number, r_n, p,
                                                             percent_infected, percent_recovered)

    # Process raw data into t, S, I, R, D arrays
    t, S, I, R, D = process_data(data_list, death_rate)

    return t, S, I, R, D


# Helper Functions
def recalibrate_graph(G, infected_list, recovered_list, birth_number, release_number, p,
                      percent_infected, percent_recovered):
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

    Returns:
        G: Networkx graph with new inmates added and released inmates removed
        infected_list: infected_list with released inmates removed
        recovered_list: recovered_list with released inmates removed
    """
    G, infected_list, recovered_list = remove_nodes(G, infected_list, recovered_list, release_number)
    G = add_nodes(G, infected_list, recovered_list, birth_number, p, percent_infected, percent_recovered)
    return G, infected_list, recovered_list


def process_data(data_list, death_rate: float):
    """Processes raw simulation loop data list into plottable times, S, I, and R arrays.

    Args:
        data_list: list of Simulation_Investigation objects as output by simulation
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
    R, D = calculate_deaths(R, death_rate)

    return t, S, I, R, D


def remove_nodes(G, infected_list, recovered_list, release_number):
    """Randomly removes release_number nodes from G and updated infected and recovered lists."""
    release_list = np.random.choice(list(G.nodes), release_number, replace=False)
    for x in release_list:
        G.remove_node(x)

        # Remove released inmates from infected and recovered lists
        if x in infected_list:
            infected_list.remove(x)
        if x in recovered_list:
            recovered_list.remove(x)

    return G, infected_list, recovered_list


def add_nodes(G, infected_list, recovered_list, birth_number, p, percent_infected, percent_recovered):
    """Adds birth_number inmates to G, with probability p of an edge forming between new node and each existing node."""
    for i in range(birth_number):
        inmate_id = list(G.nodes)[-1] + 1
        G.add_node(inmate_id)  # Make sure node ID doesn't already exist

        # Set state of new inmate
        percent_susceptible = 1 - percent_infected - percent_recovered
        state = np.random.choice(['S', 'I', 'R'], p=[percent_susceptible, percent_infected, percent_recovered])
        if state == 'I':
            infected_list.append(inmate_id)
        elif state == 'R':
            recovered_list.append(inmate_id)

        # Connect inmate to existing inmates
        for other_inmate_id in G.nodes:
            # Do not allow self-edges
            if inmate_id == other_inmate_id:
                continue
            if np.random.rand() < p:  # add edge with certain probability (G(n,p) model edge generation for new node)
                G.add_edge(inmate_id, other_inmate_id)
    return G


def calculate_deaths(R, death_rate):
    """Says percent of recovered individuals at each time step actually die, and updates R."""
    D = R * death_rate
    R = R - D
    return R, D


def get_infected(data: EoN.Simulation_Investigation, end_time: int):
    """Returns list of infected nodes."""
    return get_type_of_nodes(data, end_time, 'I')


def get_recovered(data: EoN.Simulation_Investigation, end_time: int):
    """Returns list of recovered nodes."""
    return get_type_of_nodes(data, end_time, 'R')


def get_type_of_nodes(data: EoN.Simulation_Investigation, end_time: int, state: str):
    """Returns list of certain type of nodes."""
    return [node for (node, s) in data.get_statuses(time=end_time).items() if s == state]
