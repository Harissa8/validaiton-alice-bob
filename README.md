# Alice & Bob Mutual Exclusion Protocols
## Complete Implementation with BFS, Soup DSL & Buchi Verification

**Course:** Formal Verification / Concurrent Systems
**Institution:** ENSTA Bretagne
**Student:** Harissa
**Date:** January 2026

---

## Project Structure

```
validaiton-alice-bob/
├── common/                          # Shared abstractions
│   ├── languagesemantics.py         # Abstract LanguageSemantics interface
│   ├── rootedgraph.py               # Abstract RootedGraph interface
│   ├── souplanguagesemantics.py     # Soup DSL (Piece, Soup, SoupLanguageSemantics)
│   ├── isoup.py                     # iSoup: properties as LanguageSemantics (P1-P5)
│   ├── step_sync_composition.py     # Step Synchronous Composition (system x property)
│   ├── ls2rg.py                     # LS2RG adapter (LanguageSemantics -> RootedGraph)
│   ├── bfs.py                       # BFS for RootedGraph (breadth_first_search)
│   └── buchi.py                     # Buchi cycle detection + counter-examples
├── 1-bfs/
│   └── bfs.py                       # Original BFS class
├── 2-hanoi/
│   ├── hanoi.py                     # Hanoi using BFS
│   ├── hanoilanguagesemantics.py    # Hanoi using LanguageSemantics
│   └── validation_ls.py
├── 3-protocols/
│   ├── protocols.py                 # AB1-AB3 as RootedGraph (original)
│   └── ab_models_soup.py            # AB1-AB5 using Soup DSL
├── 4-verification/
│   └── verification.py              # Simple reachability verification
├── 5-counter_examples/
│   └── counter_examples.py          # Linear counter-examples
├── 6-buchi-verification/
│   ├── verify_buchi.py              # Buchi verification runner (25 pairs)
│   └── VerificationBuchiAliceBob.md # Results documentation
└── README.md
```

---

## Architecture

```
Soup Sem (system AB1-AB5)  ──┐
                              ├── (X) StepSyncComposition ── LS2RG ── BFS ── OK / contre-example
iSoup Sem (property P1-P5) ──┘
```

### Components

| Component | File | Role |
|-----------|------|------|
| **LanguageSemantics** | `common/languagesemantics.py` | Abstract interface: `initials()`, `actions()`, `execute()` |
| **Soup DSL** | `common/souplanguagesemantics.py` | `Piece` (guard/effect) + `Soup` (pieces + init) |
| **iSoup** | `common/isoup.py` | Properties as LanguageSemantics (Buchi automata) |
| **StepSyncComposition** | `common/step_sync_composition.py` | Synchronous product: system x property |
| **LS2RG** | `common/ls2rg.py` | Adapter: LanguageSemantics -> RootedGraph |
| **BFS** | `common/bfs.py` | `breadth_first_search(rooted_graph, on_entry, opaque)` |
| **Buchi** | `common/buchi.py` | Cycle detection on composed state space |

---

## Questions 1-5 (Original)

### Q1: BFS Implementation
```bash
cd 1-bfs && python bfs.py
```

### Q2: Hanoi
```bash
cd 2-hanoi && python hanoi.py
```

### Q3: Protocol Encoding (AB1-AB3 as RootedGraph)
```bash
cd 3-protocols && python protocols.py
```

### Q4: Verification (Mutual Exclusion + Deadlock)
```bash
cd 4-verification && python verification.py
```

### Q5: Counter-Examples
```bash
cd 5-counter_examples && python counter_examples.py
```

---

## Buchi Verification (AB1-AB5 x P1-P5)

### Models (Soup DSL)

| Model | Description | Initial State |
|-------|-------------|---------------|
| AB1 | No protection (I <-> CS) | `(I, I)` |
| AB2 | Flags with waiting | `(I, I, DOWN, DOWN)` |
| AB3 | Bob backs off if Alice's flag UP | `(I, I, DOWN, DOWN)` |
| AB4 | Bob retreats to R state | `(I, I, DOWN, DOWN)` |
| AB5 | Peterson's algorithm (turn variable) | `(I, I, DOWN, DOWN, Alice)` |

### Properties (iSoup / Buchi)

| Property | Description | Accepting = bad when... |
|----------|-------------|------------------------|
| P1 | Exclusion | Both Alice & Bob in CS |
| P2 | No deadlock | System has no actions |
| P3 | At least one in CS | Nobody ever enters CS |
| P4 | If one wants in, gets in | Flag UP but never CS |
| P5 | Uncontested progress | Waiting alone, never CS |

### Run
```bash
cd 6-buchi-verification
python verify_buchi.py
```

### Results

| Model | P1 | P2 | P3 | P4 | P5 |
|-------|------|------|------|------|------|
| AB1 | FAIL | OK | OK | OK | OK |
| AB2 | OK | FAIL | FAIL | FAIL | FAIL |
| AB3 | OK | OK | FAIL | FAIL | FAIL |
| AB4 | OK | OK | OK | FAIL | FAIL |
| AB5 | OK | OK | OK | OK | OK |

- **OK** = property satisfied (no accepting cycle)
- **FAIL** = property violated (accepting cycle found, counter-example produced)

### Analysis

- **AB1**: No protection. Both can enter CS simultaneously.
- **AB2**: Flags guarantee exclusion but cause deadlock (both W with flags UP).
- **AB3**: Bob backs off to avoid deadlock, but starvation possible (Bob never gets CS).
- **AB4**: Bob retreats to R state. Better but still unfair to Bob.
- **AB5**: Peterson's algorithm. Satisfies ALL properties (exclusion, deadlock-free, fair).

Counter-examples are in `(prefix-trace, cyclic-suffix-trace)` form.
See `6-buchi-verification/VerificationBuchiAliceBob.md` for full details.
