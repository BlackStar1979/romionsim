# ENGINE TEST GRID — ROMION

Purpose:
Map canonical `docs/` fragments to a practical engine-test sequence.
This document answers three questions:
- what is already testable,
- what is blocked by missing engine capability,
- what order of stages is most efficient to close.

Scope:
This is an operational planning document.
It does not modify canonical theory or hypothesis content.

Basis used for this grid:
- `docs/THEORY_V3.9.md`
- `docs/FOUNDATION_PROJECTION.md`
- `docs/MECHANICS_EMERGENCE.md`
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `docs/SPEC_LOOP_CLASSES.md`
- `docs/HYPOTHESIS_PHASE_PROPAGATION.md`
- `docs/HYPOTHESIS_CWD_DIPOLE.md`
- `docs/ENGINE_MVP_SCOPE.md`
- `docs/ENGINE_CONTRACT.md`

---

## 1. CURRENT ENGINE-LEVEL CAPABILITIES

Confirmed from the current implementation:
- explicit params and schema-versioned logs,
- CORE graph evolution,
- simple pressure proxy (`mean_pressure`),
- boundary stabilization by visibility threshold,
- FRACTURE observables:
  - `visible_edges`
  - `visible_weight`
  - `visible_ratio`
- projection thresholds:
  - `w_cluster`
  - `w_dist`
  - `w_bridge`
- projection summary fields:
  - `background_edges`
  - `background_ratio`
  - `bridge_edges`
  - `bridge_weight`
  - `bridge_ratio`
  - `projection_regime`
  - `projection_contaminated`
- explicit freeze fields:
  - `freeze_state`
  - `freeze_reason`
- loop summary fields:
  - `loop_count`
  - `max_loop_length`
  - `min_loop_length`
  - `mean_loop_length`
  - `loop_edge_coverage_ratio`
  - `loop_detection_regime`
- experiment automation and CSV-based analysis.

Not currently implemented as engine capabilities:
- separate geometry graph vs bridge graph,
- thaw mechanics,
- loop identity / canonical signature,
- loop orientation / topological charge,
- niche identity,
- exclusion enforcement events,
- phase-mode propagation,
- anisotropy partition / dipole proxy.

---

## 2. TEST GRID

### Stage 0 — Contract / Audit Layer

Docs basis:
- `ENGINE_CONTRACT.md`
- `ENGINE_MVP_SCOPE.md`
- `THEORY_V3.9.md` sections VI.10–VI.13

Question:
Does the engine satisfy the minimal contract of explicitness,
reproducibility, fail-closed logging, and CORE/FRACTURE separation?

Feasibility:
- ready now

Status:
- effectively covered already

Closure artifact:
- validation scripts
- smoke experiment
- working memory + conclusions trail

Why this stage matters:
- every later result is invalid if contract compliance is weak

---

### Stage 1 — Boundary Visibility / Stability Region

Docs basis:
- `MECHANICS_EMERGENCE.md` sections 2–4
- `FOUNDATION_PROJECTION.md` section 3
- `ENGINE_MVP_SCOPE.md` boundary + FRACTURE requirements

Question:
Does stabilization produce a reproducible visible FRACTURE regime,
and does the visibility boundary behave coherently under parameter change?

Current proxies:
- `FRACTURE_SURVIVAL_TIME(theta = 0.1)`
- `TAIL_MEAN_VISIBLE_RATIO_N20`
- `final_visible_ratio`

Feasibility:
- ready now

Status:
- closed for the current MVP pass

Closure artifact:
- existing sweep + refine CSVs
- `conclusions/FRACTURE_STABILITY_INTERIM.md`
- `conclusions/FRACTURE_STABILITY_REFINE_INTERIM.md`
- `conclusions/FRACTURE_STABILITY_SECONDARY_METRIC.md`
- `hypotheses/HYPOTHESIS_FRACTURE_STABILITY_V1_TEST.md`

---

### Stage 2 — Projection Layer Separation

Docs basis:
- `FOUNDATION_PROJECTION.md` sections 4–6
- `THEORY_V3.9.md` section II.5

Question:
Does the engine correctly separate:
- object stabilization,
- geometry-supporting relations,
- bridge / interaction relations?

