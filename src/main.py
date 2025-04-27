import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from model import RandomNetwork, ManualNetwork, UniformShockDistribution, BetaShockDistribution, TargetedShockDistribution
from controller import Simulation
from core_periphery import create_core_periphery_network




# Reseau core-periphery bizarre
number_bank = 100
n_core = int(number_bank /2)
n_periphery = number_bank - n_core




#core_periphery_network = create_core_periphery_network(n_core, n_periphery, p_core=0.7, p_periphery=0.3)
network_random = RandomNetwork(500, 0.9)



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

plt.figure(figsize=(10, 6))
plt.plot(shock_measure_vector, default_count_vector, label='Choc linéaire')
plt.vlines(x=0.5, ymin=0, ymax=1, linestyles='dashed')
plt.title('Analyse de l\'impact des chocs linéaires')
plt.xlabel('Mesure du choc')
plt.ylabel('Proportion de défauts')
plt.legend()
plt.grid(True)
plt.savefig('linear_shock_analysis.png')
plt.show()

# Démonstration des nouvelles fonctionnalités de distribution de chocs
print("\n=== Démonstration des nouvelles distributions de chocs ===\n")

# 1. Utilisation de la distribution uniforme
print("1. Distribution de chocs uniforme")
uniform_dist = UniformShockDistribution(network_random)
simulation_uniform = Simulation("Eisenberg", network_random, uniform_dist.generate_shock(intensity=0.5))
results_uniform = simulation_uniform.run_scenarios(uniform_dist, n_scenarios=10)
print(f"Moyenne des défauts: {results_uniform['avg_default_count']:.2f}")
print(f"Maximum des défauts: {results_uniform['max_default_count']:.2f}")
print(f"Écart-type des défauts: {results_uniform['std_default_count']:.2f}")

# 2. Utilisation de la distribution Beta
print("\n2. Distribution de chocs Beta")
beta_dist = BetaShockDistribution(network_random, alpha=2, beta=5)
simulation_beta = Simulation("Eisenberg", network_random, beta_dist.generate_shock(intensity=0.5))
results_beta = simulation_beta.run_scenarios(beta_dist, n_scenarios=10)
print(f"Moyenne des défauts: {results_beta['avg_default_count']:.2f}")
print(f"Maximum des défauts: {results_beta['max_default_count']:.2f}")
print(f"Écart-type des défauts: {results_beta['std_default_count']:.2f}")

# 3. Utilisation de la distribution ciblée
print("\n3. Distribution de chocs ciblés")
targeted_dist = TargetedShockDistribution(network_random, targeting_strategy="vulnerability")
simulation_targeted = Simulation("Eisenberg", network_random, targeted_dist.generate_shock(intensity=0.5))
results_targeted = simulation_targeted.run_scenarios(targeted_dist, n_scenarios=10)
print(f"Moyenne des défauts: {results_targeted['avg_default_count']:.2f}")
print(f"Maximum des défauts: {results_targeted['max_default_count']:.2f}")
print(f"Écart-type des défauts: {results_targeted['std_default_count']:.2f}")

# 4. Analyse d'intensité avec la distribution ciblée
print("\n4. Analyse d'intensité avec la distribution ciblée")
intensity_results = simulation_targeted.run_intensity_analysis(
    TargetedShockDistribution, 
    intensity_range=(0.1, 1.0, 0.1),
    n_scenarios_per_intensity=5,
    targeting_strategy="vulnerability"
)

# Visualisation des résultats de l'analyse d'intensité
plt.figure(figsize=(10, 6))
plt.plot(intensity_results['intensities'], intensity_results['avg_default_counts'], marker='o')
plt.title('Analyse de l\'impact de l\'intensité des chocs ciblés')
plt.xlabel('Intensité du choc')
plt.ylabel('Proportion moyenne de défauts')
plt.grid(True)
plt.savefig('targeted_intensity_analysis.png')
plt.show()

print("\nAnalyse terminée. Les graphiques ont été sauvegardés.")
