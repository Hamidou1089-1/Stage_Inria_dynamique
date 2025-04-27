from abc import ABC, abstractmethod
import numpy as np

class ShockDistribution(ABC):
    """Classe abstraite pour les distributions de chocs financiers"""

    def __init__(self, network):
        self.network = network
        self.n_banks = network.number_bank

    @abstractmethod
    def generate_shock(self, intensity=1.0):
        """Génère un vecteur de choc basé sur la distribution

        Args:
            intensity: Facteur d'échelle pour l'intensité globale du choc (1.0 = normal)

        Returns:
            np.array: Vecteur de choc à appliquer au réseau
        """
        pass

    @abstractmethod
    def generate_multiple_shocks(self, n_scenarios, intensity=1.0):
        """Génère plusieurs scénarios de chocs

        Args:
            n_scenarios: Nombre de scénarios à générer
            intensity: Facteur d'échelle pour l'intensité des chocs

        Returns:
            list: Liste de vecteurs de chocs
        """
        pass