

from model import Network

from model import Model
import numpy as np

class EisenbergNoeModel(Model):


    def __init__(self, network: Network):
        super().__init__(network)


    def apply_shock(self, shock_vector: np.array):
        """
        Applies a shock vector to the financial network by modifying the outside assets
        of banks and updating their balances, net worth, and default statuses accordingly.
        The function ensures shocks do not create negative outside assets.

        :param shock_vector: Shock values to be applied to the network's outside
            assets. Its size must match the number of banks in the network.
        :type shock_vector: np.array
        :return: None
        :rtype: None
        :raises Exception: If the shock vector would result in outside assets
            becoming negative for any bank.
        """
        if np.any(self.network.get_vector_outside_assets() - shock_vector < 0):
            raise Exception("Shock vector outside assets")

        self.network.set_vector_outside_assets(self.network.get_vector_outside_assets() - shock_vector)

        [bank.update_balance() for bank in self.network.banks]
        self.network.net_worth = np.array([bank.get_net_worth() for bank in self.network.banks])

        default = [bank.is_default_bank for bank in self.network.banks]
        self.network.set_default_vector(default)

        return




    def compute_clearing_payments(self, max_iterations: int, shock_vector: np.array) -> np.array:
        """
        Calculates the clearing payments within a financial network. The method iteratively
        computes a vector of payments until it stabilizes (converges), taking into account
        the shock vector, due payments, relative liabilities, and outside assets.

        :param max_iterations: The maximum number of iterations allowed for the convergence
            computation.
        :param shock_vector: A numpy array representing the external shocks applied to
            each node in the financial network.
        :return: A numpy array representing the stabilized vector of payments after
            iterative computation.
        """

        vector_of_payments = self.network.due_payements
        if np.all(shock_vector == 0):
            return vector_of_payments
        while True:
            # Calculer de nouveaux paiements basés sur les paiements actuels
            new_vector_of_payments = np.minimum(self.network.due_payements, np.maximum(self.network.matrix_relative_liabilities.T @ vector_of_payments - shock_vector + self.network.vector_outside_asset,0))

            # Vérifier si nous avons convergé
            if np.allclose(new_vector_of_payments, vector_of_payments, 0.000000001):
                print("Is this unique ? ", vector_of_payments[0])
                return new_vector_of_payments

            # Mettre à jour pour la prochaine itération
            vector_of_payments = new_vector_of_payments









    def measure_systemic_impact(self, shock_vector: np.array):
        """
        Computes the systemic impact of a given shock vector on the financial network.

        This function evaluates the systemic impact of external shocks applied to
        a network of financial entities. It measures the ratio of the total external
        shock to the network's aggregate outside assets and determines the proportion
        of banks that are in default. These metrics provide insights into the overall
        resilience of the financial network under stress.

        :param shock_vector: A numpy array representing the external shocks applied
            to each entity in the financial network.
        :return: A tuple containing:
            - shock_measure (float): The ratio of the sum of external shocks to the
              aggregate outside assets in the network.
            - default_count_proportion (float): The proportion of banks in the
              network that are in default as a result of the applied shocks.
        """

        # This irrevelant as a measure, cause it doesn't help us visualize the real impact, or the default cascade

        shock_measure = np.sum(shock_vector)/self.network.get_sum_outside_assets()

        default_count_proportion = np.sum(self.network.default_vector)/self.network.number_bank

        return shock_measure, default_count_proportion




    def initialize(self, network):
        """
        Je ne sais pas encore si j'aurai vraiment besoin de cette méthode.
        :param network:
        :return:
        """
        pass




