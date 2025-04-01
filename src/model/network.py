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

    def set_vulnerabilities(self, vulnerabilities):
        self.vulnerabilities = vulnerabilities
        return
    def set_relative_vulnerabilities(self, relative_vulnerabilities):
        self.relative_vulnerabilities = relative_vulnerabilities
        return
    def set_matrix_obligation(self, matrix_obligation):
        self.matrix_obligation = matrix_obligation
        return
    def set_matrix_relative_liabilities(self, matrix_relative_liabilities):
        self.matrix_relative_liabilities = matrix_relative_liabilities
        return
    def set_due_payements(self, due_payements):
        self.due_payements = due_payements
        return
    def set_default_vector(self, default_vector):
        self.default_vector = default_vector
        return

    def set_banks(self, banks):
        self.banks = banks
        return

    def set_vector_outside_assets(self, vector_outside_asset):
        self.vector_outside_asset = vector_outside_asset
        return
    def set_vector_outside_liabilities(self, vector_outside_liabilities):
        self.vector_outside_liabilities = vector_outside_liabilities
        return
    def set_net_worth(self, net_worth):
        old_net_worth = self.net_worth.copy()
        self.net_worth = net_worth

        # Notifier les observateurs si la valeur nette a changé
        if not np.array_equal(old_net_worth, net_worth):
            self.notify_observers(event_type="net_worth_change",
                                  old_net_worth=old_net_worth,
                                  new_net_worth=net_worth)
        return

    def update_default(self):
        old_default = self.default_vector.copy()
        self.default_vector = [self.banks[i].is_default() for i in range(self.number_bank)]

        # Notifier les observateurs si le statut de défaut a changé
        if not np.array_equal(old_default, self.default_vector):
            self.notify_observers(event_type="default_change",
                                  old_default=old_default,
                                  new_default=self.default_vector)
        return













