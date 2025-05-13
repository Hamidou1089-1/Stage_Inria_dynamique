import copy
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx

from model import RandomNetwork
from controller import Simulation

# Paramètres de la simulation (réduits pour un temps d'exécution plus court)
bank_counts = [50, 100, 300, 400]  # Différentes tailles de réseau
probabilities = np.arange(0.1, 1.1, 0.1)  # Espacées pour plus de clarté
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

# Figure 1: Surface 3D interactive (nombre de banques, mesure du choc, proportion de défauts)
fig1 = go.Figure()

# Pour une probabilité spécifique (par exemple 0.5)
selected_prob = 0.8
colorscale = 'Viridis'

# Création des données pour la surface
x_vals = []
y_vals = []
z_vals = []

for i, num_banks in enumerate(bank_counts):
    for j, shock in enumerate(results[num_banks][selected_prob]['shock_measure']):
        x_vals.append(num_banks)
        y_vals.append(shock)
        z_vals.append(results[num_banks][selected_prob]['default_count'][j])

# Ajout de la surface
fig1.add_trace(go.Mesh3d(
    x=x_vals,
    y=y_vals,
    z=z_vals,
    intensity=z_vals,
    colorscale=colorscale,
    opacity=0.8,
    name='Proportion de défauts'
))

# Ajout d'un plan à z=0.5 pour visualiser le seuil
x_plane = np.linspace(min(bank_counts)-10, max(bank_counts)+10, 10)
z_plane = np.linspace(0, 1, 10)
x_plane, z_plane = np.meshgrid(x_plane, z_plane)
y_plane = np.ones(x_plane.shape) * 0.5

fig1.add_trace(go.Surface(
    x=x_plane,
    y=y_plane,
    z=z_plane,
    colorscale=[[0, 'red'], [1, 'red']],
    showscale=False,
    opacity=0.3,
    name='Seuil 0.5'
))

# Configuration de la disposition
fig1.update_layout(
    title='Relation 3D entre Taille du Réseau, Choc et Défauts (p=0.7)',
    scene=dict(
        xaxis_title='Nombre de Banques',
        yaxis_title='Mesure du Choc',
        zaxis_title='Proportion de Défauts',
        xaxis=dict(range=[min(bank_counts), max(bank_counts)]),
        yaxis=dict(range=[0, 1]),
        zaxis=dict(range=[0, 1]),
    ),
    width=1900,
    height=1200
)

# Enregistrement de la figure en HTML pour interaction
fig1.write_html('fig1_3d_interactive_bank_shock_default.html')

# Figure 2: Surface 3D interactive (probabilité de connexion, mesure du choc, proportion de défauts)
fig2 = go.Figure()

# Pour un nombre de banques spécifique
selected_banks = 100

# Création des données pour la surface
x_vals = []
y_vals = []
z_vals = []

for i, prob in enumerate(probabilities):
    for j, shock in enumerate(results[selected_banks][prob]['shock_measure']):
        x_vals.append(prob)
        y_vals.append(shock)
        z_vals.append(results[selected_banks][prob]['default_count'][j])

# Ajout de la surface
fig2.add_trace(go.Mesh3d(
    x=x_vals,
    y=y_vals,
    z=z_vals,
    intensity=z_vals,
    colorscale=colorscale,
    opacity=0.8,
    name='Proportion de défauts'
))

# Ajout d'un plan vertical à y=0.5 pour visualiser le seuil
x_plane = np.linspace(min(probabilities)-0.1, max(probabilities)+0.1, 10)
z_plane = np.linspace(0, 1, 10)
x_plane, z_plane = np.meshgrid(x_plane, z_plane)
y_plane = np.ones(x_plane.shape) * 0.5

fig2.add_trace(go.Surface(
    x=x_plane,
    y=y_plane,
    z=z_plane,
    colorscale=[[0, 'red'], [1, 'red']],
    showscale=False,
    opacity=0.3,
    name='Seuil 0.5'
))

# Configuration de la disposition
fig2.update_layout(
    title='Surface 3D de Défauts en fonction de la Densité et du Choc (N=100)',
    scene=dict(
        xaxis_title='Probabilité de Connexion (p)',
        yaxis_title='Mesure du Choc',
        zaxis_title='Proportion de Défauts',
        xaxis=dict(range=[min(probabilities), max(probabilities)]),
        yaxis=dict(range=[0, 1]),
        zaxis=dict(range=[0, 1]),
    ),
    width=900,
    height=700
)

