from languagesemantics import LanguageSemantics
from copy import deepcopy


# Classe Piece pour representer une regle de transformation
# Une piece contient un nom, une garde (condition) et un effet (transformation)
class Piece:
    def __init__(self, name, effect, guard):
        """
        Constructeur d'une piece.

        Args:
            name: nom de la regle
            effect: fonction lambda qui transforme l'etat (lambda state -> new_state)
            guard: fonction lambda qui teste si la regle est applicable (lambda state -> bool)
        """
        self.name = name
        self.guard = guard
        self.effect = effect

    def __repr__(self):
        return f"Piece({self.name})"


# Classe Soup pour representer un programme
# Contient une liste de pieces et un etat initial
class Soup:
    def __init__(self, pieces, init):
        """
        Constructeur d'un programme Soup.

        Args:
            pieces: liste des pieces (regles)
            init: etat initial du programme
        """
        self.pieces = pieces
        self.init = init

    def __repr__(self):
        return f"Soup(pieces={[p.name for p in self.pieces]}, init={self.init})"


# Implementation de la semantique du langage Soup
# Un etat peut etre n'importe quelle valeur Python (int, list, dict, etc.)
# Une action est une Piece dont la garde est satisfaite
class SoupLanguageSemantics(LanguageSemantics):

    # Constructeur : initialise la semantique avec un programme Soup
    def __init__(self, soup):
        self.soup = soup

    # Retourne les etats initiaux : l'etat initial du programme
    def initials(self):
        return [self.soup.init]

    # Retourne toutes les pieces dont la garde est satisfaite pour l'etat donne
    def actions(self, state):
        enabled_pieces = []

        # Pour chaque piece du programme
        for piece in self.soup.pieces:
            # Verifie si la garde est satisfaite
            if piece.guard(state):
                enabled_pieces.append(piece)

        return enabled_pieces

    # Execute une piece (action) sur un etat et retourne le nouvel etat
    def execute(self, state, action):
        # L'action est une Piece
        # On applique l'effet de la piece a l'etat
        new_state = action.effect(state)

        # Retourne une liste contenant le nouvel etat
        return [new_state]
