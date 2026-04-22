# FRACTURE Stability — Secondary Metric Check

Based on:
- `experiments/exp_mvp_stability_sweep/analysis/stability_table_auto.csv`
- `experiments/exp_mvp_stability_refine/analysis/stability_table_auto.csv`

Metrics:
- `FRACTURE_SURVIVAL_TIME(theta = 0.1)`
- `TAIL_MEAN_VISIBLE_RATIO_N20`

Revision note:
The original reading in this file reflects 100-tick runs.
See:
- `conclusions/TICK_HORIZON_REASSESSMENT_INTERIM.md`

Scaffold note:
The compared runs also share one fixed prerelease scaffold:
`seed = 42`, `n_nodes = 50`, `spawn_scale = 1.0`, `decay_scale = 1.0`,
`w_init_min = 0.01`, `w_init_max = 0.05`, `p_add = 0.05`, `w_prune = 0.0`.
So this cross-check supports a conditional slice of engine behavior,
not a scaffold-independent boundary law.

## Observations

1. `TAIL_MEAN_VISIBLE_RATIO_N20` preserves the same broad regime split already seen with `T_survival`.
2. In the coarse sweep:
   - high-survival runs also show clearly elevated late-time tail means,
   - low-survival runs show strongly reduced or zero tail means.
3. In the refine pass for `p_decay = 0.995`, the secondary metric decreases monotonically with increasing `w_visible`.
4. In the original 100-tick refine data, the secondary metric suggested a comparatively elevated late-time range through `w_visible = 0.026`,
   with decline becoming visible near `0.027`.
5. Longer-horizon reassessment shows that this boundary reading is horizon-sensitive:
   - the broad monotonic degradation survives,
   - but the crisp `0.026/0.027` break becomes much weaker at 300 ticks.
6. The secondary metric adds information beyond `final_visible_ratio` because it summarizes the late-time window rather than only the final tick.

## Technical Reading

`TAIL_MEAN_VISIBLE_RATIO_N20` behaves as a late-time plateau metric.
It does not depend on a threshold crossing and therefore provides
an independent cross-check of the stability region identified by `T_survival`.

For the original 100-tick refine pass, both metrics pointed to the same short-horizon mechanical boundary picture.

After horizon reassessment, the secondary metric should no longer be used
as evidence for a sharp boundary beginning specifically at `w_visible = 0.027`.
It still supports a broad degradation trend,
but not the earlier crisp boundary wording.

## Interpretation Boundary

These results characterize engine mechanics only.
No physical or ontological interpretation is claimed.
No scaffold-independence claim is claimed.

End.
