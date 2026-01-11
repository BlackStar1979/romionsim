# R0 Peak Investigation: The 11.29 Capacity Spike

**Date:** 2026-01-09  
**Run:** R0_base (baseline parameters, decay=1.0)  
**Discovery:** Maximum system activity @ tick 300, then catastrophic collapse  

---

## Executive Summary

R0 (baseline) exhibits a **transient peak** at tick 300 with:
- **11.294 capacity** (highest observed across all runs)
- **2204 bridges** (2.5× final value)
- **0.009 anisotropy** (lowest - perfectly balanced)

This peak represents an **ideal equilibrium state** that the system cannot maintain. Within 100 ticks, activity drops 60%, leading to eventual system freeze.

---

## Time Evolution Data

| Tick | Bridges | Capacity | Anisotropy | Phase |
|------|---------|----------|------------|-------|
| 100 | 0 | 0.000 | 0.000 | Initialization |
| 200 | 1242 | 4.499 | 0.053 | **Growth (turbulent)** |
| **300** | **2204** | **11.294** | **0.009** | **PEAK (stable)** |
| 400 | 879 | 3.577 | 0.020 | Decay phase 1 |
| 500 | 114 | 0.467 | 0.169 | **Collapse (unstable)** |
| 600 | 15 | 0.040 | 0.002 | Frozen |

---

## Phase Analysis

### Phase 1: Growth (tick 100-200)
- **Bridges:** 0 → 1242
- **Anisotropy:** 0.053 (elevated - turbulent growth)
- **Mechanism:** System exploring configuration space, high variance

### Phase 2: Peak (tick 200-300)
- **Bridges:** 1242 → 2204 (+77% growth!)
- **Anisotropy:** 0.053 → 0.009 (stabilization!)
- **Capacity:** 4.499 → 11.294 (2.5× increase!)
- **Mechanism:** System finds optimal configuration
  - **Low anisotropy = balanced structure**
  - **High bridges = maximal connectivity**
  - **High capacity = efficient flow**

**🔑 KEY INSIGHT:** Tick 300 represents **structural equilibrium**
- System has found locally optimal topology
- Balanced geometry (low anisotropy)
- Maximum information flow (high capacity)

### Phase 3: Catastrophic Decay (tick 300-400)
- **Bridges:** 2204 → 879 (-60% loss!)
- **Delta:** -1325 bridges in 100 ticks
- **Rate:** -13.25 bridges/tick
- **Mechanism:** Exponential decay overwhelms spawn
  - decay_scale = 1.0 → decay = 0.008
  - Too aggressive for sustained activity

### Phase 4: Accelerated Collapse (tick 400-500)
- **Bridges:** 879 → 114 (-87% loss!)
- **Anisotropy:** 0.020 → 0.169 (8.5× spike!)
- **Mechanism:** Structural breakdown
  - Few remaining bridges become highly asymmetric
  - Hub dominance increases
  - System fragmenting

### Phase 5: Freeze (tick 500-600)
- **Bridges:** 114 → 15 (-87% loss again!)
- **Capacity:** 0.467 → 0.040 (near zero)
- **System state:** Effectively frozen, minimal activity

---

## Anisotropy as Phase Marker

**Hypothesis:** Anisotropy signals structural instability

| Phase | Anisotropy | Interpretation |
|-------|------------|----------------|
| Growth | 0.053 | Exploration, turbulence |
| **Peak** | **0.009** | **Equilibrium, balance** |
| Decay 1 | 0.020 | Mild asymmetry |
| **Collapse** | **0.169** | **Breakdown, fragmentation** |
| Frozen | 0.002 | Dead system, no flow |

**Pattern:**
- Low anisotropy (< 0.02) = stable/balanced
- Medium anisotropy (0.02-0.05) = normal activity
- **High anisotropy (> 0.05) = instability/transition**

Anisotropy spike @ tick 500 (0.169) is **early warning** of imminent freeze!

---

## Comparison: R0 vs R2

Why does R2 (decay=0.7) sustain higher activity?

### R0 (decay=1.0) - Transient Peak
- **Peak @ tick 300:** 2204 bridges, 11.294 capacity
- **Final @ tick 600:** 15 bridges, 0.040 capacity
- **Outcome:** System collapses - decay too fast

### R2 (decay=0.7) - Sustained Activity  
- **Peak @ tick 200:** 1574 bridges, 5.88 capacity
- **Tick 300:** 326 bridges, 2.27 capacity
- **Final @ tick 600:** 387 bridges, 1.44 capacity
- **Outcome:** Lower peak but SURVIVES - decay balanced

