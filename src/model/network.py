import numpy as np
from model.bank import Bank
from abc import ABC, abstractmethod
from observer import Observable

class Network(Observable, ABC):
    """
    Interface abstraite pour different type de réseau:
    - Random
    - Small World
    - Scale free
    """

    def __init__(self, number_of_bank: int,  matrix_obligation=None,
                 vector_outside_asset=None, vector_outside_liabilities=None, probability_of_linking=0.1
                 ):

        """
        Initializes the object with banking and obligation system properties, setting up matrices
        and vectors associated with assets, liabilities, payments, probabilities, and vulnerabilities.
        The class performs critical configuration and computation of the financial network, including
        normalizing obligations, relating liabilities, and calculating vulnerabilities.

        :param number_of_bank: Number of banks in the system.
        :type number_of_bank: int
        :param matrix_obligation: Obligation matrix that represents commitments between banks, optional.
        :type matrix_obligation: numpy.ndarray or None
        :param vector_outside_asset: Array representing the external assets of the banks, optional.
        :type vector_outside_asset: numpy.ndarray or None
        :param vector_outside_liabilities: Array representing the external liabilities of the banks, optional.
        :type vector_outside_liabilities: numpy.ndarray or None
        :param probability_of_linking: Probability of establishing a connection between banks, default is 0.1.
        :type probability_of_linking: float
        """
        Observable.__init__(self)


        self.number_bank = number_of_bank
        self.vulnerabilities = np.array([0]*self.number_bank)
        self.relative_vulnerabilities = np.zeros((self.number_bank, self.number_bank))
        self.vulnerabilities_to_outside = np.array([0]*self.number_bank)
        self.matrix_obligation = matrix_obligation
        self.net_worth = np.array([0]*self.number_bank)
        self.vector_outside_asset = vector_outside_asset
        self.banks = np.empty(self.number_bank, dtype=object)
        self.vector_outside_liabilities = vector_outside_liabilities
        self.matrix_relative_liabilities = np.zeros((self.number_bank, self.number_bank))
        self.due_payements = np.array([0]*self.number_bank)
        self.default_vector = np.array([False]*self.number_bank)
        self.probability_of_linking = probability_of_linking
        self.sum_outside_asset = 0

        self.generate()

        n = self.number_bank
        self.je_dois = np.sum(self.matrix_obligation, axis=1)
        self.on_me_doit = np.sum(self.matrix_obligation , axis=0)
        self.due_payements = self.je_dois + self.vector_outside_liabilities
        # Initialisation de la matrice relative des obligations
        self.matrix_relative_liabilities = np.zeros_like(self.matrix_obligation, dtype=float)

        # Création du masque 2D pour où due_payements n'est pas zéro
        mask_2d = (self.due_payements[:, np.newaxis] != 0)

        # Division vectorisée avec masque
        np.divide(self.matrix_obligation, self.due_payements[:, np.newaxis],
                  out=self.matrix_relative_liabilities, where=mask_2d)





        self.relative_vulnerabilities = np.zeros_like(self.matrix_relative_liabilities, dtype=float)

        i_indices, j_indices = np.indices(self.matrix_relative_liabilities.shape)
        mask2d_vul = self.net_worth[i_indices] != 0
        self.relative_vulnerabilities[mask2d_vul] = ((
                self.matrix_relative_liabilities[j_indices[mask2d_vul], i_indices[mask2d_vul]] *
                (self.vector_outside_asset[j_indices[mask2d_vul]] - self.net_worth[j_indices[mask2d_vul]])) /
                                                     self.net_worth[i_indices[mask2d_vul]]
                )



        self.banks = np.array([
            Bank(outside_asset, doit, outside_liabilities, j_dois )
            for outside_asset,doit, outside_liabilities, j_dois in
            zip(self.vector_outside_asset, self.on_me_doit, self.vector_outside_liabilities, self.je_dois)],
            dtype=object
        )

        self.net_worth = np.array([bank.balance for bank in self.banks])


        mask0 = self.vector_outside_asset > 0
        x1 = self.net_worth[mask0] / self.vector_outside_asset[mask0]
        x2 = self.net_worth[~mask0]
        self.vulnerabilities = np.concatenate((x1, x2))

        self.compute_sum_outside_assets()


        # Structure of the financial network

        # this essentially the net worth, the more banks have a big level of capitalisation, the more resilient they will be
        # Is a proportion of the outside asset, like a total value of the system
        self.level_of_capitalisation = 0

        # Degree of connection is simply the likelyhood of having a link between two bank so prob of linking, esdos reyni binomial mean np
        self.degree_of_connection = (self.number_bank - 1) * self.probability_of_linking

        # The size of interbank exposure is essential for us, because it will quantify the systemic bank, it's essentially what the bank owe to the system internaly
        self.interbank_exposure = self.matrix_obligation

        # the degree of concentration of the system is the measure of heterogenity in terms
        # of distribution of the interbank exposure and the degree
        # connection; for now, I don't have a good formula to quantify it

        #=====================================================================================#

    @abstractmethod
    def generate(self):
        pass

    def get_vulnerabilities(self):
        return self.vulnerabilities

    def get_vulnerabilities_to_outside(self):
        return self.vulnerabilities_to_outside

    def get_relative_vulnerabilities(self):
        return self.relative_vulnerabilities

    def get_matrix_obligation(self):
        return self.matrix_obligation

    def get_net_worth(self):
        return self.net_worth

    def get_vector_outside_liabilities(self):
        return self.vector_outside_liabilities

    def get_vector_outside_assets(self):
        return self.vector_outside_asset

    def get_matrix_relative_liabilities(self):
        return self.matrix_relative_liabilities

    def get_due_payements(self):
        return self.due_payements

    def get_default_vector(self):
        return self.default_vector

    def get_banks(self):
        return self.banks

    def get_sum_outside_assets(self):
        return self.sum_outside_asset

    def set_sum_outside_assets(self, sum_outside_asset):
        self.sum_outside_asset = sum_outside_asset
        return

    def compute_sum_outside_assets(self):
        self.sum_outside_asset = np.sum(self.get_vector_outside_assets())
        return

    def set_vulnerabilities(self, vulnerabilities):
        self.vulnerabilities = np.copy(vulnerabilities)
        return

    def set_vulnerabilities_to_outside(self, vulnerabilities_to_outside):
        self.vulnerabilities_to_outside = np.copy(vulnerabilities_to_outside)
        return

    def set_relative_vulnerabilities(self, relative_vulnerabilities):
        self.relative_vulnerabilities = np.copy(relative_vulnerabilities)
        return

    def set_matrix_obligation(self, matrix_obligation):
        self.matrix_obligation = np.copy(matrix_obligation)
        return

    def set_matrix_relative_liabilities(self, matrix_relative_liabilities):
        self.matrix_relative_liabilities = np.copy(matrix_relative_liabilities)
        return

    def set_due_payements(self, due_payements):
        self.due_payements = np.copy(due_payements)
        return

    def set_default_vector(self, default_vector):
        self.default_vector =np.copy(default_vector)
        return

    def set_banks(self, banks):
        self.banks = np.copy(banks)
        return

    def set_vector_outside_assets(self, vector_outside_asset):
        self.vector_outside_asset = np.copy(vector_outside_asset)
        for k in range(len(vector_outside_asset)):
            self.banks[k].set_outside_asset(vector_outside_asset[k])
        return

    def set_vector_outside_liabilities(self, vector_outside_liabilities):
        self.vector_outside_liabilities = np.copy(vector_outside_liabilities)
        return

    def set_net_worth(self, net_worth):
        self.net_worth = net_worth.copy()



    def update_default(self):
        self.default_vector = np.array([bank.is_default_bank for bank in self.banks])















