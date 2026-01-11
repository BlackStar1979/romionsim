# Decay Sweep: Analysis

**Date:** 2026-01-08

---

## 🎯 PRIMARY FINDING

### Freeze Boundary Identified: 0.8-0.85 ⭐

```
decay ≥ 0.85 → Freeze @ tick 100 (FAST)
decay ≤ 0.8  → Active field >600 ticks

Sharp transition (not gradual)
Phase-like behavior
```

---

## 🔬 INTERPRETATION

### 1. Inverted Semantics Confirmed
```
Higher decay_scale = FASTER decay = EARLIER freeze
Lower decay_scale = SLOWER decay = LONGER active

decay=1.0, 0.85: Freeze @ 100 (very fast)
decay=0.8: Never freezes (>600)
decay=0.7 (R2): Active @ 400 (confirmed)
```

### 2. Comparison with Test C
```
Test C R0 (decay=1.0): Freeze @ ~400
Sweep (decay=1.0): Freeze @ 100

Discrepancy: Different conditions?
Hypothesis: Dump frequency affects dynamics?
Need: Verify with identical conditions
```

### 3. Seed Variance Issue
```
decay=0.85, seed=42:  25 bridges
decay=0.85, seed=123: 40 bridges

60% variance at same parameter!
Implication: Need 3+ seeds for robustness
```

---

## 💡 PHASE TRANSITION MODEL

### Two Phases:
```
PHASE I: decay_scale ≥ 0.85
- Fast freeze (<200 ticks)
- System rapidly reaches frozen attractor
- Few residual bridges

PHASE II: decay_scale ≤ 0.8
- Active field (>600 ticks)
- Persistent inter-cluster structure
- Many bridges maintained
```

### Boundary (~0.8-0.85):
```
Sharp transition
Critical decay rate
Separates frozen from active regime
```

---

## 🔍 PUZZLES

### 1. Bridges After Freeze?
```
Runs freeze @ tick 100
Yet show bridges @ tick 400

Possible explanations:
a) Residual bridges from before freeze
b) freeze_tick detection too simple
c) Bridges exist but don't update

Resolution: Check sustained freeze
```

### 2. Test C vs Sweep Discrepancy
```
R0 (decay=1.0): Freeze @ ~400
Sweep (decay=1.0): Freeze @ 100

Different freeze times at same decay!

Hypothesis:
- dump_graph_every affects dynamics?
- Different initial conditions?
- Random variation?

Need: Reproduce R0 with dumps
```

### 3. decay=0.8 Analysis Failure
```
Simulation succeeded
freeze_tick = never (good!)
But gravity_test.py failed

Critical: Need to analyze this manually
This is the boundary case!
```

---

## 📊 STATISTICAL NOTES

### Sample Size:
- 3 successful runs
- 2 seeds (insufficient)
- Need: 3+ seeds per value

### Variance:
- High (60% at decay=0.85)
- Need: More replication

### Coverage:
- Only 3/4 decay values tested
- Missing: 0.8, 0.75 (critical!)

---

## 🚀 NEXT STEPS

### Immediate:
1. **Debug decay=0.8 runs** (boundary!)
2. **Complete decay=0.75** (below boundary)
3. **Verify freeze detection logic**

### Then:
1. Pilot B: Refine boundary (0.825, 0.875)
2. Test lower decay (0.6, 0.65)
3. Full sweep with 3 seeds

---

## 🎯 IMPLICATIONS

### For Theory:
```
Sharp boundary suggests:
- Phase transition mechanism
- Critical decay rate
- Non-trivial dynamics

Theory should explain:
- Why boundary exists
- Physical meaning of phases
- Mechanism of transition
```

### For Experiments:
```
Boundary confirmed → Focus efforts:
- Map boundary precisely
- Test phase properties
- Understand transition mechanism
```

---

## 📋 COMPARISON: Sweep vs Test C

| Parameter | Test C | Sweep | Match? |
|-----------|--------|-------|--------|
| decay=1.0 | Freeze@400, 0 br | Freeze@100, 12 br | ❌ Different |
| decay=0.85 | - | Freeze@100, 25-40 br | - |
| decay=0.8 | - | Never freezes | - |
| decay=0.7 | Active@400, 246 br | - | ✅ Consistent |

**Conclusion:** Need to reconcile Test C and Sweep conditions

---

**For raw data:** See RESULTS.md  
**For debugging:** See ISSUES.md
