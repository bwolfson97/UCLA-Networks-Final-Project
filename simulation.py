import networkx as nx
import EoN
import matplotlib.pyplot as plt
from functions import *

# Set G(n,p) model-specific parameters
N = 1000 # number of individuals
kave = 10 # expected number of contacts per person

# Set simulation-specific parameters
birth_number = 0 # number of
probability_of_new_connection = kave / (N-1)
release_number = 50
number_of_infected_before_releases = 200
death_rate = 0.01
initial_infected = [0] # initial nodes that are infected

tau = 0.5 # transmission rate
gamma = 1.0 # recovery rate
max_time = 5

G = nx.fast_gnp_random_graph(N, probability_of_new_connection)

infected_list = initial_infected
recovered_list = []
data_list = []

# Loop over time
for i in range(max_time):
    # Run simulation
    data = EoN.fast_SIR(G, tau, gamma, initial_infecteds=infected_list, initial_recovereds=recovered_list, \
                        tmin=i, tmax=i + 1, return_full_data=True)
    data_list.append(data)

    # Update infected and recovered nodelists
    infected_list, recovered_list = get_infected(data, i + 1), get_recovered(data, i + 1)

    # Add and remove nodes
    if len(infected_list) < number_of_infected_before_releases:  # Only start inmate releases after some time
        r_n = 0
    else:
        r_n = release_number
    G, infected_list, recovered_list = recalibrate_graph(G, infected_list, recovered_list, \
                                                         birth_number, r_n, probability_of_new_connection)

times_l = []
susceptible_ll = []
infected_ll = []
recovered_ll = []

for data in data_list:
    times, dict_of_states = data.summary()
    times_l.append(np.delete(times, 0))
    susceptible_ll.append(np.delete(dict_of_states['S'], 0))
    infected_ll.append(np.delete(dict_of_states['I'], 0))
    recovered_ll.append(np.delete(dict_of_states['R'], 0))

t, S, I, R = aggregate_quantity(times_l), aggregate_quantity(susceptible_ll),\
            aggregate_quantity(infected_ll), aggregate_quantity(recovered_ll)

D = R * death_rate
R = R - D

plt.plot(t, S, label = 'Suscepible')
plt.plot(t, I, label = 'Infected')
plt.plot(t, R, label = 'Recovered')
plt.plot(t, D, label = 'Deaths')

plt.xlabel('Time')
plt.ylabel('Number infected')
plt.legend()
plt.show()