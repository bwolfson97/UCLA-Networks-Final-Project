import networkx as nx

from analysis import summary
from simulation import simulation


def end_to_end(release_number, number_infected_before_release, stop_inflow_at_intervention,
               background_inmate_turnover=20, death_rate=0.012, tau=0.03, gamma=0.07, rho=0.0003, max_time=60,
               N=3000, p=0.02, percent_infected=0.0035, percent_recovered=0.0015, save_plot=False, title='',
               social_distance=False, social_distance_tau=0.01, custom_graph=None, constant_initial_infected=False,
               initial_infected_list=None):
    """Runs end-to-end simulation and plots results.

    Args:
        background_inmate_turnover: background # of inmates added/released at each time step
        release_number: # of inmates to release
        number_infected_before_release: number of infected at which to perform release on next integer time
        death_rate: probability of dying after being infected
        tau: transmission rate
        gamma: recovery rate
        rho: percent of inmates that are initially infected
        max_time: # of time steps to run simulation
        N: # of inmates initially
        p: probability of contact between inmate and other inmates
        percent_infected: percent of general population that is infected
        percent_recovered: percent of general population that is recovered
        save_plot: should plot of results be saved to computer?
        stop_inflow_at_intervention: should we stop the background inflow of inmates at intervention time?
        title: title of plot
        social_distance: boolean flag, if we lower transmission rate after major release
        social_distance_tau: new transmission rate after major release
        custom_graph: If custom_graph passed, uses custom_graph. Otherwise, creates graph from N and p
        constant_initial_infected: if True, then patient zero will be set to node patient_zero_number
        initial_infected_list: sets node numbers of patients zero (default is 0, this parameter is arbitrary)

    Returns:
        t: array of times at which events occur
        S: # of susceptible inmates at each time
        I: # of infected inmates at each time
        R: # of recovered inmates at each time
        D: # of dead inmates at each time step
    """
    # Save parameters
    parameters_dict = locals()

    # If no initial_infected_list is passed, default to inmate 0 being infected
    if initial_infected_list is None:
        initial_infected_list = [0]

    # Use custom_graph if passed
    if custom_graph is not None:
        G = custom_graph.copy()
    else:  # Build new graph
        G = nx.fast_gnp_random_graph(N, p)

    # Run simulation
    t, S, I, R, D = simulation(G, tau, gamma, rho, max_time, number_infected_before_release, release_number,
                               background_inmate_turnover, stop_inflow_at_intervention, p, death_rate,
                               percent_infected, percent_recovered, social_distance, social_distance_tau,
                               constant_initial_infected, initial_infected_list)

    # Print summary of results
    summary(t, S, I, R, D, save_plot, title, parameters_dict)

    return t, S, I, R, D
