# Decay Sweep with Channels - Protocol

## Objective

Map decay rate (η) vs final activity with full channel diagnostics to resolve the **decay paradox**:
- Why does slower decay (R2: η=0.7) → higher activity than faster decay (R4: η=0.3)?
- Is there an optimal decay rate η* for sustainability?

## Pre-Registered Parameters

### Sweep Grid (Pilot)
- **decay_scale:** [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]
- **seeds:** [42, 123]
- **Total runs:** 12

### Analysis Thresholds (FIXED)
- **wcluster:** 0.02
- **wdist:** 0.005
- **wbridge:** 0.0
- **min-cluster-size:** 2
- **disconnected-policy:** maxdist

### Diagnostics (ENABLED)
- **channels:** ON (cut_weight mode)
- **anisotropy:** ON (5 splits)

### Checkpoints
- **Main tick:** 400
- **Freeze detection:** [100, 200, 300, 400, 500, 600]

## Expected Outputs

### Primary Metrics
1. **bridges_weight** - field activity
2. **channel_capacity** - background geometry flow
3. **anisotropy** - structural asymmetry

### Boundary Detection
- **largest_all_frozen:** max η where 100% seeds FROZEN
- **smallest_all_active:** min η where 100% seeds ACTIVE
- **interval:** (largest_all_frozen, smallest_all_active)

## Hypotheses to Test

**H1:** Decay curve is non-monotonic
- Null: bridges_weight monotonic in η
- Alternative: optimal η* exists with peak activity

**H2:** Channel capacity correlates with sustainability
- Null: cap independent of freeze_tick
- Alternative: high cap → delayed freeze

**H3:** Anisotropy signals phase transitions
- Null: aniso uncorrelated with freeze events
- Alternative: aniso spikes before freeze

## Run Command

```bash
cd C:\Work\romionsim
python scripts/batch_sweep.py pilot --tick 400 --with-diagnostics --anisotropy-splits 5
```

## Success Criteria

✅ All 12 runs complete without INVALID  
✅ Boundary interval determined  
✅ Decay curve shape identified  
✅ Correlation: cap vs freeze_tick measured  

## Next Steps

If pilot successful:
1. **Full sweep:** η ∈ [0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0] with 5 seeds
2. **Dense peak:** If η* found, refine with step 0.02 around peak
3. **Time series:** Run η* with dense checkpoints (every 10 ticks)

---

**Status:** READY TO RUN  
**Date:** 2026-01-09  
**Protocol:** docs/SWEEP_PROTOCOL.md
