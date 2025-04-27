from model.shock_distribution import ShockDistribution
import numpy as np


class TargetedShockDistribution(ShockDistribution):
    """Chocs ciblés sur les nœuds les plus vulnérables ou les plus centraux"""

    def __init__(self, network, targeting_strategy="vulnerability", intensity=1.0):
        """
        Args:
            network: Le réseau financier
            targeting_strategy: Stratégie de ciblage ('vulnerability', 'centrality', 'asset_size')
            intensity: Facteur d'échelle pour l'intensité globale du choc (1.0 = normal)
        """
        super().__init__(network)
        self.targeting_strategy = targeting_strategy
        self.intensity = intensity

    def _calculate_targeting_weights(self):
        """Calcule les poids pour cibler les nœuds selon la stratégie choisie"""
        if self.targeting_strategy == "vulnerability":
            # Plus la vulnérabilité est élevée, plus la banque est susceptible d'être ciblée
            weights = self.network.get_vulnerabilities()
        elif self.targeting_strategy == "centrality":
            # Utilise la somme des dettes/créances comme mesure de centralité
            weights = np.sum(self.network.get_matrix_obligation(), axis=0) + \
                      np.sum(self.network.get_matrix_obligation(), axis=1)
        elif self.targeting_strategy == "asset_size":
            # Les banques avec plus d'actifs sont plus ciblées
            weights = self.network.get_vector_outside_assets()
        else:
            # Par défaut, poids uniformes
            weights = np.ones(self.n_banks)

        # Normaliser pour obtenir une distribution de probabilité
        return weights / np.sum(weights)

    def generate_shock(self, intensity=None):
        # Utiliser l'intensité fournie ou celle de l'instance
        if intensity is None:
            intensity = self.intensity

        assets = self.network.get_vector_outside_assets()
        weights = self._calculate_targeting_weights()

        # Sélectionner les banques cibles avec une probabilité proportionnelle aux poids
        targeted_banks = np.random.choice(
            self.n_banks,
            size=max(1, int(self.n_banks * 0.5)),  # Cibler ~50% des banques
            p=weights,
            replace=False
        )

        # Générer des chocs importants pour les banques ciblées
        shock = np.zeros(self.n_banks)
        shock[targeted_banks] = assets[targeted_banks] * np.random.uniform(0.6, 0.9, size=len(targeted_banks))

        return intensity * shock

    def generate_multiple_shocks(self, n_scenarios, intensity=None):
        return np.array([self.generate_shock(intensity) for _ in range(n_scenarios)])
