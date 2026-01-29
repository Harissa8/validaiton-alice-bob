# Alice & Bob Mutual Exclusion Protocols
## Complete Implementation with BFS State Space Exploration

**Course:** Formal Verification / Concurrent Systems  
**Institution:** ENSTA Bretagne  
**Student:** Harissa  
**Date:** January 2026  

---

## 📋 Project Overview

This project implements and verifies three mutual exclusion protocols (AB1, AB2, AB3) using Breadth-First Search (BFS) for state space exploration. The project is organized into 5 commits, each answering one question from the assignment.

---

## 🎯 Project Structure

```
alice_bob_FINAL/
├── 1-bfs/                    
│   └── bfs.py
├── 2-hanoi/                  
│   └── hanoi.py
├── 3-protocols/              
│   └── protocols.py
├── 4-verification/          
│   └── verification.py
├── 5-counter_examples/      
│   └── counter_examples.py
└── README.md                 # This file
```

---

## 📚 Detailed Documentation

### Question 1: Assurez vous que votre implementation BFS fonctionne

**Folder:** `1-bfs/`  
**File:** `bfs.py`  

**Implementation:**
```python
class BFS:
    def explore(initial_state, get_successors_func)
    def get_path(start, end)
```

**Features:**
- Generic BFS works with any state type
- Queue-based traversal
- Maintains visited set to avoid cycles
- Builds complete state graph
- Parent pointer tracking for path reconstruction

**Tests:**
1. Simple acyclic graph (4 states)
2. Cyclic graph (handles cycles correctly)
3. Complex graph with multiple paths (finds shortest)
4. Disconnected components (handles unreachable states)

**Run:**
```bash
cd 1-bfs
python bfs.py
```

**Expected Output:** + ALL BFS TESTS PASSED! (4/4)

---

### Question 2: Assurez vous que votre implementation Hanoi fonctionne

**Folder:** `2-hanoi/`  
**File:** `hanoi.py`  

**Implementation:**
```python
class HanoiState:
    def __init__(self, pegs)
    def is_valid_move(from_peg, to_peg)
    def make_move(from_peg, to_peg)
    def get_successors()
    def is_goal(goal_peg)

class HanoiGame:
    def __init__(self, n_disks)
    def solve()  # Uses BFS from Commit 1
```

**Features:**
- Immutable state representation
- Move validation (smaller on larger)
- Uses BFS to find optimal solution
- Complete state space exploration

**Test Results:**

| Disks | States | Expected (3^n) | Moves | Expected (2^n-1) | Status |
|-------|--------|----------------|-------|------------------|--------|
| 2     | 9      | 9              | 3     | 3                | +      |
| 3     | 27     | 27             | 7     | 7                | +      |
| 4     | 81     | 81             | 15    | 15               | +      |
| 5     | 243    | 243            | 31    | 31               | +      |

**Run:**
```bash
cd 2-hanoi
python hanoi.py
```

**Expected Output:** + ALL HANOI TESTS PASSED! (4/4)

---

### Question 3: Encoder AB1, AB2, AB3 avec RootedGraph abstraction

**Folder:** `3-protocols/`  
**File:** `protocols.py`  

**Implementation:**
```python
class State:
    # Alice/Bob locations and flags
    
class RootedGraph:
    # Base class for protocols
    def get_successors(state)
    
class ProtocolAB1(RootedGraph):
    # Simple flag protocol
    
class ProtocolAB2(RootedGraph):
    # Flag with waiting
    
class ProtocolAB3(RootedGraph):
    # Polite protocol
```

**Protocol Details:**

**AB1 - Simple Flag Protocol:**
- States: 4
- Transitions: 8
- Logic: Raise flag when entering CS
- Problem: No coordination between processes

**AB2 - Flag with Waiting:**
- States: 8
- Transitions: 12
- Logic: Raise flag, then wait if other's flag is up
- Problem: Can deadlock if both raise flags simultaneously

**AB3 - Polite Protocol:**
- States: 14
- Transitions: 28
- Logic: Raise flag, if conflict then lower and retry
- Result: Safe and deadlock-free +

**Run:**
```bash
cd 3-protocols
python protocols.py
```

**Expected Output:** + ALL PROTOCOLS ENCODED AS ROOTED GRAPHS!

---

### Question 4: Verifier l'exclusion et deadlock pour chaque AB

**Folder:** `4-verification/`  
**File:** `verification.py`  

