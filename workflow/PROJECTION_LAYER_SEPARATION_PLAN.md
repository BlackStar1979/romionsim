# PROJECTION LAYER SEPARATION PLAN — KROK 31

Purpose:
Define the minimum implementation plan for introducing
projection-layer separation into the current MVP engine.

Target canonical basis:
- `docs/FOUNDATION_PROJECTION.md`
- `docs/THEORY_V3.9.md` sections II.4, II.5
- `docs/ENGINE_MVP_SCOPE.md`
- `docs/ENGINE_CONTRACT.md`

Scope:
This is a design note for the current codebase.
It is not a claim that the functionality already exists.

---

## 1. WHY THIS STAGE IS NEXT

The current engine has only one projection threshold:
- `w_visible`

This is sufficient for the MVP stability experiments,
but insufficient for testing canonical projection separation.

The next unlock requires explicit distinction between:
- object visibility / stabilization,
- background geometry support,
- bridge / interaction support.

Without that separation, the following remain blocked:
- projection-layer tests,
- freeze/thaw tests,
- phase propagation tests,
- any clean bridge-based observable.

---

## 2. LESSONS FROM THE OLD PROJECT SNAPSHOT

Useful patterns found in `workflow/oldies/romionsim_old_2/`:

1. Separate background vs bridge handling is the right direction.
   Evidence:
   - `docs/theory/MEASUREMENT_THRESHOLDS.md`
   - `tests/unit/test_background_excludes_bridges.py`

2. A contaminated / debug regime should be flagged explicitly,
   not silently treated as canonical.

3. Freeze/thaw ideas were already recognized as bridge-dependent,
   but at least one old spec (`docs/SPEC_THAW_SHOCK.md`) mixed
   real implementation with future design notes too loosely.

4. The old tree accumulated too many layers and side systems.
   For the current rebuild, we should keep the first implementation:
   - minimal,
   - logged,
   - testable,
   - without adding geometry or loop machinery yet.

Operational takeaway:
- keep the implementation narrow,
- separate canonical behavior from diagnostic fallback,
- never describe a planned feature as already present.

---

## 3. MINIMUM DESIGN GOAL

Introduce three explicit projection thresholds in the current engine:
- `w_cluster`
- `w_dist`
- `w_bridge`

And expose one minimal FRACTURE-level projection summary that distinguishes:
- object-supporting edges,
- background-geometry-supporting edges,
- bridge edges.

This stage does NOT require:
- actual geometric distance computation,
- cluster detection,
- loop detection,
- freeze/thaw state machine,
- propagation mode.

It only prepares the observables needed for later stages.

---

## 4. REQUIRED PARAMETER MODEL CHANGES

Current situation:
- `engine/api/engine.py` builds only `w_visible`

Required extension:
- keep `w_visible` temporarily for backward compatibility,
- add explicit optional params in `extra`:
  - `w_cluster`
  - `w_dist`
  - `w_bridge`

Recommended validation rules for Stage 2:
- all thresholds must be finite and >= 0 if provided,
- canonical regime requires:
  - `w_cluster >= w_dist`
  - `w_bridge > w_dist`
- if thresholds are missing:
  - preserve current MVP path using `w_visible`,
  - mark projection-layer outputs as unavailable rather than inventing values.

Important:
Do not silently map all three thresholds to one number in logs.
If a compatibility fallback is used, it must be obvious in metadata.

---

## 5. REQUIRED BOUNDARY-LAYER CHANGES

Current situation:
- `engine/boundary/stabilization.py` produces only:
  - `visible_edges`
  - `visible_weight`
  - `visible_ratio`

Required extension:
create a richer projection summary that can still be serialized safely.

Recommended additions:
- `cluster_edges`
- `cluster_ratio`
- `background_edges`
- `background_ratio`
- `bridge_edges`
- `bridge_ratio`
- `projection_regime`
- `projection_contaminated`

Minimal semantics:
- cluster edges: `w >= w_cluster`
- background edges:
  - canonical regime: `w_dist <= w < w_bridge`
  - if no `w_bridge`, background may include all `w >= w_dist`
    but must be marked non-canonical / incomplete
