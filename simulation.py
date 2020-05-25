%load_ext autoreload
%autoreload 2
%matplotlib inline

import networkx as nx
import EoN
import matplotlib.pyplot as plt
from functions import *

# Set G(n,p) model-specific parameters
N = 1000 # number of individuals
kave = 5 # expected number of contacts per person

# Set simulation-specific parameters
infected_list = [0] # initial nodes that are infected
recovered_list = [] # initial nodes that are recovered
tau = 0.7 # transmission rate
gamma = 1.0 # recovery rate
max_time = 100

G = nx.fast_gnp_random_graph(N, kave/(N-1))

t = []
S = []
I = []
R = []

# Loop over time
for i in range(max_time):
    # Run simulation
    data = EoN.fast_SIR(G, tau, gamma, initial_infecteds=infected_list, initial_recovereds=recovered_list,\
                        tmin=i, tmax=i+1, return_full_data=True)
    
    # Update infected and recovered nodelists
    infected_list, recovered_list = get_infected(data, i+1), get_recovered(data, i+1)
    
    # Add and remove nodes
    G, infected_list, recovered_list = recalibrate_graph(G, infected_list, recovered_list, 50, 50)
    
    t.append(i)
    I.append(len(infected_list))
    R.append(len(recovered_list))
    S.append(len(G.nodes)-R[-1]-I[-1])
    
plt.plot(t, S, label = 'Susceptible')
plt.plot(t, I, label = 'Infected')
plt.plot(t, R, label = 'Recovered')
# plt.plot(t_deaths, deaths, label = 'Deaths')

plt.xlabel('Time')
plt.ylabel('Number infected')
plt.legend()
plt.show()
