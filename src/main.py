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

shock_vector = [3188, 2400, 3100, 382, 500, 270, 270]

core_periphery_network = create_core_periphery_network(n_core, n_periphery)

simulation_core_network = Simulation("Eisenberg", core_periphery_network, shock_vector)

_ , shock_measure, default_count, _ = simulation_core_network.simulate()


print("measure shock: ", shock_measure)
print("default proportion: ",default_count)




