"""
Buchi automaton framework for property verification.
Includes:
- BuchiAutomaton class
- Product automaton construction
- Nested DFS for accepting cycle detection
- Counter-example generation (prefix + cyclic suffix)
- P1-P5 property definitions
"""

from collections import deque


# =============================================================================
# Buchi Automaton
# =============================================================================

class BuchiAutomaton:
    """
    A Buchi automaton defined by:
    - states: list of state labels
    - initial: initial state label
    - accepting: set of accepting state labels
    - transitions: dict mapping (buchi_state) -> list of (guard, next_buchi_state)
      where guard is a function (system_state) -> bool
    """

    def __init__(self, states, initial, accepting, transitions):
        self.states = states
        self.initial = initial
        self.accepting = set(accepting)
        self.transitions = transitions  # {buchi_state: [(guard_fn, next_state), ...]}


# =============================================================================
# Product automaton + Nested DFS verification
# =============================================================================

def get_system_neighbors(system_state, ls, ls2rg_class):
    """Get all successor system states using LanguageSemantics."""
    successors = []
    actions = ls.actions(system_state)
    for action in actions:
        next_states = ls.execute(system_state, action)
        successors.extend(next_states)
    return successors


def verify_buchi(ls, buchi, ls2rg_class=None):
    """
    Verify that the system (LanguageSemantics) satisfies a Buchi property.

    The property is SATISFIED if no accepting cycle exists in the product automaton.
    The property is VIOLATED if an accepting cycle is found.

    Uses nested DFS (Courcoubetis et al. / NDFS algorithm):
    - Outer DFS explores the product state space
    - When an accepting state is fully explored (post-order),
      inner DFS checks if a cycle back to it exists

    Args:
        ls: LanguageSemantics instance (the system model)
        buchi: BuchiAutomaton instance (the property)

    Returns:
        (satisfied, counter_example)
        - satisfied: True if property holds, False if violated
        - counter_example: None if satisfied, or (prefix, cycle) if violated
    """
    # Product state = (system_state, buchi_state)
    # Build initial product states
    initial_system_states = ls.initials()
    initial_buchi = buchi.initial

    # Nested DFS
    visited_outer = set()
    visited_inner = set()
    outer_stack = []  # (product_state, parent_info) for path reconstruction
    parent_outer = {}  # product_state -> parent product_state

    # Get product successors
    def product_successors(prod_state):
        sys_state, buchi_state = prod_state
        successors = []
        # Get system successors
        sys_actions = ls.actions(sys_state)

        # If no system actions (deadlock), still need to check buchi transitions
        # with the current state (for deadlock detection)
        if not sys_actions:
            # System is stuck - check buchi transitions with current state
            for guard, next_buchi in buchi.transitions.get(buchi_state, []):
                if guard(sys_state, True):  # True = deadlock
                    successors.append((sys_state, next_buchi))
            return successors

        for action in sys_actions:
            next_sys_states = ls.execute(sys_state, action)
            for next_sys in next_sys_states:
                # Check buchi transitions
                for guard, next_buchi in buchi.transitions.get(buchi_state, []):
                    if guard(next_sys, False):  # False = not deadlock
                        successors.append((next_sys, next_buchi))
        return successors

    def is_accepting(prod_state):
        return prod_state[1] in buchi.accepting

    # Build path from parent dict
    def build_path(parent_dict, start, end):
        path = []
        current = end
        while current is not None and current != start:
            path.append(current)
            current = parent_dict.get(current)
        if current == start:
            path.append(start)
        path.reverse()
        return path

    # Outer DFS (iterative to avoid stack overflow)
    found_cycle = [None]  # [None] or [(prefix, cycle)]

    def nested_dfs():
        # Phase 1: Outer DFS
        for init_sys in initial_system_states:
            init_prod = (init_sys, initial_buchi)
            if init_prod in visited_outer:
                continue

            # Iterative DFS with explicit stack
            # Stack items: (state, iterator_of_successors, is_expanded)
            dfs_stack = [(init_prod, None)]
            parent_outer[init_prod] = None
            path_stack = [init_prod]

            while dfs_stack and found_cycle[0] is None:
                current, succ_iter = dfs_stack[-1]

                if current not in visited_outer:
                    visited_outer.add(current)

                if succ_iter is None:
                    # First visit: create successor iterator
                    succs = product_successors(current)
                    succ_iter = iter(succs)
                    dfs_stack[-1] = (current, succ_iter)

                try:
                    next_state = next(succ_iter)
                    if next_state not in visited_outer:
                        parent_outer[next_state] = current
                        dfs_stack.append((next_state, None))
                        path_stack.append(next_state)
                except StopIteration:
                    # All successors explored - post-order processing
                    dfs_stack.pop()
                    if path_stack:
                        path_stack.pop()

                    # If accepting, run inner DFS to find cycle
                    if is_accepting(current) and found_cycle[0] is None:
                        cycle = inner_dfs(current, product_successors)
                        if cycle is not None:
                            # Build prefix: path from initial to current
                            prefix = build_path(parent_outer, init_prod, current)
                            found_cycle[0] = (prefix, cycle)
                            return

    def inner_dfs(accepting_state, get_successors):
        """Try to find a cycle back to accepting_state."""
        visited_inner_local = set()
        parent_inner = {}

        stack = [(accepting_state, None)]
        parent_inner[accepting_state] = None

        while stack:
            current, succ_iter = stack[-1]

            if current not in visited_inner_local:
                visited_inner_local.add(current)

            if succ_iter is None:
                succs = get_successors(current)
                succ_iter = iter(succs)
                stack[-1] = (current, succ_iter)

            try:
                next_state = next(succ_iter)
                if next_state == accepting_state:
                    # Found cycle back to accepting state
                    cycle = build_path(parent_inner, accepting_state, current)
                    cycle.append(accepting_state)  # Close the cycle
                    return cycle
                if next_state not in visited_inner_local:
                    parent_inner[next_state] = current
                    stack.append((next_state, None))
            except StopIteration:
                stack.pop()

        return None

    nested_dfs()

    if found_cycle[0] is not None:
        prefix, cycle = found_cycle[0]
        return False, (prefix, cycle)
    else:
        return True, None


