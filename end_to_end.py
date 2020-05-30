import networkx as nx

from analysis import summary
from simulation import simulation


def end_to_end(release_number, number_infected_before_release, stop_inflow_at_intervention,
               background_inmate_turnover=20, rho=0.0003, death_rate=0.012, tau=0.03, gamma=0.07, max_time=60,
               N=3000, p=0.02, percent_infected=0.0035, percent_recovered=0.0015, save_plot=False, title='',
               soc_dist=False, soc_dist_tau=0.001, custom_graph=None, constant_patient_zero=False,
               patient_zero_numbers=0):
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
        title: title of plot
        soc_dist: boolean flag, if we lower transmission rate after major release
        soc_dist_tau: new transmission rate after major release
        custom_graph: If custom_graph passed, uses custom_graph. Otherwise, creates graph from N and p
        constant_patient_zero: if True, then patient zero will be set to node patient_zero_number
        patient_zero_numbers: sets node numbers of patients zero (default is 0, this parameter is arbitrary)

    Returns:
        t: array of times at which events occur
        S: # of susceptible inmates at each time step
        I: # of infected inmates at each time step
        R: # of recovered inmates at each time step
        D: # of dead inmates at each time step
    """
    # Save parameters
    parameters_dict = locals()

    # Use custom_graph if passed
    if custom_graph is not None:
        G = custom_graph
    else:  # Build new graph
        G = nx.fast_gnp_random_graph(N, p)

    # Run simulation
    t, S, I, R, D = simulation(G, tau, gamma, rho, max_time, number_infected_before_release, release_number,
                               background_inmate_turnover, stop_inflow_at_intervention, p, death_rate,
                               percent_infected, percent_recovered, soc_dist, soc_dist_tau, constant_patient_zero,
                               patient_zero_numbers)

    # Print summary of results
    summary(t, S, I, R, D, save_plot, title, parameters_dict)

    return t, S, I, R, D
