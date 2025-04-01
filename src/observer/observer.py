from abc import ABC, abstractmethod

class Observer(ABC):
    """Interface pour les objets qui observent des Observables"""

    @abstractmethod
    def update(self, observable, event_type=None, **kwargs):
        """
        Méthode appelée quand l'Observable change

        Args:
            observable: L'objet Observable qui a changé
            event_type: Type d'événement qui s'est produit
            **kwargs: Données supplémentaires sur l'événement
        """
        pass