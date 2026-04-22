# EVOLVING FROZEN PERSISTENCE CONTROL PLAN — KROK 41

Purpose:
Define one narrow, registered control-experiment plan
for non-synthetic evolving frozen persistence.

This step does NOT execute the experiment yet.
It does NOT implement thaw.
It does NOT create a new hypothesis document.

---

## 1. CANONICAL BASIS

Relevant local sources:
- `docs/FOUNDATION_PROJECTION.md` section 8
- `docs/MECHANICS_EMERGENCE.md` section 7
- `workflow/FROZEN_PERSISTENCE_PLAN.md`
- `workflow/EVOLVING_FROZEN_PERSISTENCE_PLAN.md`
- `workflow/TICK_HORIZON_ASSESSMENT.md`
- `conclusions/EVOLVING_FROZEN_PERSISTENCE_INTERIM.md`

Current project state after KROK 40:
- snapshot persistence is validator-supported
- evolving persistence is validator-supported
- current evolving-support controls are synthetic
- no non-synthetic registered control run exists yet

So the next honest question is:
- can the current engine produce a real run
  with a non-trivial frozen persistence interval,
  under explicit registered parameters,
  without post-hoc log editing or synthetic tick fabrication?

---

## 2. TARGET CLAIM

The target claim for this control experiment is narrow:

A non-synthetic run supports evolving frozen persistence if:
- it uses the current engine directly,
- it uses explicit canonical-separated thresholds,
- it contains one contiguous interval of length `L_persist`,
- and for every tick in that interval:
  - `freeze_state == true`
  - `visible_edges > 0`

Registered initial interval target:
- `L_persist = 20`

This remains weaker than:
- thaw recovery
- propagation metrics
- loop persistence

---

## 3. WHAT COUNTS AS A GOOD CONTROL

The control should not be a trivial threshold artifact.

So a good control run should satisfy both:

1. It eventually contains an evolving frozen persistence interval:
   - `freeze_state == true`
   - `visible_edges > 0`
   - contiguous length `>= L_persist`

2. It also shows that the frozen interval is not merely forced from tick 0
   by a degenerate bridge cutoff.

Recommended stronger reading:
- the same run should contain at least one earlier non-legacy tick with:
  - `freeze_state == false`
  - `bridge_edges > 0`

This creates a cleaner active → frozen-but-persistent transition
within one registered trajectory.

If the first successful control is frozen from tick 0,
it may still be logged as a weaker control,
but it should be marked:
- `threshold-forced`
and not treated as the preferred Stage 3C artifact.

---

## 4. HORIZON POLICY

This step follows the current post-reassessment horizon rule:

- `300` ticks default
- `500` ticks fallback if:
  - the interval target is still not reached,
  - or the run remains too horizon-sensitive to classify honestly

This step must not default back to `100`.

Reason:
- evolving persistence is horizon-sensitive by construction
- `100` is now only a legacy baseline

---

## 5. PARAMETER POLICY

This step must remain narrow and pre-registered.

### Fixed scaffold for the first control pass

Use the current prerelease scaffold unless the registration note
states a stronger reason to change it:
- `seed = 42`
- current prerelease node count scaffold
- current prerelease initialization band
- current prerelease add / prune scaffold

Important:
- this does NOT make the result scaffold-independent
- it only keeps Stage 3C focused on existence of the control artifact

### Threshold policy

The run must be in:
- `canonical_separated`
not in:
- `legacy_visible_only`
- `diagnostic_contaminated`

Required threshold relation:
- `w_cluster >= w_dist`
- `w_bridge > w_dist`

Exact threshold values must be explicit in the registered `params.json`
for the control run family.

### Narrow search policy

Do not sweep many dimensions at once.

The first control lane should vary only:
- `w_bridge`

Keep:
- `w_cluster`
- `w_dist`
- `w_visible`
- the rest of the current scaffold
fixed for the first pass.

Reason:
- freeze is currently defined from bridge observables
- varying more than one family at once would recreate search bloat

---

## 6. REGISTERED FIRST PASS

Recommended first pass:

### Control Pass C1

Experiment family:
- `exp_mvp_frozen_persistence_control`

Initial run budget:
- 3 registered runs

Shared settings:
- canonical-separated thresholds
- `ticks = 300`
- `L_persist = 20`
- current prerelease scaffold fixed
- one seed only in this step

Only varied parameter family:
- `w_bridge`

Success condition for C1:
- at least one run returns:
  - `supports_evolving_persistence`

Preferred success condition:
- and the same run contains an earlier active phase

Failure meaning for C1:
- no registered `w_bridge` value in the narrow first lane
  produced evolving frozen persistence at `300` ticks

If C1 fails, only then open:

### Control Pass C2

Allowed change:
- increase horizon to `500`

Still fixed:
- same scaffold
- same threshold family
- same one-parameter search lane

Do not change both:
- horizon
- and multiple scaffold parameters
in the same follow-up pass.

---

## 7. WHAT MUST BE WRITTEN INTO THE EXPERIMENT SPEC

When KROK 42 begins,
the experiment spec should explicitly record:

1. target class:
   - `supports_evolving_persistence`
2. interval target:
   - `L_persist = 20`
3. horizon:
   - `300` for C1
4. regime requirement:
   - `projection_regime == canonical_separated`
5. preferred transition evidence:
   - earlier active tick before frozen persistent interval
6. acceptance logic:
   - validator result is authoritative
7. interpretation limit:
   - this is Stage 3 capability closure,
     not proof of thaw, loops, or cosmology

---

## 8. WHAT NOT TO DO

Do NOT in this step:
- tune many parameters at once
- use synthetic logs as the final control artifact
- accept contaminated runs as canonical support
- force freeze by undocumented threshold tricks and call it strong evidence
- open seed robustness yet
- open thaw work yet

This step is only about producing
one honest non-synthetic control artifact.

---

## 9. CLOSURE ARTIFACTS

KROK 41 is complete when these artifacts exist:

1. this control plan
2. updated workflow memory
3. updated test-grid guidance

KROK 41 does NOT yet prove evolving persistence in a real run.
It only registers the narrowest honest path for doing so.

---

## 10. NEXT IMPLEMENTATION MOVE

Recommended next action after this note:
- register and execute the first control family
  `exp_mvp_frozen_persistence_control`
  with a 3-run `w_bridge` lane at `300` ticks

That should become KROK 42.

Only after KROK 42 should we decide whether:
- the control is already sufficient,
- a `500`-tick follow-up is needed,
- or the question should move into robustness work.

---

End of plan
