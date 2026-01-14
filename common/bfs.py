from collections import deque


# Fonction BFS pour les graphes enracines (RootedGraph)
def breadth_first_search(rooted_graph, on_entry, opaque):
    """
    BFS pour les graphes enracines.

    Args:
        rooted_graph: Un graphe enracine (implemente roots() et neighbors())
        on_entry: Callback appele pour chaque etat visite.
                  Retourne True pour arreter le parcours.
        opaque: Donnees passees au callback

    Returns:
        Tuple (opaque, visited_states)
    """
    visited = set()
    queue = deque()

    # Ajouter toutes les racines a la queue
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
