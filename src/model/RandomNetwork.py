from model import Bank

import numpy as np
import networkx as nx
import scipy.stats as stats


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
        super().__init__(number_bank, probability_of_linking=probability_of_linking)









    def generate(self):
        """
        :return:
        """
        n = self.number_bank

        self.vector_outside_liabilities = np.array([0]*n)
        self.vector_outside_asset = np.array([0]*n)
        self.matrix_obligation = np.zeros((n, n))

        for i in range(n):
            if np.random.random() < self.probability_of_linking:
                self.vector_outside_liabilities[i] = stats.gamma.rvs(a=1.99, scale=100)
            for j in range(n):
                if np.random.random() < self.probability_of_linking:
                    if i == j or self.matrix_obligation[j][i] > 0:
                        self.matrix_obligation[i][j] = 0
                        continue
                    elif np.random.random() < 0.5:
                        self.matrix_obligation[i][j] = stats.gamma.rvs(a=1.99, scale=100)
                    else:
                        self.matrix_obligation[j][i] = stats.gamma.rvs(a=1.99, scale=100)



        je_dois = np.sum(self.matrix_obligation, axis=1)
        on_me_doit = np.sum(self.matrix_obligation , axis=0)

        for i in range(n):
            if on_me_doit[i] < je_dois[i] + self.vector_outside_liabilities[i]:
                self.vector_outside_asset[i] = abs(je_dois[i] + self.vector_outside_liabilities[i] - on_me_doit[i]) + stats.gamma.rvs(a=1.99, scale=100)
            else:
                self.vector_outside_asset[i] = stats.gamma.rvs(a=1.99, scale=100)







