import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx

from model import RandomNetwork
from controller import Simulation

# Paramètres de la simulation
bank_counts = [50, 100, 200, 300]  # Différentes tailles de réseau
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

# Figure 1: Graphique 3D (nombre de banques, mesure du choc, proportion de défauts)
SMALL_SIZE = 12
MEDIUM_SIZE = 18
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=BIGGER_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

fig1 = plt.figure(figsize=(12, 10))
ax1 = fig1.add_subplot(111, projection='3d')

# Création d'une grille pour la surface
X, Y = np.meshgrid(
    np.array(bank_counts),
    np.linspace(0, 1, shock_steps)
)

# Pour une probabilité spécifique (par exemple 0.5)
selected_prob = 0.5
Z = np.zeros((shock_steps, len(bank_counts)))

for i, num_banks in enumerate(bank_counts):
    Z[:, i] = results[num_banks][selected_prob]['default_count']

# Tracé de la surface
surf = ax1.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.8, antialiased=True)

# Ajout d'un plan à z=0.5 pour visualiser le seuil
threshold = 0.5
xx, yy = np.meshgrid(
    [min(bank_counts)-10, max(bank_counts)+10],
    [0, 1]
)
zz = np.ones(xx.shape) * threshold
ax1.plot_surface(xx, yy, zz, color='red', alpha=0.3)

# Configuration de l'axe z pour voir clairement le seuil à 0.5
ax1.set_zlim(0, 1)

# Ajout des étiquettes et de la barre de couleur
ax1.set_xlabel('Nombre de Banques')
ax1.set_ylabel('Mesure du Choc')
ax1.set_zlabel('Proportion de Défauts')
ax1.set_title(f'Relation 3D entre Taille du Réseau, Choc et Défauts (p={selected_prob})')
fig1.colorbar(surf, shrink=0.5, aspect=5)

# Enregistrement de la figure
plt.savefig('fig1_3d_bank_shock_default.png', dpi=300, bbox_inches='tight')
plt.close(fig1)

# Figure 2: Graphique 2D avec différentes probabilités
fig2, ax2 = plt.subplots(figsize=(12, 8))

# Pour un nombre de banques spécifique (par exemple 100)
selected_banks = 100
colors = plt.cm.viridis(np.linspace(0, 1, len(probabilities)))

for i, probability in enumerate(probabilities):
    ax2.plot(
        results[selected_banks][probability]['shock_measure'],
        results[selected_banks][probability]['default_count'],
        label=f'p={probability:.1f}',
        color=colors[i],
        linewidth=2
    )

# Ajout d'une ligne verticale à x=0.5 pour marquer le seuil observé
ax2.axvline(x=0.5, color='red', linestyle='--', label='Seuil critique (0.5)')

# Ajout des étiquettes et de la légende
ax2.set_xlabel('Mesure du Choc')
ax2.set_ylabel('Proportion de Défauts')
ax2.set_title(f'Impact du Choc sur les Défauts pour Différentes Densités (N={selected_banks})')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(loc='best')

# Enregistrement de la figure
plt.savefig('fig2_2d_prob_shock_default.png', dpi=300, bbox_inches='tight')
plt.close(fig2)

# Figure 3: Graphique 3D (probabilité de connexion, mesure du choc, proportion de défauts)
fig3 = plt.figure(figsize=(12, 10))
ax3 = fig3.add_subplot(111, projection='3d')

# Création d'une grille pour la surface
X, Y = np.meshgrid(
    probabilities,
    np.linspace(0, 1, shock_steps)
)

# Pour un nombre de banques spécifique
selected_banks = 100
Z = np.zeros((shock_steps, len(probabilities)))

for i, probability in enumerate(probabilities):
    Z[:, i] = results[selected_banks][probability]['default_count']

# Tracé de la surface
surf = ax3.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.8, antialiased=True)

# Ajout d'un plan vertical à x=0.5 pour visualiser le seuil
xx, zz = np.meshgrid(
    [min(probabilities)-0.1, max(probabilities)+0.1],
    [0, 1]
)
yy = np.ones(xx.shape) * 0.5
ax3.plot_surface(xx, yy, zz, color='red', alpha=0.3)

# Configuration des axes
ax3.set_xlim(min(probabilities), max(probabilities))
ax3.set_ylim(0, 1)
ax3.set_zlim(0, 1)

# Ajout des étiquettes et de la barre de couleur
ax3.set_xlabel('Probabilité de Connexion (p)')
ax3.set_ylabel('Mesure du Choc')
ax3.set_zlabel('Proportion de Défauts')
ax3.set_title(f'Surface 3D de Défauts en fonction de la Densité et du Choc (N={selected_banks})')
fig3.colorbar(surf, shrink=0.5, aspect=5)

# Enregistrement de la figure
plt.savefig('fig3_3d_prob_shock_default.png', dpi=300, bbox_inches='tight')
plt.close(fig3)

# Figure 4: Variation de la proportion de défauts en fonction du choc
fig4, ax4 = plt.subplots(figsize=(12, 8))

for i, probability in enumerate(probabilities):
    ax4.plot(
        results[selected_banks][probability]['shock_measure'][:-1],
        results[selected_banks][probability]['variation'],
        label=f'p={probability:.1f}',
        color=colors[i],
        linewidth=2
    )

# Ajout d'une ligne verticale à x=0.5 pour marquer le seuil observé
ax4.axvline(x=0.5, color='red', linestyle='--', label='Seuil critique (0.5)')

# Ajout des étiquettes et de la légende
ax4.set_xlabel('Mesure du Choc')
ax4.set_ylabel('Variation de la Proportion de Défauts')
ax4.set_title(f'Variation des Défauts en fonction du Choc pour Différentes Densités (N={selected_banks})')
ax4.grid(True, linestyle='--', alpha=0.7)
ax4.legend(loc='best')

# Enregistrement de la figure
plt.savefig('fig4_2d_variation_shock_default.png', dpi=300, bbox_inches='tight')
plt.close(fig4)