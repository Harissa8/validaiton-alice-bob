"""
This module implements the Tower of Hanoi puzzle using the BFS
algorithm from Commit 1 to find optimal solutions.
"""

import sys
from pathlib import Path
# Add parent directory to import from 1-bfs
sys.path.insert(0, str(Path(__file__).parent.parent / "1-bfs"))

from bfs import BFS
from typing import Tuple, List


class HanoiState:
    """
    Represents a state in the Tower of Hanoi puzzle.
    
    A state consists of the configuration of disks on three pegs.
    Each peg is represented as a tuple of disk numbers (from top to bottom).
    Disk 1 is the smallest, disk n is the largest.
    """
    
    def __init__(self, pegs: Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]]):
        """
        Initialize a Hanoi state.
        
        Args:
            pegs: Tuple of 3 tuples, each representing a peg with disks
                 Example: ((1, 2, 3), (), ()) means all disks on peg 0
        """
        self.pegs = pegs
    
    def __eq__(self, other):
        """Check equality based on peg configuration"""
        if not isinstance(other, HanoiState):
            return False
        return self.pegs == other.pegs
    
    def __hash__(self):
        """Hash based on peg configuration for use in sets/dicts"""
        return hash(self.pegs)
    
    def __repr__(self):
        """String representation for debugging"""
        return f"HanoiState({self.pegs})"
    
    def to_string(self):
        """Pretty string representation"""
        return f"[{self.pegs[0]}|{self.pegs[1]}|{self.pegs[2]}]"
    
    def is_valid_move(self, from_peg: int, to_peg: int) -> bool:
        """
        Check if moving the top disk from from_peg to to_peg is valid.
        
        Rules:
        - Can only move one disk at a time (the top disk)
        - Cannot place a larger disk on a smaller disk
        
        Args:
            from_peg: Source peg (0, 1, or 2)
            to_peg: Destination peg (0, 1, or 2)
        
        Returns:
            True if move is valid, False otherwise
        """
        # Check peg indices are valid
        if not (0 <= from_peg < 3 and 0 <= to_peg < 3):
            return False
        
        # Cannot move from peg to itself
        if from_peg == to_peg:
            return False
        
        # Source peg must have at least one disk
        if not self.pegs[from_peg]:
            return False
        
        # If destination peg has disks, check size constraint
        if self.pegs[to_peg]:
            # Can only place smaller disk on larger disk
            if self.pegs[from_peg][0] > self.pegs[to_peg][0]:
                return False
        
        return True
    
    def make_move(self, from_peg: int, to_peg: int) -> 'HanoiState':
        """
        Create a new state after moving the top disk.
        
        Args:
            from_peg: Source peg
            to_peg: Destination peg
        
        Returns:
            New HanoiState after the move
        """
        # Create mutable copy of pegs
        new_pegs = [list(peg) for peg in self.pegs]
        
        # Move top disk from source to destination
        disk = new_pegs[from_peg].pop(0)
        new_pegs[to_peg].insert(0, disk)
        
        # Return new immutable state
        return HanoiState(tuple(tuple(peg) for peg in new_pegs))
    
    def get_successors(self) -> List['HanoiState']:
        """
        Get all valid successor states (all possible moves).
        
        Returns:
            List of HanoiState objects reachable in one move
        """
        successors = []
        
        # Try all possible moves (from each peg to each other peg)
        for from_peg in range(3):
            for to_peg in range(3):
                if self.is_valid_move(from_peg, to_peg):
                    successors.append(self.make_move(from_peg, to_peg))
        
        return successors
    
    def is_goal(self, goal_peg: int = 2) -> bool:
        """
        Check if this is a goal state.
        
        A goal state has all disks on the goal_peg and other pegs empty.
        
        Args:
            goal_peg: The peg where all disks should be (default: 2)
        
        Returns:
            True if this is a goal state
        """
        return (not self.pegs[(goal_peg + 1) % 3] and 
                not self.pegs[(goal_peg + 2) % 3])


class HanoiGame:
    """
    Tower of Hanoi game solver using BFS.
    
    This class uses the BFS algorithm to explore the state space
    and find the optimal solution.
    """
    
    def __init__(self, n_disks: int, start_peg: int = 0, goal_peg: int = 2):
        """
        Initialize a Hanoi game instance.
        
        Args:
            n_disks: Number of disks (1 or more)
            start_peg: Peg where all disks start (0, 1, or 2)
            goal_peg: Target peg where disks should end (0, 1, or 2)
        """
        self.n_disks = n_disks
        self.start_peg = start_peg
        self.goal_peg = goal_peg
        
        # Create initial state: all disks on start_peg
        pegs = [(), (), ()]
        pegs[start_peg] = tuple(range(1, n_disks + 1))
        self.initial_state = HanoiState(tuple(pegs))
        
        self.bfs = BFS()
    
    def solve(self):
        """
        Solve the Hanoi puzzle using BFS.
        
        Returns:
            Dictionary with:
            - total_states: Number of states explored
            - total_transitions: Number of transitions
            - solution_length: Number of moves in solution
            - theoretical_minimum: Theoretical minimum (2^n - 1)
            - path: List of states in the solution
        """
        # Explore state space using BFS
        stats = self.bfs.explore(
            self.initial_state,
            lambda state: state.get_successors()
        )
        
        # Find a goal state
        goal_state = None
        for state in self.bfs.visited:
            if state.is_goal(self.goal_peg):
                goal_state = state
                break
        
        # Get solution path
        if goal_state:
            path = self.bfs.get_path(self.initial_state, goal_state)
            solution_length = len(path) - 1  # Number of moves
        else:
            path = []
            solution_length = -1
        
        return {
            'total_states': stats['total_states'],
            'total_transitions': stats['total_transitions'],
            'solution_length': solution_length,
            'theoretical_minimum': 2**self.n_disks - 1,
            'path': path
        }
    
    def print_solution(self, result):
        """Print the solution in a formatted way"""
        print(f"\n{'='*70}")
        print(f"Tower of Hanoi - {self.n_disks} disks")
        print(f"{'='*70}")
        print(f"State Space Exploration:")
        print(f"  Total states: {result['total_states']}")
        print(f"  Total transitions: {result['total_transitions']}")
        
        print(f"\nSolution:")
        print(f"  Moves: {result['solution_length']}")
        print(f"  Theoretical minimum: {result['theoretical_minimum']}")
        
        optimal = result['solution_length'] == result['theoretical_minimum']
        status = "✓ OPTIMAL" if optimal else "✗ SUBOPTIMAL"
        print(f"  Status: {status}")
        
        if result['path'] and len(result['path']) <= 10:
            print(f"\nSolution path:")
            for i, state in enumerate(result['path']):
                print(f"  Step {i}: {state.to_string()}")
        elif result['path']:
            print(f"\nSolution path (first 8 steps):")
            for i, state in enumerate(result['path'][:8]):
                print(f"  Step {i}: {state.to_string()}")
            print(f"  ... ({len(result['path']) - 8} more steps)")


