import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from observer import Observer
from model import Network

class Visualisation(Observer):
    """Visualise l'état du réseau financier"""

    def __init__(self):
        # État actuel du réseau pour la visualisation
        self.current_state = {
            "default_vector": None,
            "net_worth": None,
            "matrix_obligation": None
        }

        # Historique pour suivre l'évolution du réseau
        self.history = {
            "default_count": [],
            "total_net_worth": [],
            "event_types": []
        }

    def update(self, observable, event_type=None, **kwargs):
        """Implémentation de la méthode update de l'interface Observer"""
        # Mettre à jour l'état actuel
        self.current_state["default_vector"] = observable.get_default_vector()
        self.current_state["net_worth"] = observable.get_net_worth()
        self.current_state["matrix_obligation"] = observable.get_matrix_obligation()

        # Mettre à jour l'historique
        self.history["default_count"].append(sum(observable.get_default_vector()))
        self.history["total_net_worth"].append(sum(observable.get_net_worth()))
        self.history["event_types"].append(event_type)

        # Mettre à jour la visualisation en fonction du type d'événement
        if event_type == "default_change":
            self._visualize_defaults()
        elif event_type == "net_worth_change":
            self._visualize_net_worth()

    def _visualize_defaults(self):
        """Visualise les banques en défaut"""
        # Exemple de visualisation (à implémenter avec matplotlib)
        pass

    def _visualize_net_worth(self):
        """Visualise l'évolution de la valeur nette"""
        # Exemple de visualisation (à implémenter avec matplotlib)
        pass

    def plot_history(self):
        """Affiche l'historique des simulations"""
        # Créer un graphique avec les données historiques
        plt.figure(figsize=(10, 6))

        # Tracer le nombre de défauts
        plt.subplot(2, 1, 1)
        plt.plot(self.history["default_count"], 'r-', label='Nombre de défauts')
        plt.ylabel('Nombre de banques en défaut')
        plt.legend()

        # Tracer la valeur nette totale
        plt.subplot(2, 1, 2)
        plt.plot(self.history["total_net_worth"], 'b-', label='Valeur nette totale')
        plt.ylabel('Valeur nette totale')
        plt.xlabel('Étapes de simulation')
        plt.legend()

        plt.tight_layout()
        plt.show()