**Implementation:**
```python
class PropertyVerifier:
    def verify_mutual_exclusion()
    def verify_deadlock_freedom()
    def verify_all_properties()
```

**Verification Results:**

| Protocol | States | Mutual Exclusion | Deadlock Free | Status |
|----------|--------|------------------|---------------|--------|
| AB1      | 4      | ✗ VIOLATED       | + YES         | ❌ Unsafe |
| AB2      | 8      | + SATISFIED      | ✗ NO          | ⚠️ Can deadlock |
| AB3      | 14     | + SATISFIED      | + YES         | ✅ CORRECT |

**Explanation:**
- **AB1:** Both processes can enter CS simultaneously → Unsafe
- **AB2:** Both processes can be stuck waiting → Deadlock
- **AB3:** Properly coordinates access, no deadlock → Correct!

**Run:**
```bash
cd 4-verification
python verification.py
```

**Expected Output:** + ALL PROPERTY VERIFICATIONS COMPLETE!

---

### Question 5: Sans modifier BFS, construiser une trace de contre example

**Folder:** `5-counter_examples/`  
**File:** `counter_examples.py`  

**Implementation:**
```python
class CounterExampleGenerator:
    def generate_trace_to_state(target)
    def generate_mutual_exclusion_counter_example()
    def generate_deadlock_counter_example()
```

**Key Feature:** Uses ONLY existing BFS methods - NO modification!
- Uses `BFS.get_path()` for trace reconstruction
- Uses `BFS.visited` for reachability checking
- BFS implementation remains unchanged

**Counter-Examples Generated:**

**AB1 - Mutual Exclusion Violation (2 steps):**
```
Step 0: State(A:I, B:I, fA:DOWN, fB:DOWN)
  ↓ Alice enters CS
Step 1: State(A:CS, B:I, fA:UP, fB:DOWN)
  ↓ Bob enters CS (violation!)
Step 2: State(A:CS, B:CS, fA:UP, fB:UP) ⚠️ BOTH IN CS!
```

**AB2 - Deadlock (2 steps):**
```
Step 0: State(A:I, B:I, fA:DOWN, fB:DOWN)
  ↓ Alice raises flag and waits
Step 1: State(A:W, B:I, fA:UP, fB:DOWN)
  ↓ Bob raises flag and waits
Step 2: State(A:W, B:W, fA:UP, fB:UP) ⚠️ DEADLOCK!
```

**AB3 - No Violations:**
- + No mutual exclusion violations
- + No deadlock states
- + Protocol is correct!

**Run:**
```bash
cd 5-counter_examples
python counter_examples.py
```

**Expected Output:** + ALL COUNTER-EXAMPLES GENERATED!

---

## 🚀 How to Run Everything

### Test Each Question Individually:

```bash
# Question 1: BFS
cd 1-bfs && python bfs.py && cd ..

# Question 2: Hanoi
cd 2-hanoi && python hanoi.py && cd ..

# Question 3: Protocols
cd 3-protocols && python protocols.py && cd ..

# Question 4: Verification
cd 4-verification && python verification.py && cd ..

# Question 5: Counter-Examples
cd 5-counter_examples && python counter_examples.py && cd ..
```

### Or Run All at Once:

```bash
for dir in 1-bfs 2-hanoi 3-protocols 4-verification 5-counter_examples; do
    echo "========== Testing $dir =========="
    cd $dir && python *.py | tail -20
    cd ..
    echo ""
done
```

---

## 📊 Complete Results Summary

### ✅ All Tests Passing

| Question | Component | Tests | Status |
|----------|-----------|-------|--------|
| Q1 | BFS Implementation | 4/4 | ✅ PASS |
| Q2 | Hanoi Game | 4/4 | ✅ PASS |
| Q3 | Protocol Encoding | 3/3 | ✅ PASS |
| Q4 | Property Verification | 3/3 | ✅ PASS |
| Q5 | Counter-Examples | 3/3 | ✅ PASS |

**Total:** 17/17 tests passing ✅

### Protocol Comparison

| Protocol | Description | M. Exclusion | Deadlock Free | Conclusion |
|----------|-------------|--------------|---------------|------------|
| AB1 | Simple flag | ✗ | + | Unsafe |
| AB2 | Flag + wait | + | ✗ | Can deadlock |
| AB3 | Polite | + | + | ✅ Correct |