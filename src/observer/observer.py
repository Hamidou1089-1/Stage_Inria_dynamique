from abc import ABC, abstractmethod




class Observable(ABC):
    """Interface pour les objets qui peuvent être observés"""

    def __init__(self):
        """Initialise la liste des observateurs"""
        self._observers = []

    def add_observer(self, observer):
        """Ajoute un observateur à la liste"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """Retire un observateur de la liste"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type=None, **kwargs):
        """Notifie tous les observateurs d'un changement"""
        for observer in self._observers:
            observer.update(self, event_type, **kwargs)



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








