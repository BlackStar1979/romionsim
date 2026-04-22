# Comparison Conclusion: exp_mvp_smoke vs exp_mvp_smoke_2

Status: prerelease comparison conclusion

---

## Compared Experiments

- exp_mvp_smoke
- exp_mvp_smoke_2

The experiments are identical except for a single parameter:
- exp_mvp_smoke: p_decay = 0.99
- exp_mvp_smoke_2: p_decay = 0.995

All other parameters, seed, number of nodes, and tick count are the same.

---

## Data Sources

- exp_mvp_smoke: experiments/exp_mvp_smoke/analysis/summary.json
- exp_mvp_smoke_2: experiments/exp_mvp_smoke_2/analysis/summary.json

Logs for both experiments passed minimal schema validation.

---

## Observed Differences

### FRACTURE Visibility

- exp_mvp_smoke:
  - visible_ratio_end ≈ 0.019
  - visible_edges_end = 1
  - visible_ratio_slope ≈ −0.0064

- exp_mvp_smoke_2:
  - visible_ratio_end ≈ 0.434
  - visible_edges_end = 23
  - visible_ratio_slope ≈ −0.0022

The decay of FRACTURE visibility is significantly slower
when p_decay is increased.

---

### CORE Weight Evolution

- exp_mvp_smoke:
  - total_weight_slope ≈ −0.0081

- exp_mvp_smoke_2:
  - total_weight_slope ≈ −0.0046

The CORE weight decays more slowly for higher p_decay,
as expected from the multiplicative update rule.

---

## Conclusion

The qualitative behavior observed in exp_mvp_smoke
is not hard-coded into the engine.

The rate of FRACTURE decay is controllable
through the evolution parameter p_decay.

This establishes parametric sensitivity of the MVP engine.

---

## Interpretation Boundary

This document does not propose a physical explanation.
It records a technical comparison of two controlled runs
of the same engine under minimal parameter variation.

---

## Next Step Recommendation

The engine is now ready for first-form hypothesis work.

Possible directions:
- threshold-dependent phase persistence
- existence of quasi-stable FRACTURE regimes
- interaction between p_decay and w_visible

---

End of comparison