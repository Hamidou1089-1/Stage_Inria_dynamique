# Définir ce qui est exposé avec 'from model import *'
__all__ = ['Bank', 'Network', 'Model', 'EisenbergNoeModel']

# Importation pour simplifier l'accès
from .bank import Bank
from .network import Network
from .RandomNetwork import RandomNetwork
from .model_interface import Model
from .eisenberg_noe import EisenbergNoeModel