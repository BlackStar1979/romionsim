# Manual Decay Sweep - Execution Guide

## Problem Statement

batch_sweep.py verification pokazało że import sys.path fix działa (run_romion_extended.py --help SUCCEEDS), ale długie sweepy timeout'ują w Desktop Commander.

## Solution: Manual Execution

Wykorzystamy istniejące dane + 4 dodatkowe punkty.

## Existing Data (from Test C)

✅ **R0:** decay=1.0, seed=42 → `tests/test_c/results/R0_base/`
✅ **R2:** decay=0.7, seed=42 → `tests/test_c/results/R2_decayDown/`

Results @ tick 400:
- R0: 879 bridges, 3.577 capacity
- R2: 1389 bridges, 7.417 capacity

**Finding:** R2 (slower decay) > R0 (baseline) - paradox confirmed!

## Additional Points Needed

To map decay curve, add 4 intermediate points:

### Point 1: decay=0.85
```powershell
cd C:\Work\romionsim
python scripts/run_romion_extended.py `
  --ticks 600 `
  --decay-scale 0.85 `
  --seed 42 `
  --dump-graph-every 100 `
  --out tests/sweep_decay/manual/d0.85_s42

python analysis/gravity_test.py `
  --log tests/sweep_decay/manual/d0.85_s42/simulation.jsonl `
  --tick 400 `
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0 `
  --wdist-mode threshold --min-cluster-size 2 `
  --channels --anisotropy --anisotropy-splits 5
```

### Point 2: decay=0.75
```powershell
cd C:\Work\romionsim
python scripts/run_romion_extended.py `
  --ticks 600 `
  --decay-scale 0.75 `
  --seed 42 `
  --dump-graph-every 100 `
  --out tests/sweep_decay/manual/d0.75_s42

python analysis/gravity_test.py `
  --log tests/sweep_decay/manual/d0.75_s42/simulation.jsonl `
  --tick 400 `
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0 `
  --wdist-mode threshold --min-cluster-size 2 `
  --channels --anisotropy --anisotropy-splits 5
```

### Point 3: decay=0.65
```powershell
cd C:\Work\romionsim
python scripts/run_romion_extended.py `
  --ticks 600 `
  --decay-scale 0.65 `
  --seed 42 `
  --dump-graph-every 100 `
  --out tests/sweep_decay/manual/d0.65_s42

python analysis/gravity_test.py `
  --log tests/sweep_decay/manual/d0.65_s42/simulation.jsonl `
  --tick 400 `
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0 `
  --wdist-mode threshold --min-cluster-size 2 `
  --channels --anisotropy --anisotropy-splits 5
```

### Point 4: decay=0.6
```powershell
cd C:\Work\romionsim
python scripts/run_romion_extended.py `
  --ticks 600 `
  --decay-scale 0.6 `
  --seed 42 `
  --dump-graph-every 100 `
  --out tests/sweep_decay/manual/d0.6_s42

python analysis/gravity_test.py `
  --log tests/sweep_decay/manual/d0.6_s42/simulation.jsonl `
  --tick 400 `
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0 `
  --wdist-mode threshold --min-cluster-size 2 `
  --channels --anisotropy --anisotropy-splits 5
```

## Data Collection

After running all 4 points, collect results into CSV:

```python
# scripts/collect_decay_results.py
import csv
import re
from pathlib import Path

POINTS = [
    (1.0, "tests/test_c/results/R0_base"),
    (0.85, "tests/sweep_decay/manual/d0.85_s42"),
    (0.75, "tests/sweep_decay/manual/d0.75_s42"),
    (0.7, "tests/test_c/results/R2_decayDown"),
    (0.65, "tests/sweep_decay/manual/d0.65_s42"),
    (0.6, "tests/sweep_decay/manual/d0.6_s42"),
]

# Parse gravity_test output from each point
# Write to: tests/sweep_decay/decay_curve_manual.csv
```

## Expected Timeline

- Each simulation: ~5-10 minutes
- Each analysis: ~30 seconds
- Total: ~30-45 minutes for all 4 points

## Analysis

Once data collected:

1. Plot decay vs bridges_weight
2. Plot decay vs channel_capacity
3. Plot decay vs anisotropy
4. Identify optimal η*

## Hypothesis Test

**H1:** Decay curve is non-monotonic (optimal exists)

Prediction: Peak between 0.6 < η* < 0.8

If confirmed → refine sweep around peak with step=0.02

---

**Status:** READY FOR MANUAL EXECUTION  
**Date:** 2026-01-09  
**Next:** User runs 4 commands manually in PowerShell
