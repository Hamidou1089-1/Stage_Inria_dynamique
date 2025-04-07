import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from model import RandomNetwork, ManualNetwork
from controller import Simulation
from core_periphery import create_core_periphery_network
from scale_free import create_scalefree_network
from scale_free import create_smallworld_network

# Fixer le générateur aléatoire
np.random.seed(42)

number_bank = 7
n_core = 3
n_periphery = 4


core_periphery_network = create_core_periphery_network(n_core, n_periphery, p_core=0.95, p_periphery=0.05)







# On fixe la taille du graphe, et on fait varier uniformément, le vector de shock, puis on plot la mesure du shock par rapport a la proportion de default.

default_count_vector = []
shock_measure_vector = []


print("Outside asset : ", core_periphery_network.get_vector_outside_assets() )
vector_outside_asset = np.copy(core_periphery_network.get_vector_outside_assets())
shock_vector = np.copy(vector_outside_asset/100)
print(shock_vector)
for k in range(100):
    core_periphery_network = create_core_periphery_network(n_core, n_periphery, p_core=0.95, p_periphery=0.05)

    simulation_core_network = Simulation("Eisenberg", core_periphery_network, shock_vector)



    _ , shock_measure, default_count, _ = simulation_core_network.simulate()
    core_periphery_network.set_vector_outside_assets(vector_outside_asset)
    shock_vector += vector_outside_asset/100
    print("shock vector: ",shock_vector)
    print("Outside asset : ", core_periphery_network.get_vector_outside_assets() )


    shock_measure_vector.append(shock_measure)
    default_count_vector.append(default_count)


print("shock measure vector: ",shock_measure_vector)
print("default count vector ",default_count_vector)


plt.scatter( shock_measure_vector, default_count_vector)
plt.show()


