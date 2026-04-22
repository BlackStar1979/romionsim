# FREEZE / THAW STAGE PLAN — KROK 33

Purpose:
Define the minimum plan for introducing freeze-state detection
after projection-layer separation.

Target canonical basis:
- `docs/THEORY_V3.9.md` section II.4
- `docs/FOUNDATION_PROJECTION.md` section 8
- `docs/MECHANICS_EMERGENCE.md` section 7
- `workflow/ENGINE_TEST_GRID.md`

Scope:
This stage plans and enables explicit freeze detection only.
It does NOT implement thaw mechanics yet.

---

## 1. WHY THIS STAGE IS NEXT

After KROK 32 the engine now logs bridge-related observables:
- `bridge_edges`
- `bridge_ratio`
- projection regime fields

This unlocks the next canonical question:
- when is FRACTURE present structurally but inactive dynamically?

The docs define freeze as a bridge-level condition,
not as disappearance of structure.

So the next correct move is:
- make freeze explicit in logs,
- keep it separate from invalidity,
- defer thaw until freeze is reliable.

---

## 2. CANONICAL REQUIREMENT

From `docs/THEORY_V3.9.md` section II.4:
- a Freeze State exists when:
  - `bridges_count == 0` OR
  - `bridges_weight == 0`

From `docs/FOUNDATION_PROJECTION.md` section 8:
- freeze is a projection phenomenon,
- frozen configurations still exist relationally,
- freeze is not annihilation,
- freeze is not low-quality output.

From `docs/MECHANICS_EMERGENCE.md` section 7:
- during freeze, structure persists,
- no propagation occurs,
- thaw requires reopening bridge channels later.

Operational implication:
- freeze must be defined using bridge observables only,
- it must not be inferred from `visible_ratio == 0`,
- it must not be treated as error or invalid state.

---

## 3. MINIMUM DESIGN GOAL

Add explicit freeze-state reporting to FRACTURE snapshots.

Minimum new outputs:
- `freeze_state`
- `freeze_reason`

Recommended semantics:
- `freeze_state = true` if:
  - `bridge_edges == 0`
  - OR future `bridge_weight == 0`
- `freeze_state = false` otherwise

Recommended `freeze_reason` values:
- `no_bridges`
- `zero_bridge_weight`
- `active`
- `not_applicable`

At current MVP level, only `no_bridges` and `active` are immediately testable,
because bridge weight is not yet logged separately.

---

## 4. DEPENDENCY ON CURRENT IMPLEMENTATION

Current bridge observables after KROK 32:
- `bridge_edges`
- `bridge_ratio`

Missing for full canonical freeze rule:
- explicit `bridge_weight`

Therefore the stage should be split:

### Stage 3A — Freeze Detection (now)
- define freeze from `bridge_edges == 0`
- log explicit freeze fields
- validate that freeze is not confused with invalidity

### Stage 3B — Freeze Refinement (later)
- add `bridge_weight`
- extend rule to:
  - `bridge_edges == 0`
  - OR `bridge_weight == 0`

### Stage 3C — Thaw Mechanics (future)
- only after freeze logging is reliable

This keeps the stage honest and incremental.

---

## 5. REQUIRED CODE CHANGES

Recommended touch points:

1. `engine/boundary/stabilization.py`
   - derive `freeze_state`
   - derive `freeze_reason`
   - only for separated projection modes

2. `engine/fracture/state.py`
   - accept optional freeze fields
   - validate their types

3. `validation/`
   - add a validator for freeze-state consistency

No change required yet in:
- `engine/core/`
- propagation logic
- experiment sweeps

Reason:
- freeze is a projection/FRACTURE-layer property,
- not a CORE evolution primitive.

---

## 6. SEMANTIC RULES

The following must hold:

1. `freeze_state` is meaningful only when projection thresholds are active.
2. Legacy `w_visible` runs should not fabricate freeze fields.
3. `freeze_state = true` must not imply invalid run.
4. `freeze_state = true` must not imply object disappearance.
5. `projection_contaminated = true` and `freeze_state = true` may coexist,
   but contaminated output must remain diagnostic-only.

---

## 7. MINIMAL TEST SET

### Test A — Active canonical state

Preconditions:
- canonical-separated regime
- `bridge_edges > 0`

Expectation:
- `freeze_state == false`
- `freeze_reason == "active"`

---

### Test B — Frozen canonical state

Preconditions:
- canonical-separated regime
- `bridge_edges == 0`

Expectation:
- `freeze_state == true`
- `freeze_reason == "no_bridges"`

---

### Test C — Legacy compatibility

Preconditions:
- legacy `w_visible` run only

Expectation:
- no freeze fields are emitted
- existing experiments remain compatible

---

### Test D — Diagnostic contaminated regime

Preconditions:
- contaminated projection regime

Expectation:
- if freeze fields are emitted, they must remain clearly diagnostic
- no canonical conclusion may be inferred automatically

---

## 8. WHAT NOT TO DO YET

Do NOT in this stage:
- implement thaw mechanics,
- add fracture shock or structural fracture interventions,
- mix freeze with loop logic,
- define propagation behavior,
- add recovery triggers,
- claim that bridge absence explains all low-visibility runs.

The old `SPEC_THAW_SHOCK.md` is useful only as a warning:
- it jumps too quickly from freeze diagnosis to an intervention design.

For the current rebuild, we should not do that.

---

## 9. CLOSURE ARTIFACTS

This stage plan is fully realized at Stage 3A when these artifacts exist:

1. this stage plan
2. one implementation pass for explicit freeze logging
3. one validator for freeze-state consistency
4. one conclusions artifact stating what freeze means at MVP level

After that, the next honest move is freeze refinement,
not thaw implementation.

---

## 10. NEXT IMPLEMENTATION MOVE

Recommended next action after Stage 3A closure:
- add explicit `bridge_weight`
- refine freeze semantics from:
  - `bridge_edges == 0`
  - to `bridge_edges == 0 OR bridge_weight == 0`
- keep thaw out of scope until that refinement is validated

Smallest useful next slice:
- one design note for bridge-weight logging
- one design note for refined freeze validation
- no recovery or thaw semantics yet

---

End of plan
