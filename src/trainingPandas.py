#%% md
# # Lecture pour entrainement pandas
# 
#%%

import networkx as nx
from networkx.relabel import relabel_nodes
from importlib import reload
import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from model import RandomNetwork, ManualNetwork
from controller import Simulation


from sklearn.compose import make_column_transformer

from core_periphery import *
import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from jedi.inference.helpers import deep_ast_copy
import networkx as nx

from model import RandomNetwork, ManualNetwork, UniformShockDistribution, BetaShockDistribution, TargetedShockDistribution
from controller import Simulation
from core_periphery import create_core_periphery_network

#%% md
# > ## Different mesure for resilience of the network
#%%
# Reseau core-periphery bizarre
number_bank = 100
n_core = int(number_bank /2)
n_periphery = number_bank - n_core

#%%
probabilities = np.arange(0.1, 1.1, 0.1)
#core_periphery_network = create_core_periphery_network(n_core, n_periphery, p_core=0.7, p_periphery=0.3)
plot_probabilities = {}
mesure_centralite = {}
keeping_track_of_default = np.array([0]*number_bank)
for probability in probabilities:
    network_random = RandomNetwork(number_bank, probability)
    network_random_copy = copy.deepcopy(network_random)
    G = nx.from_numpy_array(network_random.matrix_obligation, create_using=nx.DiGraph)
    # Calculer les centralités
    degree_centrality = nx.out_degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G,weight=None)
    eigenvector_centrality = nx.eigenvector_centrality(G, weight=None)
    mesure_centralite[probability] = (degree_centrality, betweenness_centrality, eigenvector_centrality)

    #network_manual = ManualNetwork(P, c, b)

    default_count_vector = []
    shock_measure_vector = []

    #vector_outside_asset = np.copy(core_periphery_network.get_vector_outside_assets())
    vector_outside_asset = np.copy(network_random.get_vector_outside_assets())
    shock_vector = np.array([0]*number_bank)

    #print("Matrix of obligation: ", network_random.matrix_obligation)
    #print("Vector of outside assets: ", core_periphery_network.vector_outside_asset)
    #print("Net worth: ", core_periphery_network.net_worth)
    #print("vector of outside liabilities: ", core_periphery_network.vector_outside_liabilities)
    for k in range(101):
        shock_vector = k*vector_outside_asset/100
        #simulation_core_network = Simulation("Eisenberg", network_manual, shock_vector)
        #simulation_core_network = Simulation("Eisenberg", core_periphery_network, shock_vector)
        simulation_core_network = Simulation("Eisenberg",network_random, shock_vector)
        simulation_core_network.model.set_network(network_random_copy)
        if k == 42 and probability == 0.5:
            print("Vector of outside assets: ", np.array(simulation_core_network.model.network.vector_outside_asset, dtype=int))
            print("net worth : ", np.array(simulation_core_network.model.network.net_worth, dtype=int))
            print("Vulnerability external max : ", np.max(simulation_core_network.model.network.vulnerabilities))
            print("Vulnerability external min : ", np.min(simulation_core_network.model.network.vulnerabilities))
            print("Vulnerability external mean : ", np.mean(simulation_core_network.model.network.vulnerabilities))
            print("Vulnerability external std : ", np.std(simulation_core_network.model.network.vulnerabilities))

        _ , shock_measure, default_count, vulnerabilities = simulation_core_network.simulate()
        if k == 40 and probability == 1:
           keeping_track_of_default = simulation_core_network.model.network.default_vector




        #network_manual.set_vector_outside_assets(vector_outside_asset)
        #core_periphery_network.set_vector_outside_assets(vector_outside_asset)
        #network_random.set_vector_outside_assets(vector_outside_asset)

        shock_measure_vector.append(shock_measure)
        default_count_vector.append(default_count)

    plot_probabilities[probability] = (shock_measure_vector, default_count_vector)

#%%

variation_shock_measure_prob = {}
variation_default_count_prob = {}
for probability in probabilities:
    variation_shock_measure_prob[probability] = np.diff(plot_probabilities[probability][0])
    variation_default_count_prob[probability] = np.diff(plot_probabilities[probability][1])


# Créer une figure et un axe
fig, ax = plt.subplots(figsize=(10, 6))

# Créer une palette de couleurs pour distinguer les différentes probabilités
# Plus la probabilité est élevée, plus la couleur sera foncée
colors = plt.cm.viridis(np.linspace(0, 1, len(probabilities)))

# Pour chaque probabilité dans votre dictionnaire
for i, probability in enumerate(probabilities):
    # Récupérer les données pour cette probabilité
    shock_measure_vector, default_count_vector = plot_probabilities[probability]
    variation_default_count = variation_default_count_prob[probability]
    # Tracer la courbe default_count en fonction de shock_measure
    ax.plot(shock_measure_vector, default_count_vector, label=f'p={probability:.1f}',
            color=colors[i], markersize=3, linestyle='-')
    #ax.plot(shock_measure_vector[:100], variation_default_count, label=f'variation for p={probability:.1f}',color=colors[i], linestyle='-')
    #ax.vlines(shock_measure_vector[40], 0, 1, colors='red', linestyles='dashed')

# Ajouter une légende, des titres, etc.
ax.legend()
ax.set_xlabel('Shock Measure')
ax.set_ylabel('Default Count')
ax.set_title('Default Count vs Shock Measure and variation associated for Different Probabilities')

# Ajouter une grille pour faciliter la lecture
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()



#%%

betweenness = np.array([mesure_centralite[1][1][k] for k in mesure_centralite[1][1].keys()])
out_degree = np.array([mesure_centralite[1][0][k] for k in mesure_centralite[1][0].keys()])
eigenvector = np.array([mesure_centralite[1][2][k] for k in mesure_centralite[1][2].keys()])
bet_original_indices = np.argsort(betweenness)
out_original_indices = np.argsort(out_degree)
eig_original_indices = np.argsort(eigenvector)

#%%
plt.scatter(betweenness[bet_original_indices],keeping_track_of_default[bet_original_indices], label='betweenness')
plt.xlabel("measure of betweenness centrality")
plt.ylabel("number of defaults (Boolean)")
plt.legend()
plt.show()

#%%
plt.scatter(out_degree[out_original_indices],keeping_track_of_default[out_original_indices], label='out_degree')
plt.xlabel("measure of out degree centrality")
plt.ylabel("number of defaults (Boolean)")
plt.legend()
plt.show()
#%%
plt.scatter(eigenvector[eig_original_indices],keeping_track_of_default[eig_original_indices], label='eigenvector')
plt.xlabel("measure of eigenvector centrality")
plt.ylabel("number of defaults (Boolean)")
plt.legend()
plt.show()
#%%
a = np.array([1.01, 6.0, 21.01])

#%%
b = np.array(a, dtype=int)
#%%

#%%
import scipy.stats as stats
stats.gamma.rvs(a=1, scale=1)
#%%
