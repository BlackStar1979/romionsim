# TAIL_MEAN_VISIBLE_RATIO (v1)

Status: prerelease derived metric
Scope: technical / methodological only

---

## Purpose

Define a secondary FRACTURE stability metric
that does not reuse survival-time logic.

This metric is intended to:
- cross-check late-time stability,
- distinguish sustained high visibility from late decline,
- remain directly computable from engine logs.

---

## Definition

Let:

- v(t) = fracture.visible_ratio at tick t
- N be a positive integer tail-window size

### TAIL_MEAN_VISIBLE_RATIO

The tail mean over the final N ticks is defined as:

TAIL_MEAN_VISIBLE_RATIO(N) = mean { v(t) | t in final N ticks }

Operationally:
- collect all TICK events in order,
- extract fracture.visible_ratio,
- take the last N values,
- if fewer than N ticks exist, use all available ticks,
- return their arithmetic mean.

---

## v1 Parameter

For current MVP experiments, the default tail window is:

N = 20

This value is chosen to:
- sample the late-time regime rather than a single endpoint,
- avoid dependence on a threshold-crossing definition,
- stay compatible with the current 100-tick experiment runs.

---

## Range / Validation

- v(t) is expected in [0, 1]
- the mean must be finite
- if no TICK events exist, the metric is undefined and the run must be rejected

---

## Interpretation Boundary

This metric does NOT explain why FRACTURE remains visible or decays.

It only measures the average late-time visibility level
in the final observation window.

---

## Versioning

- v1: fixed tail-window mean with N = 20
- future versions may vary N or introduce normalized tail summaries

---

End of definition
