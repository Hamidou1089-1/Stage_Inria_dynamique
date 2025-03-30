import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import pandas as pd
from model import Model
from model import EisenbergNoeModel
from model import Network


class Simulation:
    """
    Etant dans une architecture MVC, je dois maintenant rassembler les classes, et les instanciers afin de faire tourner les simulations.

    Objectif :

      - Simuler pour visualiser l'évolution de la gravité d'un shock, par rapport à la proportion de default. (à quel point cela grandit vite etc, convexe, pas convexe).
      - Ensuite tester la robustesse du réseau en fonction de l'interconnexion et la gravité du shock.

    Je sais que j'ai plusieurs problèmes potentiels,
    car je pose comme mesure de la gravité du shock :
    ||x|| = Somme(|x|)/Somme(c).
    La robustesse du réseau se mesurera à la relative sensibilité d'un nœud au reste des nœuds du réseau (ça sera la norme 1 du vecteur des beta i vecteur).
    Ça sera à travers le beta (qui permet de savoir à quel point un nœud i participe au risque systemic).
    """

    def __init__(self, model: str, network: Network, shock_vector: np.ndarray):
        """
        So here we just consider that we have a network, (it can any kind of network).
        :param model: For now just Eisenberg and Noe
        :param network: Just a random network, but more soon
        """
        if model == "Eisenberg":
            self.model = EisenbergNoeModel(network)
        elif model == "Small World":
            raise NotImplementedError
        else:
            raise NotImplementedError
        self.shock_vector = shock_vector

    def simulate(self):
        """
        So here we are
        :return:
        """
        # So let's apply a shock I guess
        self.model.apply_shock(self.shock_vector)

        return

    def update(self):
        pass












