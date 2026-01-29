# Verification Buchi - Alice & Bob

## Commande
```
cd 6-buchi-verification
python verify_buchi.py
```

## Resultats

| Model | P1 | P2 | P3 | P4 | P5 |
|-------|------|------|------|------|------|
| AB1 | FAIL | OK | OK | OK | OK |
| AB2 | OK | FAIL | FAIL | FAIL | FAIL |
| AB3 | OK | OK | FAIL | FAIL | FAIL |
| AB4 | OK | OK | OK | FAIL | FAIL |
| AB5 | OK | OK | OK | OK | OK |

- **OK** = propriete satisfaite (pas de cycle acceptant)
- **FAIL** = propriete violee (cycle acceptant trouve)

## Contre-exemples

### AB1 x P1 - Exclusion (never A.CS & B.CS)
```
Prefix trace:
  0: ('I', 'I') [buchi=1]
  1: ('CS', 'I') [buchi=1]
  2: ('CS', 'CS') [buchi=0]
  3: ('I', 'CS') [buchi=0]
  4: ('I', 'I') [buchi=0]
  5: ('CS', 'I') [buchi=0]
Cyclic suffix trace:
  0: ('CS', 'I') [buchi=0]
  1: ('I', 'I') [buchi=0]
  2: ('CS', 'I') [buchi=0] (loop)
```

### AB2 x P2 - No deadlock
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=1]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=1]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=1]
  3: ('CS', 'W', 'UP', 'UP') [buchi=1]
  4: ('I', 'W', 'DOWN', 'UP') [buchi=1]
  5: ('W', 'W', 'UP', 'UP') [buchi=1]
  6: ('W', 'W', 'UP', 'UP') [buchi=0]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [buchi=0]
  1: ('W', 'W', 'UP', 'UP') [buchi=0] (loop)
```

### AB2 x P3 - At least one in CS (liveness)
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=x]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=x]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=x]
  3: ('I', 'I', 'DOWN', 'DOWN') [buchi=y]
  4: ('W', 'I', 'UP', 'DOWN') [buchi=y]
  5: ('W', 'W', 'UP', 'UP') [buchi=y]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [buchi=y]
  1: ('W', 'W', 'UP', 'UP') [buchi=y] (loop)
```

### AB2 x P4 - If one wants in, it gets in
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=0]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=0]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=0]
  3: ('CS', 'W', 'UP', 'UP') [buchi=0]
  4: ('I', 'W', 'DOWN', 'UP') [buchi=0]
  5: ('W', 'W', 'UP', 'UP') [buchi=0]
  6: ('W', 'W', 'UP', 'UP') [buchi=1]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [buchi=1]
  1: ('W', 'W', 'UP', 'UP') [buchi=1] (loop)
```

### AB2 x P5 - Uncontested progress
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=0]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=0]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=0]
  3: ('CS', 'W', 'UP', 'UP') [buchi=0]
  4: ('I', 'W', 'DOWN', 'UP') [buchi=0]
  5: ('I', 'CS', 'DOWN', 'UP') [buchi=0]
  6: ('W', 'CS', 'UP', 'UP') [buchi=0]
  7: ('W', 'I', 'UP', 'DOWN') [buchi=1]
  8: ('W', 'W', 'UP', 'UP') [buchi=1]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [buchi=1]
  1: ('W', 'W', 'UP', 'UP') [buchi=1] (loop)
```

### AB3 x P3 - At least one in CS (liveness)
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=x]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=x]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=x]
  3: ('I', 'I', 'DOWN', 'DOWN') [buchi=y]
  4: ('W', 'I', 'UP', 'DOWN') [buchi=y]
  5: ('W', 'W', 'UP', 'UP') [buchi=y]
  6: ('W', 'W', 'UP', 'DOWN') [buchi=y]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'DOWN') [buchi=y]
  1: ('W', 'W', 'UP', 'UP') [buchi=y]
  2: ('W', 'W', 'UP', 'DOWN') [buchi=y] (loop)
```

### AB3 x P4 - If one wants in, it gets in
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=0]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=0]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=0]
  3: ('CS', 'W', 'UP', 'UP') [buchi=0]
  4: ('I', 'W', 'DOWN', 'UP') [buchi=0]
  5: ('W', 'W', 'UP', 'UP') [buchi=0]
  6: ('W', 'W', 'UP', 'DOWN') [buchi=0]
  7: ('CS', 'W', 'UP', 'DOWN') [buchi=0]
  8: ('I', 'W', 'DOWN', 'DOWN') [buchi=0]
  9: ('W', 'W', 'UP', 'DOWN') [buchi=1]
  10: ('W', 'W', 'UP', 'UP') [buchi=1]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [buchi=1]
  1: ('W', 'W', 'UP', 'DOWN') [buchi=1]
  2: ('W', 'W', 'UP', 'UP') [buchi=1] (loop)
```

