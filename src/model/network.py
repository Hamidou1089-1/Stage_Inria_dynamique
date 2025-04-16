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

    def __init__(self, number_of_bank: int):

        """
        All these variable, are common to any kind of network that want to model a financial network.
        :param number_of_bank:
        """
        Observable.__init__(self)
        self.number_bank = number_of_bank
        """
        beta_i = (due_payement_i - outside_liabilities_i)/due_payement_i
        """
        self.vulnerabilities = np.array([0]*self.number_bank)

        self.relative_vulnerabilities = np.zeros((self.number_bank, self.number_bank))

        self.matrix_obligation = np.zeros((self.number_bank, self.number_bank))
        self.net_worth = np.array([0]*self.number_bank)
        self.vector_outside_asset = np.array([0]*self.number_bank)
        self.banks = np.empty(self.number_bank, dtype=object)
        self.vector_outside_liabilities = np.array([0] * self.number_bank)
        self.matrix_relative_liabilities = np.zeros((self.number_bank, self.number_bank))
        self.due_payements = np.array([0]*self.number_bank)
        self.default_vector = np.array([False]*self.number_bank)
        self.sum_outside_asset = 0


    @abstractmethod
    def generate(self):
        pass

    def get_vulnerabilities(self):
        return self.vulnerabilities

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
        self.default_vector = [self.banks[i].is_default() for i in range(self.number_bank)]
        #print("How is default vector ? ", self.default_vector)















