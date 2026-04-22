# BRIDGE WEIGHT / FREEZE REFINEMENT PLAN — KROK 35

Purpose:
Define the minimum honest plan for refining freeze semantics
from the current Stage 3A proxy:
- `bridge_edges == 0`

to the fuller canonical rule:
- `bridge_edges == 0 OR bridge_weight == 0`

This document does NOT introduce thaw mechanics.

---

## 1. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` section II.4
- `docs/FOUNDATION_PROJECTION.md` section 8
- `docs/MECHANICS_EMERGENCE.md` section 7
- `workflow/FREEZE_THAW_STAGE_PLAN.md`
- `workflow/ENGINE_TEST_GRID.md`

Canonical requirement already present in docs:
- freeze exists when:
  - `bridges_count == 0`
  - OR `bridges_weight == 0`

Current implementation after KROK 34:
- logs `bridge_edges`
- logs `freeze_state`
- logs `freeze_reason`
- does NOT log explicit `bridge_weight`

Therefore the current engine closes only Stage 3A,
not the full freeze rule.

---

## 2. WHY THIS REFINEMENT IS NEEDED

`bridge_edges == 0` is a valid fail-closed MVP proxy,
but it is weaker than the canonical rule.

Without explicit `bridge_weight`, the engine cannot distinguish:
- no bridge channels exist,
- bridge channels exist but carry zero active interaction weight.

That distinction matters because the docs treat both as freeze,
but they are not the same observational situation.

So the next honest step is not thaw.
It is making bridge-level weight explicit.

---

## 3. MINIMUM DESIGN GOAL

Add one new bridge-level observable:
- `bridge_weight`

Then refine freeze semantics to:
- `freeze_state = true` if:
  - `bridge_edges == 0`
  - OR `bridge_weight == 0`

Recommended refined reasons:
- `no_bridges`
- `zero_bridge_weight`
- `active`
- `not_applicable`

At this stage:
- do not add thaw,
- do not add propagation,
- do not reinterpret freeze as recovery trigger.

---

## 4. REQUIRED SEMANTIC DECISION

Before implementation, the project should adopt one explicit meaning of
`bridge_weight`.

Recommended MVP meaning:
- `bridge_weight` = sum of weights of all edges satisfying `w >= w_bridge`

Why this definition is the safest current choice:
- it uses already existing edge weights,
- it requires no new ontology,
- it stays inside the projection / bridge layer,
- it is directly serializable,
- it is consistent with current `bridge_edges`.

Not recommended yet:
- normalized bridge energy,
- weighted bridge centrality,
- per-cluster bridge mass,
- time-averaged bridge activity.

Those may be useful later, but they are not needed to close Stage 3B.

---

## 5. REQUIRED CODE CHANGES

Minimal touch points:

1. `engine/boundary/stabilization.py`
   - compute `bridge_weight`
   - add `bridge_weight` to projection-layer summary
   - refine freeze rule using:
     - `bridge_edges`
     - `bridge_weight`

2. `engine/fracture/state.py`
   - accept optional `bridge_weight`
   - validate it as finite and `>= 0`
   - validate consistency:
     - `freeze_reason == "zero_bridge_weight"` requires `bridge_weight == 0`
     - `freeze_reason == "active"` requires positive bridge support

3. `validation/`
   - add or extend validator coverage for:
     - active with positive `bridge_weight`
     - frozen by zero `bridge_weight`
     - frozen by zero `bridge_edges`

No change required yet in:
- `engine/core/`
- loop logic
- thaw behavior
- hypothesis files

---

## 6. RECOMMENDED FAIL-CLOSED RULES

The following should hold after refinement:

1. Legacy runs must still omit:
   - `bridge_weight`
   - `freeze_state`
   - `freeze_reason`

2. If `bridge_weight` is emitted, then:
   - `projection_regime` must also be emitted
   - `bridge_edges` must also be emitted

3. `bridge_weight` must be:
   - finite
   - `>= 0`

4. `freeze_reason = "zero_bridge_weight"` is valid only if:
   - `bridge_edges > 0`
   - `bridge_weight == 0`

5. `freeze_reason = "no_bridges"` is valid only if:
   - `bridge_edges == 0`

6. `freeze_reason = "active"` is valid only if:
   - `bridge_edges > 0`
   - `bridge_weight > 0`

7. Diagnostic contaminated runs may emit `bridge_weight`,
   but the result remains diagnostic-only.

---

## 7. MINIMAL TEST SET FOR STAGE 3B

### Test A — Active canonical state

Preconditions:
- `canonical_separated`
- `bridge_edges > 0`
- `bridge_weight > 0`

Expectation:
- `freeze_state == false`
- `freeze_reason == "active"`

---

### Test B — Frozen by no bridges

Preconditions:
- `canonical_separated`
- `bridge_edges == 0`

Expectation:
- `freeze_state == true`
- `freeze_reason == "no_bridges"`

---

### Test C — Frozen by zero bridge weight

Preconditions:
- `canonical_separated`
- `bridge_edges > 0`
- `bridge_weight == 0`

Expectation:
- `freeze_state == true`
- `freeze_reason == "zero_bridge_weight"`

Note:
- this test may require a targeted synthetic or controlled run,
  because ordinary positive-weight logs may not reach it naturally.

---

### Test D — Legacy compatibility

Preconditions:
- `legacy_visible_only`

Expectation:
- no `bridge_weight`
- no freeze fields

---

### Test E — Diagnostic contaminated regime

Preconditions:
- `diagnostic_contaminated`

Expectation:
- fields may exist,
- no canonical inference is made automatically.

---

## 8. WHAT NOT TO DO YET

Do NOT in this step:
- implement thaw,
- add recovery triggers,
- add propagation semantics,
- normalize freeze into a ranked score,
- create a new hypothesis document,
- claim physical meaning for bridge-weight behavior.

This remains a capability-refinement stage only.

---

## 9. CLOSURE ARTIFACTS

KROK 35 is complete when these artifacts exist:

1. this design note
2. updated workflow memory
3. updated test-grid guidance

KROK 35 does NOT implement the feature itself.
It only defines the next narrow implementation target.

---

## 10. NEXT IMPLEMENTATION MOVE

Recommended next action after this note:
- implement `bridge_weight` in the boundary/FRACTURE path
- refine freeze validation to distinguish:
  - `no_bridges`
  - `zero_bridge_weight`
  - `active`

That should become KROK 36.

Only after that should thaw planning resume.

---

End of plan
