# Channel Metrics Comparison: R0-R5 @ tick 400
# Date: 2026-01-08
# Test: Full comparison with new channel/anisotropy metrics

## Parameters
- wcluster: 0.02 (cluster definition)
- wdist: 0.005 (background geometry)
- wbridge: 0.0 (all bridges)
- anisotropy_splits: 5

## Summary Table

| Run | Clusters | Bridges | Hub% | Cover% | Ch.Cap | Aniso |
|-----|----------|---------|------|--------|--------|-------|
| R0_base | 695 | 879 | 0.7% | 73.5% | 3.577 | 0.0201 |
| R1_spawnUp | 580 | 440 | 1.1% | 59.3% | 1.680 | 0.0610 |
| R2_decayDown | 451 | 1389 | 2.6% | 66.7% | **7.417** | 0.0277 |
| R3_tensionUp | 691 | 1045 | 0.6% | 75.7% | 4.538 | 0.0452 |
| R4_combo | 465 | 797 | 1.2% | 66.7% | 4.306 | 0.0385 |
| R5_shock | 695 | 879 | 0.7% | 73.5% | 3.577 | 0.0201 |

## Key Observations

### 1. Channel Capacity Ranking
```
R2_decayDown: 7.417  ← HIGHEST (decay×0.7 creates strongest channels)
R3_tensionUp: 4.538
R4_combo:     4.306
R0_base:      3.577
R5_shock:     3.577  ← Same as R0 (shock had no lasting effect)
R1_spawnUp:   1.680  ← LOWEST (spawn×1.2 fragments structure)
```

**Interpretation:** 
- Slower decay (R2) allows stronger, more stable channel formation
- Higher spawn (R1) creates fragmentation, reducing channel connectivity
- Shock (R5) reverted to baseline - no lasting structural change

### 2. Anisotropy Ranking
```
R1_spawnUp:   0.0610  ← HIGHEST (most asymmetric)
R3_tensionUp: 0.0452
R4_combo:     0.0385
R2_decayDown: 0.0277
R0_base:      0.0201  ← LOWEST (most symmetric)
R5_shock:     0.0201  ← Same as R0
```

**Interpretation:**
- Higher spawn (R1) creates more asymmetric structure
- Baseline (R0) is most symmetric
- Anisotropy anti-correlates with channel capacity

### 3. R5_shock = R0_base (Identical!)

This is remarkable: R5 (with shock) has **exactly the same** metrics as R0 (baseline):
- Same clusters: 695
- Same bridges: 879
- Same hub_share: 0.7%
- Same coverage: 73.5%
- Same channel_capacity: 3.577
- Same anisotropy: 0.0201

**Conclusion:** The shock mechanism in R5 either:
1. Did not activate, or
2. Fully reverted to baseline by tick 400

This needs investigation - check SPEC_THAW_SHOCK.md for expected behavior.

### 4. Cluster Count vs Channel Capacity

| Run | Clusters | Ch.Cap | Ratio |
|-----|----------|--------|-------|
| R2 | 451 | 7.417 | 0.0164 |
| R4 | 465 | 4.306 | 0.0093 |
| R1 | 580 | 1.680 | 0.0029 |
| R3 | 691 | 4.538 | 0.0066 |
| R0 | 695 | 3.577 | 0.0051 |

**Pattern:** Fewer clusters → higher channel capacity per cluster
- R2 has fewest clusters (451) and highest capacity (7.417)
- R1 has many clusters (580) but lowest capacity (1.680)

### 5. Coverage Patterns

All runs have similar coverage (59-76%), suggesting:
- The field touches most of the structure regardless of parameters
- Coverage is not a discriminating metric for these parameter ranges

## Correlations (Visual)

```
Channel Capacity vs Bridges:
  R2: ████████████████████████████████████ 1389 bridges, 7.4 capacity
  R3: ██████████████████████████ 1045 bridges, 4.5 capacity  
  R0: ██████████████████████ 879 bridges, 3.6 capacity
  R4: ████████████████████ 797 bridges, 4.3 capacity
  R1: ███████████ 440 bridges, 1.7 capacity

→ Strong positive correlation: more bridges = higher channel capacity
```

```
Anisotropy vs Clusters:
  R1: ████████████████████████████████ 580 clusters, 0.061 aniso
  R3: ███████████████████████████████████ 691 clusters, 0.045 aniso
  R4: ████████████████████ 465 clusters, 0.039 aniso
  R2: ██████████████████ 451 clusters, 0.028 aniso
  R0: ███████████████████████████████████ 695 clusters, 0.020 aniso

→ Weak/no correlation between cluster count and anisotropy
```

## Conclusions

1. **R2_decayDown is the "winner" for channel metrics:**
   - Highest channel capacity (7.417)
   - Highest bridge count (1389)
   - Low anisotropy (symmetric structure)
   - Decay×0.7 creates optimal conditions for channel formation

2. **R1_spawnUp creates fragmented, asymmetric structure:**
   - Lowest channel capacity (1.680)
   - Highest anisotropy (0.0610)
   - Spawn×1.2 fragments the graph

3. **R5_shock needs investigation:**
   - Identical to R0 baseline
   - Shock either didn't work or fully reverted

4. **Channel capacity correlates strongly with bridge count:**
   - More bridges = more cross-region connectivity = higher capacity

5. **Anisotropy is generally low (0.02-0.06):**
   - All configurations produce relatively symmetric structures
   - May need different parameters or longer runs to see higher anisotropy

## Next Steps

1. Investigate R5_shock - why identical to R0?
2. Test at different ticks (100, 200, 300) to see evolution
3. Try higher wdist to see if anisotropy increases
4. Compare with different anisotropy_splits values
