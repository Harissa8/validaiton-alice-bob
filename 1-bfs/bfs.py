"""
This module implements a generic Breadth-First Search algorithm
that can be used for state space exploration.
"""

from collections import deque
from typing import Set, List, Dict, Any


class BFS:
    """
    Breadth-First Search implementation for exploring state spaces.
    
    This is a generic implementation that works with any state type.
    It tracks visited states, builds a graph, and maintains parent pointers
    for path reconstruction.
    """
    
    def __init__(self):
        """Initialize BFS data structures"""
        self.visited: Set[Any] = set()
        self.graph: Dict[Any, List[Any]] = {}
        self.parent: Dict[Any, Any] = {}
    
    def explore(self, initial_state, get_successors_func):
        """
        Explore state space starting from initial_state using BFS.
        
        Args:
            initial_state: The starting state for exploration
            get_successors_func: Function that takes a state and returns 
                               list of successor states
        
        Returns:
            Dictionary with exploration statistics:
            - total_states: Number of states visited
            - total_transitions: Number of edges in the graph
        """
        queue = deque([initial_state])
        self.visited.add(initial_state)
        self.parent[initial_state] = None
        self.graph[initial_state] = []
        
        while queue:
            current = queue.popleft()
            
            # Get successors using provided function
            successors = get_successors_func(current)
            self.graph[current] = successors
            
            # Process each successor
            for successor in successors:
                if successor not in self.visited:
                    self.visited.add(successor)
                    self.parent[successor] = current
                    queue.append(successor)
        
        return {
            'total_states': len(self.visited),
            'total_transitions': sum(len(v) for v in self.graph.values())
        }
    
    def get_path(self, start, end):
        """
        Reconstruct path from start to end using parent pointers.
        
        Args:
            start: Starting state
            end: Target state
        
        Returns:
            List of states forming the path from start to end,
            or empty list if no path exists
        """
        if end not in self.visited:
            return []
        
        path = []
        current = end
        
        # Backtrack from end to start using parent pointers
        while current is not None:
            path.append(current)
            current = self.parent.get(current)
        
        # Reverse to get path from start to end
        path.reverse()
        
        # Verify the path starts at the correct state
        return path if path and path[0] == start else []


# =============================================================================
# TESTS TO VERIFY BFS IMPLEMENTATION
# =============================================================================

def test_simple_graph():
    """Test 1: Simple acyclic graph"""
    print("=" * 70)
    print("TEST 1: Simple Acyclic Graph")
    print("=" * 70)
    
    # Define a simple graph
    # Structure: 0 -> [1, 2], 1 -> [3], 2 -> [3], 3 -> []
    graph = {
        0: [1, 2],
        1: [3],
        2: [3],
        3: []
    }
    
    def get_successors(state):
        return graph.get(state, [])
    
    # Run BFS
    bfs = BFS()
    stats = bfs.explore(0, get_successors)
    
    # Display results
    print(f"\nGraph structure: {graph}")
    print(f"Starting from state: 0")
    print(f"States visited: {sorted(bfs.visited)}")
    print(f"Total states: {stats['total_states']}")
    print(f"Total transitions: {stats['total_transitions']}")
    
    # Test path finding
    path = bfs.get_path(0, 3)
    print(f"\nShortest path from 0 to 3: {path}")
    print(f"Path length: {len(path) - 1} steps")
    
    # Verify correctness
    assert stats['total_states'] == 4, "Should visit 4 states"
    assert len(path) > 0, "Should find path from 0 to 3"
    assert path[0] == 0 and path[-1] == 3, "Path should start at 0 and end at 3"
    
    print("\n✓ Test passed!\n")
    return True


def test_cyclic_graph():
    """Test 2: Graph with cycles"""
    print("=" * 70)
    print("TEST 2: Cyclic Graph")
    print("=" * 70)
    
    # Graph with cycle: 2 points back to 0
    graph = {
        0: [1],
        1: [2],
        2: [0, 3],  # Creates cycle back to 0
        3: []
    }
    
    def get_successors(state):
        return graph.get(state, [])
    
    # Run BFS
    bfs = BFS()
    stats = bfs.explore(0, get_successors)
    
    # Display results
    print(f"\nGraph with cycle: {graph}")
    print(f"Starting from state: 0")
    print(f"States visited: {sorted(bfs.visited)}")
    print(f"Total states: {stats['total_states']}")
    
    # Verify BFS handles cycles correctly
    assert stats['total_states'] == 4, "Should visit 4 states despite cycle"
    assert 0 in bfs.visited and 1 in bfs.visited, "Should visit all reachable states"
    
    print("\n✓ Test passed - BFS handles cycles correctly!\n")
    return True


