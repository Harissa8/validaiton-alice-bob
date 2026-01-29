"""
AB1-AB5 Alice & Bob protocols encoded using Soup DSL.
Each model uses Piece (guard/effect) to define transitions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))

from souplanguagesemantics import Piece, Soup, SoupLanguageSemantics


# =============================================================================
# State representation
# =============================================================================
# State is a tuple for hashability:
#   AB1: (alice_loc, bob_loc)
#   AB2-AB4: (alice_loc, bob_loc, flagAlice, flagBob)
#   AB5: (alice_loc, bob_loc, flagAlice, flagBob, turn)
#
# Locations: "I" (Idle), "W" (Waiting), "CS" (Critical Section),
#            "R" (Retreat, AB4 only)


# =============================================================================
# AB1: No flags, simple alternation I <-> CS
# =============================================================================
# Alice: I -> CS (a1), CS -> I (a2)
# Bob:   I -> CS (b1), CS -> I (b2)

def make_ab1():
    pieces = [
        # Alice transitions
        Piece("a1",
              lambda s: ("CS", s[1]),
              lambda s: s[0] == "I"),
        Piece("a2",
              lambda s: ("I", s[1]),
              lambda s: s[0] == "CS"),
        # Bob transitions
        Piece("b1",
              lambda s: (s[0], "CS"),
              lambda s: s[1] == "I"),
        Piece("b2",
              lambda s: (s[0], "I"),
              lambda s: s[1] == "CS"),
    ]
    return Soup(pieces, ("I", "I"))


# =============================================================================
# AB2: Flag-based protocol with waiting
# =============================================================================
# Alice: I -> W / flagA=UP (a1)
#        W -> CS [flagB==DOWN] (a2)
#        CS -> I / flagA=DOWN (a3)
# Bob:   I -> W / flagB=UP (b1)
#        W -> CS [flagA==DOWN] (b2)
#        CS -> I / flagB=DOWN (b3)

def make_ab2():
    pieces = [
        # Alice transitions
        Piece("a1",
              lambda s: ("W", s[1], "UP", s[3]),
              lambda s: s[0] == "I"),
        Piece("a2",
              lambda s: ("CS", s[1], s[2], s[3]),
              lambda s: s[0] == "W" and s[3] == "DOWN"),
        Piece("a3",
              lambda s: ("I", s[1], "DOWN", s[3]),
              lambda s: s[0] == "CS"),
        # Bob transitions
        Piece("b1",
              lambda s: (s[0], "W", s[2], "UP"),
              lambda s: s[1] == "I"),
        Piece("b2",
              lambda s: (s[0], "CS", s[2], s[3]),
              lambda s: s[1] == "W" and s[2] == "DOWN"),
        Piece("b3",
              lambda s: (s[0], "I", s[2], "DOWN"),
              lambda s: s[1] == "CS"),
    ]
    return Soup(pieces, ("I", "I", "DOWN", "DOWN"))


# =============================================================================
# AB3: Bob backs off if Alice's flag is up
# =============================================================================
# Alice: same as AB2 (a1, a2, a3)
# Bob:   I -> W / flagB=UP (b1)
#        W -> CS [flagA==DOWN] (b2)
#        CS -> I / flagB=DOWN (b3)
#        W -> W [flagA==UP] / flagB=DOWN (b4) -- Bob backs off
#        W -> W [flagA==DOWN] / flagB=UP (b5) -- Bob retries (from flag DOWN)

def make_ab3():
    pieces = [
        # Alice transitions (same as AB2)
        Piece("a1",
              lambda s: ("W", s[1], "UP", s[3]),
              lambda s: s[0] == "I"),
        Piece("a2",
              lambda s: ("CS", s[1], s[2], s[3]),
              lambda s: s[0] == "W" and s[3] == "DOWN"),
        Piece("a3",
              lambda s: ("I", s[1], "DOWN", s[3]),
              lambda s: s[0] == "CS"),
        # Bob transitions
        Piece("b1",
              lambda s: (s[0], "W", s[2], "UP"),
              lambda s: s[1] == "I"),
        Piece("b2",
              lambda s: (s[0], "CS", s[2], s[3]),
              lambda s: s[1] == "W" and s[3] == "UP" and s[2] == "DOWN"),
        Piece("b3",
              lambda s: (s[0], "I", s[2], "DOWN"),
              lambda s: s[1] == "CS"),
        # Bob backs off: flag is UP and Alice's flag is UP -> lower flag
        Piece("b4",
              lambda s: (s[0], s[1], s[2], "DOWN"),
              lambda s: s[1] == "W" and s[3] == "UP" and s[2] == "UP"),
        # Bob retries: flag is DOWN -> raise flag again
        Piece("b5",
              lambda s: (s[0], s[1], s[2], "UP"),
              lambda s: s[1] == "W" and s[3] == "DOWN"),
    ]
    return Soup(pieces, ("I", "I", "DOWN", "DOWN"))


# =============================================================================
# AB4: Bob retreats to R state if Alice's flag is up
# =============================================================================
# Alice: same as AB2 (a1, a2, a3)
# Bob:   I -> W / flagB=UP (b1)
#        W -> CS [flagA==DOWN] (b2)
#        CS -> I / flagB=DOWN (b3)
#        W -> R [flagA==UP] / flagB=DOWN (b4) -- Bob retreats
#        R -> W [flagA==DOWN] / flagB=UP (b5) -- Bob retries from R

def make_ab4():
    pieces = [
        # Alice transitions (same as AB2)
        Piece("a1",
              lambda s: ("W", s[1], "UP", s[3]),
              lambda s: s[0] == "I"),
        Piece("a2",
              lambda s: ("CS", s[1], s[2], s[3]),
              lambda s: s[0] == "W" and s[3] == "DOWN"),
        Piece("a3",
              lambda s: ("I", s[1], "DOWN", s[3]),
              lambda s: s[0] == "CS"),
        # Bob transitions
        Piece("b1",
              lambda s: (s[0], "W", s[2], "UP"),
              lambda s: s[1] == "I"),
        Piece("b2",
              lambda s: (s[0], "CS", s[2], s[3]),
              lambda s: s[1] == "W" and s[3] == "UP" and s[2] == "DOWN"),
        Piece("b3",
              lambda s: (s[0], "I", s[2], "DOWN"),
              lambda s: s[1] == "CS"),
        # Bob retreats to R state, lowers flag
        Piece("b4",
              lambda s: (s[0], "R", s[2], "DOWN"),
              lambda s: s[1] == "W" and s[3] == "UP" and s[2] == "UP"),
        # Bob retries from R: raises flag and goes to W
        Piece("b5",
              lambda s: (s[0], "W", s[2], "UP"),
              lambda s: s[1] == "R" and s[2] == "DOWN"),
    ]
    return Soup(pieces, ("I", "I", "DOWN", "DOWN"))


# =============================================================================
# AB5: Peterson's algorithm with turn variable
# =============================================================================
# State: (alice_loc, bob_loc, flagAlice, flagBob, turn)
# Alice: I -> W / flagA=UP, turn=Bob (a1)
#        W -> CS [turn==Alice || flagB==DOWN] (a2)
#        CS -> I / flagA=DOWN (a3)
# Bob:   I -> W / flagB=UP, turn=Alice (b1)
#        W -> CS [turn==Bob || flagA==DOWN] (b2)
#        CS -> I / flagB=DOWN (b3)

def make_ab5():
    pieces = [
        # Alice transitions
        Piece("a1",
              lambda s: ("W", s[1], "UP", s[3], "Bob"),
              lambda s: s[0] == "I"),
        Piece("a2",
              lambda s: ("CS", s[1], s[2], s[3], s[4]),
              lambda s: s[0] == "W" and (s[4] == "Alice" or s[3] == "DOWN")),
        Piece("a3",
              lambda s: ("I", s[1], "DOWN", s[3], s[4]),
              lambda s: s[0] == "CS"),
        # Bob transitions
        Piece("b1",
              lambda s: (s[0], "W", s[2], "UP", "Alice"),
              lambda s: s[1] == "I"),
        Piece("b2",
              lambda s: (s[0], "CS", s[2], s[3], s[4]),
              lambda s: s[1] == "W" and (s[4] == "Bob" or s[2] == "DOWN")),
        Piece("b3",
              lambda s: (s[0], "I", s[2], "DOWN", s[4]),
              lambda s: s[1] == "CS"),
    ]
    return Soup(pieces, ("I", "I", "DOWN", "DOWN", "Alice"))


# =============================================================================
# Helper to create semantics for each model
# =============================================================================

def get_model(name):
    """Return SoupLanguageSemantics for the given model name."""
    models = {
        "AB1": make_ab1,
        "AB2": make_ab2,
        "AB3": make_ab3,
        "AB4": make_ab4,
        "AB5": make_ab5,
    }
    return SoupLanguageSemantics(models[name]())


# =============================================================================
# Quick test
# =============================================================================

if __name__ == "__main__":
    from ls2rg import LS2RG
    from bfs import breadth_first_search

    for name in ["AB1", "AB2", "AB3", "AB4", "AB5"]:
        sem = get_model(name)
        rg = LS2RG(sem)

        count = [0]
        def on_entry(state, opaque):
            opaque[0] += 1
            return False

        _, visited = breadth_first_search(rg, on_entry, count)
        print(f"{name}: {len(visited)} states")
