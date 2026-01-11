# Time Evolution Analysis: R0 vs R2
# Date: 2026-01-08
# Test: Channel metrics evolution across ticks 100-600

## Parameters
- wcluster: 0.02
- wdist: 0.005
- wbridge: 0.0
- anisotropy_splits: 5

## Data Table

| Tick | R0 Bridges | R0 Ch.Cap | R0 Aniso | R2 Bridges | R2 Ch.Cap | R2 Aniso |
|------|------------|-----------|----------|------------|-----------|----------|
| 100 | 0 | 0.000 | 0.000 | 0 | 0.000 | 0.000 |
| 200 | 1242 | 4.499 | 0.053 | 1574 | 5.882 | 0.064 |
| 300 | 2204 | **11.294** | 0.009 | 326 | 2.266 | **0.239** |
| 400 | 879 | 3.577 | 0.020 | 1389 | **7.417** | 0.028 |
| 500 | 114 | 0.467 | 0.169 | 988 | 4.412 | 0.035 |
| 600 | 15 | 0.040 | 0.002 | 387 | 1.442 | 0.018 |

## Key Discoveries

### 1. R0 Has a Hidden Peak at Tick 300!

**Unexpected finding:** R0_base (baseline) has:
- Peak bridges at tick 300: **2204** (not at tick 200 or 400!)
- Peak channel capacity at tick 300: **11.294** (higher than R2's best!)

This means R0 actually has MORE activity at tick 300 than R2!

But by tick 400-600, R0 collapses:
- Tick 400: 879 bridges
- Tick 500: 114 bridges  
- Tick 600: 15 bridges (nearly frozen)

### 2. R2 Has Sustained Activity

R2 (decay×0.7) shows different pattern:
- No dramatic peak
- Steady activity: 326 → 1389 → 988 → 387 bridges
- Channel capacity stable: 2.3 → 7.4 → 4.4 → 1.4

### 3. Anisotropy Signals Structural Transitions

**R2 tick 300:** Anisotropy = 0.239 (HIGHEST in dataset!)
- This is 10x higher than other measurements
- Coincides with LOW bridge count (326)
- Suggests structural reorganization phase

**R0 tick 500:** Anisotropy = 0.169
- Second highest measurement
- Coincides with collapse (114 bridges)
- Pre-freeze asymmetric structure

### 4. Phase Diagram Interpretation

```
R0 Evolution:
  tick 100: Quiet (no bridges)
  tick 200: Building (1242 bridges)
  tick 300: PEAK (2204 bridges, 11.3 capacity) ← Maximum activity!
  tick 400: Declining (879 bridges)
  tick 500: Collapsing (114 bridges, high aniso)
  tick 600: Near-frozen (15 bridges)

R2 Evolution:
  tick 100: Quiet (no bridges)
  tick 200: Building (1574 bridges)
  tick 300: TRANSITION (326 bridges, 0.24 aniso) ← Structural reorganization
  tick 400: Stable peak (1389 bridges, 7.4 capacity)
  tick 500: Slow decline (988 bridges)
  tick 600: Lower but active (387 bridges)
```

### 5. The "Decay Paradox"

**Counter-intuitive finding:**
- R0 (normal decay) has HIGHER peak activity at tick 300
- R2 (slower decay) has LOWER peak but more sustained activity

**Interpretation:**
- Normal decay allows rapid buildup AND rapid collapse
- Slower decay prevents both extremes → more stable system
- "Less is more" - slower decay = longer-lived channels

## Hypotheses for Future Testing

### H1: Peak-Collapse Pattern
R0's pattern (build → peak → collapse) may be universal for baseline parameters.
**Test:** Run more seeds and check if peak always occurs around tick 300.

### H2: Anisotropy as Transition Marker
High anisotropy (>0.1) indicates structural transition.
**Test:** Track anisotropy continuously and correlate with bridge count changes.

### H3: Decay Rate Determines Stability
decay×0.7 creates ~3x more stable late-phase activity than baseline.
**Test:** Map decay sweep with channel metrics, find optimal decay rate.

## Revised Conclusions

1. **R0 is NOT simply "frozen"** - it has active phases, just collapses faster
2. **R2's advantage is SUSTAINABILITY**, not peak activity
3. **Tick 400 was misleading** - comparing only at tick 400 missed R0's peak
4. **Anisotropy is a valuable diagnostic** - signals structural transitions

## Recommendations

1. **Always analyze multiple ticks** - single-tick comparison is insufficient
2. **Track anisotropy evolution** - it reveals phase transitions
3. **Define "success" carefully** - peak vs sustained activity are different goals
4. **R0 and R2 represent different strategies:**
   - R0: High-risk, high-reward (big peak, fast collapse)
   - R2: Conservative, sustainable (moderate peak, slow decline)
