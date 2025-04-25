import numpy as np
from model import Network, Bank


class ManualNetwork(Network):

    def __init__(self, matrix_obligation, vector_outside_asset, vector_outside_liabilities):
        super().__init__(len(vector_outside_asset), matrix_obligation=matrix_obligation, vector_outside_asset=vector_outside_asset,
                         vector_outside_liabilities=vector_outside_liabilities)



    def generate(self):
        return




