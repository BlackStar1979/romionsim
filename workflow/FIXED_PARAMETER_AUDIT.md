# FIXED PARAMETER AUDIT — Inherited and Hardcoded Values

Purpose:
Record which fixed values currently exist in the rebuilt repo,
which of them are explicit and acceptable,
and which of them narrow the scope of earlier conclusions.

This document exists to prevent inherited constants
from being mistaken for canonical or horizon-independent facts.

Companion note:
- `workflow/INHERITED_PARAMETER_ORIGINS.md`
  reconstructs where the main inherited values came from
  in the local old project materials.

---

## 1. AUDIT RESULT

The repo contains four different classes of fixed values:

1. explicit experiment registration values
2. explicit metric-definition defaults
3. fixed experimental scaffold parameters
4. engine-side compatibility fallbacks

These classes must not be mixed together.

---

## 2. EXPLICIT EXPERIMENT REGISTRATION VALUES

These are acceptable when treated as experiment design,
not as universal project defaults.

Observed examples:
- `analysis/automation/run_stability_sweep.py`
  - `PARAM_GRID`
  - `THETA = 0.1`
- `analysis/automation/run_stability_refine.py`
  - `PARAM_GRID`
  - `THETA = 0.1`
- `analysis/automation/generate_refine_runs.py`
  - `P_DECAY = 0.995`
  - `W_VALUES = [0.018 .. 0.030]`
- `analysis/automation/add_tail_metric_to_csv.py`
  - `N_TAIL = 20`
- `workflow/EVOLVING_FROZEN_PERSISTENCE_PLAN.md`
  - `L_persist = 20`

Status:
- explicit
- acceptable as experiment registration
- must be documented whenever reused

Current risk:
- low, if conclusions stay tied to the named experiment or metric version

---

## 3. EXPLICIT METRIC-DEFINITION DEFAULTS

These are fixed by current metric definitions,
so they are not hidden.

Observed examples:
- `analysis/metrics/FRACTURE_SURVIVAL_TIME_v1.md`
  - `theta = 0.1`
- `analysis/metrics/TAIL_MEAN_VISIBLE_RATIO_v1.md`
  - `N = 20`
- `workflow/EVOLVING_FROZEN_PERSISTENCE_PLAN.md`
  - first planned persistence window `L_persist = 20`

Status:
- explicit
- methodological, not ontological
- valid only at the version that defines them

Current contamination assessment:
- no hidden contamination by themselves
- but every conclusion using them is scoped to those versions

---

## 4. FIXED EXPERIMENTAL SCAFFOLD PARAMETERS

These are the most important inherited fixed values
because they shaped multiple completed experiments
while not being varied in the same passes.

Observed across current stability experiments:
- `seed = 42`
- `n_nodes = 50`
- `spawn_scale = 1.0`
- `decay_scale = 1.0`
- `w_max = null`
- `w_init_min = 0.01`
- `w_init_max = 0.05`
- `p_add = 0.05`
- `w_prune = 0.0`

Only these were intentionally swept in the completed stability passes:
- `p_decay`
- `w_visible`

Status:
- explicit in `params.json`
- not hidden
- but still fixed scaffold assumptions

Current contamination assessment:
- earlier stability conclusions are NOT universal over engine parameter space
- they are conditional on this scaffold
- this does not erase the findings
- it narrows them to:
  - the current scaffold,
  - the tested horizon policy,
  - and the tested metric versions

Required interpretation:
- previous conclusions should be read as
  "under the current prerelease scaffold"
  rather than
  "for ROMION in general"

Highest-risk fixed scaffold members:
1. `seed = 42`
   - current results are single-seed results, not robustness claims
   - old local materials show that `42` was a reproducibility baseline,
     usually paired with additional seeds such as `123`
2. `n_nodes = 50`
   - current results are size-specific
3. `p_add = 0.05`
   - current stability behavior is conditional on this injection rate
4. `w_init_min = 0.01`, `w_init_max = 0.05`
   - current runs depend on this initial edge-weight band
5. `w_prune = 0.0`
   - current decay and persistence behavior assumes no post-decay pruning

---

## 5. ENGINE-SIDE COMPATIBILITY FALLBACKS

These are the most dangerous values conceptually,
because they sit in code and can look canonical
even though they are only compatibility support.

Observed examples:
- `engine/api/engine.py`
  - `seed=0`
  - `n_nodes=0`
  - `ticks=0`
  - `spawn_scale=1.0`
  - `decay_scale=1.0`
  - `_build_evolution_params()` fallbacks:
    - `w_init_min=0.01`
    - `w_init_max=0.05`
    - `p_add=0.02`
    - `p_decay=0.99`
    - `w_prune=0.0`
    - `w_visible=0.0`
- `engine/core/evolution.py`
  - dataclass defaults with the same MVP values

Status:
- not canonical
- not approved as experimental baselines
- only compatibility / fail-closed support

Current contamination assessment:
- low for completed experiments, because current `params.json` files are explicit
- medium future risk, because these fallbacks could be mistaken for recommended defaults

Required interpretation:
- these are implementation fallbacks only
- they must never be cited as recommended experimental settings

Origin note:
- unlike some old historically grounded values,
  these current fallbacks do not carry a strong old protocol justification
  into the rebuilt MVP

---

## 6. WHAT WAS ALREADY CONTAMINATED

### Already revised

1. `ticks = 100`
- previously treated too casually as default
- now revised to:
  - `100` legacy baseline
  - `300` exploratory default
  - `500` for persistence or still-saturating runs

2. earlier 100-tick plateau claims
- already revised in conclusions and hypothesis test artifacts

### Newly identified scope restriction

The remaining stability conclusions are also conditional on the fixed scaffold:
- single seed
- single node count
- single initializer band
- single add-rate and prune policy

This is a scope restriction, not an automatic falsification.

---

## 7. WORKING RULE GOING FORWARD

For every new experiment family:

1. name the swept variables explicitly
2. name the fixed scaffold explicitly
3. state whether a metric default is version-fixed or experiment-fixed
4. never let engine-side fallbacks stand in for experiment registration

Required wording pattern for conclusions:
- "under the current scaffold ..."
- "for the tested horizon ..."
- "for metric version ..."

---

## 8. PRACTICAL OUTCOME OF THIS AUDIT

After this audit:
- no completed conclusion should be read as scaffold-independent
- no engine fallback should be read as canonical
- no new experiment should omit its fixed scaffold from the spec or conclusion layer

This is now the project rule.

End of audit
