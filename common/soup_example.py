from souplanguagesemantics import Piece, Soup, SoupLanguageSemantics
from bfs import breadth_first_search
from ls2rg import LS2RG


# ============================================================================
# Exemple 1: Horloge binaire (Clock)
# ============================================================================
# Etat: un entier (0 ou 1)
# Regles: to1 (passe a 1 si 0), to0 (passe a 0 si 1)

# Definition des pieces
to1 = Piece("to1", lambda c: 1, lambda c: c == 0)
to0 = Piece("to0", lambda c: 0, lambda c: c == 1)

# Programme Soup pour l'horloge
clk1 = Soup([to1, to0], 0)

# Creation de la semantique
clk_semantics = SoupLanguageSemantics(clk1)

# Test de l'horloge
print("=== Exemple 1: Horloge binaire ===")
print(f"Etat initial: {clk_semantics.initials()}")

# Depuis l'etat 0
state0 = 0
print(f"\nEtat courant: {state0}")
actions0 = clk_semantics.actions(state0)
print(f"Actions possibles: {actions0}")
if actions0:
    new_states = clk_semantics.execute(state0, actions0[0])
    print(f"Apres execution de {actions0[0].name}: {new_states}")

# Depuis l'etat 1
state1 = 1
print(f"\nEtat courant: {state1}")
actions1 = clk_semantics.actions(state1)
print(f"Actions possibles: {actions1}")
if actions1:
    new_states = clk_semantics.execute(state1, actions1[0])
    print(f"Apres execution de {actions1[0].name}: {new_states}")


# ============================================================================
# Exemple 2: Compteur (0 -> 1 -> 2 -> 0)
# ============================================================================

inc0 = Piece("inc0", lambda c: 1, lambda c: c == 0)
inc1 = Piece("inc1", lambda c: 2, lambda c: c == 1)
reset = Piece("reset", lambda c: 0, lambda c: c == 2)

counter = Soup([inc0, inc1, reset], 0)
counter_semantics = SoupLanguageSemantics(counter)

print("\n\n=== Exemple 2: Compteur cyclique ===")
current = 0
for i in range(6):
    print(f"\nEtat {i}: {current}")
    actions = counter_semantics.actions(current)
    print(f"Actions possibles: {actions}")
    if actions:
        new_states = counter_semantics.execute(current, actions[0])
        current = new_states[0]


# ============================================================================
# Exemple 3: Utilisation avec BFS
# ============================================================================

# Objectif: trouver le chemin de 0 a 2 dans le compteur
print("\n\n=== Exemple 3: BFS sur le compteur ===")

# Convertir la semantique en graphe enracine
counter_graph = LS2RG(counter_semantics)

# Fonction callback appelee lors de la visite de chaque etat
def on_entry(state, opaque):
    # Si on atteint l'etat 2, on le stocke dans opaque et on arrete
    if state == 2:
        opaque.append(state)
        return True  # Arrete le parcours
    return False  # Continue le parcours

# Utilisation de BFS
opaque, visited = breadth_first_search(counter_graph, on_entry, [])

if opaque:
    print(f"Etat cible trouve: {opaque[0]}")
    print(f"Nombre d'etats explores: {len(visited)}")
    print(f"Etats visites: {sorted(visited)}")
else:
    print("Aucun etat cible trouve")


# ============================================================================
# Exemple 4: Programme plus complexe avec etats composites
# ============================================================================

# Etat: dictionnaire avec deux variables
# Exemple: {"x": 0, "y": 0}

inc_x = Piece("inc_x",
              lambda s: {"x": s["x"] + 1, "y": s["y"]},
              lambda s: s["x"] < 3)

inc_y = Piece("inc_y",
              lambda s: {"x": s["x"], "y": s["y"] + 1},
              lambda s: s["y"] < 3)

dec_x = Piece("dec_x",
              lambda s: {"x": s["x"] - 1, "y": s["y"]},
              lambda s: s["x"] > 0)

dec_y = Piece("dec_y",
              lambda s: {"x": s["x"], "y": s["y"] - 1},
              lambda s: s["y"] > 0)

# Programme avec etat initial
grid_program = Soup([inc_x, inc_y, dec_x, dec_y], {"x": 0, "y": 0})
grid_semantics = SoupLanguageSemantics(grid_program)

print("\n\n=== Exemple 4: Grille 2D ===")
state = {"x": 0, "y": 0}
print(f"Etat initial: {state}")
actions = grid_semantics.actions(state)
print(f"Actions possibles: {[a.name for a in actions]}")

# Executer quelques actions
state = {"x": 1, "y": 1}
print(f"\nEtat: {state}")
actions = grid_semantics.actions(state)
print(f"Actions possibles: {[a.name for a in actions]}")
