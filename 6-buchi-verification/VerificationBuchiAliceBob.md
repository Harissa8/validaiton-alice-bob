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
  0: ('I', 'I') [prop=1]
  1: ('CS', 'I') [prop=1]
  2: ('CS', 'CS') [prop=0]
Cyclic suffix trace:
  0: ('CS', 'CS') [prop=0]
  1: ('I', 'CS') [prop=0]
  2: ('CS', 'CS') [prop=0] (loop)
```

### AB2 x P2 - No deadlock
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=1]
  1: ('W', 'I', 'UP', 'DOWN') [prop=1]
  2: ('W', 'W', 'UP', 'UP') [prop=0]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [prop=0]
  1: ('W', 'W', 'UP', 'UP') [prop=0] (loop)
```

### AB2 x P3 - At least one in CS (liveness)
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=x]
  1: ('W', 'I', 'UP', 'DOWN') [prop=x]
  2: ('W', 'W', 'UP', 'UP') [prop=y]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [prop=y]
  1: ('W', 'W', 'UP', 'UP') [prop=y] (loop)
```

### AB2 x P4 - If one wants in, it gets in
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=0]
  1: ('W', 'I', 'UP', 'DOWN') [prop=0]
  2: ('W', 'W', 'UP', 'UP') [prop=1]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [prop=1]
  1: ('W', 'W', 'UP', 'UP') [prop=1] (loop)
```

### AB2 x P5 - Uncontested progress
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=0]
  1: ('W', 'I', 'UP', 'DOWN') [prop=1]
  2: ('W', 'W', 'UP', 'UP') [prop=1]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [prop=1]
  1: ('W', 'W', 'UP', 'UP') [prop=1] (loop)
```

### AB3 x P3 - At least one in CS (liveness)
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=x]
  1: ('W', 'I', 'UP', 'DOWN') [prop=x]
  2: ('W', 'W', 'UP', 'UP') [prop=y]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [prop=y]
  1: ('W', 'W', 'UP', 'DOWN') [prop=y]
  2: ('W', 'W', 'UP', 'UP') [prop=y] (loop)
```

### AB3 x P4 - If one wants in, it gets in
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=0]
  1: ('W', 'I', 'UP', 'DOWN') [prop=0]
  2: ('W', 'W', 'UP', 'UP') [prop=1]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [prop=1]
  1: ('W', 'W', 'UP', 'DOWN') [prop=1]
  2: ('W', 'W', 'UP', 'UP') [prop=1] (loop)
```

### AB3 x P5 - Uncontested progress
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=0]
  1: ('W', 'I', 'UP', 'DOWN') [prop=1]
  2: ('W', 'W', 'UP', 'UP') [prop=1]
Cyclic suffix trace:
  0: ('W', 'W', 'UP', 'UP') [prop=1]
  1: ('W', 'W', 'UP', 'DOWN') [prop=1]
  2: ('W', 'W', 'UP', 'UP') [prop=1] (loop)
```

### AB4 x P4 - If one wants in, it gets in
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=0]
  1: ('W', 'I', 'UP', 'DOWN') [prop=0]
  2: ('CS', 'I', 'UP', 'DOWN') [prop=0]
  3: ('CS', 'W', 'UP', 'UP') [prop=2]
  4: ('CS', 'R', 'UP', 'DOWN') [prop=2]
Cyclic suffix trace:
  0: ('CS', 'R', 'UP', 'DOWN') [prop=2]
  1: ('I', 'R', 'DOWN', 'DOWN') [prop=2]
  2: ('W', 'R', 'UP', 'DOWN') [prop=2]
  3: ('CS', 'R', 'UP', 'DOWN') [prop=2] (loop)
```

### AB4 x P5 - Uncontested progress
```
Prefix trace:
  0: ('I', 'I', 'DOWN', 'DOWN') [prop=0]
  1: ('I', 'W', 'DOWN', 'UP') [prop=2]
  2: ('W', 'W', 'UP', 'UP') [prop=2]
  3: ('W', 'R', 'UP', 'DOWN') [prop=2]
  4: ('CS', 'R', 'UP', 'DOWN') [prop=2]
Cyclic suffix trace:
  0: ('CS', 'R', 'UP', 'DOWN') [prop=2]
  1: ('I', 'R', 'DOWN', 'DOWN') [prop=2]
  2: ('W', 'R', 'UP', 'DOWN') [prop=2]
  3: ('CS', 'R', 'UP', 'DOWN') [prop=2] (loop)
```

## Analyse

### Differences entre les modeles

- **AB1**: Pas de mecanisme de protection. Alice et Bob peuvent entrer en CS simultanement.
- **AB2**: Utilise des drapeaux. Garantit l'exclusion mutuelle mais peut causer un deadlock (les deux en W avec drapeaux UP).
- **AB3**: Bob recule si le drapeau d'Alice est leve. Evite le deadlock mais Bob peut etre en famine (starvation).
- **AB4**: Bob se retire dans un etat R avant de reessayer. Similaire a AB3 avec un etat de repli explicite.
- **AB5**: Algorithme de Peterson avec variable `turn`. Garantit exclusion mutuelle, absence de deadlock, et equite.
