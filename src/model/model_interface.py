from abc import ABC, abstractmethod
from model import NetworkGenerator
import numpy as np

class Model(ABC):
    """Interface abstraite pour différents modèles de contagion financière"""


    @abstractmethod
    def initialize(self, network: NetworkGenerator):
        """Initialise le modèle avec un réseau"""
        pass

    @abstractmethod
    def apply_shock(self, shock_type):
        """Applique un choc exogène au système"""
        pass

    @abstractmethod
    def compute_clearing_payments(self, max_iterations: int, shock_vector: np.array):
        """Calcule le vecteur de paiements d'équilibre"""
        pass

    @abstractmethod
    def measure_systemic_impact(self, shock_vector: np.array):
        """Mesure l'impact systémique après la propagation"""
        pass
