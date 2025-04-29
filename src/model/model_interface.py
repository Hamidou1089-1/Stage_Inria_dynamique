from abc import ABC, abstractmethod
from copy import deepcopy

from model import RandomNetwork, Network
import numpy as np

class Model(ABC):
    """Interface abstraite pour différents modèles de contagion financière"""

    def __init__(self, network: Network):
        self.network = network

    @abstractmethod
    def initialize(self, network: Network):
        """Initialise le modèle avec un réseau"""
        pass

    @abstractmethod
    def apply_shock(self, shock_type):
        """
        Defines an abstract method to apply a shock to a system.

        This method serves as a blueprint for subclasses that need
        to implement specific functionality for applying a shock of
        a given type.

        :param shock_type: Specifies the type of shock to be applied.
        :type shock_type: np.array

        :return: None
        """
        pass

    @abstractmethod
    def compute_clearing_payments(self, max_iterations: int, shock_vector: np.array):
        """
        Compute clearing payments to achieve financial equilibrium among institutions
        in a network affected by external shocks. This method serves as an abstract
        specification that must be implemented by subclasses to perform the iterative
        calculation of equilibrium payments.

        :param max_iterations: Maximum number of iterations to compute clearing payments.
        :type max_iterations: int
        :param shock_vector: Array representing the external shocks applied to each
            institution in the network.
        :type shock_vector: numpy.array
        :return: Calculated clearing payments achieving financial equilibrium.
        :rtype: numpy.array
        """
        pass

    @abstractmethod
    def measure_systemic_impact(self, shock_vector: np.array):
        """
        Measure the systemic impact of a given shock vector.

        This is an abstract method that should be implemented by subclasses to define
        how a provided shock vector affects the overall system.

        :param shock_vector: Array representing the shock vector to be analyzed. The
                             vector encapsulates the intensity and distribution of
                             shocks within the system.
        :type shock_vector: np.array
        :return: None
        """
        pass

    def get_network(self):
        return self.network
    def set_network(self, network: Network):
        self.network = deepcopy(network)
        return


