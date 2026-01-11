# Test C: Analysis & Interpretation

**Date:** 2026-01-08

---

## 🎯 MAIN CONCLUSIONS

### 1. Baseline Reaches Frozen Attractor
```
NOT just "weakening" - complete FREEZE
R0, R1, R5: 0 bridges @ 400
No inter-cluster bridges remain
System locked in frozen state
```

### 2. decay×0.7 Prevents Freeze ⭐
```
Not extension - PREVENTION
Shifts system outside freeze basin
R2 active when others frozen
Effect: +∞ vs baseline (246 vs 0)
```

### 3. Only decay Parameter Effective
```
spawn×1.2: FROZEN (worse than baseline)
tension×1.2: Weak (95% worse than decay)
combo: Non-linear failure (85% worse)
shock: No effect on frozen attractor

Conclusion: decay is primary control parameter
```

### 4. Range=1 Universal Ceiling
```
Even R2 (best run) has range=1
No bridges @ dist≥2 anywhere
Long-range requires new mechanism
Candidate: S2-tail (weak long-range links)
```

---

## 🔬 DECAY_SCALE SEMANTICS

### How it Works:
```python
params['decay'] *= args.decay_scale

Base decay: 0.008
decay_scale=1.0 → decay=0.008 (FAST decay)
decay_scale=0.7 → decay=0.0056 (SLOW decay)
```

### Effect:
```
Higher scale → FASTER decay → EARLIER freeze
Lower scale → SLOWER decay → LONGER active

R0 (scale=1.0): Fast decay → freeze @ 400
R2 (scale=0.7): Slow decay → active @ 400+
```

### Interpretation:
**Decay rate controls system lifetime**
- Too fast: Bridge weights decay faster than spawn
- Optimal: Balance between spawn and decay
- System reaches frozen vs active state

---

## 💡 PHASE-LIKE BEHAVIOR

### Two Regimes:
```
FROZEN: decay_scale ≥ ~0.8-0.85
- Reaches frozen attractor
- 0 bridges @ finite time
- System "dies"

ACTIVE: decay_scale ≤ ~0.7-0.8
- Maintains bridge field
- Persistent inter-cluster structure
- System "alive"
```

### Transition:
Sharp boundary (not gradual)  
See: tests/sweep_decay/

---

## 🔍 NON-LINEAR INTERACTIONS

### R4 (Combo) Failure:
```
Expected: R2 (decay alone) = 246 bridges
Actual: R4 (decay+spawn+tension) = 38 bridges

Loss: 85% (!!)
```

### Hypothesis:
```
spawn×1.2 + tension×1.2 may:
1. Accelerate cluster formation
2. Reduce inter-cluster bridges
3. Counteract decay benefits

Needs: Careful parameter interaction study
```

---

## 🎯 FALSIFICATION STATUS

### Predictions Tested:
1. ❌ Long-range field (range≥2) - NOT FOUND
2. ✅ Parameter sensitivity - CONFIRMED
3. ✅ Field lifetime extension - CONFIRMED (via decay)

### Still Open:
1. Can ANY parameters create range≥2?
2. What is minimum decay for active field?
3. Does S2-tail enable long-range?

---

## 📊 STATISTICAL NOTES

### Seed Variance:
- Single seed (42) for Test C
- Sweep uses multiple seeds
- Need: Test C replication

### Metrics Robustness:
- After bug fix: hub<100% ✓
- Coverage=100% ✓
- Consistent across runs ✓

---

## 🚀 IMPLICATIONS FOR THEORY

### 1. Decay as Fundamental Control
Theory should explain:
- Why decay_scale controls freeze
- Physical meaning of "frozen attractor"
- Relationship to field dynamics

### 2. Range=1 Ceiling
Theory should address:
- Why local only (no long-range)
- Is S2-tail mechanism needed?
- Physical constraints on range

### 3. Non-Linear Parameter Space
Theory should predict:
- Parameter interactions
- Optimal configurations
- Phase boundaries

---

**For raw data:** See RESULTS.md  
**For bug fix details:** See COMPARISON.md