# Enregistrement de la figure en HTML pour interaction
fig2.write_html('fig2_3d_interactive_prob_shock_default.html')

# Figure 3: Visualisation des courbes 2D avec animation de la rotation et curseur
# pour la probabilité
fig3 = make_subplots(rows=1, cols=1)

# Création d'une palette de couleurs
colorscale = [
    [0, 'rgb(68, 1, 84)'],  # Violet foncé
    [0.2, 'rgb(59, 82, 139)'],  # Bleu
    [0.4, 'rgb(33, 144, 141)'],  # Turquoise
    [0.6, 'rgb(90, 200, 81)'],  # Vert
    [0.8, 'rgb(253, 231, 37)'],  # Jaune
    [1, 'rgb(255, 255, 255)']   # Blanc
]

# Pour un nombre de banques spécifique
selected_banks = 100

# Ajout des courbes pour chaque probabilité
for i, probability in enumerate(probabilities):
    # Calculer la couleur correspondante
    color_index = i / (len(probabilities) - 1)
    rgb_color = f'rgb({int(255 * (1-color_index))}, {int(200 * color_index)}, {int(255 * color_index)})'

    fig3.add_trace(
        go.Scatter(
            x=results[selected_banks][probability]['shock_measure'],
            y=results[selected_banks][probability]['default_count'],
            mode='lines',
            name=f'p={probability:.1f}',
            line=dict(color=rgb_color, width=3)
        )
    )

# Ajout d'une ligne verticale pour le seuil critique
fig3.add_shape(
    type="line",
    x0=0.5, y0=0, x1=0.5, y1=1,
    line=dict(color="Red", width=2, dash="dash"),
)

# Configuration de la disposition
fig3.update_layout(
    title='Impact du Choc sur les Défauts pour Différentes Densités (N=100)',
    xaxis_title='Mesure du Choc',
    yaxis_title='Proportion de Défauts',
    legend_title='Probabilité de connexion',
    xaxis=dict(range=[0, 1]),
    yaxis=dict(range=[0, 1]),
    width=900,
    height=600,
    plot_bgcolor='rgba(240, 240, 240, 0.8)'
)

# Ajout d'une grille pour faciliter la lecture
fig3.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

# Enregistrement de la figure en HTML pour interaction
fig3.write_html('fig3_2d_interactive_shock_default.html')

# Figure 4: Visualisation interactive des variations
fig4 = make_subplots(rows=1, cols=1)

# Ajout des courbes pour chaque probabilité
for i, probability in enumerate(probabilities):
    # Calculer la couleur correspondante
    color_index = i / (len(probabilities) - 1)
    rgb_color = f'rgb({int(255 * (1-color_index))}, {int(200 * color_index)}, {int(255 * color_index)})'

    fig4.add_trace(
        go.Scatter(
            x=results[selected_banks][probability]['shock_measure'][:-1],
            y=results[selected_banks][probability]['variation'],
            mode='lines',
            name=f'p={probability:.1f}',
            line=dict(color=rgb_color, width=3)
        )
    )

# Ajout d'une ligne verticale pour le seuil critique
fig4.add_shape(
    type="line",
    x0=0.5, y0=0, x1=0.5, y1=0.3,  # Adapter la hauteur en fonction des données
    line=dict(color="Red", width=2, dash="dash"),
)

# Configuration de la disposition
fig4.update_layout(
    title='Variation de la Proportion de Défauts en fonction du Choc (N=100)',
    xaxis_title='Mesure du Choc',
    yaxis_title='Variation de la Proportion de Défauts',
    legend_title='Probabilité de connexion',
    xaxis=dict(range=[0, 1]),
    yaxis=dict(range=[0, 0.3]),  # Adapter en fonction des données
    width=900,
    height=600,
    plot_bgcolor='rgba(240, 240, 240, 0.8)'
)

# Ajout d'une grille pour faciliter la lecture
fig4.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig4.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

# Enregistrement de la figure en HTML pour interaction
fig4.write_html('fig4_2d_interactive_variation.html')

print("Toutes les visualisations interactives ont été générées avec succès!")