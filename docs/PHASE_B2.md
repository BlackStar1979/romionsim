# Phase B.2 — Schema v2.0 & Canonical Metrics

**Status:** COMPLETE ✅  
**Date:** 2026-01-11 (ROMION Semantic Correction Applied)

## Overview

Phase B.2 closes tool and schema gaps from Phase B, ensuring experiments are reproducible and canonical.

**Key achievements:**
1. ✅ Exp 2B: Bridge distance distribution (canonical P(dist|bridge))
2. ✅ Exp 5: Schema v2.0 with complete projection metrics
3. ✅ One-command smoke test (generate + validate + check)
4. ✅ ROMION semantic correction (2026-01-11)

---

## Experiments Status

| Experiment | Status | Implementation |
|------------|--------|----------------|
| Exp 1 | ✅ PASS | Hub dominance bounded |
| Exp 2A | ✅ PASS | Distance ordering (counts) |
| **Exp 2B** | ✅ PASS | **Bridge distance distribution** P(dist\|bridge) |
| Exp 3 | ✅ PASS | Coverage correlation |
| Exp 4 | ❌ FAIL | wcluster-dependent (documented) |
| **Exp 5** | ✅ PASS | **Projection consistency** (v2.0 schema) |

**Final:** 5/6 PASS, 1/6 FAIL (valuable falsification)

---

## Files Added

### Core functionality:
- `core/projection.py` — compute_projection_metrics() for L2-FRACTURE
- `analysis/gravity_test/export.py` — JSON/CSV export for R2 tables

### Testing:
- `tests/unit/test_r2_denominators.py` — Unit tests for canonical R2
- `analysis/phase_b/exp5_check.py` — Automated Exp 5 bounds checker

### Tools:
- `tools/run_phase_b2_v2_smoke.py` — **ONE-COMMAND SMOKE TEST**

### Documentation:
- `docs/PHASE_B2.md` — This file

---

## Quick Start

### Generate & validate schema v2.0 log:

```bash
# One command (all-in-one):
python tools/run_phase_b2_v2_smoke.py

# Manual steps:
python tools/run_phase_b2_v2_smoke.py  # Generates results/phase_b2_smoke.jsonl
python scripts/validate_log_schema.py results/phase_b2_smoke.jsonl  # → VALID
python analysis/phase_b/exp5_check.py results/phase_b2_smoke.jsonl  # → PASS
```

**Expected output:**
```
✅✅ SMOKE TEST PASSED ✅✅
```

### Minimal parameters (smoke run):
- **Nodes:** 200
- **Ticks:** 20
- **STATE events:** 5 (every 5 ticks)
- **Runtime:** ~10 seconds

---

## Schema v2.0 Requirements

**Required fields in STATE events:**

```python
{
  'type': 'STATE',
  'tick': int,
  
  'metrics_pre': {
    'layer': 'L1-CORE',
    'computed_before_U': True,
    'mean_kappa': float,
    'mean_pressure': float,
    'mean_frustration': float,  # Required
    'total_weight': float,
    'n_edges': int,
    'n_nodes': int
  },
  
  'metrics_post': {
    'layer': 'L1-CORE',
    'computed_after_U': True,
    'mean_kappa': float,        # Required for Exp 5
    'mean_pressure': float,
    'mean_frustration': float,  # Required
    'total_weight': float,
    'n_edges': int,
    'n_nodes': int
  },
  
  'projection': {
    'layer': 'L2-FRACTURE',
    'uses_metrics_post': True,  # Must be True
    'theta': float,              # Required for Exp 5
    'visible_edges': int,
    'visible_ratio': float,      # Required for Exp 5
    'mean_kappa_visible': float  # Required for Exp 5
  },
  
  'evolution': {...},
  'observables': {...}
}
```

---

## Exp 2B: Bridge Distance Distribution

**ROMION SEMANTICS (2026-01-11 Correction):**

The canonical metric is **P(dist | bridge)** — the probability distribution of distances
FOR ACTUAL BRIDGED PAIRS, not hypothetical "candidate pairs".

