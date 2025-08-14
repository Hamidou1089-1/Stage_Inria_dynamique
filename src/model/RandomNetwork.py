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
        Initializes an instance of the class with the given number of banks and
        probability of linking. Sets up the necessary attributes by invoking
        the parent class's constructor.

        :param number_bank: The number of banks to be initialized.
        :type number_bank: int
        :param probability_of_linking: The probability of linking between entities.
                                       Default is 0.1.
        :type probability_of_linking: float
        """
        super().__init__(number_bank, probability_of_linking=probability_of_linking)









    def generate(self):
        """
        Generates and initializes the financial network of obligations, liabilities, and assets for a set of banks
        based on the given number of banks and the probability of connections between them. This includes random
        generation of liabilities, assets, and inter-bank obligations using a gamma distribution. The method
        ensures proper balancing of obligations and liabilities in the system.



        :return: None
        """
        n = self.number_bank

        self.vector_outside_liabilities = np.array([0]*n)
        self.vector_outside_asset = np.array([0]*n)
        self.matrix_obligation = np.zeros((n, n))

        for i in range(n):
            if np.random.random() < self.probability_of_linking:
                self.vector_outside_liabilities[i] = stats.gamma.rvs(a=150)
            for j in range(n):
                if np.random.random() < self.probability_of_linking:
                    if i == j:
                        self.matrix_obligation[i][j] = 0
                        continue
                    self.matrix_obligation[i][j] = stats.gamma.rvs(a=150)


        je_dois = np.sum(self.matrix_obligation, axis=1)
        on_me_doit = np.sum(self.matrix_obligation , axis=0)

        for i in range(n):
            if on_me_doit[i] < je_dois[i] + self.vector_outside_liabilities[i]:
                self.vector_outside_asset[i] = je_dois[i] + self.vector_outside_liabilities[i] - on_me_doit[i] + 10
            else:
                self.vector_outside_asset[i] = 10








