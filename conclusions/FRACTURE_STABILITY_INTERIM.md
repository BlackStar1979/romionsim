# FRACTURE Stability — Interim Technical Conclusions

Revision note:
These observations are preserved as 100-tick baseline results only.
See:
- `conclusions/TICK_HORIZON_REASSESSMENT_INTERIM.md`

The broad parameter ordering remains useful,
but any statement tied to 100-tick saturation
must be treated as short-horizon only.

Scaffold note:
These observations were produced under a fixed prerelease scaffold:
`seed = 42`, `n_nodes = 50`, `spawn_scale = 1.0`, `decay_scale = 1.0`,
`w_init_min = 0.01`, `w_init_max = 0.05`, `p_add = 0.05`, `w_prune = 0.0`.
So this file supports a conditional parameter-slice reading,
not scaffold-independent behavior.

Based on: experiments/exp_mvp_stability_sweep/analysis/stability_table_auto.csv

## Observations

1. For theta = 0.1, FRACTURE_SURVIVAL_TIME depends strongly on both parameters p_decay and w_visible.
2. For p_decay = 0.99, increasing w_visible reduces survival time over the 100-tick horizon (99 -> 78 -> 36).
3. For p_decay = 0.995, survival is high over the 100-tick horizon at w_visible <= 0.02 (99) and drops at w_visible = 0.03 (74).
4. For p_decay = 0.999, survival saturates the 100-tick horizon across all tested w_visible values including 0.03.
5. Final visibility at tick 99 correlates with the short-horizon survival regime.

## Interpretation Boundary

These are mechanical conclusions only.
No physical or ontological interpretation is implied.
No scaffold-independence claim is implied either.

End.
