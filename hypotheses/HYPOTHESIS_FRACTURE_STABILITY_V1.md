# Hypothesis H1 — FRACTURE Stability Region (v1)

Status: MVP hypothesis  
Based on: stability_table.csv (KROK 26)

---

## Statement

For a fixed visibility threshold θ = 0.1, there exists a non-empty region
in the (p_decay, w_visible) parameter space where
FRACTURE_SURVIVAL_TIME(θ) remains close to its maximum value (≈ ticks − 1),
while outside this region the survival time drops sharply.

---

## Evidence Basis

- Mini-sweep over p_decay ∈ {0.99, 0.995, 0.999}
- Mini-sweep over w_visible ∈ {0.015, 0.02, 0.03}
- Observed survival times range from full-length (99) to short-lived (≤ 36)

---

## Falsification Criterion

This hypothesis is falsified if, after refining the parameter grid,
no contiguous parameter region with consistently high
FRACTURE_SURVIVAL_TIME(θ) can be identified.

---

## Interpretation Boundary

This hypothesis concerns engine mechanics only.
No physical or ontological interpretation is implied.

---

End of hypothesis