import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from model import RandomNetwork
from controller import Simulation

# Fixer le générateur aléatoire
np.random.seed(42)

# Créer un réseau plus contrôlé
def create_controlled_network(num_banks, connection_prob):
    """Crée un réseau où les banques ont des valeurs nettes plus homogènes"""
    network = RandomNetwork(num_banks, connection_prob)

    # Normaliser les actifs extérieurs pour qu'ils soient plus homogènes
    mean_asset = np.mean(network.vector_outside_asset)
    network.vector_outside_asset = np.ones(num_banks) * mean_asset * (0.8 + 0.4 * np.random.random(num_banks))

    # Recalculer les valeurs nettes
    for i in range(num_banks):
        on_me_doit = np.array([1]*num_banks).T @ network.matrix_obligation
        je_dois = network.matrix_obligation @ np.array([1]*num_banks)
        network.banks[i].set_outside_asset(network.vector_outside_asset[i])
        network.banks[i].set_net_worth(network.vector_outside_asset[i] + on_me_doit[i] -
                                       network.vector_outside_liabilities[i] - je_dois[i])

    return network

# Test avec chocs croissants sur le même réseau
def test_shock_sensitivity(num_banks=50, connection_prob=0.3):
    network = create_controlled_network(num_banks, connection_prob)
    results = []

    # Créer une base de choc
    base_shock = np.ones(num_banks) * np.mean(network.vector_outside_asset) * 0.5

    # Tester différentes intensités sur le même réseau
    for intensity in np.linspace(0.0, 1.0, 20):
        shock_vector = base_shock * intensity

        # Faire une copie du réseau pour chaque test
        test_network = copy.deepcopy(network)
        simulation = Simulation("Eisenberg", test_network, shock_vector)
        _, shock_measure, default_count, _ = simulation.simulate()

        results.append({
            'intensity': intensity,
            'shock_measure': shock_measure,
            'default_proportion': default_count
        })

    return pd.DataFrame(results)

# Fonction modifiée pour travailler avec les résultats de test_shock_sensitivity
def plot_sensitivity_results(results_df):
    plt.figure(figsize=(10, 6))

    # Tracer la relation entre l'intensité du choc et la proportion de défauts
    plt.scatter(results_df['shock_measure'], results_df['default_proportion'])

    # Ajouter une ligne de tendance
    z = np.polyfit(results_df['shock_measure'], results_df['default_proportion'], 2)
    p = np.poly1d(z)
    x_range = np.linspace(min(results_df['shock_measure']),
                          max(results_df['shock_measure']), 100)
    plt.plot(x_range, p(x_range), 'r--')

    plt.title('Relation entre la gravité du choc et la proportion de défauts')
    plt.xlabel('Mesure du choc')
    plt.ylabel('Proportion de banques en défaut')
    plt.grid(True, alpha=0.3)

    return plt.gcf()

# Pour tester plusieurs configurations
def run_multiple_tests():
    # Configuration à tester
    configs = [
        {'num_banks': 100, 'connection_prob': 0.01},
        {'num_banks': 100, 'connection_prob': 0.1},
        {'num_banks': 100, 'connection_prob': 0.2},
        {'num_banks': 100, 'connection_prob': 0.3},
        {'num_banks': 100, 'connection_prob': 0.4},
        {'num_banks': 100, 'connection_prob': 0.6},
        {'num_banks': 100, 'connection_prob': 0.7},
        {'num_banks': 100, 'connection_prob': 0.8},
        {'num_banks': 100, 'connection_prob': 0.9},
        {'num_banks': 1000, 'connection_prob': 0.01},
        {'num_banks': 1000, 'connection_prob': 0.1},
        {'num_banks': 1000, 'connection_prob': 0.2},
        {'num_banks': 1000, 'connection_prob': 0.3},
        {'num_banks': 1000, 'connection_prob': 0.4},
        {'num_banks': 1000, 'connection_prob': 0.6},
        {'num_banks': 1000, 'connection_prob': 0.7},
        {'num_banks': 1000, 'connection_prob': 0.8},
        {'num_banks': 1000, 'connection_prob': 0.9}
    ]

    all_results = []

    for config in configs:
        results = test_shock_sensitivity(**config)
        results['bank_size'] = config['num_banks']
        results['connection_prob'] = config['connection_prob']
        all_results.append(results)

    return pd.concat(all_results)

# Exécuter plusieurs tests
all_results = run_multiple_tests()

# Créer un graphique avec une sous-figure pour chaque configuration
def plot_multiple_tests(results_df):
    unique_sizes = results_df['bank_size'].unique()
    unique_probs = results_df['connection_prob'].unique()

    fig, axes = plt.subplots(len(unique_sizes), len(unique_probs),
                             figsize=(4*len(unique_probs), 4*len(unique_sizes)),
                             sharex=True, sharey=True)

    for i, size in enumerate(unique_sizes):
        for j, prob in enumerate(unique_probs):
            subset = results_df[(results_df['bank_size'] == size) &
                                (results_df['connection_prob'] == prob)]

            # Accéder au bon sous-graphique
            if len(unique_sizes) > 1 and len(unique_probs) > 1:
                ax = axes[i, j]
            elif len(unique_sizes) > 1:
                ax = axes[i]
            elif len(unique_probs) > 1:
                ax = axes[j]
            else:
                ax = axes

            # Tracer les points
            ax.scatter(subset['shock_measure'], subset['default_proportion'])

            # Ajouter une ligne de tendance
            if len(subset) > 1:
                z = np.polyfit(subset['shock_measure'], subset['default_proportion'], 2)
                p = np.poly1d(z)
                x_range = np.linspace(min(subset['shock_measure']),
                                      max(subset['shock_measure']), 100)
                ax.plot(x_range, p(x_range), 'r--')

            ax.set_title(f'Banques: {size}, Conn. prob: {prob}')
            ax.set_xlabel('Gravité du choc')
            ax.set_ylabel('Proportion de défauts')
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

# Visualiser tous les résultats
fig = plot_multiple_tests(all_results)
plt.savefig('multiple_tests.png', dpi=300)
plt.show()


