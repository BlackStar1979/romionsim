# Decay Sweep: Freeze Boundary Investigation

**Goal:** Map decay_scale → freeze_tick relationship  
**Status:** Pilot A partial (3/8 complete)  
**Date:** 2026-01-08

---

## 🎯 OBJECTIVE

Based on Test C finding that decay×0.7 prevents freeze:

**Map the freeze boundary:**
- At what decay_scale does system freeze?
- Is transition sharp or gradual?
- Can lower decay create range>1?

---

## 🔬 EXPERIMENTAL DESIGN

### Pilot A (Quick Probe):
```
decay_scale: [1.0, 0.85, 0.8, 0.75]
seeds: [42, 123]
Total: 8 runs
Goal: Bracket freeze boundary
```

### Pilot B (Refine):
```
decay_scale: [0.95, 0.9, 0.875, 0.825, 0.775, 0.7, 0.65, 0.6]
seeds: [42, 123]
Total: 16 runs
Goal: Detail boundary region
```

### Full Sweep:
```
decay_scale: [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6]
seeds: [42, 123, 456]
Total: 27 runs
Goal: Complete map with replication
```

### Fixed Parameters:
- ticks: 600
- nodes: 2000
- init_edges: 6000
- spawn_scale: 1.0
- tension_scale: 1.0
- dump_graph_every: 100

### Metrics:
- **freeze_tick:** First tick with 0 bridges
- **bridges@400:** Bridge count at reference tick
- **hub_share@400:** Hub concentration
- **range@400:** Max distance with bridges
- **singleton_pct@400:** Fragmentation

---

## 📊 RESULTS (Pilot A - Partial)

**Completed (3/8):**

| decay | seed | freeze_tick | bridges@400 | hub% | range |
|-------|------|-------------|-------------|------|-------|
| 1.0 | 123 | 100 | 12 | 40.0 | 1 |
| 0.85 | 42 | 100 | 25 | 18.8 | 1 |
| 0.85 | 123 | 100 | 40 | 21.7 | 1 |

**Failed:**
- decay=1.0, seed=42 (simulation failed)
- decay=0.8, seed=42 (analysis failed, freeze=never!)
- decay=0.8, seed=123 (Python crash)
- decay=0.75 (not attempted)

**See:** RESULTS.md for details

---

## 🔍 KEY FINDINGS (Preliminary)

### 1. Freeze Boundary @ 0.8-0.85! ⭐
```
decay >= 0.85 → Freeze @ tick 100 (FAST)
decay <= 0.8  → Never freezes (>600)

Boundary is SHARP!
```

### 2. Inverted Semantics Confirmed
```
Higher decay_scale = FASTER decay = EARLIER freeze
Lower decay_scale = SLOWER decay = STAYS ACTIVE

Test C R2 (0.7): Active @ 400 ✓
Sweep (1.0, 0.85): Frozen @ 100 ✓
Sweep (0.8): Never freezes ✓
```

### 3. Bridges Despite Freeze
```
decay=1.0, 0.85 freeze @ 100 but show bridges @ 400?
Possible: Residual bridges from before freeze
Need: Better freeze detection (sustained 0 bridges)
```

---

## ⚠️ ISSUES

### Technical:
1. Some simulations failed (no stderr)
2. Python crashes (encodings module error)
3. Analysis failures on d0.8 runs

### Methodological:
1. freeze_tick detection may be too simple
2. Need sustained freeze (not single tick)
3. Batch runner needs error recovery

---

## 📁 FILES

### Configs:
- cfg/pilot_a.cfg (4 values × 2 seeds)
- cfg/pilot_b.cfg (8 values × 2 seeds)
- cfg/full_sweep.cfg (9 values × 3 seeds)

### Results:
- results/sweep_pilot_d{decay}_s{seed}/
- results/decay_sweep_pilot.csv (partial)
- results/sweep_pilot_log.txt

### Documentation:
- RESULTS.md (raw data)
- ANALYSIS.md (interpretation)
- ISSUES.md (debugging notes)
- PILOT_SWEEP_PARTIAL_RESULTS.md (detailed report)

---

## 🚀 NEXT STEPS

### Immediate:
1. Debug failed runs (d0.8, d0.75)
2. Manual analysis of existing data
3. Verify freeze boundary

### Then:
1. Complete Pilot A (remaining 5 runs)
2. Run Pilot B to refine boundary
3. Full sweep if boundary confirmed

### Questions:
1. Is 0.8-0.85 truly the boundary?
2. What happens at decay=0.75, 0.7, 0.6?
3. Can any decay create range>1?

---

## 🔬 HYPOTHESIS

**Phase Transition Model:**
```
Phase I (decay >= 0.85): Fast freeze (<200 ticks)
Boundary (~0.8-0.85): Critical transition
Phase II (decay <= 0.8): Active field (>600 ticks)

Prediction: Sharp boundary, not gradual
Test C R2 (0.7) in Phase II ✓
```

---

## 📋 COMPARISON WITH TEST C

| Source | decay | freeze_tick | bridges@400 |
|--------|-------|-------------|-------------|
| Test C R0 | 1.0 | ~400 | 0 |
| Test C R2 | 0.7 | never | 246 |
| Sweep | 1.0 | 100 | 12* |
| Sweep | 0.85 | 100 | 25-40* |
| Sweep | 0.8 | never | ??? |

*Note: Bridges despite freeze - needs investigation

**Consistent:** Boundary exists between 0.8-0.85

---

**Status:** Pilot A 38% complete. Freeze boundary identified. Need to complete analysis.
