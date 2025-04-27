import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import pandas as pd
from model import Model, ShockDistribution
from model import EisenbergNoeModel
from model import Network


class Simulation:
    """
    Étant dans une architecture MVC, je dois maintenant rassembler les classes, et les instanciers afin de faire tourner les simulations.

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
        Simulates the effects of applying a shock to the financial network model and computes systemic impact.
        The function first applies a given shock to the model, computes clearing payments if defaults occur,
        updates bank balances, and gathers systemic impact measures such as vulnerabilities and default counts.

        :raises ValueError: If the model or shock vector is improperly configured.
        :param self: The current instance of the simulation containing the financial model and network details.
        :type self: Simulation
        :return: A tuple containing:
            - vector_payments (ndarray): The computed clearing payment vectors.
            - shock_measure (float): The systemic shock measure after simulation.
            - default_count (int): The number of defaulted banks.
            - vulnerabilities (ndarray): The vulnerabilities of the network after the shock.
        :rtype: Tuple[ndarray, float, int, ndarray]
        """

        self.model.apply_shock(self.shock_vector)
        vector_payments = np.zeros((len(self.shock_vector),1))

        if np.any(self.model.network.default_vector == True):
            vector_payments = self.model.compute_clearing_payments(len(self.shock_vector)*1000 ,self.shock_vector)
            self.model.network.set_matrix_obligation(self.model.network.matrix_relative_liabilities * vector_payments[:, np.newaxis])

        self.model.network.set_due_payements(np.sum(self.model.network.matrix_obligation, axis=1))

        temp_networth = np.array([0]*self.model.network.number_bank)
        for k in range(len(self.shock_vector)):
            self.model.network.banks[k].set_outside_asset(self.model.network.get_vector_outside_assets()[k])
            self.model.network.banks[k].set_liabilities(self.model.network.get_due_payements()[k])
            self.model.network.banks[k].set_assets(np.sum(self.model.network.get_matrix_obligation(), axis=0)[k])
            self.model.network.banks[k].update_balance()
            temp_networth[k] = self.model.network.banks[k].get_net_worth()

        self.update()

        self.model.network.set_net_worth(temp_networth)

        shock_measure, default_count = self.model.measure_systemic_impact(self.shock_vector)
        return vector_payments, shock_measure, default_count, self.model.network.get_vulnerabilities()


    def update(self):
        """
        Updates the default configuration of the network model.

        This method is used to invoke the update process on the default settings
        of the network model. It ensures that the most recent changes or updates
        are applied to the network.

        :return: None
        """
        self.model.network.update_default()
        return





    def run_scenarios(self, shock_distribution: ShockDistribution, n_scenarios=20, restore_network=True):
        """Exécute plusieurs scénarios de chocs basés sur une distribution

        Args:
            shock_distribution: Objet de distribution de chocs qui génère des vecteurs de choc
            n_scenarios: Nombre de scénarios à exécuter
            restore_network: Si True, restaure l'état du réseau après chaque simulation

        Returns:
            dict: Résultats des simulations avec statistiques
        """
        results = {
            'shock_measures': [],
            'default_counts': [],
            'vulnerabilities': []
        }

        # Sauvegarder l'état initial
        if restore_network:
            original_assets = np.copy(self.model.network.get_vector_outside_assets())

        for _ in range(n_scenarios):
            # Générer un nouveau vecteur de choc
            self.shock_vector = shock_distribution.generate_shock()

            # Exécuter la simulation
            _, shock_measure, default_count, vulnerabilities = self.simulate()

            # Stocker les résultats
            results['shock_measures'].append(shock_measure)
            results['default_counts'].append(default_count)
            results['vulnerabilities'].append(vulnerabilities)

            # Restaurer l'état du réseau
            if restore_network:
                self.model.network.set_vector_outside_assets(np.copy(original_assets))
                # Réinitialiser les autres états si nécessaire
                self.model.network.update_default()

        # Calculer des statistiques agrégées
        results['avg_shock_measure'] = np.mean(results['shock_measures'])
        results['avg_default_count'] = np.mean(results['default_counts'])
        results['max_default_count'] = np.max(results['default_counts'])
        results['std_default_count'] = np.std(results['default_counts'])

        return results

    def run_intensity_analysis(self, shock_distribution_class, intensity_range=(0.1, 1.0, 0.1),
                               n_scenarios_per_intensity=10, **dist_params):
        """Analyse l'impact de l'intensité des chocs sur le réseau

        Args:
            shock_distribution_class: Classe de distribution de chocs (pas une instance)
            intensity_range: Tuple (min, max, step) pour les niveaux d'intensité
            n_scenarios_per_intensity: Nombre de scénarios par niveau d'intensité
            **dist_params: Paramètres additionnels pour l'initialisation de la distribution

        Returns:
            dict: Résultats de l'analyse par intensité
        """
        intensity_analysis = {
            'intensities': [],
            'avg_default_counts': [],
            'shock_measures': []
        }

        # Sauvegarder l'état initial du réseau
        original_assets = np.copy(self.model.network.get_vector_outside_assets())

        # Pour chaque niveau d'intensité
        for intensity in np.arange(intensity_range[0], intensity_range[1] + 1e-10, intensity_range[2]):
            # Créer une instance de la distribution avec cette intensité
            shock_dist = shock_distribution_class(self.model.network, intensity=intensity, **dist_params)

            # Exécuter les scénarios pour cette intensité
            results = self.run_scenarios(shock_dist, n_scenarios=n_scenarios_per_intensity)

            # Stocker les résultats pour cette intensité
            intensity_analysis['intensities'].append(intensity)
            intensity_analysis['avg_default_counts'].append(results['avg_default_count'])
            intensity_analysis['shock_measures'].append(results['avg_shock_measure'])

            # Restaurer l'état du réseau pour la prochaine intensité
            self.model.network.set_vector_outside_assets(np.copy(original_assets))
            self.model.network.update_default()

        return intensity_analysis







