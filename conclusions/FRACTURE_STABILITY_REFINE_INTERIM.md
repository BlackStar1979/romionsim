# FRACTURE Stability — Refine Interim (p_decay = 0.995)

Based on: experiments/exp_mvp_stability_refine/analysis/stability_table_auto.csv  
Metric: FRACTURE_SURVIVAL_TIME(theta = 0.1)

Revision note:
The original 100-tick interpretation in this file was right-censored.
See:
- `conclusions/TICK_HORIZON_REASSESSMENT_INTERIM.md`

Scaffold note:
This refine pass also held the remaining prerelease scaffold fixed:
`seed = 42`, `n_nodes = 50`, `spawn_scale = 1.0`, `decay_scale = 1.0`,
`w_init_min = 0.01`, `w_init_max = 0.05`, `p_add = 0.05`, `w_prune = 0.0`.
So the reported ordering is conditional on that scaffold.

## Observations

1. Under the original 100-tick protocol, FRACTURE showed a contiguous horizon-saturating region:
   - w_visible ∈ [0.018, 0.026] -> T_survival = 99

2. A transition region begins at higher w_visible values:
   - w_visible = 0.027 -> T_survival = 95
   - w_visible = 0.028 -> T_survival = 88
   - w_visible = 0.029 -> T_survival = 81
   - w_visible = 0.030 -> T_survival = 74

3. Longer-horizon reassessment shows that the apparent plateau was a short-horizon artifact:
   - at 300 ticks, the same range declines from about 176 down to 103 rather than staying maximal

4. final_visible_ratio decreases monotonically with w_visible across the original 100-tick scanned range.

## Falsification Result (H1)

The original 100-tick refine scan did support the existence of a contiguous horizon-limited region rather than isolated spikes.

After horizon reassessment, the stronger claim of a contiguous maximal plateau is no longer supported.
The broad monotonic degradation remains real,
but the plateau language must be treated as contaminated by 100-tick censoring.

## Interpretation Boundary

These results characterize engine mechanics only.
No physical interpretation is claimed.
No seed-robust or scaffold-robust claim is claimed.

Related hypothesis:
- hypotheses/HYPOTHESIS_FRACTURE_STABILITY_V1.md
- hypotheses/HYPOTHESIS_FRACTURE_STABILITY_V1_TEST.md


End.
