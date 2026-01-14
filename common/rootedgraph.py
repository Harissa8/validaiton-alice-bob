from abc import ABC, abstractmethod

# Classe abstraite définissant l'interface d'un graphe enraciné
class RootedGraph(ABC):

    # Méthode abstraite qui doit retourner la liste des sommets racines du graphe
    @abstractmethod
    def roots(self):
        pass

    # Méthode abstraite qui doit retourner les voisins d'un sommet donné
    @abstractmethod
    def neighbors(self, vertex):
        pass