Required capabilities:
- explicit `w_cluster`, `w_dist`, `w_bridge`
- distinct derived graphs or equivalent logs
- fail-closed rejection of mixed-layer metrics

Feasibility:
- implemented at minimum useful level

Why this should be next:
- it unlocks multiple later tests,
- it directly targets a canonical foundation document,
- it is a cleaner dependency than jumping straight to exotic hypotheses.

Minimal test set after implementation:
1. threshold separation test
2. graph-role consistency test
3. invalid mixed-layer metric rejection test

Closure criterion:
- projection layers are logged distinctly,
- no layer-mixing ambiguity remains,
- one conclusions artifact documents passing behavior.

Status:
- closed at the current MVP level via:
  - explicit threshold params,
  - `projection_regime`,
  - `projection_contaminated`,
  - background / bridge summary fields,
  - `validation/validate_projection_modes.py`,
  - `conclusions/PROJECTION_LAYER_SEPARATION_INTERIM.md`

---

### Stage 3 — Freeze / Thaw Phase Behavior

Docs basis:
- `THEORY_V3.9.md` section II.4
- `MECHANICS_EMERGENCE.md` section 7
- `FOUNDATION_PROJECTION.md` section 8

Question:
Can the engine distinguish active vs frozen FRACTURE states
using bridge activity rather than object disappearance?

Required capabilities:
- bridge observables
- explicit freeze-state criteria in logs
- ideally reactivation / thaw pathway

Feasibility:
- freeze detection is now implemented at MVP level
- thaw mechanics remain unimplemented

Minimal test set after implementation:
1. freeze detection test
2. frozen-not-annihilated persistence test
3. thaw recovery test

Closure criterion:
- frozen runs are identifiable without reinterpretation,
- freeze is not conflated with invalidity or annihilation.

Status:
- partially closed at Stage 3A via:
  - explicit `freeze_state`
  - explicit `freeze_reason`
  - `validation/validate_freeze_modes.py`
  - `conclusions/FREEZE_STATE_INTERIM.md`
- refined at Stage 3B via:
  - explicit `bridge_weight`
  - refined freeze validation for `zero_bridge_weight`
  - `conclusions/FREEZE_STATE_REFINED_INTERIM.md`
- persistence support is now validated via:
  - `validation/validate_frozen_persistence.py`
  - `conclusions/FROZEN_PERSISTENCE_INTERIM.md`
- evolving frozen persistence is now validator-tested via:
  - `validation/validate_frozen_persistence.py --mode evolving`
  - `conclusions/EVOLVING_FROZEN_PERSISTENCE_INTERIM.md`
- non-synthetic evolving frozen persistence is now control-tested via:
  - `experiments/exp_mvp_frozen_persistence_control/`
  - `conclusions/EVOLVING_FROZEN_PERSISTENCE_CONTROL_INTERIM.md`
- not yet closed for full Stage 3 because:
  - thaw recovery is not implemented,
  - thaw recovery is still not tested as a real capability.
- Stage 3B planning is now captured in:
  - `workflow/BRIDGE_WEIGHT_FREEZE_REFINEMENT_PLAN.md`
- frozen-persistence planning is now captured in:
  - `workflow/FROZEN_PERSISTENCE_PLAN.md`
- evolving frozen-persistence planning is now captured in:
  - `workflow/EVOLVING_FROZEN_PERSISTENCE_PLAN.md`
- evolving frozen-persistence control planning is now captured in:
  - `workflow/EVOLVING_FROZEN_PERSISTENCE_CONTROL_PLAN.md`

---

### Stage 4 — Loop Detection / Loop-State Stability

Docs basis:
- `THEORY_V3.9.md` section III.1–III.3
- `MECHANICS_EMERGENCE.md` section 4
- `SPEC_LOOP_CLASSES.md`

Question:
Can the engine detect and track loop-like stabilized structures
as explicit analytical objects?

Required capabilities:
- loop detection in projected structure
- explicit loop metrics:
  - topological length
  - stability proxy
  - optional orientation / charge placeholders
- run-to-run reproducible loop summaries

Feasibility:
- partially unlocked at MVP level

Minimal test set after implementation:
1. loop detection sanity test
2. loop persistence across ticks test
3. loop-class reproducibility test

