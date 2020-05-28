import os

import matplotlib.pyplot as plt
import numpy as np


def summary(t, S, I, R, D, save_plot, title, parameters):
    """Plots graph of simulation and computes various statistics."""
    # Print parameters
    print('############################## Parameters ##############################')
    print(parameters)

    # Print statistics
    print('\n############################## Results ##############################')
    print('Total # of infections: ', count_total_infected(I))
    print('Total # of deaths: ', count_total_deaths(D))

    # Plot graph
    plot(t, S, I, R, D, save_plot, title, parameters)


def count_total_infected(I):
    """Counts total number of infected cases by summing all positive changes in I at each time step."""
    changes = I[1:] - I[:-1]
    infected = np.sum(changes[changes > 0])
    return infected + I[0]  # add initial infected


def count_total_deaths(D):
    """Returns total number of deaths."""
    return D[-1]


def plot(t, S, I, R, D, save_plot, title, parameters):
    """Creates plot showing S, I, R, D(eaths) against time.

    Args:
        t: array of times at which events occur
        S: # of susceptible inmates at each time step
        I: # of infected inmates at each time step
        R: # of recovered inmates at each time step
        D: # of dead inmates at each time step
        save_plot: should plot be saved to computer?
        title: title of plot
        parameters: dict of parameters end_to_end was called with
    """
    # Set figure size and font size
    WIDTH = 6
    HEIGHT = 4
    FONT_SIZE = 11
    set_plot_display_settings(WIDTH, HEIGHT, FONT_SIZE)

    plt.plot(t, S, label='Susceptible', color='b')
    plt.plot(t, I, label='Infected', color='r')
    plt.plot(t, R, label='Recovered', color='g')
    plt.plot(t, D, label='Deaths', color='k')

    plt.xlabel('Time')
    plt.ylabel('Number of inmates')
    plt.title(title)
    plt.legend()
    plt.show()

    # Save plot if wanted
    if save_plot:
        # Place plots in folder 'plots'
        if not os.path.exists('plots'):
            os.makedirs('plots')
        filename = f'simulation_plot{parameters_into_string(parameters)}'
        plt.savefig(f'plots/{filename}.png')
        print(f'Plot saved with filename: {filename}')


# Helper functions
def parameters_into_string(parameters):
    """Turns parameter dictionary into string for use in naming plot file."""
    parameter_string = str()
    for parameter, value in parameters.items():
        # Logic to shorten parameter names because ran into too long filename problems
        if parameter == 'save_plot':  # redundant to include
            continue
        if parameter == 'number_infected_before_release':
            parameter = 'num_inf_bf_release'
        elif parameter == 'background_inmate_turnover':
            parameter = 'bck_turnover'
        elif parameter == 'stop_inflow_at_intervention':
            parameter = 'stp_in_at_int'

        parameter_string += f'_{parameter}-{value}_'
    return parameter_string


def set_plot_display_settings(plot_width, plot_height, font_size):
    plt.rcParams.update({"figure.figsize": (plot_width, plot_height)})
    plt.rcParams.update({'font.size': font_size})
