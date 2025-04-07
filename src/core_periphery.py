import networkx as nx
import numpy as np
from model import Network, Bank, ManualNetwork

def create_core_periphery_network(n_core, n_periphery, p_core=0.7, p_periphery=0.2,
                                 weight_scale=100, baseline_asset=1000):
    """
    Crée un réseau core-periphery bancaire.

    Args:
        n_core: Nombre de banques dans le core
        n_periphery: Nombre de banques en périphérie
        p_core: Probabilité de connexion entre banques du core
        p_periphery: Probabilité de connexion entre core et périphérie
        weight_scale: Échelle des poids pour les obligations
        baseline_asset: Valeur de base pour les actifs extérieurs
    """
    n_total = n_core + n_periphery

    # Créer un graphe vide
    G = nx.DiGraph()
    G.add_nodes_from(range(n_total))

    ## Connecter les banques du core entre elles (réseau dense)
    for i in range(n_core):
        for j in range(n_core):
            if i != j and np.random.random() < p_core:
                # Direction déterminée par la taille relative des banques
                G.add_edge(i, j, weight=np.random.normal(weight_scale*3, weight_scale))

    # Connecter la périphérie au core avec des directions significatives
    for i in range(n_core, n_total):
        for j in range(n_core):
            if np.random.random() < p_periphery:
                # Les petites banques empruntent aux grandes (direction économique)
                G.add_edge(i, j, weight=np.random.normal(weight_scale, weight_scale/2))
            if np.random.random() < p_periphery/2:
                # Les grandes banques prêtent parfois aux petites (moins fréquent)
                G.add_edge(j, i, weight=np.random.normal(weight_scale/2, weight_scale/4))

    # Conversion en matrice d'obligation
    matrix_obligation = np.zeros((n_total, n_total))
    for i, j, data in G.edges(data=True):
        matrix_obligation[i, j] = data['weight']

    # Calculer actifs et passifs interbancaires
    internal_assets = np.sum(matrix_obligation, axis=1)  # Ce que les autres doivent à chaque banque
    internal_liabilities = np.sum(matrix_obligation, axis=0)  # Ce que chaque banque doit aux autres

    # Générer actifs et passifs externes pour équilibrer les bilans
    vector_outside_asset = np.zeros(n_total)
    vector_outside_liabilities = np.zeros(n_total)

    for i in range(n_total):
        # Les banques du core ont généralement plus d'actifs externes
        if i < n_core:
            base = baseline_asset * 5
        else:
            base = baseline_asset

        # Assurer un bilan positif
        net_internal = internal_assets[i] - internal_liabilities[i]
        if net_internal < 0:
            # Si le bilan interne est négatif, ajouter des actifs externes
            vector_outside_asset[i] = base + abs(net_internal) * 1.1
            vector_outside_liabilities[i] = base * 0.5
        else:
            # Si le bilan interne est positif, ajouter des passifs externes
            vector_outside_asset[i] = base
            vector_outside_liabilities[i] = base * 0.5 + net_internal * 0.8

    # Calculer les matrices dérivées nécessaires pour ManualNetwork
    matrix_relative_liabilities = np.zeros((n_total, n_total))
    due_payments = internal_liabilities + vector_outside_liabilities

    for i in range(n_total):
        if due_payments[i] > 0:
            matrix_relative_liabilities[i, :] = matrix_obligation[i, :] / due_payments[i]

    # Créer le réseau manuel
    return ManualNetwork(
        matrix_obligation=matrix_obligation,
        vector_outside_asset=vector_outside_asset,
        asset=internal_assets,
        vector_outside_liabilities=vector_outside_liabilities,
        liabilities=internal_liabilities,
        matrix_relative_liabilities=matrix_relative_liabilities
    )