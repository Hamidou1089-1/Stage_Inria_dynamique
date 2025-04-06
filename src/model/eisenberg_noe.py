from model import Network

from model import Model
import numpy as np

class EisenbergNoeModel(Model):


    def __init__(self, network: Network):
        super().__init__(network)


    def apply_shock(self, shock_vector: np.array):
        self.network.set_net_worth(self.network.net_worth - shock_vector)
        default = [self.network.net_worth[k]<=0 for k in range(len(self.network.net_worth))]
        self.network.set_default_vector(default)
        return


    def compute_clearing_payments(self, max_iterations: int, shock_vector: np.array) -> np.array:
        vector_of_payments = self.network.due_payements
        while max_iterations > 0:
            # Calculer de nouveaux paiements basés sur les paiements actuels
            new_vector_of_payments = np.minimum(self.network.due_payements, np.maximum(self.network.matrix_relative_liabilities.T @ vector_of_payments - shock_vector + self.network.vector_outside_asset,0))

            # Vérifier si nous avons convergé
            if np.allclose(new_vector_of_payments, vector_of_payments, 0.001):
                return new_vector_of_payments

            # Mettre à jour pour la prochaine itération
            vector_of_payments = new_vector_of_payments
            max_iterations -= 1

        # Si on n'a pas convergé, renvoyer la dernière approximation
        return vector_of_payments

    def measure_systemic_impact(self, shock_vector: np.array):
        """
        We compute the number of default in terms of proportion.
        And measure how big the shock was in terms of proportion (a shock can't surpass the total outside asset)
        :param shock_vector:
        :return:
        """
        shock_measure = np.sum(shock_vector)/np.sum(self.network.vector_outside_asset)

        default_count_proportion = self.network.default_vector.count(True)/self.network.number_bank

        """
        Vulnerabilities measure, just through the vector beta
        """
        vulnerabilities_measure = np.max(self.network.vulnerabilities)

        return shock_measure, default_count_proportion, vulnerabilities_measure




    def initialize(self, network):
        """
        Je ne sais pas encore si j'aurai vraiment besoin de cette méthode.
        :param network:
        :return:
        """
        pass




