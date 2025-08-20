#%% md
# # Simulation deuxieme partie du stage
# 
#%%
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
from typing import Tuple, Optional, Dict, List
from abc import ABC, abstractmethod
from enum import Enum
#%%
class NetworkTopology(Enum):
    ERDOS_RENYI = "erdos_renyi"
    SMALL_WORLD = "small_world"
    SCALE_FREE = "scale_free"


#%%
class BankingNetwork:
    """
    Classe pour générer et gérer un réseau bancaire avec différentes topologies.
    Conserve l'implémentation NetworkX propre et le mécanisme d'Eisenberg-Noe.
    """

    def __init__(self, number_bank: int, topology: NetworkTopology,
                 probability_of_linking: float = 0.1, **topology_params):
        self.number_bank = number_bank
        self.topology = topology
        self.probability_of_linking = probability_of_linking
        self.topology_params = topology_params

        # Structures de données (conservées de l'implémentation précédente)
        self.graph = None
        self.vector_outside_liabilities = None
        self.vector_outside_asset = None
        self.matrix_obligation = None
        self.matrix_relative_exposures = None

        # Génération du réseau
        self.generate()

    def generate(self):
        """Génère le réseau selon la topologie choisie."""
        # Génération du graphe
        if self.topology == NetworkTopology.ERDOS_RENYI:
            self.graph = self._generate_erdos_renyi()
        elif self.topology == NetworkTopology.SMALL_WORLD:
            self.graph = self._generate_small_world()
        elif self.topology == NetworkTopology.SCALE_FREE:
            self.graph = self._generate_scale_free()

        # Génération des bilans (méthode conservée)
        self._generate_balance_sheets()

    def _generate_erdos_renyi(self):
        """Génère un graphe Erdős-Rényi dirigé."""
        return nx.erdos_renyi_graph(
            n=self.number_bank,
            p=self.probability_of_linking,
            directed=True
        )

    def _get_calibrated_params(self):
        """Calibre automatiquement les paramètres selon le nombre de banques."""
        target_avg_degree = self.probability_of_linking * (self.number_bank - 1)

        params = {
            NetworkTopology.SMALL_WORLD: {
                'k': max(2, int(2 * target_avg_degree)),  # k doit être pair et ≥ 2
                'p': 0.3  # Bon compromis clustering/distance
            },
            NetworkTopology.SCALE_FREE: {
                'm': max(1, int(target_avg_degree / 2))  # m ≥ 1
            }
        }

        # Override avec paramètres utilisateur si fournis
        if self.topology in params:
            params[self.topology].update(self.topology_params)
            return params[self.topology]
        return {}

    def _generate_small_world(self):
        """Génère un graphe Small World dirigé avec calibrage automatique."""
        calibrated = self._get_calibrated_params()
        k, p = calibrated['k'], calibrated['p']

        # Assure que k est valide pour la taille du réseau
        k = min(k, self.number_bank - 1)
        if k % 2 == 1: k -= 1  # k doit être pair
        if k < 2: k = 2

        undirected = nx.watts_strogatz_graph(self.number_bank, k, p)
        return self._convert_to_directed(undirected)

    def _generate_scale_free(self):
        """Génère un graphe Scale-Free dirigé avec calibrage automatique."""
        calibrated = self._get_calibrated_params()
        m = min(calibrated['m'], self.number_bank - 1)  # m < n

        undirected = nx.barabasi_albert_graph(self.number_bank, m)
        return self._convert_to_directed(undirected, preferential=True)

    def _convert_to_directed(self, undirected_graph, preferential=False):
        """Convertit un graphe non-dirigé en dirigé de manière cohérente."""
        directed = nx.DiGraph()
        directed.add_nodes_from(range(self.number_bank))

        for u, v in undirected_graph.edges():
            # Direction aléatoire pour chaque arête
            if np.random.random() < 0.5:
                directed.add_edge(u, v)
            else:
                directed.add_edge(v, u)

            # Probabilité d'arête bidirectionnelle
            if preferential:
                # Pour scale-free : probabilité basée sur les degrés
                degree_sum = undirected_graph.degree(u) + undirected_graph.degree(v)
                prob_bidirectional = min(0.5, degree_sum / (4 * self.number_bank))
            else:
                # Pour small world : probabilité fixe
                prob_bidirectional = self.probability_of_linking * 0.3

            if np.random.random() < prob_bidirectional:
                if directed.has_edge(u, v):
                    directed.add_edge(v, u)
                else:
                    directed.add_edge(u, v)

        return directed

    def _generate_balance_sheets(self):
        """Génère les bilans bancaires (méthode conservée de ton implémentation)."""
        n = self.number_bank
        self.vector_outside_liabilities = np.zeros(n)
        self.vector_outside_asset = np.zeros(n)
        self.matrix_obligation = np.zeros((n, n))

        # Génération des passifs externes
        for i in range(n):
            if np.random.random() < self.probability_of_linking:
                self.vector_outside_liabilities[i] = stats.gamma.rvs(a=150)

        # Génération des obligations interbancaires
        for i, j in self.graph.edges():
            self.matrix_obligation[i][j] = stats.gamma.rvs(a=150)

        # Équilibrage des bilans et calcul des expositions relatives
        self._balance_sheets()

    def _balance_sheets(self):
        """Méthode conservée de ton implémentation."""
        je_dois = np.sum(self.matrix_obligation, axis=1)
        on_me_doit = np.sum(self.matrix_obligation, axis=0)

        for i in range(self.number_bank):
            deficit_total = je_dois[i] + self.vector_outside_liabilities[i] - on_me_doit[i]

            if deficit_total > 0:
                self.vector_outside_asset[i] = deficit_total + stats.gamma.rvs(a=200)
            else:
                self.vector_outside_asset[i] = stats.gamma.rvs(a=200)

        self._compute_relative_exposures()

    def _compute_relative_exposures(self):
        """Calcule la matrice relative d'exposition."""
        self.matrix_relative_exposures = np.zeros_like(self.matrix_obligation)

        for i in range(self.number_bank):
            total_du_par_i = np.sum(self.matrix_obligation[i, :])
            if total_du_par_i > 0:
                self.matrix_relative_exposures[i, :] = self.matrix_obligation[i, :] / total_du_par_i

    def compute_clearing_payments(self, shock_vector: np.array,
                                tolerance: float = 1e-9) -> np.array:
        """Méthode Eisenberg-Noe conservée."""
        due_payments = np.sum(self.matrix_obligation, axis=1)
        vector_of_payments = due_payments.copy()

        if np.all(shock_vector == 0):
            return vector_of_payments

        while True:
            new_vector_of_payments = np.minimum(
                due_payments,
                np.maximum(
                    self.matrix_relative_exposures.T @ vector_of_payments
                    - shock_vector
                    + self.vector_outside_asset,
                    0
                )
            )

            if np.allclose(new_vector_of_payments, vector_of_payments, rtol=tolerance):
                return new_vector_of_payments

            vector_of_payments = new_vector_of_payments



    def get_net_worth_after_clearing(self, shock_vector: np.array) -> Tuple[np.array, np.array]:
        """Calcule le net worth après clearing (méthode conservée)."""
        payments = self.compute_clearing_payments(shock_vector)
        updated_obligations = self.get_updated_obligation_matrix(payments)

        actifs_internes_effectifs = np.sum(updated_obligations, axis=0)

        net_worth = (
            (self.vector_outside_asset - shock_vector) +
            actifs_internes_effectifs -
            self.vector_outside_liabilities -
            payments
        )

        return net_worth, payments

    def get_updated_obligation_matrix(self, payments_vector: np.array) -> np.array:
        """Matrice d'obligations actualisée après clearing."""
        updated_matrix = np.zeros_like(self.matrix_obligation)

        for i in range(self.number_bank):
            updated_matrix[i, :] = payments_vector[i] * self.matrix_relative_exposures[i, :]

        return updated_matrix

    def count_defaults(self, shock_vector: np.array, threshold: float = 0.0) -> int:
        """Compte les défauts après clearing."""
        net_worth, _ = self.get_net_worth_after_clearing(shock_vector)
        return np.sum(net_worth <= threshold)

    def compute_connectivity_metrics(self) -> Dict:
        """Calcule les métriques de connectivité pour comparaison entre topologies."""
        n = self.number_bank
        m = self.graph.number_of_edges()

        return {
            'density': m / (n * (n-1)) if n > 1 else 0,
            'avg_degree': 2*m / n if n > 0 else 0,
            'clustering': nx.average_clustering(self.graph) if n > 0 else 0,
            'max_degree': max(dict(self.graph.degree()).values()) if n > 0 else 0,
            'degree_variance': np.var(list(dict(self.graph.degree()).values())) if n > 0 else 0
        }

