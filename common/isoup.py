"""
iSoup: Properties encoded as LanguageSemantics.
Each property is a Buchi automaton wrapped in the LanguageSemantics interface.

The iSoup state is the automaton state (0, 1, 2, "x", "y", etc.).
Transitions are guarded by predicates on the SYSTEM state.
Accepting states are marked for Buchi cycle detection.
"""

from languagesemantics import LanguageSemantics


class ISoupSemantics(LanguageSemantics):
    """
    Base class for iSoup properties.
    Wraps a Buchi automaton as a LanguageSemantics.

    Subclasses define:
    - _initial: initial automaton state
    - _accepting: set of accepting states
    - _transitions: dict {state: [(guard_fn, target_state), ...]}
      where guard_fn takes (system_state, is_deadlock) -> bool
    """

    def __init__(self):
        self._initial = None
        self._accepting = set()
        self._transitions = {}

    def initials(self):
        return [self._initial]

    def actions(self, prop_state):
        """Return all transitions from this property state."""
        return self._transitions.get(prop_state, [])

    def execute(self, prop_state, action):
        """Action is a (guard_fn, target_state) tuple. Return [target_state]."""
        _, target = action
        return [target]

    def is_accepting(self, prop_state):
        return prop_state in self._accepting

    def enabled_transitions(self, prop_state, system_state, is_deadlock):
        """Return transitions whose guard is satisfied by the system state."""
        result = []
        for guard, target in self._transitions.get(prop_state, []):
            if guard(system_state, is_deadlock):
                result.append((guard, target))
        return result


# =============================================================================
# Helper functions to read system state tuples
# =============================================================================

def _alice_in_cs(s):
    return s[0] == "CS"

def _bob_in_cs(s):
    return s[1] == "CS"

def _both_in_cs(s):
    return _alice_in_cs(s) and _bob_in_cs(s)

def _flag_alice(s):
    return s[2] if len(s) > 2 else "DOWN"

def _flag_bob(s):
    return s[3] if len(s) > 3 else "DOWN"

def _alice_loc(s):
    return s[0]

def _bob_loc(s):
    return s[1]


# =============================================================================
# P1: Exclusion (never A.CS & B.CS)
# =============================================================================
# Accepts bad traces where both are in CS
# State 1 (initial): stays while not both in CS
# State 0 (accepting trap): both were in CS, stays forever

class P1Exclusion(ISoupSemantics):
    def __init__(self):
        super().__init__()
        self._initial = 1
        self._accepting = {0}
        self._transitions = {
            1: [
                (lambda s, d: not _both_in_cs(s), 1),
                (lambda s, d: _both_in_cs(s), 0),
            ],
            0: [
                (lambda s, d: True, 0),
            ],
        }


# =============================================================================
# P2: No deadlock
# =============================================================================
# Accepts bad traces where a deadlock occurs
# State 1 (initial): stays while no deadlock
# State 0 (accepting trap): deadlock found

class P2Deadlock(ISoupSemantics):
    def __init__(self):
        super().__init__()
        self._initial = 1
        self._accepting = {0}
        self._transitions = {
            1: [
                (lambda s, d: not d, 1),
                (lambda s, d: d, 0),
            ],
            0: [
                (lambda s, d: True, 0),
            ],
        }


# =============================================================================
# P3: At least one in CS (liveness)
# =============================================================================
# Accepts bad traces where nobody ever enters CS
# State "x" (initial): can stay or go to "y" when nobody in CS
# State "y" (accepting): stays while nobody in CS

class P3AtLeastOneIn(ISoupSemantics):
    def __init__(self):
        super().__init__()
        self._initial = "x"
        self._accepting = {"y"}

        def q(s, d):
            return _alice_in_cs(s) or _bob_in_cs(s)

        self._transitions = {
            "x": [
                (lambda s, d: True, "x"),
                (lambda s, d: not q(s, d), "y"),
            ],
            "y": [
                (lambda s, d: not q(s, d), "y"),
            ],
        }


# =============================================================================
# P4: If one wants in, it will get in
# =============================================================================
# Accepts bad traces where someone wants in but never gets CS
# State 0 (initial): normal
# State 1 (accepting): Alice wants in (flagA==UP) but never gets CS
# State 2 (accepting): Bob wants in (flagB==UP) but never gets CS

class P4WantsIn(ISoupSemantics):
    def __init__(self):
        super().__init__()
        self._initial = 0
        self._accepting = {1, 2}
        self._transitions = {
            0: [
                (lambda s, d: True, 0),
                (lambda s, d: _flag_alice(s) == "UP" and not _alice_in_cs(s), 1),
                (lambda s, d: _flag_bob(s) == "UP" and not _bob_in_cs(s), 2),
            ],
            1: [
                (lambda s, d: not _alice_in_cs(s), 1),
            ],
            2: [
                (lambda s, d: not _bob_in_cs(s), 2),
            ],
        }


# =============================================================================
# P5: Uncontested progress
# =============================================================================
# Accepts bad traces where one waits alone but never gets CS
# State 0 (initial): normal
# State 1 (accepting): Alice waiting, Bob not interested, Alice never gets CS
# State 2 (accepting): Bob waiting, Alice not interested, Bob never gets CS

class P5UncontestedProgress(ISoupSemantics):
    def __init__(self):
        super().__init__()
        self._initial = 0
        self._accepting = {1, 2}
        self._transitions = {
            0: [
                (lambda s, d: True, 0),
                (lambda s, d: _alice_loc(s) == "W" and not _alice_in_cs(s) and _bob_loc(s) == "I", 1),
                (lambda s, d: _bob_loc(s) == "W" and not _bob_in_cs(s) and _alice_loc(s) == "I", 2),
            ],
            1: [
                (lambda s, d: not _alice_in_cs(s), 1),
            ],
            2: [
                (lambda s, d: not _bob_in_cs(s), 2),
            ],
        }


# =============================================================================
# Factory
# =============================================================================

def get_isoup_property(name):
    """Return an ISoupSemantics for the given property name."""
    props = {
        "P1": P1Exclusion,
        "P2": P2Deadlock,
        "P3": P3AtLeastOneIn,
        "P4": P4WantsIn,
        "P5": P5UncontestedProgress,
    }
    return props[name]()