# =============================================================================
# Property definitions P1-P5
# =============================================================================
# Guards take (system_state, is_deadlock) as arguments.
# system_state format varies by model:
#   AB1: (alice, bob)
#   AB2-AB4: (alice, bob, flagA, flagB)
#   AB5: (alice, bob, flagA, flagB, turn)

def _alice_loc(s):
    return s[0]

def _bob_loc(s):
    return s[1]

def _flag_alice(s):
    return s[2] if len(s) > 2 else "DOWN"

def _flag_bob(s):
    return s[3] if len(s) > 3 else "DOWN"

def _alice_in_cs(s):
    return s[0] == "CS"

def _bob_in_cs(s):
    return s[1] == "CS"

def _both_in_cs(s):
    return _alice_in_cs(s) and _bob_in_cs(s)


# --- P1: Exclusion (never A.CS & B.CS) ---
# Buchi automaton that ACCEPTS bad traces (where both are in CS simultaneously)
# State 1 (initial, accepting): stays while not both in CS
# State 0: trap (both were in CS) - self-loop, accepting
# Property violated = accepting cycle found

def make_p1():
    transitions = {
        1: [
            # Stay in 1 if NOT both in CS
            (lambda s, d: not _both_in_cs(s), 1),
            # Go to 0 if both in CS
            (lambda s, d: _both_in_cs(s), 0),
        ],
        0: [
            # Trap state - always stay (any state)
            (lambda s, d: True, 0),
        ],
    }
    return BuchiAutomaton(
        states=[0, 1],
        initial=1,
        accepting={0},
        transitions=transitions,
    )


# --- P2: No deadlock ---
# Accepts bad traces where a deadlock occurs
# State 1 (initial, accepting): stays while no deadlock
# State 0: trap (deadlock found) - self-loop, accepting

def make_p2():
    transitions = {
        1: [
            # Stay in 1 if not deadlock
            (lambda s, d: not d, 1),
            # Go to 0 if deadlock
            (lambda s, d: d, 0),
        ],
        0: [
            # Trap state
            (lambda s, d: True, 0),
        ],
    }
    return BuchiAutomaton(
        states=[0, 1],
        initial=1,
        accepting={0},
        transitions=transitions,
    )


# --- P3: At least one in CS (liveness) ---
# Accepts bad traces where NOBODY ever enters CS (infinitely)
# State x (initial): can stay with q (someone in CS) or !q; goes to y on !q
# State y (accepting): stays on !q (nobody in CS forever = bad)
#
# q = Alice@CS or Bob@CS