#%%
class ShockModel(ABC):
    """Classe abstraite pour les différents modèles de chocs."""

    @abstractmethod
    def generate_shock(self, network: BankingNetwork) -> Tuple[np.array, Dict]:
        """Génère un vecteur de chocs et retourne des métadonnées."""
        pass
#%%
class TargetedShockModel(ShockModel):
    """Modèle de choc ciblé (comme dans le papier de référence)."""

    def __init__(self, target_strategy: str = "random", shock_intensity: float = 1.0):
        self.target_strategy = target_strategy
        self.shock_intensity = shock_intensity

    def generate_shock(self, network: BankingNetwork) -> Tuple[np.array, Dict]:
        """Génère un choc ciblé sur une banque spécifique."""
        target = self._select_target(network)

        shock_vector = np.zeros(network.number_bank)
        shock_vector[target] = self.shock_intensity * network.vector_outside_asset[target]

        metadata = {
            'type': 'targeted',
            'target': target,
            'target_strategy': self.target_strategy,
            'shock_size': shock_vector[target]
        }

        return shock_vector, metadata

    def _select_target(self, network: BankingNetwork) -> int:
        """Sélectionne la banque à cibler selon la stratégie."""
        if self.target_strategy == "max_degree":
            degrees = dict(network.graph.degree())
            return max(degrees, key=degrees.get)
        elif self.target_strategy == "max_assets":
            return np.argmax(network.vector_outside_asset)
        elif self.target_strategy == "systemic":
            scores = []
            for i in range(network.number_bank):
                degree = network.graph.degree(i)
                assets = network.vector_outside_asset[i]
                scores.append(degree * assets)
            return np.argmax(scores)
        else:  # random
            return np.random.randint(0, network.number_bank)

