# Définir ce qui est exposé avec 'from model import *'
__all__ = ['Bank', 'Network', 'Model', 'EisenbergNoeModel', 'RandomNetwork', 'ManualNetwork', 'TrivialNetwork']

# Importation pour simplifier l'accès
from .bank import Bank
from .network import Network
from .RandomNetwork import RandomNetwork
from .model_interface import Model
from .eisenberg_noe import EisenbergNoeModel
from .manual_network import ManualNetwork
from .trivial_network import TrivialNetwork