Closure criterion:
- loops are no longer inferred indirectly from `visible_ratio`,
- at least one loop-based summary can be validated and compared across runs.

Planning status:
- Stage 4 planning is now captured in:
  - `workflow/LOOP_DETECTION_PLAN.md`

Status:
- partially closed at Stage 4A via:
  - minimal loop summary fields in `fracture`
  - `validation/validate_loop_modes.py`
  - `workflow/loop_test_logs/`
  - `conclusions/LOOP_DETECTION_INTERIM.md`
- Stage 4B planning is now captured in:
  - `workflow/LOOP_PERSISTENCE_PLAN.md`
- Stage 4B is now validator-closed via:
  - `validation/validate_loop_persistence.py`
  - `conclusions/LOOP_PERSISTENCE_INTERIM.md`
- Stage 4C planning is now captured in:
  - `workflow/LOOP_IDENTITY_PLAN.md`
- Stage 4C is now validator-closed via:
  - `validation/validate_loop_identity.py`
  - `workflow/loop_identity_test_logs/`
  - `conclusions/LOOP_IDENTITY_INTERIM.md`
- not yet closed for full Stage 4 because:
  - loop-class reproducibility is not yet tested
  - full exclusion-ready identity is not yet available
  - richer invariants such as orientation, charge, and niche are not yet exposed

---

### Stage 5 — Topological Exclusion

Docs basis:
- `THEORY_V3.9.md` section III.4
- `SPEC_EXCLUSION_MECHANICS.md`

Question:
Does the engine enforce niche uniqueness as a structural rejection rule?

Required capabilities:
- loop identity
- niche identity
- attempted duplicate-state creation path
- rejection logging

Feasibility:
- partially unlocked at audit level

Minimal test set after implementation:
1. duplicate niche-state rejection test
2. non-identical degeneracy allowed test
3. exclusion-event logging test

Closure criterion:
- exclusion violations are rejected structurally,
- allowed degeneracy remains distinguishable,
- exclusion events are auditable, not silent.

Planning status:
- Stage 5 readiness planning is now captured in:
  - `workflow/EXCLUSION_READINESS_PLAN.md`
- Stage 5 ingredient planning is now captured in:
  - `workflow/EXCLUSION_INGREDIENTS_PLAN.md`
- Stage 5 instrumentation planning is now captured in:
  - `workflow/EXCLUSION_INGREDIENT_INSTRUMENTATION_PLAN.md`

Status:
- partially closed at audit level via:
  - `validation/validate_exclusion_readiness.py`
  - `workflow/exclusion_readiness_test_logs/`
  - `conclusions/EXCLUSION_READINESS_INTERIM.md`
- partially closed at instrumentation level via:
  - `validation/validate_exclusion_ingredients.py`
  - `workflow/exclusion_ingredient_test_logs/`
  - `conclusions/EXCLUSION_INGREDIENT_INSTRUMENTATION_INTERIM.md`
- partially closed at candidate-path level via:
  - `validation/validate_exclusion_candidate_path.py`
  - `workflow/exclusion_candidate_path_test_logs/`
  - `conclusions/EXCLUSION_CANDIDATE_PATH_INTERIM.md`
- the audit now distinguishes:
  - legacy-only not-ready cases
  - contaminated not-ready cases
  - operational-identity-only partial readiness
  - candidate-ready synthetic cases
- not yet closed for full Stage 5 because:
  - real duplicate-state candidate paths do not yet exist in the engine
  - no structural rejection events are implemented yet

---

### Stage 6 — Phase Propagation vs Relational Density

Docs basis:
- `HYPOTHESIS_PHASE_PROPAGATION.md`
- `MECHANICS_EMERGENCE.md` sections 5–6, 9
- `FOUNDATION_PROJECTION.md`

Question:
Does propagation slow down in denser / higher-tension relational regions?

Required capabilities:
- bridge graph
- explicit propagation mode
- pre-registered density proxy
- propagation arrival metric

Feasibility:
- blocked by Stages 2 and 3

Minimal test set after implementation:
1. fixed-threshold propagation experiment
2. density proxy correlation test
3. multi-seed robustness test

Closure criterion:
- either a stable monotonic relation is found,
- or the hypothesis is cleanly falsified.

