from bank import Bank
import numpy as np

from model.network import Network


class RandomNetwork(Network):
    """
    This class generates a network of bank throughout their debt and assets.

    It can be random like erdos reyni.

    Enfaite cette classe : nous permet de generer le reseau de depart.

    Un choix que j'ai fais mais qui va etre embettant apres, je me débrouille pour que le net worth soit toujours positif, mais lorque je vais instancier, faut que j'interdise cette possibilité.
    Car pour le moment c'est juste generer en random.
    """

    def __init__(self, number_bank: int, probability_of_linking=0.1):
        """
        Le reseau de depart.
        :param number_bank: How many banks should be generated ?
        :param at_random: Do you want to generate at random ?
        :param probability_of_linking: If you want to generate at random, what should the probability of linking ?
        """
        self.number_bank = number_bank
        self.probability_of_linking = probability_of_linking
        self.generate()
        self.due_payements = self.matrix_obligation @ np.array([1]*self.number_bank) + self.vector_outside_liabilities
        self.matrix_relative_liabilities = np.zeros((self.number_bank, self.number_bank))
        for k in range(number_bank):
            for j in range(number_bank):
                if self.due_payements[k] == 0:
                    self.matrix_relative_liabilities[k][j] = 0
                else:
                    self.matrix_relative_liabilities[k][j] = self.matrix_obligation[k][j]/self.due_payements[k]

        self.default_vector = [self.banks[i].is_default() for i in range(self.number_bank)]



    def generate(self):
        """
        :return:
        """
        n = self.number_bank
        for i in range(n):
            if np.random.random() < self.probability_of_linking:
                self.vector_outside_liabilities[i] = np.random.uniform(1,n**2)
            for j in range(n):
                if np.random.random() < self.probability_of_linking:
                    if i == j:
                        self.matrix_obligation[i][j] = 0
                        continue
                    self.matrix_obligation[i][j] = np.random.binomial(n*100, 0.2)

        je_dois = self.matrix_obligation @ np.array([1]*n)
        on_me_doit =  np.array([1]*n).T @ self.matrix_obligation

        for i in range(n):
            if on_me_doit[i] < je_dois[i] + self.vector_outside_liabilities[i]:
                self.vector_outside_asset[i] = abs(je_dois[i] + self.vector_outside_liabilities[i] - on_me_doit[i]) + np.random.uniform(1, n**2)
            else:
                self.vector_outside_asset[i] = np.random.uniform(1, n**3)


        for i in range(n):
            self.banks[i] = Bank(self.vector_outside_asset[i], on_me_doit[i], self.vector_outside_liabilities[i], je_dois[i])
            self.net_worth[i] = self.banks[i].balance
