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
        All these variable, are common to any kind of network that want to model a financial network.
        :param number_of_bank:
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


        self.generate()

        n = self.number_bank
        self.je_dois = np.sum(self.matrix_obligation, axis=1)
        self.on_me_doit = np.sum(self.matrix_obligation , axis=0)
        self.due_payements = self.matrix_obligation @ np.array([1]*self.number_bank) + self.vector_outside_liabilities
        for k in range(n):
            for j in range(n):
                if self.due_payements[k] == 0:
                    self.matrix_relative_liabilities[k][j] = 0
                else:
                    self.matrix_relative_liabilities[k][j] = self.matrix_obligation[k][j]/self.due_payements[k]

        for i in range(n):
            for j in range(n):
                if self.matrix_relative_liabilities[j][i] == 0 or self.net_worth[i] == 0:
                    self.relative_vulnerabilities[i][j] = 0
                else:
                    self.relative_vulnerabilities[i][j] = self.matrix_relative_liabilities[j][i]*(self.vector_outside_asset[j] - self.net_worth[j])/self.net_worth[i]

        for i in range(n):
            self.banks[i] = Bank(self.vector_outside_asset[i], self.on_me_doit[i], self.vector_outside_liabilities[i], self.je_dois[i])
            self.net_worth[i] = self.banks[i].balance

        #self.vulnerabilities = [self.net_worth[k] / self.vector_outside_asset[k] if self.vector_outside_asset[k] != 0 else self.net_worth[k] for k in range(n)]
        mask0 = self.vector_outside_asset > 0
        x1 = self.net_worth[mask0] / self.vector_outside_asset[mask0]
        x2 = self.net_worth[~mask0]
        self.vulnerabilities = np.concatenate((x1, x2))

        self.compute_sum_outside_assets()

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
        self.default_vector = [self.banks[i].is_default_bank for i in range(self.number_bank)]















