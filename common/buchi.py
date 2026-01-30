"""
Buchi verification using the existing BFS + LS2RG infrastructure.

Architecture (matches whiteboard):
  Soup Sem (system) + iSoup Sem (property)
      -> StepSyncComposition
      -> LS2RG
      -> BFS (existing breadth_first_search)
      -> detect accepting cycle -> OK or counter-example

Cycle detection: after BFS explores the full composed state space,
we search for accepting cycles using DFS on the visited states.
Counter-example = (prefix_trace, cyclic_suffix_trace).
"""

from ls2rg import LS2RG
from bfs import breadth_first_search
from step_sync_composition import StepSyncComposition
from collections import deque


def verify_buchi(system_ls, property_ls):
    """
    Verify that a system satisfies a Buchi property.

    Uses the architecture:
      StepSyncComposition -> LS2RG -> BFS -> cycle detection

    Args:
        system_ls: LanguageSemantics (Soup model, e.g. AB1-AB5)
        property_ls: ISoupSemantics (iSoup property, e.g. P1-P5)

    Returns:
        (satisfied, counter_example)
        - satisfied: True if no accepting cycle found
        - counter_example: None or (prefix, cycle)
    """
    # Step 1: Compose system x property
    composed = StepSyncComposition(system_ls, property_ls)

    # Step 2: Convert to RootedGraph
    rg = LS2RG(composed)

    # Step 3: BFS to explore full state space and build parent map
    parent_map = {}
    all_states = []

    def on_entry(state, opaque):
        all_states.append(state)
        return False  # Explore everything

    _, visited = breadth_first_search(rg, on_entry, None)

    # Build adjacency + parent map from composed LS (for path reconstruction)
    adjacency = {}
    parent_map = {}
    bfs_queue = deque()

    for init in composed.initials():
        if init in visited:
            parent_map[init] = None
            bfs_queue.append(init)

    visited_bfs = set()
    while bfs_queue:
        current = bfs_queue.popleft()
        if current in visited_bfs:
            continue
        visited_bfs.add(current)

        actions = composed.actions(current)
        neighbors = []
        for action in actions:
            next_states = composed.execute(current, action)
            neighbors.extend(next_states)
        adjacency[current] = neighbors

        for n in neighbors:
            if n not in visited_bfs:
                if n not in parent_map:
                    parent_map[n] = current
                bfs_queue.append(n)

    # Step 4: Find accepting cycles
    # For each accepting state, do a DFS to see if we can reach it again
    accepting_states = [s for s in visited if composed.is_accepting(s)]

    for acc_state in accepting_states:
        # DFS from acc_state through adjacency, looking for cycle back to acc_state
        cycle = _find_cycle_from(acc_state, adjacency, visited)
        if cycle is not None:
            # Build prefix: path from initial to acc_state
            prefix = _build_path(parent_map, acc_state)
            return False, (prefix, cycle)

    return True, None


def _find_cycle_from(target, adjacency, all_visited):
    """
    DFS from target to find a path back to target (a cycle).
    Returns the cycle path or None.
    """
    visited = set()
    parent = {}

    stack = [(target, iter(adjacency.get(target, [])))]
    visited.add(target)

    while stack:
        current, neighbors_iter = stack[-1]
        try:
            next_state = next(neighbors_iter)
            if next_state == target:
                # Found cycle! Build cycle path
                cycle = _build_path_from_parent(parent, current, target)
                cycle.append(target)  # Close the cycle
                return cycle
            if next_state not in visited and next_state in all_visited:
                visited.add(next_state)
                parent[next_state] = current
                stack.append((next_state, iter(adjacency.get(next_state, []))))
        except StopIteration:
            stack.pop()

    return None


def _build_path_from_parent(parent, end, start):
    """Build path from start to end using parent dict."""
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent.get(current)
        if current is None:
            break
    path.append(start)
    path.reverse()
    return path


def _build_path(parent_map, target):
    """Build path from root to target using BFS parent map."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    path.reverse()
    return path


def format_counter_example(ce):
    """Format a counter-example (prefix, cycle) as a readable string."""
    if ce is None:
        return "No counter-example (property satisfied)"

    prefix, cycle = ce
    lines = []
    lines.append("Prefix trace:")
    for i, (sys_state, prop_state) in enumerate(prefix):
        lines.append(f"  {i}: {sys_state} [prop={prop_state}]")
    lines.append("Cyclic suffix trace:")
    for i, (sys_state, prop_state) in enumerate(cycle):
        marker = " (loop)" if i == len(cycle) - 1 else ""
        lines.append(f"  {i}: {sys_state} [prop={prop_state}]{marker}")
    return "\n".join(lines)
