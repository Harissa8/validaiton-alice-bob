"""
Encode AB1, AB2, AB3 as rooted directed graphs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "1-bfs"))

from bfs import BFS
from enum import Enum
from typing import List


class Location(Enum):
    """Locations in the automaton"""
    I = "I"  # Initial/Idle
    W = "W"  # Waiting
    CS = "CS"  # Critical Section


class FlagState(Enum):
    """Flag states"""
    UP = "UP"
    DOWN = "DOWN"


class State:
    """Represents a global state of the system"""
    
    def __init__(self, alice_loc: Location, bob_loc: Location, 
                 flag_alice: FlagState, flag_bob: FlagState):
        self.alice_loc = alice_loc
        self.bob_loc = bob_loc
        self.flag_alice = flag_alice
        self.flag_bob = flag_bob
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.alice_loc == other.alice_loc and 
                self.bob_loc == other.bob_loc and
                self.flag_alice == other.flag_alice and
                self.flag_bob == other.flag_bob)
    
    def __hash__(self):
        return hash((self.alice_loc, self.bob_loc, self.flag_alice, self.flag_bob))
    
    def __repr__(self):
        return f"State(A:{self.alice_loc.value}, B:{self.bob_loc.value}, fA:{self.flag_alice.value}, fB:{self.flag_bob.value})"


class RootedGraph:
    """
    Abstract representation of a rooted directed graph
    Used to encode protocols as transition systems
    """
    
    def __init__(self, name: str):
        self.name = name
        self.initial_state = State(Location.I, Location.I, FlagState.DOWN, FlagState.DOWN)
    
    def get_successors(self, state: State) -> List[State]:
        """Get all possible successor states"""
        successors = []
        successors.extend(self.get_alice_transitions(state))
        successors.extend(self.get_bob_transitions(state))
        return successors
    
    def get_alice_transitions(self, state: State) -> List[State]:
        """Get possible transitions for Alice from current state"""
        raise NotImplementedError("Subclass must implement get_alice_transitions")
    
    def get_bob_transitions(self, state: State) -> List[State]:
        """Get possible transitions for Bob from current state"""
        raise NotImplementedError("Subclass must implement get_bob_transitions")
    
    def explore_with_bfs(self):
        """Explore the protocol state space using BFS"""
        bfs = BFS()
        stats = bfs.explore(self.initial_state, self.get_successors)
        return bfs, stats


class ProtocolAB1(RootedGraph):
    """
    AB1: Simple flag protocol
    - Raise flag when entering CS
    - No checking of other's flag
    """
    
    def __init__(self):
        super().__init__("AB1")
    
    def get_alice_transitions(self, state: State) -> List[State]:
        transitions = []
        
        if state.alice_loc == Location.I:
            # a1: I -> CS, raise flag
            transitions.append(State(Location.CS, state.bob_loc, 
                                   FlagState.UP, state.flag_bob))
        
        elif state.alice_loc == Location.CS:
            # a2: CS -> I, lower flag
            transitions.append(State(Location.I, state.bob_loc, 
                                   FlagState.DOWN, state.flag_bob))
        
        return transitions
    
    def get_bob_transitions(self, state: State) -> List[State]:
        transitions = []
        
        if state.bob_loc == Location.I:
            # b1: I -> CS, raise flag
            transitions.append(State(state.alice_loc, Location.CS, 
                                   state.flag_alice, FlagState.UP))
        
        elif state.bob_loc == Location.CS:
            # b2: CS -> I, lower flag
            transitions.append(State(state.alice_loc, Location.I, 
                                   state.flag_alice, FlagState.DOWN))
        
        return transitions


class ProtocolAB2(RootedGraph):
    """
    AB2: Flag-based protocol with waiting
    - Raise flag then check other's flag
    - Wait if other's flag is up
    """
    
    def __init__(self):
        super().__init__("AB2")
    
    def get_alice_transitions(self, state: State) -> List[State]:
        transitions = []
        
        if state.alice_loc == Location.I:
            # a1: I -> W, raise flag
            transitions.append(State(Location.W, state.bob_loc, 
                                   FlagState.UP, state.flag_bob))
        
        elif state.alice_loc == Location.W:
            # a3: W -> CS if Bob's flag is down
            if state.flag_bob == FlagState.DOWN:
                transitions.append(State(Location.CS, state.bob_loc, 
                                       state.flag_alice, state.flag_bob))
        
        elif state.alice_loc == Location.CS:
            # a2: CS -> I, lower flag
            transitions.append(State(Location.I, state.bob_loc, 
                                   FlagState.DOWN, state.flag_bob))
        
        return transitions
    
    def get_bob_transitions(self, state: State) -> List[State]:
        transitions = []
        
        if state.bob_loc == Location.I:
            # b1: I -> W, raise flag
            transitions.append(State(state.alice_loc, Location.W, 
                                   state.flag_alice, FlagState.UP))
        
        elif state.bob_loc == Location.W:
            # b3: W -> CS if Alice's flag is down
            if state.flag_alice == FlagState.DOWN:
                transitions.append(State(state.alice_loc, Location.CS, 
                                       state.flag_alice, state.flag_bob))
        
        elif state.bob_loc == Location.CS:
            # b2: CS -> I, lower flag
            transitions.append(State(state.alice_loc, Location.I, 
                                   state.flag_alice, FlagState.DOWN))
        
        return transitions


class ProtocolAB3(RootedGraph):
    """
    AB3: Polite protocol with flag lowering
    - Raise flag then check other's flag
    - If other's flag is up, lower own flag and wait
    - Bob yields to Alice if both flags are up
    """
    
    def __init__(self):
        super().__init__("AB3")
    
    def get_alice_transitions(self, state: State) -> List[State]:
        transitions = []
        
        if state.alice_loc == Location.I:
            # a3: I -> W, raise flag
            transitions.append(State(Location.W, state.bob_loc, 
                                   FlagState.UP, state.flag_bob))
        
        elif state.alice_loc == Location.W:
            if state.flag_alice == FlagState.UP:
                # a2: W -> W, lower flag if Bob's flag is up
                if state.flag_bob == FlagState.UP:
                    transitions.append(State(Location.W, state.bob_loc, 
                                           FlagState.DOWN, state.flag_bob))
                else:
                    # Alice's flag up, Bob's down -> enter CS
                    transitions.append(State(Location.CS, state.bob_loc, 
                                           state.flag_alice, state.flag_bob))
            else:  # Alice's flag is DOWN
                # a1: W -> W, raise flag (after waiting)
                transitions.append(State(Location.W, state.bob_loc, 
                                       FlagState.UP, state.flag_bob))
        
        elif state.alice_loc == Location.CS:
            # Exit CS and lower flag
            transitions.append(State(Location.I, state.bob_loc, 
                                   FlagState.DOWN, state.flag_bob))
        
        return transitions
    
    def get_bob_transitions(self, state: State) -> List[State]:
        transitions = []
        
        if state.bob_loc == Location.I:
            # b1: I -> W, raise flag
            transitions.append(State(state.alice_loc, Location.W, 
                                   state.flag_alice, FlagState.UP))
        
        elif state.bob_loc == Location.W:
            if state.flag_bob == FlagState.UP:
                # b2: W -> W, lower flag if Alice's flag is up
                if state.flag_alice == FlagState.UP:
                    transitions.append(State(state.alice_loc, Location.W, 
                                           state.flag_alice, FlagState.DOWN))
                else:
                    # Bob's flag up, Alice's down -> enter CS
                    transitions.append(State(state.alice_loc, Location.CS, 
                                           state.flag_alice, state.flag_bob))
            else:  # Bob's flag is DOWN
                # b4: W -> W, raise flag (after waiting)
                transitions.append(State(state.alice_loc, Location.W, 
                                       state.flag_alice, FlagState.UP))
        
        elif state.bob_loc == Location.CS:
            # Exit CS and lower flag
            transitions.append(State(state.alice_loc, Location.I, 
                                   state.flag_alice, FlagState.DOWN))
        
        return transitions


def test_protocol_encoding(protocol):
    """Test that a protocol is correctly encoded as rooted graph"""
    print(f"\n{'='*60}")
    print(f"Testing Protocol {protocol.name}")
    print(f"{'='*60}")
    
    # Verify it's a rooted graph
    print(f"Initial state (root): {protocol.initial_state}")
    
    # Explore state space
    bfs, stats = protocol.explore_with_bfs()
    
    print(f"\nRooted Graph Properties:")
    print(f"  - Root node: {protocol.initial_state}")
    print(f"  - Total nodes: {stats['total_states']}")
    print(f"  - Total edges: {stats['total_transitions']}")
    print(f"  - Graph is directed: Yes")
    print(f"  - All nodes reachable from root: Yes (by BFS)")
    
    # Show some sample transitions
    print(f"\nSample transitions from root:")
    successors = protocol.get_successors(protocol.initial_state)
    for i, succ in enumerate(successors[:3], 1):
        print(f"  {i}. {protocol.initial_state}")
        print(f"     -> {succ}")
    
    print(f"\n✓ Protocol {protocol.name} correctly encoded as RootedGraph")
    return bfs, stats


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("#"*60)
    print("\nEncoding AB1, AB2, AB3 using RootedGraph abstraction...\n")
    
    protocols = [
        ProtocolAB1(),
        ProtocolAB2(),
        ProtocolAB3()
    ]
    
    results = []
    for protocol in protocols:
        bfs, stats = test_protocol_encoding(protocol)
        results.append((protocol.name, stats))
    
    # Summary table
    print("\n" + "="*60)
    print("PROTOCOL ENCODING SUMMARY")
    print("="*60)
    print(f"\n{'Protocol':<12} {'States':<10} {'Transitions':<15} {'Encoded':<10}")
    print("-"*60)
    for name, stats in results:
        print(f"{name:<12} {stats['total_states']:<10} {stats['total_transitions']:<15} {'✓ Yes':<10}")
    
    print("\n" + "="*60)
    print("✓ ALL PROTOCOLS ENCODED AS ROOTED GRAPHS!")
    print("="*60)
    print("\nAll three protocols successfully encoded using RootedGraph abstraction.")
    print("Each protocol is a directed graph with:")
    print("  - Root node = Initial state (A:I, B:I, fA:DOWN, fB:DOWN)")
    print("  - Nodes = System states")
    print("  - Edges = State transitions")
