import numpy as np
from model import Network, Bank


class ManualNetwork(Network):

    def __init__(self, matrix_obligation, vector_outside_asset, vector_outside_liabilities):
        """
        Initializes an instance of a class that performs financial computations pertaining
        to obligations, assets, and liabilities. This constructor method sets up the
        necessary data structures and inherits from the superclass.

        :param matrix_obligation: The obligation matrix that represents financial liabilities
            or dependencies among entities.
        :type matrix_obligation: Any
        :param vector_outside_asset: The vector representing assets held outside of the
            examining entity or system.
        :param vector_outside_liabilities: The vector representing liabilities held outside
            of the examining entity or system.
        """
        super().__init__(len(vector_outside_asset), matrix_obligation=matrix_obligation, vector_outside_asset=vector_outside_asset,
                         vector_outside_liabilities=vector_outside_liabilities)



    def generate(self):
        return




