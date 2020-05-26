import matplotlib.pyplot as plt


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