### AB3 x P5 - Uncontested progress
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=0]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=0]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=0]
  3: ('CS', 'W', 'UP', 'UP') [buchi=0]
  4: ('I', 'W', 'DOWN', 'UP') [buchi=0]
  5: ('W', 'W', 'UP', 'UP') [buchi=0]
  6: ('W', 'W', 'UP', 'DOWN') [buchi=0]
  7: ('CS', 'W', 'UP', 'DOWN') [buchi=0]
  8: ('I', 'W', 'DOWN', 'DOWN') [buchi=0]
  9: ('I', 'W', 'DOWN', 'UP') [buchi=2]
  10: ('W', 'W', 'UP', 'UP') [buchi=2]
  11: ('W', 'W', 'UP', 'DOWN') [buchi=2]
  12: ('CS', 'W', 'UP', 'DOWN') [buchi=2]
  13: ('I', 'W', 'DOWN', 'DOWN') [buchi=2]
Cyclic suffix trace:
  0: ('I', 'W', 'DOWN', 'DOWN') [buchi=2]
  1: ('W', 'W', 'UP', 'DOWN') [buchi=2]
  2: ('CS', 'W', 'UP', 'DOWN') [buchi=2]
  3: ('I', 'W', 'DOWN', 'DOWN') [buchi=2] (loop)
```

### AB4 x P4 - If one wants in, it gets in
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=0]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=0]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=0]
  3: ('CS', 'W', 'UP', 'UP') [buchi=0]
  4: ('I', 'W', 'DOWN', 'UP') [buchi=0]
  5: ('W', 'W', 'UP', 'UP') [buchi=0]
  6: ('W', 'R', 'UP', 'DOWN') [buchi=0]
  7: ('CS', 'R', 'UP', 'DOWN') [buchi=0]
  8: ('I', 'R', 'DOWN', 'DOWN') [buchi=0]
  9: ('I', 'W', 'DOWN', 'UP') [buchi=2]
  10: ('W', 'W', 'UP', 'UP') [buchi=2]
  11: ('W', 'R', 'UP', 'DOWN') [buchi=2]
  12: ('CS', 'R', 'UP', 'DOWN') [buchi=2]
  13: ('I', 'R', 'DOWN', 'DOWN') [buchi=2]
Cyclic suffix trace:
  0: ('I', 'R', 'DOWN', 'DOWN') [buchi=2]
  1: ('W', 'R', 'UP', 'DOWN') [buchi=2]
  2: ('CS', 'R', 'UP', 'DOWN') [buchi=2]
  3: ('I', 'R', 'DOWN', 'DOWN') [buchi=2] (loop)
```

### AB4 x P5 - Uncontested progress
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [buchi=0]
  1: ('W', 'I', 'UP', 'DOWN') [buchi=0]
  2: ('CS', 'I', 'UP', 'DOWN') [buchi=0]
  3: ('CS', 'W', 'UP', 'UP') [buchi=0]
  4: ('I', 'W', 'DOWN', 'UP') [buchi=0]
  5: ('W', 'W', 'UP', 'UP') [buchi=0]
  6: ('W', 'R', 'UP', 'DOWN') [buchi=0]
  7: ('CS', 'R', 'UP', 'DOWN') [buchi=0]
  8: ('I', 'R', 'DOWN', 'DOWN') [buchi=0]
  9: ('I', 'W', 'DOWN', 'UP') [buchi=2]
  10: ('W', 'W', 'UP', 'UP') [buchi=2]
  11: ('W', 'R', 'UP', 'DOWN') [buchi=2]
  12: ('CS', 'R', 'UP', 'DOWN') [buchi=2]
  13: ('I', 'R', 'DOWN', 'DOWN') [buchi=2]
Cyclic suffix trace:
  0: ('I', 'R', 'DOWN', 'DOWN') [buchi=2]
  1: ('W', 'R', 'UP', 'DOWN') [buchi=2]
  2: ('CS', 'R', 'UP', 'DOWN') [buchi=2]
  3: ('I', 'R', 'DOWN', 'DOWN') [buchi=2] (loop)
```

## Analyse

### Differences entre les modeles

- **AB1**: Pas de mecanisme de protection. Alice et Bob peuvent entrer en CS simultanement.
- **AB2**: Utilise des drapeaux. Garantit l'exclusion mutuelle mais peut causer un deadlock (les deux en W avec drapeaux UP).
- **AB3**: Bob recule si le drapeau d'Alice est leve. Evite le deadlock mais Bob peut etre en famine (starvation).
- **AB4**: Bob se retire dans un etat R avant de reessayer. Similaire a AB3 avec un etat de repli explicite.
- **AB5**: Algorithme de Peterson avec variable `turn`. Garantit exclusion mutuelle, absence de deadlock, et equite.
