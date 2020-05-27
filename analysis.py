import matplotlib.pyplot as plt
import numpy as np


def summary(t, S, I, R, D):
    # Plot graph
    plot(t, S, I, R, D)

    # Print statistics
    print('Total # of infections: ', count_total_infected(I))
    print('Total # of deaths: ', count_total_deaths(D))


def count_total_infected(I):
    """Counts total number of infected cases by summing all positive changes in I at each time step."""
    changes = I[1:] - I[:-1]
    infected = np.sum(changes[changes > 0])
    return infected + I[0]  # add initial infected


def count_total_deaths(D):
    """Returns total number of deaths."""
    return D[-1]


def plot(t, S, I, R, D):
    """Creates plot showing S, I, R, D(eaths) against time.

    Args:
        t: array of times at which events occur
        S: # of susceptible inmates at each time step
        I: # of infected inmates at each time step
        R: # of recovered inmates at each time step
        D: # of dead inmates at each time step
    """
    plt.plot(t, S, label='Susceptible', color='b')
    plt.plot(t, I, label='Infected', color='r')
    plt.plot(t, R, label='Recovered', color='g')
    plt.plot(t, D, label='Deaths', color='k')

    plt.xlabel('Time')
    plt.ylabel('Number of inmates')
    plt.legend()
    plt.show()
