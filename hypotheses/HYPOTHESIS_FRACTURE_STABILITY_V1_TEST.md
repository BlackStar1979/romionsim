# HYPOTHESIS TEST RESULT — FRACTURE_STABILITY_V1

Status: MVP test result revised after tick-horizon reassessment

Reference hypothesis:
- HYPOTHESIS_FRACTURE_STABILITY_V1.md

Evidence sources:
- experiments/exp_mvp_stability_sweep/analysis/stability_table_auto.csv
- experiments/exp_mvp_stability_refine/analysis/stability_table_auto.csv

Metric:
- FRACTURE_SURVIVAL_TIME(theta = 0.1)

Secondary support metric:
- TAIL_MEAN_VISIBLE_RATIO_N20

Methodological revision source:
- conclusions/TICK_HORIZON_REASSESSMENT_INTERIM.md

---

## Outcome

The original 100-tick refine scan (p_decay = 0.995, w_visible in [0.018..0.030])
appeared to show a contiguous region where survival time remained maximal
for a range of w_visible values, followed by decline beyond the boundary.

After reassessment at longer horizons, that maximal-plateau reading
is no longer supported as stated.

What remains supported:
- survival still degrades monotonically with increasing `w_visible`,
- a broad region of higher stability still exists relative to higher-threshold runs,
- the original plateau claim was right-censored by the 100-tick horizon.
- the current evidence remains conditional on the prerelease scaffold
  held fixed during these runs

Secondary metric support:
- TAIL_MEAN_VISIBLE_RATIO_N20 decreases monotonically across the refine range,
- but its earlier sharp boundary picture is also horizon-sensitive,
- so it should now be treated as broad trend support rather than crisp boundary confirmation.

This does not replace the primary hypothesis metric,
but it strengthens the same mechanics-level reading
with an independent late-time summary.

---

## Falsification Status

INCONCLUSIVE after horizon reassessment.

Reason:
- the stronger claim of survival remaining close to maximum
  through the refined `p_decay = 0.995` range
  was contaminated by 100-tick censoring,
- but the broader ordering and non-random degradation pattern remain real
  within the current fixed scaffold.

---

## Interpretation Boundary

This is a mechanics-level result.
No physical interpretation is implied.
No seed-robust or scaffold-robust claim is implied.

End.
