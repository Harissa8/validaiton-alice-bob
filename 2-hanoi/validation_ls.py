# Validation utilisant l'approche Language Semantics
# Ce fichier démontre comment utiliser LS2RG pour transformer une sémantique
# de langage en graphe enraciné, puis appliquer BFS dessus

import sys
from pathlib import Path
# Add common and 1-bfs directories to import shared classes
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))
sys.path.insert(0, str(Path(__file__).parent.parent / "1-bfs"))

from hanoilanguagesemantics import HanoiLanguageSemantics
from ls2rg import LS2RG
from bfs import BFS
from collections import deque


# Fonction BFS adaptée pour les graphes enracinés (RootedGraph)
def breadth_first_search_rg(rooted_graph, on_entry, opaque):
    """
    BFS pour les graphes enracinés.

    Args:
        rooted_graph: Un graphe enraciné (implémente roots() et neighbors())
        on_entry: Callback appelé pour chaque état visité.
                  Retourne True pour arrêter le parcours.
        opaque: Données passées au callback

    Returns:
        Tuple (opaque, visited_states)
    """
    visited = set()
    queue = deque()

    # Ajouter toutes les racines à la queue
    for root in rooted_graph.roots():
        if root not in visited:
            visited.add(root)
            queue.append(root)
            if on_entry(root, opaque):
                return opaque, visited

    # Parcours BFS
    while queue:
        current = queue.popleft()

        # Explorer les voisins
        for neighbor in rooted_graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                if on_entry(neighbor, opaque):
                    return opaque, visited
                queue.append(neighbor)

    return opaque, visited


# Fonction pour résoudre Hanoi avec l'approche Language Semantics
def hanoi_solver_ls(n):
    # Étape 1: Créer la sémantique du langage pour Hanoi
    ls = HanoiLanguageSemantics(n)

    # Étape 2: Transformer la sémantique en graphe enraciné
    rg = LS2RG(ls)

    # Étape 3: Définir le callback pour trouver la solution
    def on_entry(state, opaque):
        # Si on trouve une solution, on l'ajoute à opaque
        if ls.is_solution(state):
            opaque.append(state)
        # Arrête le parcours dès qu'une solution est trouvée
        return ls.is_solution(state)

    # Étape 4: Lancer BFS sur le graphe enraciné
    return breadth_first_search_rg(rg, on_entry, [])


# Test avec 3 disques
if __name__ == "__main__":
    print("=== Resolution de Hanoi avec Language Semantics ===")
    opaque, visited_states = hanoi_solver_ls(3)

    print(f"Nombre d'etats explores : {len(visited_states)}")
    print(f"Solution trouvee : {opaque}")

    # Demonstration des concepts de Language Semantics
    print("\n=== Demonstration des methodes Language Semantics ===")
    ls = HanoiLanguageSemantics(3)

    # Afficher l'etat initial
    initial_state = ls.initials()[0]
    print(f"Etat initial : {initial_state}")

    # Afficher les actions possibles
    actions = ls.actions(initial_state)
    print(f"\nActions possibles depuis l'etat initial : {actions}")

    # Executer la premiere action
    if actions:
        first_action = actions[0]
        print(f"\nExecution de l'action {first_action} (deplacer de tige {first_action[0]} vers tige {first_action[1]})")
        next_states = ls.execute(initial_state, first_action)
        print(f"Etat resultant : {next_states[0]}")

        # Afficher les actions possibles depuis ce nouvel etat
        next_actions = ls.actions(next_states[0])
        print(f"Actions possibles depuis le nouvel etat : {next_actions}")
