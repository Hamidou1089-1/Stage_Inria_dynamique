import numpy as np
from model.bank import Bank
from abc import ABC, abstractmethod


class Network(ABC):
    """
    Interface abstraite pour different type de reseau:
    - Random
    - Small World
    - Scale free
    """

    @abstractmethod
    def generate(self):
        pass