#%%
class CorrelatedShockModel(ShockModel):
    """Modèle de chocs corrélés avec facteur commun."""

    def __init__(self, correlation_strength: float = 0.3, crisis_prob: float = 0.1):
        self.correlation_strength = correlation_strength
        self.crisis_prob = crisis_prob

    def generate_shock(self, network: BankingNetwork) -> Tuple[np.array, Dict]:
        """Génère des chocs corrélés."""
        n = network.number_bank

        is_crisis = np.random.random() < self.crisis_prob
        alpha = 0.7 if is_crisis else self.correlation_strength

        common_factor = np.random.pareto(2.0)
        idiosyncratic = np.random.pareto(2.0, size=n)

        shock_intensities = alpha * common_factor + (1-alpha) * idiosyncratic
        shock_intensities = shock_intensities / np.max(shock_intensities) * 0.5  # Normalisation

        shock_vector = shock_intensities * network.vector_outside_asset

        metadata = {
            'type': 'correlated',
            'is_crisis': is_crisis,
            'correlation_strength': alpha,
            'common_factor': common_factor
        }

        return shock_vector, metadata

#%%
class LiquidityShockModel(ShockModel):
    """Modèle de choc de liquidité avec ventes forcées."""

    def __init__(self, distress_prob: float = 0.2, fire_sale_intensity: float = 0.5):
        self.distress_prob = distress_prob
        self.fire_sale_intensity = fire_sale_intensity

    def generate_shock(self, network: BankingNetwork) -> Tuple[np.array, Dict]:
        """Génère un choc de liquidité."""
        n = network.number_bank

        distressed = np.random.random(n) < self.distress_prob
        total_fire_sales = np.sum(network.vector_outside_asset[distressed])

        if total_fire_sales > 0:
            price_impact = np.exp(-self.fire_sale_intensity * total_fire_sales /
                                np.sum(network.vector_outside_asset))
        else:
            price_impact = 1.0

        shock_vector = (1 - price_impact) * network.vector_outside_asset

        metadata = {
            'type': 'liquidity',
            'distressed_banks': distressed,
            'price_impact': price_impact,
            'total_fire_sales': total_fire_sales
        }

        return shock_vector, metadata

#%%
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List

