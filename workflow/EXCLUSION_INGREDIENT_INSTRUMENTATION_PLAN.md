# EXCLUSION INGREDIENT INSTRUMENTATION PLAN — KROK 52

Purpose:
Define the smallest honest implementation slice
for emitting exclusion-relevant identity ingredients
without yet implementing exclusion itself.

This step does NOT implement rejection.
This step does NOT implement loop classes.
This step does NOT open thaw or propagation work.

---

## 1. WHY THIS STEP IS NEXT

KROK 50 closed the readiness audit.
KROK 51 narrowed the missing gap.

That gap is now explicit:
- real canonical runs do not emit richer exclusion-relevant identity fields
- real canonical runs do not expose a duplicate-state candidate path

So the next honest move is:
- instrument the missing ingredients minimally,
- keep them explicit,
- keep them fail-closed,
- and avoid pretending that instrumentation already means exclusion.

---

## 2. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` section III.2–III.4
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/EXCLUSION_READINESS_PLAN.md`
- `workflow/EXCLUSION_INGREDIENTS_PLAN.md`
- `conclusions/EXCLUSION_READINESS_INTERIM.md`

Canonical requirements extracted from those files:
- exclusion needs more than signature alone
- the relevant identity attributes are:
  - signature
  - orientation `sigma`
  - topological charge `Q_T`
  - excitation index `n`
  - niche anchor
- partial similarity must remain non-identical
- exclusion must remain blocked until complete identity is explicit

---

## 3. CURRENT ENGINE BASELINE

The current engine already emits:
- `loop_signatures`
- `loop_identity_regime = canonical_exact_signature`
- summary loop metrics

This is enough for:
- strict tracked operational identity
- distinguishing same-summary / different-structure cases

This is not enough for:
- exclusion-ready identity
- duplicate-niche candidate testing
- structural rejection logic

---

## 4. MINIMAL NEW FIELDS

The smallest useful new `fracture` richer-identity fields should be:
- `loop_orientation`
- `loop_charge`
- `loop_excitation_index`
- `loop_niche_anchor`

These richer-identity fields should only appear in:
- `canonical_separated`

They should remain absent in:
- `legacy_visible_only`
- `diagnostic_contaminated`

Additionally,
one explicit regime field should be emitted:
- `exclusion_candidate_regime`

That regime field may appear across projection modes,
because its purpose is to keep readiness status explicit and fail-closed.

Reason:
- we must preserve the same fail-closed regime discipline
  already used for freeze and loop identity.

---

## 5. MINIMAL SEMANTICS FOR EACH FIELD

### 5.1 `loop_orientation`

Status:
experimental identity ingredient, not yet full canonical proof.

Minimal semantics:
- list aligned with `loop_signatures`
- values restricted to `+1` or `-1`
- for the first implementation pass,
  derived deterministically from canonical cycle ordering
  and documented as an operational convention

Reason:
- the canon requires explicit orientation,
  but the current MVP engine does not yet have richer geometric structure.
- so the first pass must be explicit and reproducible,
  not metaphysically overclaimed.

### 5.2 `loop_charge`

Status:
derived operational field, directly tied to current theory.

Minimal semantics:
- list aligned with `loop_signatures`
- computed as:
  `loop_charge = loop_orientation * (loop_length mod 2)`

Reason:
- this follows the current canonical formula for `Q_T`
  more cleanly than any heuristic proxy.

### 5.3 `loop_excitation_index`

Status:
experimental placeholder for exclusion readiness,
not yet a full loop-class theory.

Minimal semantics:
- list aligned with `loop_signatures`
- integer values only
- first MVP pass may use:
  `0` for all detected loops

Reason:
- exclusion readiness needs an explicit slot for `n`
- but current engine does not yet have a justified dynamics-based excitation ladder
- setting a clear baseline placeholder is more honest
  than silently inferring a fake hierarchy

### 5.4 `loop_niche_anchor`

Status:
experimental niche identity field.

Minimal semantics:
- list aligned with `loop_signatures`
- each item should identify the loop's current core cluster anchor
- first MVP pass should use:
  a deterministic canonical node anchor from the same signature
  such as the minimum node id in the cycle

Reason:
- THEORY states that niche includes core cluster plus excitation index
- current MVP does not yet expose richer core-cluster identity
- a deterministic anchor placeholder is enough for validator-first readiness work
  as long as it is clearly documented as provisional

### 5.5 `exclusion_candidate_regime`

Status:
explicit diagnostic field for readiness only.

Allowed values in the first pass:
- `not_applicable_legacy`
- `not_applicable_contaminated`
- `canonical_identity_only`
- `canonical_candidate_path`

Reason:
- this makes it explicit whether a run merely emits richer identity
  or also exposes a candidate duplicate-state path

---

## 6. DUPLICATE-CREATION PATH

The smallest honest first path is not full rejection.

It is:
- one pre-registered synthetic or tightly controlled canonical path
  that logs an attempted duplicate-state candidate

Minimal requirement:
- a log-level marker showing that a candidate duplicate-state attempt
  was constructed or detected for audit purposes

Recommended first placement:
- `meta` or `notes` field on a terminal event
- or a dedicated small event type if that is cleaner in the current API

For the first implementation pass,
the simpler and safer route is:
- keep the event outside `fracture`
- keep `fracture` focused on state fields
- keep the duplicate-path marker in a separate event or event note

---

## 7. VALIDATION RULES FOR THE NEXT PASS

The next implementation pass should validate that:

1. legacy logs do NOT emit richer exclusion fields
2. contaminated logs do NOT emit richer exclusion fields
3. canonical logs emit all richer fields together or none
4. all richer field lists align in length with `loop_signatures`
5. `loop_orientation` values are only `+1` or `-1`
6. `loop_charge` is consistent with orientation and loop length parity
7. `loop_excitation_index` is integer and non-negative
8. `loop_niche_anchor` is deterministic and non-empty
9. candidate-path markers remain explicit and auditable

---

## 8. WHAT NOT TO DO

Do NOT:
- claim that provisional orientation semantics are final ontology
- infer excitation hierarchy from summary metrics
- collapse niche anchor into a vague summary label
- implement rejection in the same step
- silently emit partial richer fields

Either the richer identity layer appears coherently,
or it should be absent.

---

## 9. FILES EXPECTED IN THE NEXT IMPLEMENTATION STEP

Likely touched files in the next step:
- `engine/boundary/stabilization.py`
- `engine/fracture/state.py`
- one new validator in `validation/`
- one small targeted control set in `workflow/`

Not expected yet:
- `hypotheses/`
- exclusion enforcement logic
- thaw-related files

---

## 10. RECOMMENDED NEXT STEP

Recommended next action after this note:
- `KROK 53 — Exclusion Ingredient Instrumentation Implementation`

Expected result type:
- technical conclusion

That step should:
- emit the richer identity fields
- validate them fail-closed
- keep duplicate-candidate signaling explicit
- still stop before actual exclusion enforcement

---

## 11. OUTCOME

KROK 52 is complete when:
- this instrumentation plan exists
- workflow memory points to the implementation step
- the engine-test grid identifies Stage 5 as instrumented-next,
  not exclusion-next

---

End of plan
