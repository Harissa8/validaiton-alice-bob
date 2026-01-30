"""
Step Synchronous Composition.
Combines a system LanguageSemantics (Soup) with a property LanguageSemantics (iSoup)
into a new LanguageSemantics.

Composed state = (system_state, property_state)
"""

from languagesemantics import LanguageSemantics


class StepSyncComposition(LanguageSemantics):
    """
    Synchronous product of system x property.

    At each step:
    1. System executes an action -> produces next system state
    2. Property observes the next system state -> advances property automaton
    3. Composed state = (next_sys_state, next_prop_state)

    Deadlock detection: if the system has no actions from a state,
    the property can still transition (to detect deadlock properties).
    """

    def __init__(self, system_ls, property_ls):
        """
        Args:
            system_ls: LanguageSemantics for the system (Soup)
            property_ls: ISoupSemantics for the property (iSoup)
        """
        self.system = system_ls
        self.prop = property_ls

    def initials(self):
        """Cartesian product of initial states."""
        composed = []
        for sys_init in self.system.initials():
            for prop_init in self.prop.initials():
                # Check which property transitions are enabled for the initial system state
                is_deadlock = len(self.system.actions(sys_init)) == 0
                enabled = self.prop.enabled_transitions(prop_init, sys_init, is_deadlock)
                for _, next_prop in enabled:
                    composed.append((sys_init, next_prop))
        return composed

    def actions(self, composed_state):
        """
        Return system actions that are possible from this composed state.
        If system is in deadlock, return a special deadlock marker.
        """
        sys_state, prop_state = composed_state
        sys_actions = self.system.actions(sys_state)

        if not sys_actions:
            # Deadlock: return special marker so property can observe it
            return ["__deadlock__"]

        return sys_actions

    def execute(self, composed_state, action):
        """
        Execute a system action and advance the property automaton.
        Returns list of (next_sys_state, next_prop_state) pairs.
        """
        sys_state, prop_state = composed_state
        results = []

        if action == "__deadlock__":
            # System is stuck - let property observe the deadlock
            enabled = self.prop.enabled_transitions(prop_state, sys_state, True)
            for _, next_prop in enabled:
                results.append((sys_state, next_prop))
            return results

        # Execute system action
        next_sys_states = self.system.execute(sys_state, action)

        for next_sys in next_sys_states:
            # Check if next system state is a deadlock
            is_deadlock = len(self.system.actions(next_sys)) == 0
            # Get property transitions enabled by the next system state
            enabled = self.prop.enabled_transitions(prop_state, next_sys, is_deadlock)
            for _, next_prop in enabled:
                results.append((next_sys, next_prop))

        return results

    def is_accepting(self, composed_state):
        """Check if the property component is in an accepting state."""
        _, prop_state = composed_state
        return self.prop.is_accepting(prop_state)
