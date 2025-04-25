from model import Network

from model import Model
import numpy as np

class EisenbergNoeModel(Model):


    def __init__(self, network: Network):
        super().__init__(network)


    def apply_shock(self, shock_vector: np.array):
        """Ce comporte comme prevue"""
        if np.any(self.network.get_vector_outside_assets() - shock_vector < 0):
            raise Exception("Shock vector outside assets")

        self.network.set_vector_outside_assets(self.network.get_vector_outside_assets() - shock_vector)

        for k in range(len(shock_vector)):
            self.network.banks[k].update_balance()
            self.network.net_worth[k] = self.network.banks[k].get_net_worth()
        default = [self.network.banks[k].is_default_bank for k in range(len(self.network.net_worth))]
        #print("Default ",default)
        self.network.set_default_vector(default)
        return




    def compute_clearing_payments(self, max_iterations: int, shock_vector: np.array) -> np.array:

        vector_of_payments = self.network.due_payements
        if np.all(shock_vector == 0):
            return vector_of_payments
        while max_iterations > 0:
            # Calculer de nouveaux paiements basés sur les paiements actuels
            new_vector_of_payments = np.minimum(self.network.due_payements, np.maximum(self.network.matrix_relative_liabilities.T @ vector_of_payments - shock_vector + self.network.vector_outside_asset,0))

            # Vérifier si nous avons convergé
            if np.allclose(new_vector_of_payments, vector_of_payments, 0.00001):
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
        shock_measure = np.sum(shock_vector)/self.network.get_sum_outside_assets()

        default_count_proportion = self.network.default_vector.count(True)/self.network.number_bank
        #print("Default count proportion: ", default_count_proportion)
        """
        Vulnerabilities measure, A bank is vulnerable if the ratio between his networth and his outside assets is less than 1, the
        more his close to zero, the quicker he will be at default when a shock happens. 
        """


        return shock_measure, default_count_proportion




    def initialize(self, network):
        """
        Je ne sais pas encore si j'aurai vraiment besoin de cette méthode.
        :param network:
        :return:
        """
        pass




