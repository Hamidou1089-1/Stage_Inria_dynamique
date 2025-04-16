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
number_bank = 1000
n_core = int(number_bank /2)
n_periphery = number_bank - n_core



#network_manual = TrivialNetwork(5000)




#core_periphery_network = create_core_periphery_network(n_core, n_periphery, p_core=0.85, p_periphery=0.3)

#network_random = RandomNetwork(400, 0.5)



network_manual = ManualNetwork(P, c, P@np.array([1]*4), b, P.T@np.array([1]*4), A)

default_count_vector = []
shock_measure_vector = []


vector_outside_asset = np.copy(network_manual.get_vector_outside_assets())
shock_vector = np.array([0]*4)

liste = np.arange(0, 1, 10)

for k in range(11):
    shock_vector = k*vector_outside_asset/10
    simulation_core_network = Simulation("Eisenberg", network_manual, shock_vector)
    #simulation_core_network = Simulation("Eisenberg", core_periphery_network, shock_vector)
    #simulation_core_network = Simulation("Eisenberg",network_random, shock_vector)



    _ , shock_measure, default_count, _ = simulation_core_network.simulate()
    #print("How can i have the vector of clearing payment :", simulation_core_network.model.compute_clearing_payments(100,shock_vector))



    network_manual.set_vector_outside_assets(vector_outside_asset)
    #core_periphery_network.set_vector_outside_assets(vector_outside_asset)
    #network_random.set_vector_outside_assets(vector_outside_asset)





    shock_measure_vector.append(shock_measure)
    default_count_vector.append(default_count)


print("shock measure vector: ",shock_measure_vector[-1])
print("default count vector ",default_count_vector[-1])


plt.plot( shock_measure_vector, default_count_vector)
plt.show()