**KEY DIFFERENCE:**
- **R0:** Reaches higher peak but cannot sustain it
- **R2:** Lower peak but maintains baseline activity
- **Mechanism:** Slower decay (η=0.7) allows spawn to keep up

---

## Physical Interpretation

### What IS tick 300 peak?

**Hypothesis 1: Critical Point**
- System reaches critical connectivity threshold
- Spawn rate peaks due to high coherence
- Bridge reinforcement maximized

**Hypothesis 2: Phase Transition**
- System transitions from growth → decay phase
- Tick 300 = equilibrium point
- Post-300: decay dominates spawn

**Hypothesis 3: Resonance**
- Spawn/decay rates briefly synchronize
- Creates temporary "sweet spot"
- Inherently unstable - small perturbations collapse it

### Why Does It Collapse?

**Decay Death Spiral:**
1. High bridge count @ tick 300
2. More bridges → more decay targets
3. decay_scale = 1.0 → aggressive pruning
4. Spawn cannot compensate for mass decay
5. **Positive feedback:** fewer bridges → lower spawn → fewer bridges
6. System enters death spiral → freeze

**R2 Survival:**
- decay_scale = 0.7 → gentler pruning
- Spawn can keep up with decay
- **Negative feedback:** bridges decrease → decay slows → spawn catches up
- System finds sustainable equilibrium

---

## Testable Predictions

### H1: Decay Rate Determines Sustainability
- **Test:** Sweep decay_scale ∈ [0.5, 1.0]
- **Prediction:** Optimal η* exists where peak is sustained
- **Falsification:** If all decay rates collapse OR all survive

### H2: Anisotropy Predicts Collapse
- **Test:** Track anisotropy continuously (every 10 ticks)
- **Prediction:** Anisotropy spike precedes bridge collapse by ~50 ticks
- **Falsification:** If anisotropy uncorrelated with stability

### H3: Peak Height Inversely Correlates with Sustainability
- **Test:** Compare peak_capacity vs final_capacity across decay values
- **Prediction:** Higher peaks → faster collapse (overshoot)
- **Falsification:** If peak height uncorrelated with survival

### H4: Critical Connectivity Threshold Exists
- **Test:** Identify minimum bridge count for sustained activity
- **Prediction:** Below threshold → inevitable freeze
- **Falsification:** If no clear threshold exists

---

## Implications for ROMION O'LOGIC

### Cosmological Analogy: Inflationary Epoch?

**R0 tick 300 peak = Early universe "hot phase"**
- Briefly reaches maximum "temperature" (activity)
- Cannot maintain → exponential cooling (decay)
- Ends in "freeze out" (low activity)

**R2 sustained activity = Stable cosmology**
- Lower peak "temperature"
- Gradual cooling → maintains structure
- Analog: Our universe (not too hot, not too cold)

### Design Implications

**For sustainable CORE systems:**
1. ✅ **Tune decay rate** - Not too fast (R0) or too slow
2. ✅ **Monitor anisotropy** - Early warning system
3. ✅ **Avoid overshoot** - High peaks unstable
4. ✅ **Feedback control** - Adapt decay based on activity

---

## Next Steps

### Immediate
1. ✅ **Analyze decay sweep** - Find optimal η* (IN PROGRESS)
2. ⏳ **Time series @ optimal η*** - Verify sustained peak
3. ⏳ **Anisotropy tracking** - Implement continuous monitoring

### Near-term
4. ⏳ **Critical threshold study** - Min bridge count for stability
5. ⏳ **Spawn/decay balance** - Derive equilibrium condition
6. ⏳ **Feedback mechanism** - Adaptive decay control

### Long-term
7. ⏳ **Cosmology mapping** - Early universe analogies
8. ⏳ **Phase diagram** - Map stability regions in parameter space
9. ⏳ **Loop topology** - Does peak correlate with loop structures?

---

## References

**Data:**
- tests/test_c/results/R0_base/peak_analysis_dense.csv
- tests/test_c/RESULTS.md (R0-R5 comparison)

**Theory:**
- docs/COSMOLOGY_MAPPING.md (H-C1: Structure formation)
- docs/theory/INDEX.md (CORE evolution)

**Scripts:**
- scripts/investigate_r0_peak.py (this analysis)
- scripts/sweep_inprocess.py (ongoing decay sweep)

---

**Status:** ✅ MECHANISM UNDERSTOOD  
**Key Finding:** Tick 300 = ideal equilibrium, unsustainable with decay=1.0  
**Next:** Identify optimal decay rate for sustained peak activity  

---

*Analysis complete: 2026-01-09*
