class Bank:
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


    def can_modify_balance(self, kind_of_balance: str, quantity: float ):
        """
        Avant d'emprunter, on vérifie qu'on est solvable
        :return:
        """
        if kind_of_balance == 'asset':
            if quantity <= 0:
                raise ValueError('Quantity must be positive')
            self.balance += quantity
            self.outside_asset += quantity
            return True
        elif kind_of_balance == 'liabilities':
            if quantity <= 0:
                raise ValueError('Quantity must be positive')
            m = self.balance - quantity
            if m < 0:
                return False
            self.balance -= quantity
            self.outside_liabilities += quantity
            return True

    def is_default(self):
        return self.balance <= 0

    def update_bank(self):

        return

    def show(self):
        print(f" Asset : {self.asset}\n Outside Asset : {self.outside_asset}\n Liabilities : {self.liabilities}\n Outside Liabilities : {self.outside_liabilities}\n Net worth : {self.balance}")


