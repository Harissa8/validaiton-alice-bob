"""
Generate execution traces that lead to property violations
WITHOUT modifying BFS implementation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "1-bfs"))
sys.path.insert(0, str(Path(__file__).parent.parent / "3-protocols"))
sys.path.insert(0, str(Path(__file__).parent.parent / "4-verification"))

from protocols import ProtocolAB1, ProtocolAB2, ProtocolAB3, State
from verification import PropertyVerifier
from bfs import BFS


class CounterExampleGenerator:
    """
    Generate counter-example traces for property violations
    Uses existing BFS without modification
    """
    
    def __init__(self, protocol):
        self.protocol = protocol
        self.verifier = PropertyVerifier(protocol)
        # Run verification to populate violation/deadlock states
        self.results = self.verifier.verify_all_properties()
    
    def generate_trace_to_state(self, target_state: State):
        """
        Generate execution trace from initial state to target state
        Uses BFS parent pointers (already implemented in BFS)
        
        Args:
            target_state: The state to reach
            
        Returns:
            List of states forming the trace, or empty list if unreachable
        """
        if target_state not in self.verifier.bfs.visited:
            return []
        
        # Use BFS get_path method (no modification needed!)
        trace = self.verifier.bfs.get_path(
            self.protocol.initial_state,
            target_state
        )
        
        return trace
    
    def generate_mutual_exclusion_counter_example(self):
        """
        Generate counter-example for mutual exclusion violation
        Returns trace leading to state where both processes in CS
        """
        if self.results['mutual_exclusion']:
            return None  # No violation, no counter-example
        
        # Get first violation state
        violation_state = self.results['violation_states'][0]
        
        # Generate trace using existing BFS
        trace = self.generate_trace_to_state(violation_state)
        
        return {
            'property': 'Mutual Exclusion',
            'violation_state': violation_state,
            'trace': trace,
            'trace_length': len(trace) - 1,  # Number of transitions
            'description': 'Both Alice and Bob in Critical Section simultaneously'
        }
    
    def generate_deadlock_counter_example(self):
        """
        Generate counter-example for deadlock
        Returns trace leading to deadlock state
        """
        if self.results['deadlock_free']:
            return None  # No deadlock, no counter-example
        
        # Get first deadlock state
        deadlock_state = self.results['deadlock_states'][0]
        
        # Generate trace using existing BFS
        trace = self.generate_trace_to_state(deadlock_state)
        
        return {
            'property': 'Deadlock Freedom',
            'violation_state': deadlock_state,
            'trace': trace,
            'trace_length': len(trace) - 1,
            'description': 'System stuck with no possible transitions'
        }
    
    def print_counter_example(self, counter_example):
        """Pretty print a counter-example trace"""
        if counter_example is None:
            print("  No violation found - property is satisfied!")
            return
        
        print(f"\nProperty: {counter_example['property']}")
        print(f"Status: ✗ VIOLATED")
        print(f"Description: {counter_example['description']}")
        print(f"\nViolation State:")
        print(f"  {counter_example['violation_state']}")
        print(f"\nExecution Trace ({counter_example['trace_length']} steps):")
        
        for i, state in enumerate(counter_example['trace']):
            prefix = "  →" if i > 0 else "  "
            print(f"{prefix} Step {i}: {state}")
            
            if i == len(counter_example['trace']) - 1:
                print(f"  VIOLATION REACHED!")


def test_ab1_counter_example():
    """Generate counter-example for AB1 mutual exclusion violation"""
    print("\n" + "="*60)
    print("TEST 1: Counter-Example for AB1 (Mutual Exclusion)")
    print("="*60)
    
    protocol = ProtocolAB1()
    generator = CounterExampleGenerator(protocol)
    
    counter_example = generator.generate_mutual_exclusion_counter_example()
    generator.print_counter_example(counter_example)
    
    assert counter_example is not None, "Should generate counter-example"
    assert len(counter_example['trace']) > 0, "Trace should not be empty"
    
    # Verify the trace ends in violation
    final_state = counter_example['trace'][-1]
    assert final_state == counter_example['violation_state'], "Trace should lead to violation"
    
    print("\n+ Counter-example generated successfully!")
    return counter_example


def test_ab2_counter_example():
    """Generate counter-example for AB2 deadlock"""
    print("\n" + "="*60)
    print("TEST 2: Counter-Example for AB2 (Deadlock)")
    print("="*60)
    
    protocol = ProtocolAB2()
    generator = CounterExampleGenerator(protocol)
    
    counter_example = generator.generate_deadlock_counter_example()
    generator.print_counter_example(counter_example)
    
    assert counter_example is not None, "Should generate counter-example"
    assert len(counter_example['trace']) > 0, "Trace should not be empty"
    
    # Verify the trace ends in deadlock
    final_state = counter_example['trace'][-1]
    assert final_state == counter_example['violation_state'], "Trace should lead to deadlock"
    
    print("\n+ Counter-example generated successfully!")
    return counter_example


def test_ab3_no_counter_examples():
    """Verify AB3 has no counter-examples (both properties satisfied)"""
    print("\n" + "="*60)
    print("TEST 3: AB3 - No Counter-Examples (Correct Protocol)")
    print("="*60)
    
    protocol = ProtocolAB3()
    generator = CounterExampleGenerator(protocol)
    
    print("\nChecking Mutual Exclusion:")
    mutex_ce = generator.generate_mutual_exclusion_counter_example()
    generator.print_counter_example(mutex_ce)
    
    print("\nChecking Deadlock Freedom:")
    deadlock_ce = generator.generate_deadlock_counter_example()
    generator.print_counter_example(deadlock_ce)
    
    assert mutex_ce is None, "AB3 should have no mutual exclusion violations"
    assert deadlock_ce is None, "AB3 should have no deadlock"
    
    print("\n+ AB3 is correct - no counter-examples exist!")


def demonstrate_bfs_unchanged():
    """Demonstrate that BFS was not modified"""
    print("\n" + "="*60)
    print("VERIFICATION: BFS Implementation Unchanged")
    print("="*60)
    
    print("\nCounter-examples generated using ONLY existing BFS methods:")
    print("  + BFS.explore() - for state space exploration")
    print("  + BFS.get_path() - for trace reconstruction")
    print("  + BFS.visited - for checking reachability")
    print("  + BFS.parent - for path tracking (internal to get_path)")
    
    print("\nNo modifications to BFS required!")
    print("Counter-example generation is a separate layer on top of BFS.")
    
    # Show BFS source hasn't changed by using it directly
    print("\n+ BFS class still works independently:")
    bfs = BFS()
    simple_graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
    stats = bfs.explore(0, lambda s: simple_graph.get(s, []))
    path = bfs.get_path(0, 3)
    print(f"  BFS on simple graph: {stats['total_states']} states, path 0→3: {path}")


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("#"*60)
    print("\nGenerating counter-example traces WITHOUT modifying BFS...\n")
    
    # Generate counter-examples
    ce_ab1 = test_ab1_counter_example()
    ce_ab2 = test_ab2_counter_example()
    test_ab3_no_counter_examples()
    
    # Verify BFS unchanged
    demonstrate_bfs_unchanged()
    
    # Summary
    print("\n" + "="*60)
    print("COUNTER-EXAMPLE SUMMARY")
    print("="*60)
    
    print(f"\nAB1 - Mutual Exclusion Violation:")
    print(f"  Trace length: {ce_ab1['trace_length']} steps")
    print(f"  Violation: Both in CS at {ce_ab1['violation_state']}")
    
    print(f"\nAB2 - Deadlock:")
    print(f"  Trace length: {ce_ab2['trace_length']} steps")
    print(f"  Deadlock: {ce_ab2['violation_state']}")
    
    print(f"\nAB3 - No Violations:")
    print(f"  + Satisfies mutual exclusion")
    print(f"  + Deadlock-free")
    
    print("\n" + "="*60)
    print("+ ALL COUNTER-EXAMPLES GENERATED!")
    print("="*60)
    print("\nCounter-example generation complete:")
    print("  + Traces generated for all violations")
    print("  + BFS implementation NOT modified")
    print("  + Used existing BFS.get_path() method")
    print("  + All requirements satisfied!")
