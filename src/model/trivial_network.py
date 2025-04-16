from model import ManualNetwork, Network, Bank
import numpy as np

class TrivialNetwork(Network):

    def __init__(self, number_of_bank):
        super().__init__(number_of_bank)
        n = self.number_bank

        self.matrix_obligation = np.triu(100*np.ones((n,n)), k=1)
        size = n
        n_init = n-1
        values = np.array([1/(n_init-i) if n_init-i > 0 else 0 for i in range(size)])
        mask = np.triu(np.ones((size, size)), k=1).astype(bool)
        for i in range(size):
            row_mask = mask[i]
            self.matrix_relative_liabilities[i, row_mask] = values[i]
        b = self.matrix_obligation  @ np.array([1]*n)
        for i in range(n):
            self.vector_outside_asset[i] = b[i] - 2*b[i]
        self.vector_outside_liabilities = np.array([0]*n)


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
            self.net_worth[i] = self.banks[i].get_net_worth()
