import numpy as np
from model.bank import Bank
from abc import ABC, abstractmethod


class Network(ABC):
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
        self.default_vector = np.array([0]*self.number_bank)


    @abstractmethod
    def generate(self):
        pass














