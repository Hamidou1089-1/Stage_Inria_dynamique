import networkx as nx
import numpy as np
from model import Network, Bank, ManualNetwork

def create_core_periphery_network(n_core, n_periphery, p_core=0.7, p_periphery=0.2,
                                 weight_scale=100, baseline_asset=1000):
    n = n_core + n_periphery
    matrix_obligation = np.zeros((n, n))
    vector_outside_asset = np.array([0]*n)
    vector_outside_liabilities = np.array([0]*n)


    for k in range(n):
        for l in range(n):
            pass


