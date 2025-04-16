import numpy as np
from model import Network, Bank


class ManualNetwork(Network):

    def __init__(self, matrix_obligation, vector_outside_asset, asset, vector_outside_liabilities, liabilities, matrix_relative_liabilities ):
        super().__init__(len(vector_outside_asset))
        self.matrix_relative_liabilities = matrix_relative_liabilities
        self.vector_outside_asset = vector_outside_asset
        self.asset = asset
        self.vector_outside_liabilities = vector_outside_liabilities
        self.liabilities = liabilities
        self.matrix_obligation = matrix_obligation
        self.matrix_relative_liabilities = matrix_relative_liabilities
        self.generate()

    def generate(self):
        n = self.number_bank

        je_dois = self.matrix_obligation @ np.array([1]*n)
        on_me_doit =  np.array([1]*n).T @ self.matrix_obligation
        self.due_payements = self.matrix_obligation @ np.array([1]*self.number_bank) + self.vector_outside_liabilities

        for k in range(n):
            if self.due_payements[k] == 0:
                self.vulnerabilities[k] = 0
            else:
                self.vulnerabilities[k] = (self.due_payements[k] - self.vector_outside_liabilities[k])/self.due_payements[k]

        self.vulnerabilities = (self.vulnerabilities / np.sum(self.vulnerabilities)) if np.sum(self.vulnerabilities)!=0 else self.vulnerabilities

        for i in range(n):
            for j in range(n):
                if self.matrix_relative_liabilities[j][i] == 0 or self.net_worth[i] == 0:
                    self.relative_vulnerabilities[i][j] = 0
                else:
                    self.relative_vulnerabilities[i][j] = self.matrix_relative_liabilities[j][i]*(self.vector_outside_asset[j] - self.net_worth[j])/self.net_worth[i]

        for i in range(n):
            self.banks[i] = Bank(self.vector_outside_asset[i], on_me_doit[i], self.vector_outside_liabilities[i], je_dois[i])
            self.net_worth[i] = self.banks[i].balance


