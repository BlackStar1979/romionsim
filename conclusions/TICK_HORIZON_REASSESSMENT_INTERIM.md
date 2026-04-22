# Tick Horizon Reassessment — Interim Conclusion

Based on:
- `workflow/TICK_HORIZON_ASSESSMENT.md`
- `workflow/tick_reassessment/tick_reassessment_100_vs_300.csv`
- current engine behavior under 100- and 300-tick reruns

## Main Result

The earlier `100`-tick baseline is now shown to be a short-horizon protocol choice,
not a safe universal observation horizon.

Under the rebuilt engine:
- runtime no longer justifies keeping `100` as the universal default
- several earlier stability conclusions were right-censored by the `100`-tick horizon

## What Remains Valid

1. The current engine still shows clear parameter sensitivity.
2. Lower `p_decay` still decays faster than higher `p_decay`.
3. `p_decay = 0.999` remains visibly more persistent than `0.995` and `0.99`.
4. The refine ordering for `p_decay = 0.995` still degrades as `w_visible` increases.

These broad mechanical orderings survive the horizon increase.

## What Was Contaminated by 100 Ticks

### 1. The \"maximal plateau\" reading at `p_decay = 0.995`

The earlier refine conclusion said:
- `w_visible ∈ [0.018, 0.026] -> T_survival = 99`

At `300` ticks, the same range becomes approximately:
- `0.018 -> 176`
- `0.019 -> 166`
- `0.020 -> 155`
- `0.021 -> 146`
- `0.022 -> 136`
- `0.023 -> 127`
- `0.024 -> 119`
- `0.025 -> 111`
- `0.026 -> 103`

So the earlier statement of a contiguous maximal plateau
was a horizon-censoring artifact.

### 2. The claim of a crisp secondary-metric boundary near `0.027`

At `100` ticks, `TAIL_MEAN_VISIBLE_RATIO_N20`
looked strongly elevated through `0.026`
and then visibly broke near `0.027`.

At `300` ticks, the tail means compress substantially
and the `0.026/0.027` contrast becomes much weaker.

So the earlier secondary-metric boundary reading
should be treated as short-horizon only.

### 3. The coarse claim that `p_decay = 0.999` remains \"maximal\"

At `100` ticks this was true only because the horizon ended.

At `300` and `1000` ticks,
these runs still remain highly persistent,
but the correct reading is:
- high-stability regime beyond the 100-tick horizon

not:
- conclusively maximal in any horizon-independent sense

## Revised Reading

The current evidence supports this narrower and more honest interpretation:

1. `100`-tick results are valid as short-horizon technical baselines.
2. They are not sufficient to infer long-horizon persistence plateaus.
3. The strongest contamination affects:
   - \"maximal plateau\" claims
   - any conclusion tied to `ticks - 1` saturation
4. Broad parameter ordering remains intact,
   but boundary sharpness and plateau language must be revised.

Additional scope restriction:
The reassessed ordering is still conditional on the fixed prerelease scaffold
used in the original runs:
- `seed = 42`
- `n_nodes = 50`
- `spawn_scale = 1.0`
- `decay_scale = 1.0`
- `w_init_min = 0.01`
- `w_init_max = 0.05`
- `p_add = 0.05`
- `w_prune = 0.0`

So this reassessment repairs horizon overreach,
but it does not yet establish scaffold-robust behavior.

## Recommended Policy

- keep completed 100-tick experiments as historical baseline artifacts
- do not use them alone for long-horizon stability claims
- use `300` ticks as the new default for new exploratory runs
- escalate to `500` when the run still saturates the observation horizon

## Interpretation Boundary

This is a methodological reassessment only.
It does not alter canonical theory.

It does alter how much trust should be placed
in earlier 100-tick mechanical conclusions.

End.