- bridge edges: `w >= w_bridge`

Important:
This is still a projection summary over CORE edges.
Do not claim that these are already cluster-graph or meta-graph edges.

That richer graph construction belongs to a later stage if needed.

---

## 6. REQUIRED FRACTURE-STATE CHANGES

Current situation:
- `engine/fracture/state.py` stores only visible-edge observables

Required extension:
allow additional projection-layer fields in `FractureState`
without breaking the current log schema order.

Recommended rule:
- keep existing fields unchanged,
- add new optional fields only when projection thresholds are active,
- preserve fail-closed validation for ranges and types.

Suggested optional fields:
- `cluster_edges`
- `cluster_ratio`
- `background_edges`
- `background_ratio`
- `bridge_edges`
- `bridge_ratio`
- `projection_regime`
- `projection_contaminated`

This preserves backward compatibility for existing analysis code.

---

## 7. LOGGING PLAN

Do not change the event order.
Keep:
- `METADATA`
- `PARAMS`
- `TICK`
- `END`

Extend only the payload contents.

Required logging behavior:
1. `PARAMS` must include the final used threshold values.
2. `TICK.fracture` may include new projection fields.
3. `projection_regime` must say whether the run is:
   - `legacy_visible_only`
   - `canonical_separated`
   - `diagnostic_contaminated`

This avoids the old failure mode where a debug regime can be mistaken
for canonical output.

---

## 8. MINIMAL TEST SET FOR THIS STAGE

These tests should be enough to close Stage 2.

### Test A — Canonical separation

Preconditions:
- `w_cluster >= w_dist`
- `w_bridge > w_dist`

Expectation:
- background counts exclude bridge edges,
- `projection_contaminated == false`

---

### Test B — Legacy compatibility

Preconditions:
- only `w_visible` provided

Expectation:
- current visible metrics remain available,
- projection-layer metrics are either absent or explicitly marked legacy,
- no existing sweep scripts break.

---

### Test C — Contaminated diagnostic regime

Preconditions:
- `w_bridge <= w_dist`

Expectation:
- run does not silently claim canonical separation,
- `projection_contaminated == true`,
- output is still loggable and analyzable as diagnostic-only.

---

### Test D — PARAMS explicitness

Expectation:
- all used thresholds are written into `PARAMS`
- no hidden defaults with ontological meaning

---

## 9. IMPLEMENTATION ORDER INSIDE THE CODEBASE

Recommended order:

1. `engine/api/engine.py`
   - accept and log new threshold params

2. `engine/boundary/stabilization.py`
   - implement projection summary logic

3. `engine/fracture/state.py`
   - accept the richer snapshot safely

4. `engine/core/evolution.py`
   - thread the richer boundary output into FRACTURE state

5. validation / experiments
   - add one targeted stage-2 experiment or validator path

Reason:
- this touches the minimum number of files,
- keeps CORE free of geometry semantics,
- concentrates new logic in the boundary layer.

---

## 10. WHAT NOT TO DO IN THIS STAGE

Do NOT:
- implement actual distances,
- invent cluster meta-graphs as if already canonical output,
- add loop detection,
- add freeze/thaw mechanics yet,
- add domain mappings,
- retrofit old architecture wholesale from `romionsim_old_2`.

This stage should remain a narrow enabling layer.

---

## 11. STAGE-CLOSURE OUTPUTS

KROK 31 is complete when these artifacts exist:

1. this design note
2. one implementation pass for threshold separation
3. one validation/test artifact for canonical vs contaminated behavior
4. one conclusions artifact summarizing the result

Only after that should we move to freeze/thaw.

---

## 12. NEXT IMPLEMENTATION MOVE

Recommended next action after this plan:
- implement threshold support and projection summary
  in the boundary/FRACTURE path while preserving current sweeps.

Immediate coding target:
- add explicit threshold parameters
- add `projection_regime` + `projection_contaminated`
- add `background_*` and `bridge_*` counts/ratios

That is the smallest useful vertical slice.

---

End of plan
