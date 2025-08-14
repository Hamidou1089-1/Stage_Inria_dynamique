import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx

from model import RandomNetwork
from controller import Simulation

# Paramètres de la simulation
bank_counts = [100]  # Différentes tailles de réseau
probabilities = np.arange(0.1, 1.1, 0.1)  # Différentes densités
shock_steps = 101  # Nombre de pas pour la mesure du choc (de 0 à 1)

# Stockage des résultats
results = {}

# Exécution des simulations pour différentes tailles de réseau et différentes densités
for num_banks in bank_counts:
    results[num_banks] = {}

    for probability in probabilities:
        print(f"Simulation: {num_banks} banques, probabilité {probability:.1f}")

        # Initialisation du réseau aléatoire
        network_random = RandomNetwork(num_banks, probability)
        network_random_copy = copy.deepcopy(network_random)

        # Vecteurs pour stocker les résultats
        default_count_vector = []
        shock_measure_vector = []
        variation_default_count = []

        # Vecteur d'actifs extérieurs
        vector_outside_asset = np.copy(network_random.get_vector_outside_assets())
        shock_vector = np.array([0]*num_banks)

        # Application progressive du choc
        for k in range(shock_steps):
            # Choc proportionnel aux actifs extérieurs
            shock_vector = k * vector_outside_asset / (shock_steps - 1)

            # Simulation du choc
            simulation = Simulation("Eisenberg", network_random, shock_vector)
            simulation.model.set_network(network_random_copy)

            # Récupération des résultats
            _, shock_measure, default_count, _ = simulation.simulate()

            # Stockage des résultats
            shock_measure_vector.append(shock_measure)
            default_count_vector.append(default_count)

        # Calcul de la variation de la proportion de défauts
        variation_default_count = np.diff(default_count_vector)

        # Stockage des résultats finaux
        results[num_banks][probability] = {
            'shock_measure': shock_measure_vector,
            'default_count': default_count_vector,
            'variation': variation_default_count
        }



for prob in probabilities:
    plt.plot(results[100][prob]['shock_measure'], results[100][prob]['default_count'], label=f"p = {prob} ")
    plt.legend()
    plt.show()
