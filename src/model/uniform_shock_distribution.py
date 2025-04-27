import numpy as np
from model.shock_distribution import ShockDistribution

class UniformShockDistribution(ShockDistribution):
    """Chocs uniformes sur tous les nœuds"""

    def __init__(self, network, intensity=1.0):
        """
        Initializes the shock with the specified network and intensity.

        Parameters
        ----------
        :param network:
            The network object to be associated with this instance. Must be compatible
            with the superclass initialization.
        :param intensity:
            The intensity value, default is ``1.0``. Represents the level of intensity
            associated with the instance.
        """
        super().__init__(network)
        self.intensity = intensity

    def generate_shock(self, intensity=None):
        # Utiliser l'intensité fournie ou celle de l'instance
        if intensity is None:
            intensity = self.intensity

        # Choc uniforme : même pourcentage d'actifs pour chaque banque
        assets = self.network.get_vector_outside_assets()
        shock = intensity * assets * np.random.uniform(0, 1, size=self.n_banks)
        return shock

    def generate_multiple_shocks(self, n_scenarios, intensity=None):
        return np.array([self.generate_shock(intensity) for _ in range(n_scenarios)])
