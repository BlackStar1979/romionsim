# Decay Sweep: Predictions vs Reality

**Created:** 2026-01-09 (before sweep completion)  
**Purpose:** Test prediction accuracy  

---

## PREDICTIONS (made @ 67% completion)

Based on partial data (decay 0.8-1.0) + Test C (decay 0.7):

### Bridges @ Tick 400 (n=1000 systems)

| Decay | Predicted | Confidence | Basis |
|-------|-----------|------------|-------|
| 1.00 | 0 | ✅ High | Observed |
| 0.90 | 0 | ✅ High | Observed |
| 0.85 | 0 | ✅ High | Observed |
| 0.80 | 1-3 | ✅ High | Observed (avg=1.5) |
| 0.75 | 100-500 | 🟡 Medium | Between critical & active |
| **0.70** | **1000-1500** | 🟡 Medium | Test C analogy (n=2000: 1389) |
| 0.65 | 500-1000 | 🟢 Low | Below peak |
| 0.60 | 300-800 | 🟢 Low | Moderate activity |
| 0.50 | 100-500 | 🟢 Low | Lower activity |

### Channel Capacity @ Tick 400

| Decay | Predicted Capacity | Basis |
|-------|-------------------|-------|
| 1.00 | 0.0 | Frozen |
| 0.90 | 0.0 | Frozen |
| 0.85 | 0.0 | Frozen |
| 0.80 | ~0.01 | Marginal |
| 0.75 | 1-3 | Growing |
| **0.70** | **5-8** | Peak (Test C: 7.417) |
| 0.65 | 3-5 | Post-peak |
| 0.60 | 2-4 | Declining |
| 0.50 | 1-2 | Lower |

### Curve Shape Prediction

```
Bridges
  1500 |           *  (0.70 predicted peak)
       |          / \
  1000 |         /   \
       |        /     \
   500 |       /       \
       |      /         \___
   100 |     /              \___
       |  * /                   \___
     0 |_*_*_________________________
       0.5  0.7  0.9  1.1  decay

   FREEZE BOUNDARY at 0.80-0.85 -->
```

**Expected pattern:**
- Monotonic increase from 0.5 to 0.7
- Peak @ decay=0.7 (or nearby)
- Sharp decline 0.7 to 0.8
- Freeze @ 0.85+

---

## HYPOTHESES TO TEST

### H1: Peak Location
**Prediction:** Maximum activity @ decay=0.65-0.75  
**Test:** Find decay with max(bridges, capacity)  
**Falsification:** If peak outside this range  

### H2: Curve Shape
**Prediction:** Non-monotonic, single peak  
**Test:** Plot bridges vs decay  
**Falsification:** If monotonic or multiple peaks  

### H3: Sharp Transition
**Prediction:** Freeze boundary width Δ < 0.1  
**Test:** Measure critical interval  
**Falsification:** If gradual decline Δ > 0.2  

### H4: Capacity Follows Bridges
**Prediction:** capacity ∝ bridges (roughly)  
**Test:** Correlation coefficient  
**Falsification:** If r < 0.7  

### H5: Anisotropy Anti-Correlation
**Prediction:** High bridges → low anisotropy  
**Test:** Correlation at active points  
**Falsification:** If r > -0.5  

---

## ACTUAL RESULTS

**To be filled when sweep completes:**

### Bridges @ Tick 400 (ACTUAL)

| Decay | Predicted | Actual | Δ | Status |
|-------|-----------|--------|---|--------|
| 1.00 | 0 | ___ | ___ | ___ |
| 0.90 | 0 | ___ | ___ | ___ |
| 0.85 | 0 | ___ | ___ | ___ |
| 0.80 | 1-3 | ___ | ___ | ___ |
| 0.75 | 100-500 | ___ | ___ | ___ |
| 0.70 | 1000-1500 | ___ | ___ | ___ |
| 0.65 | 500-1000 | ___ | ___ | ___ |
| 0.60 | 300-800 | ___ | ___ | ___ |
| 0.50 | 100-500 | ___ | ___ | ___ |

### Prediction Accuracy

**Metrics:**
- Mean Absolute Error: ___
- Max Error: ___
- Direction Correct: ___/9
- Range Correct: ___/9

### Hypothesis Results

- [ ] H1: Peak location - ___
- [ ] H2: Curve shape - ___
- [ ] H3: Sharp transition - ___
- [ ] H4: Capacity follows bridges - ___
- [ ] H5: Anisotropy anti-correlation - ___

---

## SURPRISES / UNEXPECTED RESULTS

**To be filled after analysis:**

1. ___
2. ___
3. ___

---

## LESSONS FOR FUTURE PREDICTIONS

**What worked:**
- ___

**What didn't work:**
- ___

**Improvements needed:**
- ___

---

## UPDATED MODEL

Based on actual results, update prediction model:

**New formula:**
```
bridges(decay, N) = ???
```

**Key parameters:**
- Peak location: ___
- Peak height: ___
- Decay rate: ___
- Freeze boundary: ___

---

**STATUS:** 🟡 AWAITING COMPLETION  
**Fill in:** When analyze_sweep.py completes  
**Then:** Compare predictions vs actuals  

*Template created: 2026-01-09*
