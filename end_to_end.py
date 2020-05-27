import networkx as nx
from simulation import simulation
from analysis import plot


def end_to_end(birth_number, release_number, release_time, death_rate=0.01, rho=None,
               tau=0.05, gamma=1.0, max_time=10, N=5000, p=0.02):
    """Runs end-to-end simulation and plots results.

    Args:
        birth_number: # of inmates added at each time step
        release_number: # of inmates to release
        release_time: time step at which to release inmates
        death_rate:
        rho: percent of inmates that are initially infected
        tau: transmission rate
        gamma: recovery rate
        max_time: # of time steps to run simulation
        N: # of inmates initially
        p: probability of contact between inmate and other inmates

    Returns:
        t: array of times at which events occur
        S: # of susceptible inmates at each time step
        I: # of infected inmates at each time step
        R: # of recovered inmates at each time step
        D: # of dead inmates at each time step
    """
    # Build graph
    G = nx.fast_gnp_random_graph(N, p)

    # Run simulation
    t, S, I, R, D = simulation(G, tau, gamma, rho, max_time, release_time, release_number, birth_number, p, death_rate)

    # Plot and analyze results
    plot(t, S, I, R, D)
    return t, S, I, R, D