# =============================================================================
# TESTS TO VERIFY HANOI IMPLEMENTATION
# =============================================================================

def test_hanoi_2_disks():
    """Test 1: Hanoi with 2 disks"""
    print("="*70)
    print("TEST 1: Hanoi with 2 Disks")
    print("="*70)
    
    game = HanoiGame(n_disks=2)
    result = game.solve()
    
    print(f"\nStates explored: {result['total_states']}")
    print(f"Solution: {result['solution_length']} moves")
    print(f"Expected: {result['theoretical_minimum']} moves")
    print(f"Optimal: {'✓ Yes' if result['solution_length'] == 3 else '✗ No'}")
    
    assert result['solution_length'] == 3, "2 disks should take 3 moves"
    assert result['total_states'] == 9, "2 disks should have 9 states (3^2)"
    
    print("\n✓ Test passed!\n")
    return True


def test_hanoi_3_disks():
    """Test 2: Hanoi with 3 disks"""
    print("="*70)
    print("TEST 2: Hanoi with 3 Disks")
    print("="*70)
    
    game = HanoiGame(n_disks=3)
    result = game.solve()
    game.print_solution(result)
    
    assert result['solution_length'] == 7, "3 disks should take 7 moves"
    assert result['total_states'] == 27, "3 disks should have 27 states (3^3)"
    
    print("\n✓ Test passed!\n")
    return True


def test_hanoi_4_disks():
    """Test 3: Hanoi with 4 disks"""
    print("="*70)
    print("TEST 3: Hanoi with 4 Disks")
    print("="*70)
    
    game = HanoiGame(n_disks=4)
    result = game.solve()
    
    print(f"\nStates explored: {result['total_states']}")
    print(f"Solution: {result['solution_length']} moves")
    print(f"Expected: {result['theoretical_minimum']} moves")
    print(f"Optimal: {'✓ Yes' if result['solution_length'] == 15 else '✗ No'}")
    
    assert result['solution_length'] == 15, "4 disks should take 15 moves"
    assert result['total_states'] == 81, "4 disks should have 81 states (3^4)"
    
    print("\n✓ Test passed!\n")
    return True


def test_hanoi_state_growth():
    """Test 4: Verify state space growth formula"""
    print("="*70)
    print("TEST 4: State Space Growth Verification")
    print("="*70)
    
    print("\n| Disks | States | Expected (3^n) | Moves | Expected (2^n-1) | Status |")
    print("|"+ "-"*68 + "|")
    
    all_correct = True
    for n in range(2, 6):
        game = HanoiGame(n_disks=n)
        result = game.solve()
        
        expected_states = 3**n
        expected_moves = 2**n - 1
        
        states_match = result['total_states'] == expected_states
        moves_match = result['solution_length'] == expected_moves
        status = "✓" if states_match and moves_match else "✗"
        
        if not (states_match and moves_match):
            all_correct = False
        
        print(f"| {n:5} | {result['total_states']:6} | {expected_states:14} | "
              f"{result['solution_length']:5} | {expected_moves:16} | {status:6} |")
    
    assert all_correct, "All test cases should match expected values"
    
    print("\nGrowth patterns verified!\n")
    return True


def run_all_tests():
    """Run all Hanoi tests"""
    print("\n" + "#"*70)
    print("# COMMIT 2: HANOI GAME IMPLEMENTATION")
    print("# Question 2: Assurez vous que votre implementation Hanoi fonctionne")
    print("#"*70)
    print()
    
    tests = [
        ("2 Disks", test_hanoi_2_disks),
        ("3 Disks", test_hanoi_3_disks),
        ("4 Disks", test_hanoi_4_disks),
        ("State Growth", test_hanoi_state_growth)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{test_name} failed: {e}\n")
            results.append((test_name, False))
    
    # Print summary
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
    
    print("="*70)
    print(f"Total: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n ALL HANOI TESTS PASSED! ")
        print("\nHanoi Implementation Summary:")
        print("  + State representation correct")
        print("  ✓ Move validation working")
        print("  ✓ BFS finds optimal solutions")
        print("  ✓ State space matches 3^n formula")
        print("  ✓ Solution length matches 2^n-1 formula")
        print("  ✓ Ready for protocol implementation!")
    else:
        print(f"\n {total - passed} test(s) failed")
    
    print()
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
