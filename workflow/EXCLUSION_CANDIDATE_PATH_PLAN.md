# EXCLUSION CANDIDATE PATH PLAN — KROK 54

Purpose:
Define the narrowest honest next step
for creating a real duplicate-state candidate path
before any exclusion enforcement is attempted.

This step does NOT implement exclusion.
This step does NOT implement rejection events.
This step does NOT open thaw, loop classes, or propagation work.

---

## 1. WHY THIS STEP IS NEXT

KROK 53 closed the richer-identity instrumentation pass.

That means Stage 5 is no longer blocked by complete absence of:
- orientation
- charge
- excitation slot
- niche anchor

The remaining blocker is now narrower and concrete:
- the engine still lacks a real path
  that can produce a duplicate-state candidate
  under auditable conditions.

So the next honest move is:
- define one registered candidate path,
- define where it is logged,
- define how it stays separate from actual exclusion logic.

---

## 2. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` section III.4
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/EXCLUSION_READINESS_PLAN.md`
- `workflow/EXCLUSION_INGREDIENTS_PLAN.md`
- `workflow/EXCLUSION_INGREDIENT_INSTRUMENTATION_PLAN.md`
- `conclusions/EXCLUSION_INGREDIENT_INSTRUMENTATION_INTERIM.md`

Canonical constraints extracted from them:
- exclusion concerns identical loop states in the same niche
- exclusion is a structural constraint, not a force
- attempted violations must be explicit and auditable
- partial similarity must not be promoted to exclusion

So the candidate path must be:
- explicit
- reproducible
- structurally narrow
- still pre-exclusion

---

## 3. WHAT THE CANDIDATE PATH MUST ACHIEVE

The first real candidate path does not need to reject anything yet.

It only needs to create a situation where the log can say:
- a candidate duplicate-state attempt was formed or approached
- the candidate had a fully explicit identity tuple
- the candidate shared the same niche anchor and exclusion-relevant identity
  with an existing tracked loop

This is enough to unblock the future exclusion step,
because it turns Stage 5 from:
- "identity exists in principle"

into:
- "a concrete exclusion-relevant conflict can be constructed and inspected"

---

## 4. SMALLEST HONEST PATH

The narrowest useful first path should be:

- one synthetic-but-engine-shaped control family
  or one tightly controlled canonical path
- that creates:
  - one existing loop-bearing state
  - one second candidate with the same:
    - signature
    - orientation
    - charge
    - excitation index
    - niche anchor

The safer order is:
1. first define the candidate path structurally
2. then implement its signaling
3. only later decide whether rejection occurs

---

## 5. RECOMMENDED SIGNALING PLACEMENT

The cleanest first placement is:
- outside `fracture`
- in an explicit event-level marker or event note

Recommended first shape:
- terminal or dedicated event note:
  - `duplicate_creation_path: true`
  - `duplicate_candidate_identity_complete: true`
  - `duplicate_candidate_source: ...`

Reason:
- `fracture` should remain the state layer
- candidate-attempt signaling is process/event information
- this keeps state identity separate from attempted conflict generation

---

## 6. MINIMAL CANDIDATE-PATH REGIMES

For the first pass, the engine or validator layer should distinguish:
- `candidate_path_absent`
- `candidate_path_partial_identity`
- `candidate_path_identity_complete`

Interpretation:
- `candidate_path_absent`:
  no auditable duplicate-state attempt exists
- `candidate_path_partial_identity`:
  a second candidate exists, but at least one exclusion-relevant field is missing or differs
- `candidate_path_identity_complete`:
  a full exclusion-relevant duplicate candidate exists

This remains readiness language,
not yet rejection language.

---

## 7. MINIMAL TEST SET FOR THE NEXT STEP

### Test A — Canonical Identity-Only Control

Expectation:
- no candidate path
- richer identity fields exist
- no exclusion interpretation

### Test B — Partial Duplicate Candidate

Expectation:
- candidate path exists
- at least one exclusion-relevant attribute differs
- still no exclusion-ready duplicate

### Test C — Complete Duplicate Candidate

Expectation:
- candidate path exists
- all exclusion-relevant identity attributes match
- run becomes a valid pre-exclusion conflict candidate

---

## 8. WHAT NOT TO DO

Do NOT:
- implement rejection in this step
- silently treat synthetic candidate paths as final closure
- collapse candidate-path signaling into `fracture` state fields
- treat similarity of summary metrics as duplicate identity
- use loose textual notes without structured fields

---

## 9. FILES EXPECTED IN THE NEXT IMPLEMENTATION STEP

Likely touched files after this plan:
- one validator or validator extension in `validation/`
- one targeted control set in `workflow/`
- possibly one small logging extension in `engine/api/` or event-generation flow

Not expected yet:
- exclusion enforcement logic
- hypothesis files
- thaw-related files

---

## 10. RECOMMENDED NEXT STEP

Recommended next action after this note:
- `KROK 55 — Exclusion Candidate Path Implementation`

Expected result type:
- technical conclusion

That step should:
- emit one explicit candidate-path signal
- distinguish partial vs complete duplicate candidates
- stay clearly before exclusion enforcement

---

## 11. OUTCOME

KROK 54 is complete when:
- this plan exists
- workflow memory points to the candidate-path implementation step
- the engine-test grid identifies candidate-path construction,
  not exclusion enforcement, as the next honest move

---

End of plan
