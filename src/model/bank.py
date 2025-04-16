
from observer import Observer

class Bank(Observer):
    """
    La structure de donnée bank permet simplement de decrire une banque avec son bilan simplifié.

    Dans le futur, on pourra peut être complexifié avec des formes d'obligation.
    """
    def __init__(self, outside_asset, asset, outside_liabilities, liabilities):
        self.outside_asset = outside_asset
        self.asset = asset
        self.outside_liabilities = outside_liabilities
        self.liabilities = liabilities
        self.is_default_bank = False
        t = outside_asset + asset - liabilities - outside_liabilities
        if t < 0:
            self.is_default_bank = True
            self.balance = t
        else:
            self.balance = t


    def update_balance(self):
        """
        Permet à la banque de se mettre à jour, en cas de shock dans la simulation.
        Économiquement, cela permet de rendre les banques dynamiques (ils peuvent modifier leur bilan)
        :return: None
        """
        self.balance = self.asset + self.outside_asset - (self.outside_liabilities + self.liabilities)
        self.is_default_bank = self.is_default()
        return



    def is_default(self):
        return self.balance <= 0


    def show(self):
        print(f" Asset : {self.asset}\n Outside Asset : {self.outside_asset}\n Liabilities : {self.liabilities}\n Outside Liabilities : {self.outside_liabilities}\n Net worth : {self.balance}")

    def get_outside_liabilities(self):
        return self.outside_liabilities
    def get_liabilities(self):
        return self.liabilities

    def get_net_worth(self):
        return self.balance

    def get_outside_assets(self):
        return self.outside_asset
    def get_assets(self):
        return self.asset

    def get_state_balance(self):
        """
        Boolean, True if in default bank, False otherwise
        :return:
        """
        return self.is_default()

    def set_net_worth(self, state_balance):
        self.balance = state_balance
        return

    def set_outside_liabilities(self, outside_liabilities):
        self.outside_liabilities = outside_liabilities
        return

    def set_liabilities(self, liabilities):
        self.liabilities = liabilities
        return

    def set_outside_asset(self, outside_asset):
        self.outside_asset = outside_asset
        return

    def set_assets(self, assets):
        self.asset = assets
        return

    def update(self, observable, event_type=None, **kwargs):
        """
        Réagit aux changements du réseau

        Args:
            observable: L'objet Network qui a changé
            event_type: Type d'événement
            **kwargs: Données supplémentaires
        """
        if event_type == "net_worth_change":
            # La banque pourrait réagir au changement de valeur nette du réseau
            pass

        elif event_type == "default_change":
            # La banque pourrait réagir aux changements de statut de défaut
            # Par exemple, ajuster sa stratégie de risque
            pass

        elif event_type == "payment_cleared":
            # La banque pourrait réagir aux paiements effectués
            payment_vector = kwargs.get("payment_vector", None)
            if payment_vector is not None:
                # Ajuster le bilan en fonction des paiements
                pass





