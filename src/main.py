import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from model import RandomNetwork, ManualNetwork, TrivialNetwork
from controller import Simulation
from core_periphery import create_core_periphery_network
from scale_free import create_scalefree_network
from scale_free import create_smallworld_network


P = np.array([
    [0, 100, 100, 100],
    [0, 0, 100, 100],
    [0, 0, 0, 100],
    [0, 0, 0, 0]
])

A = np.array([
    [0, 1/3, 1/3, 1/3],
    [0, 0, 1/2, 1/2],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
])

c = np.array([301, 101, 1, 0])
b = np.array([ 0, 0, 0, 0])



# Reseau core-periphery bizarre
number_bank = 100
n_core = int(number_bank /2)
n_periphery = number_bank - n_core



#network_manual = TrivialNetwork(5000)
#core_periphery_network = create_core_periphery_network(n_core, n_periphery, p_core=0.7, p_periphery=0.3)
network_random = RandomNetwork(100, 0.9)



#network_manual = ManualNetwork(P, c, b)

default_count_vector = []
shock_measure_vector = []


#vector_outside_asset = np.copy(core_periphery_network.get_vector_outside_assets())
vector_outside_asset = np.copy(network_random.get_vector_outside_assets())
shock_vector = np.array([0]*100)
#print("Matrix of obligation: ", network_random.matrix_obligation)
#print("Vector of outside assets: ", core_periphery_network.vector_outside_asset)
#print("Net worth: ", core_periphery_network.net_worth)
#print("vector of outside liabilities: ", core_periphery_network.vector_outside_liabilities)
for k in range(101):
    shock_vector = k*vector_outside_asset/100
    #simulation_core_network = Simulation("Eisenberg", network_manual, shock_vector)
    #simulation_core_network = Simulation("Eisenberg", core_periphery_network, shock_vector)
    simulation_core_network = Simulation("Eisenberg",network_random, shock_vector)



    _ , shock_measure, default_count, vulnerabilities = simulation_core_network.simulate()



    #network_manual.set_vector_outside_assets(vector_outside_asset)
    #core_periphery_network.set_vector_outside_assets(vector_outside_asset)
    network_random.set_vector_outside_assets(vector_outside_asset)





    shock_measure_vector.append(shock_measure)
    default_count_vector.append(default_count)

#print("shock measure vector: ",shock_measure_vector)
#print("default count vector ",default_count_vector)
#print("Vulnerabilities: ", vulnerabilities)

plt.plot( shock_measure_vector, default_count_vector)
plt.vlines(x=0.5, ymin=0, ymax=1, linestyles='dashed')
plt.show()