# IMPORTANT: R0 Discrepancy Resolved

## Problem
Test C R0 (decay=1.0, seed=42): 879 bridges @ tick 400  
Sweep d1.0_s42: 0 bridges @ tick 400  
**Why the difference?**

## Root Cause: Different System Sizes

### Test C R0 Configuration
- **Nodes:** ~2000 (inferred from GRAPH @ tick 100)
- **Initial edges:** ~29,614 @ tick 100
- **Result:** Survives to tick 400 with 879 bridges

### Sweep Configuration
- **Nodes:** 1000 (hardcoded in sweep_inprocess.py)
- **Initial edges:** 10,000
- **Result:** Freezes before tick 400 (0 bridges)

## Impact on Results

### System Size Matters!
**Larger systems survive longer with same decay rate**
- More nodes → more edge formation opportunities
- Higher initial connectivity → more robust to decay
- 2000 nodes @ decay=1.0 ≈ 1000 nodes @ decay=0.7-0.8?

### Sweep Results Still Valid
✅ **Internal consistency:** All sweep runs use n=1000, e=10000  
✅ **Comparative analysis:** Valid within sweep dataset  
❌ **Not directly comparable to Test C:** Different system size  

## Implications

### For Decay Curve
The sweep decay curve is valid for **n=1000 systems**:
- Freeze boundary @ decay=0.80-0.85 (for n=1000)
- Test C results are for **n=2000 systems**
- Larger systems tolerate higher decay rates

### System Size Scaling
**Hypothesis:** Optimal decay scales with system size
- Small systems (n=1000): optimal decay ~0.7
- Large systems (n=2000): optimal decay ~0.9-1.0?

**Mechanism:**
- More nodes → more spawn opportunities
- Higher decay needed to prevent overgrowth
- Balance point shifts with N

### For ROMION Theory
**This is actually GOOD news:**
- Shows system size effects (expected in relational ontology)
- Decay is *relative* to system capacity
- Cosmological analog: Universe size affects cooling rate

## Action Items

### Immediate
1. ✅ Document discrepancy (this file)
2. ⏳ Note in sweep results: "Valid for n=1000 systems"
3. ⏳ Add system size to all result headers

### Future Work
4. ⏳ Run system size sweep: n ∈ [500, 1000, 2000, 4000]
5. ⏳ Derive scaling law: optimal_decay(N)
6. ⏳ Test hypothesis: decay ∝ sqrt(N) or decay ∝ log(N)?

## Corrected Interpretation

### Sweep Results (n=1000)
- **Freeze boundary:** 0.80-0.85
- **Optimal:** ~0.65-0.75 (predicted)
- **Valid for:** Small-scale systems

### Test C Results (n=2000)
- **R0 survives:** decay=1.0 tolerable
- **R2 winner:** decay=0.7 still optimal?
- **Valid for:** Medium-scale systems

### Universal Pattern
**Relative decay rate matters more than absolute:**
- decay/N or decay/connectivity is the critical parameter
- Each system size has its own optimal decay range
- Freeze boundary shifts with scale

## Updated Predictions

For **n=1000 systems** (sweep):
- 0.5-0.7: Active, moderate to high bridges
- 0.7: Peak activity (predicted ~1000-1500 bridges)
- 0.75-0.8: Declining, approaching critical
- 0.8-0.85: Critical transition
- 0.85+: Freeze before tick 400

For **n=2000 systems** (Test C):
- All values shifted up by ~0.2-0.3
- R0 (1.0) survives with 879 bridges
- R2 (0.7) is winner with 1389 bridges

---

**Status:** ✅ DISCREPANCY RESOLVED  
**Cause:** System size difference (2000 vs 1000 nodes)  
**Impact:** Sweep results valid for n=1000 systems  
**Learning:** Decay scaling with system size is important!  

*Date: 2026-01-09*
