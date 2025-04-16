from abc import ABC

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from controller import Simulation
from model import Network

class Visualisation():
    """Visualise l'état du réseau financier"""

    def __init__(self, simulation: Simulation):
        self.simulation = simulation


    def visualize_default_shock(self):
        pass