**Implementation:** `analysis/gravity_test/distances.py`

**Key function:**
```python
def distance_table(bridges, dists) -> List[Dict]:
    """
    ROMION SEMANTICS:
    Computes P(dist | bridge) - probability distribution of distances
    FOR ACTUAL BRIDGED PAIRS.
    
    Returns:
        [{
            'dist': d,
            'bridged_pairs': count,           # Pairs with bridges at distance d
            'p_dist_given_bridge': float,     # PRIMARY: P(dist=d | bridge)
            'bridges': int,
            'weight': float,
            'avg_bridges_per_pair': float,
            'avg_weight_per_pair': float,
            'background_pairs': int,          # DIAGNOSTIC: all pairs at d
            'p_bridge_given_dist': float      # DIAGNOSTIC: P(bridge | dist=d)
        }]
    """
```

**Output format:**
```
BRIDGE DISTANCE DISTRIBUTION:
  Dist   Bridged    P(d|br)    BkgPairs   P(br|d)    Bridges    Weight
  ------------------------------------------------------------------------
  1      1079       1.0000     1079       1.0000     1389       14.659
  2      0          0.0000     8633       0.0000     0          0.000
```

**PRIMARY ROMION METRIC:**
```
P(dist | bridge) = bridged_pairs_at_d / total_bridged_pairs
```

**DIAGNOSTIC (for reference):**
```
P(bridge | dist) = bridged_pairs_at_d / background_pairs_at_d
```

**Interpretation:**
- **Finite range:** If P(dist=1|bridge) ≈ 1.0, field has d_max=1 (nearest-neighbor only)
- **Extended range:** If P(dist|bridge) has non-trivial tail at d≥2, field exhibits long-range coupling

**Validation:**
```python
# Distribution must sum to 1.0
assert abs(sum(row['p_dist_given_bridge'] for row in rows) - 1.0) < 1e-6
```

**Test:**
```bash
python tests/unit/test_r2_denominators.py
```

---

## Exp 5: Mean Kappa Visible Consistency

**Checks:**
1. **Bounds:** `0 ≤ visible_ratio ≤ 1`
2. **Bounds:** `theta ≤ mean_kappa_visible ≤ 1.0`
3. **Selection:** `mean_kappa_visible ≥ mean_kappa` (post)

**Automated checker:**
```bash
python analysis/phase_b/exp5_check.py <log.jsonl>
```

**Exit codes:**
- 0: PASS (all bounds hold)
- 1: FAIL (bounds violated)
- 2: INVALID (missing fields)

---

## Frustration Mode

Current implementation: `frustration_mode = 'exact'`

Schema v2.0 **requires** `mean_frustration` in both metrics_pre and metrics_post.

**Future modes (not yet implemented):**
- `'none'` → mean_frustration = null (WARNING in validator)
- `'approx'` → Fast approximation (to be defined)

---

## Definition of Done

Phase B.2 is considered complete when:

- [x] `python tools/run_phase_b2_v2_smoke.py` → exit 0
- [x] `validate_log_schema.py phase_b2_smoke.jsonl` → VALID
- [x] `analysis/phase_b/exp5_check.py phase_b2_smoke.jsonl` → PASS
- [x] Exp 2B computes canonical R2 (with denominators)
- [x] Tests pass for R2 denominators

**Status: ALL CRITERIA MET ✅**

---

## Next Steps

Phase B.2 is now closed. Choose:

1. **Paper Mode:** Publish Phase B + B.2 results
   - 5 confirmed patterns
   - 1 valuable falsification (hub_share)
   - Complete methodology validation

2. **Phase C:** Metric redesign
   - Fix hub_share wcluster dependency
   - Design cluster-independent field metrics

**Recommendation:** Paper Mode (publication-ready results)

---

## References

- `PHASE_B2_REPORT.md` — Detailed technical report
- `CANONICAL_METRICS.md` — Authoritative metric definitions
- `docs/METHODOLOGY.md` — Fail-closed principles
- `STATUS.md` — Current project status