# Configuration des graphiques
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'lines.linewidth': 3,
    'lines.markersize': 8,
    'grid.alpha': 0.3,
    'axes.grid': True
})

def run_simple_simulations(n_banks=50, n_simulations=30):
    """
    Simulations directes pour démontrer les effets de diversification et contagion.
    """

    # =========================================================================
    # GRAPHIQUE 1: EFFET DE LA DIVERSIFICATION - CHOC CIBLÉ
    # Pour chaque topologie séparément
    # =========================================================================

    print("1. Simulation effet de diversification avec choc ciblé...")

    # Plage de connectivité à tester
    connectivity_range = np.linspace(0.05, 0.9, 15)

    # Pour chaque topologie
    topologies = [
        (NetworkTopology.ERDOS_RENYI, "Erdős-Rényi"),
        (NetworkTopology.SMALL_WORLD, "Small World"),
        (NetworkTopology.SCALE_FREE, "Scale-Free")
    ]

    for topology_enum, topology_name in topologies:
        print(f"  - {topology_name}...")

        mean_defaults = []
        std_defaults = []

        for p in connectivity_range:
            defaults_per_sim = []

            for _ in range(n_simulations):
                # Créer le réseau
                if topology_enum == NetworkTopology.SMALL_WORLD:
                    network = BankingNetwork(
                        number_bank=n_banks,
                        topology=topology_enum,
                        probability_of_linking=p,
                        k=max(4, int(n_banks * p)),
                        p=0.3
                    )
                elif topology_enum == NetworkTopology.SCALE_FREE:
                    network = BankingNetwork(
                        number_bank=n_banks,
                        topology=topology_enum,
                        probability_of_linking=p,
                        m=max(2, int(n_banks * p / 2))
                    )
                else:
                    network = BankingNetwork(
                        number_bank=n_banks,
                        topology=topology_enum,
                        probability_of_linking=p
                    )

                # Choc ciblé: retirer TOUS les actifs externes de la banque systémique
                shock_model = TargetedShockModel("systemic", shock_intensity=1.0)
                shock_vector, _ = shock_model.generate_shock(network)

                # Compter les défauts après propagation
                n_defaults = network.count_defaults(shock_vector)
                defaults_per_sim.append(n_defaults)

            mean_defaults.append(np.mean(defaults_per_sim))
            std_defaults.append(np.std(defaults_per_sim))

        # Graphique individuel pour chaque topologie
        fig, ax = plt.subplots(figsize=(10, 7))

        ax.plot(connectivity_range, mean_defaults,
                color='#2C3E50', linewidth=3,
                marker='o', markersize=8)

        ax.fill_between(connectivity_range,
                        np.array(mean_defaults) - np.array(std_defaults),
                        np.array(mean_defaults) + np.array(std_defaults),
                        alpha=0.2, color='#2C3E50')

        ax.set_xlabel('Connectivité (p)', fontsize=16, fontweight='bold')
        ax.set_ylabel('Nombre de défauts', fontsize=16, fontweight='bold')
        ax.set_title(f'Effet de Diversification - {topology_name}\n(Choc ciblé systémique)',
                    fontsize=18, fontweight='bold')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"figures_rapport/diversification_{topology_name.lower().replace(' ', '_')}.pdf")
        plt.show()

    # =========================================================================
    # GRAPHIQUE 2: CHOC EXOGÈNE - ERDŐS-RÉNYI UNIQUEMENT
    # Transition de phase pour différents niveaux de connectivité
    # =========================================================================

    print("\n2. Simulation choc exogène corrélé (Erdős-Rényi)...")

    # Niveaux de connectivité à tester
    connectivity_levels = [0.1, 0.3, 0.5, 0.7, 0.9]

    # Intensités de choc à tester
    shock_intensities = np.linspace(0, 1, 20)

    fig, ax = plt.subplots(figsize=(12, 8))

    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(connectivity_levels)))

    for idx, p in enumerate(connectivity_levels):
        print(f"  - Connectivité p={p}...")

        mean_defaults_by_intensity = []

        for intensity in shock_intensities:
            defaults_per_sim = []

            for _ in range(n_simulations):
                # Créer réseau Erdős-Rényi
                network = BankingNetwork(
                    number_bank=n_banks,
                    topology=NetworkTopology.ERDOS_RENYI,
                    probability_of_linking=p
                )

                # Choc exogène corrélé avec intensité variable
                # On simule un choc qui affecte toutes les banques
                shock_vector = intensity * network.vector_outside_asset

                # Compter les défauts
                n_defaults = network.count_defaults(shock_vector)
                defaults_per_sim.append(n_defaults / n_banks)  # Proportion

            mean_defaults_by_intensity.append(np.mean(defaults_per_sim))

        # Tracer la courbe
        ax.plot(shock_intensities, mean_defaults_by_intensity,
                color=colors[idx], linewidth=3,
                marker='o', markersize=6, markevery=3,
                label=f'p = {p}')

    ax.set_xlabel('Intensité du choc exogène', fontsize=16, fontweight='bold')
    ax.set_ylabel('Proportion de défauts', fontsize=16, fontweight='bold')
    ax.set_title('Transition de Phase - Choc Exogène\n(Réseau Erdős-Rényi)',
                fontsize=18, fontweight='bold')
    ax.legend(loc='best', fontsize=14, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    plt.tight_layout()
    plt.savefig("figures_rapport/transition_phase_exogene.pdf")
    plt.show()

    # =========================================================================
    # GRAPHIQUE 3: CAPACITÉ D'ABSORPTION - NET WORTH TOTAL
    # Évolution du coussin de sécurité avec la connectivité
    # =========================================================================

    print("\n3. Simulation capacité d'absorption (net worth)...")

    connectivity_range = np.linspace(0.05, 0.9, 15)

    # Pour Erdős-Rényi uniquement
    net_worth_before = []
    net_worth_after = []

    for p in connectivity_range:
        nw_before_sim = []
        nw_after_sim = []

        for _ in range(n_simulations):
            network = BankingNetwork(
                number_bank=n_banks,
                topology=NetworkTopology.ERDOS_RENYI,
                probability_of_linking=p
            )

            # Net worth initial (coussin de sécurité total)
            initial_net_worth = (network.vector_outside_asset -
                                network.vector_outside_liabilities -
                                np.sum(network.matrix_obligation, axis=1))
            total_nw_before = np.sum(np.maximum(0, initial_net_worth))

            # Appliquer un choc ciblé
            shock_model = TargetedShockModel("systemic", shock_intensity=1.0)
            shock_vector, _ = shock_model.generate_shock(network)

            # Net worth après clearing
            net_worth_after_clearing, _ = network.get_net_worth_after_clearing(shock_vector)
            total_nw_after = np.sum(np.maximum(0, net_worth_after_clearing))

            nw_before_sim.append(total_nw_before)
            nw_after_sim.append(total_nw_after)

        net_worth_before.append(np.mean(nw_before_sim))
        net_worth_after.append(np.mean(nw_after_sim))

    # Graphique du coussin de sécurité
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(connectivity_range, net_worth_before,
            color='#27AE60', linewidth=3,
            marker='s', markersize=8,
            label='Net worth initial')

    ax.plot(connectivity_range, net_worth_after,
            color='#E74C3C', linewidth=3,
            marker='o', markersize=8,
            label='Net worth après choc')

    # Zone de perte
    ax.fill_between(connectivity_range,
                    net_worth_after, net_worth_before,
                    alpha=0.2, color='red',
                    label='Perte de valeur')

    ax.set_xlabel('Connectivité (p)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Net Worth Total du Réseau', fontsize=16, fontweight='bold')
    ax.set_title('Capacité d\'Absorption du Réseau\n(Coussin de sécurité)',
                fontsize=18, fontweight='bold')
    ax.legend(loc='best', fontsize=14, framealpha=0.95)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("figures_rapport/capacite_absorption.pdf")
    plt.show()

    print("\n✅ Toutes les simulations terminées!")
    print("Graphiques sauvegardés dans 'figures_rapport/'")

# =========================================================================
# LANCEMENT
# =========================================================================

if __name__ == "__main__":
    # Créer le dossier de sauvegarde
    import os
    if not os.path.exists("figures_rapport"):
        os.makedirs("figures_rapport")

    # Lancer les simulations
    # Paramètres légers pour test rapide
    run_simple_simulations(n_banks=300, n_simulations=100)

    # Pour des résultats de meilleure qualité:
    # run_simple_simulations(n_banks=50, n_simulations=50)
#%%

#%%