---

### Stage 7 — CWD Dipole / Loop-Repetition Cost Bias

Docs basis:
- `HYPOTHESIS_CWD_DIPOLE.md`
- `SPEC_LOOP_CLASSES.md`
- `SPEC_EXCLUSION_MECHANICS.md`

Question:
Can loop repetition asymmetry produce a durable anisotropy proxy?

Required capabilities:
- loop repetition metric
- region split rule
- anisotropy proxy
- multi-seed comparison

Feasibility:
- blocked by Stages 4 and 5

Minimal test set after implementation:
1. repeat-rate metric registration
2. anisotropy proxy experiment
3. repeat-rate vs anisotropy coupling test

Closure criterion:
- either sustained anisotropy emerges under pre-registered conditions,
- or the hypothesis is rejected fail-closed.

---

## 3. RECOMMENDED ORDER

Optimal order for the next major stages:

1. Stage 4 — Loop Detection / Loop-State Stability
2. Stage 5 — Topological Exclusion
3. Stage 6 — Phase Propagation vs Relational Density
4. Stage 7 — CWD Dipole / Loop-Repetition Cost Bias

Reasoning:
- Stage 2 is closed and the freeze-side part of Stage 3 now has a real control artifact.
- Thaw remains explicitly deferred rather than silently half-implemented.
- Stages 4 and 5 unlock the loop ontology already present in THEORY.
- Stages 6 and 7 are hypothesis-heavy and should not start before enabling observables exist.

---

## 4. STAGE-CLOSURE POLICY

The most efficient way to close stages is not by document count,
but by capability bands.

For each stage, close it only when all four artifacts exist:

1. one pre-registered test target
2. one executable experiment or validator path
3. one human-readable conclusion artifact
4. one workflow-memory update

Additional rule:
- update `hypotheses/` only if the stage directly tests a hypothesis,
- otherwise close the stage in `conclusions/` + `workflow/` only.

This keeps closure lightweight:
- contract / capability stages close in `conclusions/` and `workflow/`,
- hypothesis stages additionally update `hypotheses/*_TEST.md`.

---

## 5. NEXT OPTIMAL MOVE

Recommended next stage:
- Repo hygiene — first snapshot planning after local Git bootstrap

Recommended immediate output:
- one narrow repo-hygiene note for:
  - first local snapshot scope
  - what should enter the first commit
  - what should stay out pending later review

Reason:
- Stage 5 audit is closed,
  KROK 53 closes richer identity instrumentation,
  KROK 55 closes candidate-path signaling,
  KROK 56 narrows the first enforcement point,
  KROK 57 closes explicit rejection signaling,
  KROK 58 closes rejection-outcome planning,
  KROK 59 closes rejection-outcome validation,
  KROK 60 closes minimal-enforcement planning,
  KROK 61 closes minimal-enforcement validation,
  KROK 62 closes contract narrowing,
  KROK 63 closes contract boundary clarification,
  KROK 64 closes promotion planning,
  KROK 65 closes candidate identification,
  KROK 66 closes promotion-gate planning,
  KROK 67 closes promotion-gate assessment,
  KROK 68 closes narrow contract-proposal planning,
  KROK 69 closes narrow contract-proposal note,
  KROK 70 closes contract-patch candidate planning,
  KROK 71 closes contract-patch candidate note,
  KROK 72 closes canonical-patch gate planning,
  KROK 73 closes canonical-patch gate assessment,
  KROK 74 closes human-review packet planning,
  KROK 75 closes human-review packet note,
  KROK 76 closes review-handoff planning,
  KROK 77 closes review-handoff note,
  KROK 78 closes workflow-consolidation planning,
  KROK 79 closes workflow-consolidation execution,
  KROK 80 closes local Git bootstrap,
  KROK 60 closes minimal enforcement planning,
  KROK 61 closes minimal enforcement validation,
  KROK 62 closes contract narrowing,
  KROK 63 closes the explicit contract-boundary note,
  KROK 64 closes promotion planning,
  KROK 65 closes the promotion-candidate note,
  KROK 66 closes the promotion-gate plan,
  and the next honest blocker is promotion-gate assessment
  before broader exclusion implementation is attempted.

---

End of test grid
