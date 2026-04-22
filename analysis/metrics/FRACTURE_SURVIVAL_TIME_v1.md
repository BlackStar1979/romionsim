# FRACTURE_SURVIVAL_TIME (v1)

Status: prerelease metric definition  
Scope: technical / methodological only

---

## Purpose

Define a simple, robust metric for temporal stability of FRACTURE
that can be computed directly from engine logs.

This metric is intended for:
- experiment comparison,
- parameter sweeps,
- falsifiable hypothesis formulation.

---

## Definition

Let:

- v(t) = fracture.visible_ratio at tick t
- θ ∈ (0, 1) be a fixed visibility threshold

### FRACTURE_SURVIVAL_TIME

The survival time up to threshold θ is defined as:

T_survival(θ) = max { t | for all τ ≤ t : v(τ) ≥ θ }

Operationally:
- iterate ticks from t = 0,
- find the first tick where v(t) < θ,
- return t − 1,
- if no such tick exists, return (ticks − 1).

---

## Default Threshold

For current MVP experiments, the default threshold is:

θ = 0.1

This value is chosen to:
- exclude near-zero noise,
- clearly distinguish observed regimes,
- remain independent of theoretical interpretation.

---

## Interpretation Boundary

This metric does NOT explain why FRACTURE persists or decays.

It only measures the temporal extent of visibility under a given threshold.

---

## Versioning

- v1: single-threshold survival time (θ = 0.1)
- future versions may include multi-threshold or normalized variants

---

End of definition