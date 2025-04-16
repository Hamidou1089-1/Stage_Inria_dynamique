from model import Bank

import numpy as np
import networkx as nx

from model.network import Network


class RandomNetwork(Network):
    """
    This class generates a network of bank throughout their debt and assets.

    It can be random like erdos reyni.

    Enfaite cette classe : nous permet de generer le reseau de depart.

    Un choix que j'ai fait, mais qui va être embettant apres, je me débrouille pour que le net worth soit toujours positif, mais lorque, je vais instancier, il faut que j'interdise cette possibilité.
    Car pour le moment, c'est juste generer en random.
    """

    def __init__(self, number_bank: int, probability_of_linking=0.1):
        """
        Le réseau de depart.
        :param number_bank: How many banks should be generated ?
        :param at_random: Do you want to generate at random ?
        :param probability_of_linking: If you want to generate at random, what should the probability of linking ?
        """
        super().__init__(number_bank)
        self.probability_of_linking = probability_of_linking
        self.generate()







    def generate(self):
        """
        :return:
        """
        n = self.number_bank
        for i in range(n):
            if np.random.random() < self.probability_of_linking:
                #self.vector_outside_liabilities[i] = np.random.uniform(1,n**2)
                self.vector_outside_liabilities[i] = np.random.uniform(1, n**2)
            for j in range(n):
                if np.random.random() < self.probability_of_linking:
                    if i == j or self.matrix_obligation[j][i] > 0:
                        self.matrix_obligation[i][j] = 0
                        continue
                    elif np.random.random() < 0.5:
                        self.matrix_obligation[i][j] = np.random.uniform(1, n**2)
                    else:
                        self.matrix_obligation[j][i] = np.random.uniform(1, n**2)

        je_dois = self.matrix_obligation @ np.array([1]*n)
        on_me_doit =  np.array([1]*n).T @ self.matrix_obligation

        for i in range(n):
            if on_me_doit[i] < je_dois[i] + self.vector_outside_liabilities[i]:
                self.vector_outside_asset[i] = abs(je_dois[i] + self.vector_outside_liabilities[i] - on_me_doit[i]) + np.random.uniform(1, n**2)
            else:
                self.vector_outside_asset[i] = np.random.uniform(1, n**2)

        self.due_payements = self.matrix_obligation @ np.array([1]*self.number_bank) + self.vector_outside_liabilities

        for k in range(n):
            if self.due_payements[k] == 0:
                self.vulnerabilities[k] = 0
            else:
                self.vulnerabilities[k] = (self.due_payements[k] - self.vector_outside_liabilities[k])/self.due_payements[k]

        self.vulnerabilities = (self.vulnerabilities / np.sum(self.vulnerabilities)) if np.sum(self.vulnerabilities)!=0 else self.vulnerabilities


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
            self.banks[i] = Bank(self.vector_outside_asset[i], on_me_doit[i], self.vector_outside_liabilities[i], je_dois[i])
            self.net_worth[i] = self.banks[i].balance

        return





