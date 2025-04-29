import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from jedi.inference.helpers import deep_ast_copy

from model import RandomNetwork, ManualNetwork, UniformShockDistribution, BetaShockDistribution, TargetedShockDistribution
from controller import Simulation
from core_periphery import create_core_periphery_network




# Reseau core-periphery bizarre
number_bank = 500
n_core = int(number_bank /2)
n_periphery = number_bank - n_core




#core_periphery_network = create_core_periphery_network(n_core, n_periphery, p_core=0.7, p_periphery=0.3)
network_random = RandomNetwork(number_bank, 0.9)
network_random_copy = copy.deepcopy(network_random)


#network_manual = ManualNetwork(P, c, b)

default_count_vector = []
shock_measure_vector = []


#vector_outside_asset = np.copy(core_periphery_network.get_vector_outside_assets())
vector_outside_asset = np.copy(network_random.get_vector_outside_assets())
shock_vector = np.array([0]*number_bank)
print("His net worth ? ", network_random.net_worth[0])

#print("Matrix of obligation: ", network_random.matrix_obligation)
#print("Vector of outside assets: ", core_periphery_network.vector_outside_asset)
#print("Net worth: ", core_periphery_network.net_worth)
#print("vector of outside liabilities: ", core_periphery_network.vector_outside_liabilities)
for k in range(101):
    shock_vector =   k*vector_outside_asset/100
    #simulation_core_network = Simulation("Eisenberg", network_manual, shock_vector)
    #simulation_core_network = Simulation("Eisenberg", core_periphery_network, shock_vector)
    simulation_core_network = Simulation("Eisenberg",network_random, shock_vector)
    simulation_core_network.model.set_network(network_random_copy)


    _ , shock_measure, default_count, vulnerabilities = simulation_core_network.simulate()



    #network_manual.set_vector_outside_assets(vector_outside_asset)
    #core_periphery_network.set_vector_outside_assets(vector_outside_asset)
    #network_random.set_vector_outside_assets(vector_outside_asset)





    shock_measure_vector.append(shock_measure)
    default_count_vector.append(default_count)


#print("default count vector ",default_count_vector)
#print("Vulnerabilities: ", vulnerabilities)

plt.figure(figsize=(10, 6))
plt.plot(shock_measure_vector, default_count_vector, label='Choc linéaire')
plt.vlines(x=0.5, ymin=0, ymax=1, linestyles='dashed', colors='red', label="Un seuil")
plt.title('Analyse de l\'impact des chocs linéaires')
plt.xlabel('Mesure du choc')
plt.ylabel('Proportion de défauts')
plt.legend()
plt.grid(True)
plt.savefig('linear_shock_analysis.png')
plt.show()