def test_complex_graph():
    """Test 3: More complex graph with multiple paths"""
    print("=" * 70)
    print("TEST 3: Complex Graph with Multiple Paths")
    print("=" * 70)
    
    # More complex graph structure
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': ['G'],
        'E': ['G'],
        'F': ['G'],
        'G': []
    }
    
    def get_successors(state):
        return graph.get(state, [])
    
    # Run BFS
    bfs = BFS()
    stats = bfs.explore('A', get_successors)
    
    # Display results
    print(f"\nStates visited: {sorted(bfs.visited)}")
    print(f"Total states: {stats['total_states']}")
    print(f"Total transitions: {stats['total_transitions']}")
    
    # Test shortest path
    path_to_g = bfs.get_path('A', 'G')
    print(f"\nShortest path A -> G: {path_to_g}")
    print(f"Path length: {len(path_to_g) - 1} steps")
    
    # Test multiple paths exist but BFS finds shortest
    path_to_d = bfs.get_path('A', 'D')
    path_to_f = bfs.get_path('A', 'F')
    print(f"Path A -> D: {path_to_d}")
    print(f"Path A -> F: {path_to_f}")
    
    # Verify correctness
    assert stats['total_states'] == 7, "Should visit 7 states"
    assert len(path_to_g) == 4, "Shortest path A->G should be 4 nodes (A->B->D->G)"
    
    print("\n✓ Test passed!\n")
    return True


def test_disconnected_nodes():
    """Test 4: Graph with unreachable nodes"""
    print("=" * 70)
    print("TEST 4: Graph with Unreachable Nodes")
    print("=" * 70)
    
    # Graph with disconnected component
    graph = {
        0: [1, 2],
        1: [],
        2: [],
        5: [6],  # Disconnected component - not reachable from 0
        6: []
    }
    
    def get_successors(state):
        return graph.get(state, [])
    
    # Run BFS starting from 0
    bfs = BFS()
    stats = bfs.explore(0, get_successors)
    
    # Display results
    print(f"\nStarting from state: 0")
    print(f"States visited: {sorted(bfs.visited)}")
    print(f"States NOT visited: [5, 6] (disconnected)")
    
    # Try to get path to unreachable node
    path = bfs.get_path(0, 5)
    print(f"\nPath to unreachable node 5: {path}")
    print("(Empty list indicates no path exists)")
    
    # Verify correctness
    assert 5 not in bfs.visited, "Node 5 should not be visited"
    assert 6 not in bfs.visited, "Node 6 should not be visited"
    assert len(path) == 0, "No path should exist to unreachable node"
    
    print("\n✓ Test passed - correctly handles unreachable nodes!\n")
    return True


def run_all_tests():
    """Run all BFS tests"""
    print("\n" + "#" * 70)
    print("# COMMIT 1: BFS IMPLEMENTATION VERIFICATION")
    print("# Question 1: Assurez vous que votre implementation BFS fonctionne")
    print("#" * 70)
    print()
    
    tests = [
        ("Simple Acyclic Graph", test_simple_graph),
        ("Cyclic Graph", test_cyclic_graph),
        ("Complex Graph", test_complex_graph),
        ("Disconnected Nodes", test_disconnected_nodes)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed: {e}\n")
            results.append((test_name, False))
    
    # Print summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 70)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 70)
    
    if passed == total:
        print("\n ALL BFS TESTS PASSED! ")
        print("\nBFS Implementation Summary:")
        print("  ✓ Explores state space correctly")
        print("  ✓ Handles cycles properly")
        print("  ✓ Finds shortest paths")
        print("  ✓ Handles disconnected components")
        print("  ✓ Ready to use for Hanoi and Protocols!")
    else:
        print(f"\n {total - passed} test(s) failed")
    
    print()
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
