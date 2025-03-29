from model import NetworkGenerator

from model import Model
import numpy as np

class EisenbergNoeModel(Model):


    def __init__(self, network: NetworkGenerator):
        self.network = network

    def apply_shock(self, shock_vector: np.array):
        self.network.net_worth = self.network.net_worth - shock_vector


    def compute_clearing_payments(self, max_iterations: int, shock_vector: np.array) -> np.array:
        """
        On part du principe que cette methode n'est appéllé que lorsqu'une banque ou plusieurs banques, sont en default.
        :return:  Clearing_payments
        """
        vector_of_payments = self.network.due_payements
        while max_iterations > 0:
            new_vector_of_payments = np.copy(vector_of_payments)
            vector_of_payments = np.minimum(self.network.due_payements, np.maximum(self.network.matrix_relative_liabilities.T @ new_vector_of_payments - shock_vector + self.network.vector_outside_asset, 0))

            if np.allclose(vector_of_payments, new_vector_of_payments, 0.001):
                return vector_of_payments
            max_iterations -= 1


    def measure_systemic_impact(self, shock_vector: np.array):
        """
        We compute the number of default in terms of proportion.
        And measure how big the shock was in terms of proportion (a shock can't surpass the total outside asset)
        :param shock_vector:
        :return:
        """
        shock_measure = np.sum(shock_vector)/np.sum(self.network.vector_outside_asset)

        default_count = self.network.default_vector.count(True)/self.network.number_bank
        return shock_measure, default_count


    def initialize(self, network):
        """
        Je ne sais pas encore si j'aurai vraiment besoin de cette méthode.
        :param network:
        :return:
        """
        pass



