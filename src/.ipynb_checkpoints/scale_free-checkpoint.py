import networkx as nx
import numpy as np
from model import Network, Bank, ManualNetwork


def create_scalefree_network(n, m=2, weight_scale=100, baseline_asset=1000):
    """Crée un réseau scale-free avec le modèle Barabási-Albert"""
    G = nx.barabasi_albert_graph(n, m)
    # Convertir en matrice d'obligation...
    # [Suite similaire à la fonction précédente]

def create_smallworld_network(n, k=4, p=0.1, weight_scale=100, baseline_asset=1000):
    """Crée un réseau small-world avec le modèle Watts-Strogatz"""
    G = nx.watts_strogatz_graph(n, k, p)
    # Convertir en matrice d'obligation...
