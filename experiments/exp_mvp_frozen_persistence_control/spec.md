# EXPERIMENT SPEC — MVP Frozen Persistence Control

Purpose:
Produce the first narrow non-synthetic Stage 3C control family
for evolving frozen persistence.

This experiment follows:
- `workflow/EVOLVING_FROZEN_PERSISTENCE_CONTROL_PLAN.md`
- `workflow/TICK_HORIZON_ASSESSMENT.md`

---

## Registered Goal

Test whether the current engine can produce,
under explicit canonical-separated thresholds,
at least one real run classified as:
- `supports_evolving_persistence`

using:
- `L_persist = 20`
- `ticks = 300`

---

## Registered Lane

Fixed scaffold for this first pass:
- `seed = 42`
- `n_nodes = 50`
- `ticks = 300`
- `spawn_scale = 1.0`
- `decay_scale = 1.0`
- `w_init_min = 0.01`
- `w_init_max = 0.05`
- `p_add = 0.05`
- `p_decay = 0.995`
- `w_prune = 0.0`
- `w_visible = 0.02`
- `w_cluster = 0.025`
- `w_dist = 0.015`

Only varied family:
- `w_bridge`

Registered values:
- `0.0200`
- `0.0225`
- `0.0250`

---

## Acceptance Logic

Primary validator:
- `validation/validate_frozen_persistence.py --mode evolving --l-persist 20`

Success condition for this first family:
- at least one run returns `supports_evolving_persistence`

Preferred stronger success:
- the same run shows an earlier active phase before the frozen persistent interval

If no run succeeds:
- family is still valid,
- result is negative / inconclusive for this narrow lane,
- next move is decided by workflow, not improvised tuning.

---

## What This Experiment Does NOT Claim

It does not claim:
- thaw recovery
- loop persistence
- propagation metrics
- scaffold robustness
- cosmological interpretation

This is a Stage 3 capability-control experiment only.

---

End of spec
