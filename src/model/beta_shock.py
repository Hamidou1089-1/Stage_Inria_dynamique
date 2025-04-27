from model.shock_distribution import ShockDistribution

import numpy as np

class BetaShockDistribution(ShockDistribution):
    """Chocs suivant une distribution Beta"""

    def __init__(self, network, alpha=2, beta=5, intensity=1.0):
        super().__init__(network)
        self.alpha = alpha
        self.beta = beta
        self.intensity = intensity

    def generate_shock(self, intensity=None):
        """
        Generates a shock based on the provided or instance-specific intensity,
        distributing it over the network's external assets.

        The method calculates shock values using a beta distribution, characterized
        by the instance's alpha and beta parameters, which define the shape of the
        distribution. The generated shock is proportional to the intensity, external
        assets, and random shock ratios.

        :param intensity: The magnitude of the shock to be applied. If not provided,
                          the instance's intensity value will be used.
                          (default is None)
        :type intensity: float or None
        :return: An array representing the computed shock values for each entity
                 in the network.
        :rtype: numpy.ndarray
        """
        # Utiliser l'intensité fournie ou celle de l'instance
        if intensity is None:
            intensity = self.intensity

        assets = self.network.get_vector_outside_assets()
        # La distribution Beta donne des valeurs entre 0 et 1
        # Plus alpha est petit et beta grand, plus les chocs seront concentrés près de 0
        shock_ratios = np.random.beta(self.alpha, self.beta, size=self.n_banks)
        shock = intensity * assets * shock_ratios
        return shock

    def generate_multiple_shocks(self, n_scenarios, intensity=None):
        """
        Generates multiple shock scenarios given a specific intensity and the
        number of scenarios requested.

        :param n_scenarios: Number of shock scenarios to generate.
        :type n_scenarios: int
        :param intensity: Intensity value for the shocks to be generated. If not
            provided, a default intensity will be applied.
        :type intensity: Optional[float]
        :return: A list containing the generated shock scenarios.
        :rtype: List
        """
        return [self.generate_shock(intensity) for _ in range(n_scenarios)]
