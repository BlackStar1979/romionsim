# Experiment: exp_mvp_stability_sweep

Status: prerelease technical sweep

---

## Goal

Measure FRACTURE stability under variation of two engine parameters:
- p_decay
- w_visible

using a fixed stability metric: FRACTURE_SURVIVAL_TIME(θ = 0.1).

---

## Parameters

- p_decay ∈ {0.99, 0.995, 0.999}
- w_visible ∈ {0.015, 0.02, 0.03}

All other parameters and seed are fixed.

---

## Metric

- FRACTURE_SURVIVAL_TIME(θ = 0.1)

as defined in:
analysis/metrics/FRACTURE_SURVIVAL_TIME_v1.md

---

## Interpretation Boundary

This experiment maps parameter sensitivity only.
No physical interpretation is claimed.

---

End of spec