def make_p3():
    def q(s, d):
        return _alice_in_cs(s) or _bob_in_cs(s)

    transitions = {
        "x": [
            # Stay in x on any condition
            (lambda s, d: True, "x"),
            # Go to y on !q (nobody in CS)
            (lambda s, d: not q(s, d), "y"),
        ],
        "y": [
            # Stay in y while nobody in CS (accepting = bad)
            (lambda s, d: not q(s, d), "y"),
        ],
    }
    return BuchiAutomaton(
        states=["x", "y"],
        initial="x",
        accepting={"y"},
        transitions=transitions,
    )


# --- P4: If one wants in, it will get in ---
# Accepts bad traces where someone wants in (flag UP) but never gets CS
# State 0 (initial): normal operation
# State 1 (accepting): Alice wants in (flagA==UP) but never gets CS
# State 2 (accepting): Bob wants in (flagB==UP) but never gets CS
#
# p0 = flagAlice == UP, q0 = Alice@CS
# p1 = flagBob == UP, q1 = Bob@CS

def make_p4():
    transitions = {
        0: [
            # Stay in 0 always
            (lambda s, d: True, 0),
            # Go to 1: Alice wants in (flag UP) and not in CS
            (lambda s, d: _flag_alice(s) == "UP" and not _alice_in_cs(s), 1),
            # Go to 2: Bob wants in (flag UP) and not in CS
            (lambda s, d: _flag_bob(s) == "UP" and not _bob_in_cs(s), 2),
        ],
        1: [
            # Stay in 1 while Alice NOT in CS (bad: she never gets in)
            (lambda s, d: not _alice_in_cs(s), 1),
        ],
        2: [
            # Stay in 2 while Bob NOT in CS (bad: he never gets in)
            (lambda s, d: not _bob_in_cs(s), 2),
        ],
    }
    return BuchiAutomaton(
        states=[0, 1, 2],
        initial=0,
        accepting={1, 2},
        transitions=transitions,
    )


# --- P5: Uncontested progress ---
# Accepts bad traces where one is waiting alone but never gets CS
# State 0 (initial): normal
# State 1 (accepting): Alice waiting, Bob not interested, Alice never gets CS
# State 2 (accepting): Bob waiting, Alice not interested, Bob never gets CS
#
# aIsWaiting = Alice @ W
# bNotInterested = Bob @ I (or flag DOWN, or not in W/CS)
# aNotInterested = Alice @ I
# bIsWaiting = Bob @ W

def make_p5():
    def a_waiting_b_not_interested(s, d):
        return (_alice_loc(s) == "W" and
                not _alice_in_cs(s) and
                _bob_loc(s) == "I")

    def b_waiting_a_not_interested(s, d):
        return (_bob_loc(s) == "W" and
                not _bob_in_cs(s) and
                _alice_loc(s) == "I")

    transitions = {
        0: [
            # Stay in 0 always
            (lambda s, d: True, 0),
            # Go to 1: Alice waiting, Bob not interested
            (lambda s, d: a_waiting_b_not_interested(s, d), 1),
            # Go to 2: Bob waiting, Alice not interested
            (lambda s, d: b_waiting_a_not_interested(s, d), 2),
        ],
        1: [
            # Stay in 1 while Alice not in CS
            (lambda s, d: not _alice_in_cs(s), 1),
        ],
        2: [
            # Stay in 2 while Bob not in CS
            (lambda s, d: not _bob_in_cs(s), 2),
        ],
    }
    return BuchiAutomaton(
        states=[0, 1, 2],
        initial=0,
        accepting={1, 2},
        transitions=transitions,
    )


# =============================================================================
# Property factory
# =============================================================================

def get_property(name):
    """Return a BuchiAutomaton for the given property name."""
    props = {
        "P1": make_p1,
        "P2": make_p2,
        "P3": make_p3,
        "P4": make_p4,
        "P5": make_p5,
    }
    return props[name]()


# =============================================================================
# Formatting counter-examples
# =============================================================================

def format_counter_example(ce):
    """Format a counter-example (prefix, cycle) as a readable string."""
    if ce is None:
        return "No counter-example (property satisfied)"

    prefix, cycle = ce
    lines = []
    lines.append("Prefix trace:")
    for i, (sys_state, buchi_state) in enumerate(prefix):
        lines.append(f"  {i}: {sys_state} [buchi={buchi_state}]")
    lines.append("Cyclic suffix trace:")
    for i, (sys_state, buchi_state) in enumerate(cycle):
        marker = " (loop)" if i == len(cycle) - 1 else ""
        lines.append(f"  {i}: {sys_state} [buchi={buchi_state}]{marker}")
    return "\n".join(lines)
