
from abc import ABC, abstractmethod

# Classe abstraite définissant l'interface d'une sémantique de langage
class LanguageSemantics(ABC):

    # Méthode abstraite qui doit retourner la liste des états initiaux
    @abstractmethod
    def initials(self):
        pass

    # Méthode abstraite qui doit retourner les actions possibles à partir d'un état donné
    @abstractmethod
    def actions(self, state):
        pass

    # Méthode abstraite qui doit exécuter une action sur un état donné
    @abstractmethod
    def execute(self, state, action):
        pass
