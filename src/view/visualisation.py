from abc import ABC

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from observer import Observer
from model import Network

class Visualisation(Observer):
    """Visualise l'état du réseau financier"""

    def update(self, observable, event_type=None, **kwargs):
        pass

