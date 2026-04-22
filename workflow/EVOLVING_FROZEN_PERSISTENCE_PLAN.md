# EVOLVING FROZEN PERSISTENCE PLAN — KROK 39

Purpose:
Define the minimum honest next-step artifact for the stronger Stage 3 claim
that frozen structure can persist across an evolving trajectory,
not only as a single frozen snapshot classification.

This step does NOT implement thaw.
It does NOT introduce propagation mechanics.

---

## 1. CANONICAL BASIS

Relevant local sources:
- `docs/FOUNDATION_PROJECTION.md` section 8
- `docs/MECHANICS_EMERGENCE.md` section 7
- `workflow/FROZEN_PERSISTENCE_PLAN.md`
- `conclusions/FROZEN_PERSISTENCE_INTERIM.md`
- `workflow/TICK_HORIZON_ASSESSMENT.md`

Canonical statements already in the repo:
- frozen configurations still exist relationally
- during freeze, structure persists
- during freeze, no propagation occurs

Current project state after KROK 38:
- we can classify single logs as:
  - `supports_persistence`
  - `frozen_without_persistence_support`
  - `not_frozen`
- this is enough for snapshot-level support
- it is not enough for evolving persistence across time

---

## 2. WHAT IS STILL MISSING

The missing stronger claim is not:
- can freeze and structure coexist at least once?

That is already supported.

The missing stronger claim is:
- can a run remain frozen while retaining structure
  across a non-trivial interval of ticks?

This is the smallest useful meaning of:
- evolving frozen persistence

It remains intentionally weaker than:
- thaw recovery
- propagation absence as a measured field dynamic
- loop persistence

---

## 3. RECOMMENDED MVP TARGET

Define one narrow Stage 3 target:

### Evolving Frozen Persistence Target

A run supports evolving frozen persistence if there exists
one contiguous interval of length `L_persist`
such that for every tick in that interval:
- `freeze_state == true`
- `visible_edges > 0`

Recommended first parameter:
- `L_persist = 20`

Reason:
- long enough to exceed a one-tick coincidence
- short enough to remain practical in current logs
- naturally aligned with the current 20-tick tail convention

This target uses current observables only.

---

## 4. TICK-HORIZON IMPLICATION

This stage should not use `100` ticks as the default.

Reason:
- a persistence interval target is horizon-sensitive by construction
- the current project already reassessed `100` as a short-horizon baseline only

Recommended horizon policy for this stage:
- `300` ticks default
- `500` ticks if the run still saturates or if the interval target is too easy

This keeps the stage aligned with:
- `workflow/TICK_HORIZON_ASSESSMENT.md`

---

## 5. IMPLEMENTATION OPTIONS

Two honest options exist.

### Option A — Extend the Persistence Validator

Add an interval-based mode to the persistence validator.

Recommended result classes:
- `supports_evolving_persistence`
- `frozen_but_not_persistent_enough`
- `supports_persistence`
- `frozen_without_persistence_support`
- `not_frozen`
- `legacy_only`

Advantage:
- builds directly on KROK 38
- no engine changes required
- keeps semantics explicit

### Option B — Controlled Longer Run

Create one controlled longer-horizon run
designed to maintain:
- `freeze_state == true`
- `visible_edges > 0`
for at least `L_persist` ticks.

Advantage:
- produces a concrete Stage 3 control artifact

Risk:
- can drift into experiment tuning before the criterion is encoded clearly

Recommended order:
- do Option A first
- use Option B only if no existing or trivial control log satisfies the interval target

---

## 6. RECOMMENDED VALIDATOR LOGIC

For each non-legacy tick:
- read `freeze_state`
- read `visible_edges`

Then compute the longest contiguous interval where:
- `freeze_state == true`
- `visible_edges > 0`

Classify:
- if no frozen ticks exist -> `not_frozen`
- if frozen ticks exist but no tick has `visible_edges > 0` -> `frozen_without_persistence_support`
- if frozen ticks with `visible_edges > 0` exist but longest interval < `L_persist`
  -> `frozen_but_not_persistent_enough`
- if longest interval >= `L_persist`
  -> `supports_evolving_persistence`

Legacy logs remain:
- `legacy_only`

This keeps the logic observational and fail-closed.

---

## 7. MINIMAL TEST SET

### Test A — Active run

Expectation:
- `not_frozen`

---

### Test B — Snapshot persistence only

Preconditions:
- frozen ticks with retained structure exist
- but contiguous interval is shorter than `L_persist`

Expectation:
- `frozen_but_not_persistent_enough`

---

### Test C — Evolving frozen persistence

Preconditions:
- one contiguous interval satisfies:
  - `freeze_state == true`
  - `visible_edges > 0`
  - length >= `L_persist`

Expectation:
- `supports_evolving_persistence`

---

### Test D — Frozen without persistence support

Expectation:
- `frozen_without_persistence_support`

---

### Test E — Legacy compatibility

Expectation:
- `legacy_only`

---

## 8. WHAT NOT TO DO YET

Do NOT in this step:
- implement thaw
- define recovery triggers
- require explicit propagation metrics
- require loop detection
- promote this to a new hypothesis

This remains a Stage 3 capability-closure step only.

---

## 9. CLOSURE ARTIFACTS

KROK 39 is complete when these artifacts exist:

1. this plan
2. updated workflow memory
3. updated test-grid guidance

KROK 39 does NOT yet prove evolving persistence.
It defines the narrowest honest target for proving it.

---

## 10. NEXT IMPLEMENTATION MOVE

Recommended next action after this note:
- extend `validation/validate_frozen_persistence.py`
  with an interval-based evolving-persistence mode

That should become KROK 40.

Only after that should we decide
whether a dedicated longer-horizon control experiment is still needed.

---

End of plan
