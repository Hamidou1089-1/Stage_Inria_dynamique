
from observer import Observer

class Bank(Observer):
    """
    La structure de donnée bank permet simplement de decrire une banque avec son bilan simplifié.

    Dans le futur, on pourra peut être complexifié avec des formes d'obligation.
    """
    def __init__(self, outside_asset, asset, outside_liabilities, liabilities):
        """
        Represents a financial entity with the ability to determine whether it is in
        default based on its assets and liabilities.

        This class initializes with external assets, internal assets, external
        liabilities, and internal liabilities, calculating the financial balance, and
        determining the default status. If the calculated balance is negative, the
        entity is marked as a default entity.

        :param outside_asset: External assets of the financial entity.
        :type outside_asset: float
        :param asset: Internal assets of the financial entity.
        :type asset: float
        :param outside_liabilities: External liabilities of the financial entity.
        :type outside_liabilities: float
        :param liabilities: Internal liabilities of the financial entity.
        :type liabilities: float

        :attribute outside_asset: External assets of the financial entity.
        :attribute asset: Internal assets of the financial entity.
        :attribute outside_liabilities: External liabilities of the financial entity.
        :attribute liabilities: Internal liabilities of the financial entity.
        :attribute is_default_bank: A boolean indicating if the financial entity is in
            default (`True`) or not (`False`).
        :attribute balance: The net financial balance of the entity after subtracting
            liabilities and adding assets. Calculated during initialization.
        """
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
        Recalculates the bank's financial state after changes in the simulation.

        This method:
        1. Calculates the current balance (net worth) as:
           total assets (internal + external) minus total liabilities (internal + external)
        2. Updates the default status of the bank based on the new balance

        This allows banks to dynamically respond to economic shocks in the simulation.

        """
        self.balance = self.asset + self.outside_asset - (self.outside_liabilities + self.liabilities)
        self.is_default_bank = self.is_default()
        return



    def is_default(self):
        return self.balance <= 1e-5


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





