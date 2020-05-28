import networkx as nx

from analysis import summary
from simulation import simulation


def end_to_end(background_inmate_turnover, release_number, number_infected_before_release, rho=0.0003, death_rate=0.012,
               tau=0.03, gamma=1.0, max_time=10, N=3000, p=0.02, percent_infected=0.0035, percent_recovered=0.0015,
               save_plot=False, stop_inflow_at_intervention=False):
    """Runs end-to-end simulation and plots results.

    Args:
        background_inmate_turnover: background # of inmates added/released at each time step
        release_number: # of inmates to release
        number_infected_before_release: number of infected at which to perform release on next integer time
        rho: percent of inmates that are initially infected
        death_rate: probability of dying after being infected
        tau: transmission rate
        gamma: recovery rate
        max_time: # of time steps to run simulation
        N: # of inmates initially
        p: probability of contact between inmate and other inmates
        percent_infected: percent of general population that is infected
        percent_recovered: percent of general population that is recovered
        save_plot: should plot of results be saved to computer?
        stop_inflow_at_intervention: should we stop the background inflow of inmates at intervention time?

    Returns:
        t: array of times at which events occur
        S: # of susceptible inmates at each time step
        I: # of infected inmates at each time step
        R: # of recovered inmates at each time step
        D: # of dead inmates at each time step
    """
    # Save parameters
    parameters_dict = locals()

    # Build graph
    G = nx.fast_gnp_random_graph(N, p)

    # Run simulation
    t, S, I, R, D = simulation(G, tau, gamma, rho, max_time, number_infected_before_release, release_number,
                               background_inmate_turnover, stop_inflow_at_intervention, p, death_rate,
                               percent_infected, percent_recovered)

    # Print summary of results
    summary(t, S, I, R, D, save_plot, parameters_dict)

    return t, S, I, R, D
