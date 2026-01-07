"""
Verify mutual exclusion and deadlock properties for AB1, AB2, AB3
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "1-bfs"))
sys.path.insert(0, str(Path(__file__).parent.parent / "3-protocols"))

from protocols import ProtocolAB1, ProtocolAB2, ProtocolAB3, Location, State
from bfs import BFS
from typing import List, Set


class PropertyVerifier:
    """
    Verifies properties of protocols using BFS exploration
    """
    
    def __init__(self, protocol):
        self.protocol = protocol
        self.bfs = BFS()
        self.violation_states: List[State] = []
        self.deadlock_states: List[State] = []
    
    def verify_mutual_exclusion(self) -> bool:
        """
        Verify mutual exclusion property:
        Alice and Bob should never both be in Critical Section simultaneously
        
        Returns:
            True if property is satisfied, False if violated
        """
        self.violation_states = []
        
        for state in self.bfs.visited:
            if state.alice_loc == Location.CS and state.bob_loc == Location.CS:
                self.violation_states.append(state)
        
        return len(self.violation_states) == 0
    
    def verify_deadlock_freedom(self) -> bool:
        """
        Verify deadlock freedom:
        System should not reach a state where no progress is possible
        A state is a deadlock if it has no successors and is not the initial state
        
        Returns:
            True if deadlock-free, False if deadlock exists
        """
        self.deadlock_states = []
        
        for state in self.bfs.visited:
            successors = self.protocol.get_successors(state)
            # Deadlock: no successors and not initial state
            if len(successors) == 0 and state != self.protocol.initial_state:
                self.deadlock_states.append(state)
        
        return len(self.deadlock_states) == 0
    
    def verify_all_properties(self):
        """
        Explore state space and verify all properties
        """
        # First explore the state space
        stats = self.bfs.explore(
            self.protocol.initial_state,
            self.protocol.get_successors
        )
        
        # Then verify properties
        mutex_satisfied = self.verify_mutual_exclusion()
        deadlock_free = self.verify_deadlock_freedom()
        
        return {
            'protocol': self.protocol.name,
            'total_states': stats['total_states'],
            'total_transitions': stats['total_transitions'],
            'mutual_exclusion': mutex_satisfied,
            'deadlock_free': deadlock_free,
            'violation_states': self.violation_states.copy(),
            'deadlock_states': self.deadlock_states.copy()
        }
    
    def print_results(self, results):
        """Print verification results"""
        print(f"\n{'='*60}")
        print(f"Protocol: {results['protocol']}")
        print(f"{'='*60}")
        print(f"State Space:")
        print(f"  Total states: {results['total_states']}")
        print(f"  Total transitions: {results['total_transitions']}")
        
        print(f"\nProperty Verification:")
        
        # Mutual Exclusion
        mutex_status = "+ SATISFIED" if results['mutual_exclusion'] else "- VIOLATED"
        print(f"  Mutual Exclusion: {mutex_status}")
        if not results['mutual_exclusion']:
            print(f"    Violations found: {len(results['violation_states'])}")
            for state in results['violation_states'][:2]:
                print(f"      - {state}")
        
        # Deadlock Freedom
        deadlock_status = "+ NO DEADLOCK" if results['deadlock_free'] else "- HAS DEADLOCK"
        print(f"  Deadlock Freedom: {deadlock_status}")
        if not results['deadlock_free']:
            print(f"    Deadlock states: {len(results['deadlock_states'])}")
            for state in results['deadlock_states'][:2]:
                print(f"      - {state}")


def verify_protocol(protocol):
    """Verify a single protocol"""
    verifier = PropertyVerifier(protocol)
    results = verifier.verify_all_properties()
    verifier.print_results(results)
    return results


def test_ab1_verification():
    """Test AB1 - Should violate mutual exclusion but no deadlock"""
    print("\n" + "="*60)
    print("TEST 1: Verify Protocol AB1")
    print("="*60)
    
    protocol = ProtocolAB1()
    results = verify_protocol(protocol)
    
    # AB1 should NOT have mutual exclusion
    assert not results['mutual_exclusion'], "AB1 should violate mutual exclusion"
    assert len(results['violation_states']) > 0, "Should find violation states"
    
    # AB1 should be deadlock-free
    assert results['deadlock_free'], "AB1 should be deadlock-free"
    
    print("\n+ AB1 verification correct!")
    print("  Expected: No mutual exclusion, No deadlock")
    print("  Result: + Matches expected behavior")
    return results


def test_ab2_verification():
    """Test AB2 - Should have mutual exclusion but has deadlock"""
    print("\n" + "="*60)
    print("TEST 2: Verify Protocol AB2")
    print("="*60)
    
    protocol = ProtocolAB2()
    results = verify_protocol(protocol)
    
    # AB2 should have mutual exclusion
    assert results['mutual_exclusion'], "AB2 should satisfy mutual exclusion"
    
    # AB2 should have deadlock
    assert not results['deadlock_free'], "AB2 should have deadlock"
    assert len(results['deadlock_states']) > 0, "Should find deadlock states"
    
    print("\n+ AB2 verification correct!")
    print("  Expected: Mutual exclusion, Has deadlock")
    print("  Result: + Matches expected behavior")
    return results


def test_ab3_verification():
    """Test AB3 - Should have mutual exclusion AND be deadlock-free"""
    print("\n" + "="*60)
    print("TEST 3: Verify Protocol AB3")
    print("="*60)
    
    protocol = ProtocolAB3()
    results = verify_protocol(protocol)
    
    # AB3 should have mutual exclusion
    assert results['mutual_exclusion'], "AB3 should satisfy mutual exclusion"
    
    # AB3 should be deadlock-free
    assert results['deadlock_free'], "AB3 should be deadlock-free"
    
    print("\n+ AB3 verification correct!")
    print("  Expected: Mutual exclusion, No deadlock")
    print("  Result: + Matches expected behavior - CORRECT PROTOCOL!")
    return results


def generate_comparison_table(all_results):
    """Generate comparison table for all protocols"""
    print("\n" + "="*60)
    print("VERIFICATION COMPARISON TABLE")
    print("="*60)
    
    print(f"\n{'Protocol':<12} {'States':<10} {'Mutual Excl.':<15} {'Deadlock Free':<15}")
    print("-"*60)
    
    for results in all_results:
        mutex = "+" if results['mutual_exclusion'] else "-"
        deadlock = "+" if results['deadlock_free'] else "-"
        
        print(f"{results['protocol']:<12} {results['total_states']:<10} "
              f"{mutex:<15} {deadlock:<15}")
    
    print("\n" + "="*60)
    print("LEGEND:")
    print("  + = Property satisfied")
    print("  - = Property violated")
    print("\nCONCLUSION:")
    print("  AB1: - Unsafe (no mutual exclusion)")
    print("  AB2:  Can deadlock")
    print("  AB3: + CORRECT (safe and deadlock-free)")
    print("="*60)


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# COMMIT 4: PROPERTY VERIFICATION")
    print("#"*60)
    print("\nVerifying mutual exclusion and deadlock for each protocol...\n")
    
    # Verify each protocol
    results_ab1 = test_ab1_verification()
    results_ab2 = test_ab2_verification()
    results_ab3 = test_ab3_verification()
    
    # Generate comparison table
    all_results = [results_ab1, results_ab2, results_ab3]
    generate_comparison_table(all_results)
    
    print("\n" + "="*60)
    print("+ ALL PROPERTY VERIFICATIONS COMPLETE!")
    print("="*60)
    print("\nAll protocols verified using BFS state space exploration:")
    print("  + Mutual exclusion checked for all states")
    print("  + Deadlock freedom verified")
    print("  + Results match expected behavior")
    print("\nReady for next commit: Counter-example traces")
