# Test C: Parameter Exploration

**Goal:** Find parameters that extend field lifetime or create long-range bridges  
**Status:** Complete (bug-fixed)  
**Date:** 2025-01 (original), 2026-01-08 (corrected)

---

## 🎯 OBJECTIVE

Test whether varying spawn_scale, decay_scale, or tension_scale can:
1. Extend bridge lifetime beyond baseline freeze (~tick 400)
2. Create bridges at dist >= 2 (long-range field)

---

## 🔬 EXPERIMENTAL DESIGN

### Runs:
| ID | Config | Parameter | Expected |
|----|--------|-----------|----------|
| R0 | R0_baseline.cfg | Baseline | Reference |
| R1 | R1_spawn_up.cfg | spawn×1.2 | Test spawn effect |
| R2 | R2_decay_slow.cfg | decay×0.7 | Test decay effect |
| R3 | R3_tension_up.cfg | tension×1.2 | Test tension effect |
| R4 | R4_combo.cfg | All combined | Test interactions |
| R5 | R5_shock.cfg | Shock perturbation | Test resilience |

### Fixed Parameters:
- ticks: 600
- nodes: 2000
- init_edges: 6000
- seed: 42
- dump_graph_every: 100 (for analysis)

### Analysis:
- Tick: 400 (after baseline freeze)
- Method: gravity_test.py
- Metrics: bridges, pairs, hub_share, range

---

## 📊 RESULTS (Corrected)

**After node2c=-1 leak bug fix:**

| Run | decay_scale | bridges@400 | hub% | range | status |
|-----|-------------|-------------|------|-------|--------|
| R0 | 1.0 | 0 | 0.0 | 0 | FROZEN |
| R1 | 1.0 | 0 | 0.0 | 0 | FROZEN |
| R2 | 0.7 | 246 | 10.7 | 1 | ACTIVE ⭐ |
| R3 | 1.0 | 12 | 25.0 | 1 | WEAK |
| R4 | 0.7 | 38 | 16.0 | 1 | WEAK |
| R5 | 1.0 | 0 | 0.0 | 0 | FROZEN |

**See:** RESULTS.md for detailed metrics

---

## 🔍 KEY FINDINGS

### 1. Baseline Freezes @ ~400
- R0, R1, R5: 0 bridges @ tick 400
- System reaches frozen attractor
- No inter-cluster bridges remain

### 2. decay×0.7 Prevents Freeze ⭐
- R2: 246 bridges @ tick 400 (only active run!)
- Hub distributed (10.7%, not concentrated)
- Shifts system outside freeze basin

### 3. Other Parameters Ineffective
- spawn×1.2: FROZEN (worse than baseline)
- tension×1.2: Weak (12 bridges, 95% worse than R2)
- combo: Non-linear failure (85% worse than R2 alone)
- shock: No effect on frozen attractor

### 4. Range=1 Universal
- No bridges @ dist>=2 in ANY run
- Even R2 (best) has range=1
- Long-range requires new mechanism (S2-tail?)

---

## 💡 INTERPRETATION

### decay_scale Semantics:
```
Higher scale → FASTER decay → EARLIER freeze
Lower scale → SLOWER decay → LONGER active

decay_scale multiplies base decay rate:
- 1.0 → decay = 0.008 (baseline, freezes)
- 0.7 → decay = 0.0056 (slow, stays active)
```

### Critical Insight:
**Not just lifetime extension - freeze PREVENTION**
- R0: Reaches frozen attractor
- R2: Shifted outside freeze basin
- Phase-like transition behavior

---

## 📁 FILES

### Configs:
- cfg/R0_baseline.cfg
- cfg/R1_spawn_up.cfg
- cfg/R2_decay_slow.cfg ⭐
- cfg/R3_tension_up.cfg
- cfg/R4_combo.cfg
- cfg/R5_shock.cfg

### Results:
- results/R0_base/
- results/R2_decayDown/ ⭐
- results/summary.csv (corrected)

### Documentation:
- RESULTS.md (detailed data)
- ANALYSIS.md (interpretation)
- TEST_C_CORRECTED_RESULTS.md (full report)

---

## 🚀 NEXT STEPS

Based on Test C findings:
1. ✅ decay_scale = primary control parameter
2. → Sweep decay_scale to map freeze boundary
3. → Test if lower decay creates range>1
4. → S2-tail theory if range=1 persists

**See:** ../sweep_decay/ for follow-up investigation

---

## 🐛 BUG FIX NOTE

**Original Results (WRONG):**
- R2: 976 bridges (4× inflated!)
- R0: 150 bridges (artifact!)
- Hub >100% (impossible!)

**Cause:** node2c=-1 leak counted unassigned nodes

**Fixed:** 2026-01-08  
**See:** ../../docs/CRITICAL_BUG_FIX_20260108.md
