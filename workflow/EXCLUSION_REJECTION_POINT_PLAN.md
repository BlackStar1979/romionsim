# EXCLUSION REJECTION POINT PLAN — KROK 56

Purpose:
Define the narrowest honest next step
for where exclusion rejection should occur
once a complete duplicate-state candidate exists.

This step does NOT implement exclusion enforcement.
This step does NOT implement thaw, loop classes, or propagation work.

---

## 1. WHY THIS STEP IS NEXT

KROK 55 closed the candidate-path signaling pass.

That means Stage 5 now has:
- richer identity instrumentation,
- explicit candidate-path signaling,
- distinction between absent / partial / complete duplicate candidates.

So the next blocker is no longer:
- "can we describe a duplicate candidate?"

but:
- "where should structural rejection occur,
  and how should it be signaled,
  once a complete candidate exists?"

That is the smallest honest next planning question.

---

## 2. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` section III.4
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/EXCLUSION_CANDIDATE_PATH_PLAN.md`
- `conclusions/EXCLUSION_CANDIDATE_PATH_INTERIM.md`
- `workflow/ENGINE_TEST_GRID.md`

Canonical constraints extracted from them:
- exclusion is a structural constraint, not a force
- attempted duplicate states are structurally rejected
- enforcement may happen at:
  - creation / stabilization
  - fusion / bundling
  - re-projection
- attempted violations should be auditable

For the current MVP,
the narrowest honest enforcement point is:
- creation / stabilization

Reason:
- it is the earliest and cleanest enforcement point named in the spec
- it avoids premature branching into fusion or re-projection mechanics
- it fits the current engine architecture best

---

## 3. RECOMMENDED FIRST REJECTION POINT

The first rejection point should be:
- boundary-level stabilization

Operational reading:
- a duplicate-state candidate becomes visible enough
  to be considered a stabilization attempt
- if its exclusion-relevant identity is complete
  and matches an existing same-niche loop state
  then stabilization should fail

This is the cleanest MVP interpretation of:
- "the loop dissolves or never forms"

---

## 4. WHAT MUST BE DECIDED BEFORE IMPLEMENTATION

### 4.1 Rejection timing

The implementation must choose one of two explicit semantics:

1. pre-visibility rejection
   - candidate is blocked before appearing in `fracture`

2. same-tick attempted stabilization rejection
   - candidate attempt is logged
   - but the duplicate state is not allowed to persist as a valid stabilized loop

Recommended first pass:
- same-tick attempted stabilization rejection

Reason:
- it preserves audibility
- it matches the existing candidate-path work better
- it lets the project log a real failed attempt
  without silently erasing evidence

### 4.2 Rejection signal

The smallest honest rejection signal should be:
- an explicit event-level note or dedicated event carrying:
  - `exclusion_rejection: true`
  - `rejection_stage: "stabilization"`
  - `rejection_reason: "duplicate_niche_identity"`
  - `rejection_identity_complete: true`

This should remain outside `fracture`,
because it is an event/process fact,
not a stable state field.

### 4.3 Allowed non-rejection case

The implementation must also preserve:
- complete candidate path absent -> no rejection
- partial identity candidate -> no rejection

Otherwise Stage 5 would collapse
back into a coarse similarity rule,
which the theory does not allow.

---

## 5. MINIMAL ENFORCEMENT LOGIC

The first pass should reject only when all are true:
- candidate path exists
- candidate identity is complete
- signature matches
- orientation matches
- charge matches
- excitation index matches
- niche anchor matches

If any of those differ:
- no exclusion rejection

This is intentionally strict.

---

## 6. MINIMAL TEST SET FOR THE NEXT STEP

### Test A — No Candidate Path

Expectation:
- no rejection

### Test B — Partial Candidate Identity

Expectation:
- no rejection
- explicit non-rejection despite candidate-path presence

### Test C — Complete Candidate Identity

Expectation:
- explicit rejection signal
- rejection stage = stabilization
- no claim yet about fusion or re-projection

---

## 7. WHAT NOT TO DO

Do NOT:
- reject partial identity candidates
- hide rejection only by disappearance with no signal
- mix rejection facts into `fracture` state fields
- generalize immediately to fusion / bundling / re-projection
- claim full exclusion closure after one stabilization-point pass

---

## 8. FILES EXPECTED IN THE NEXT IMPLEMENTATION STEP

Likely touched files after this plan:
- `engine/api/log_contract.py` or nearby event-generation flow
- one validator or validator extension in `validation/`
- one targeted control set in `workflow/`

Possibly touched, but only if needed:
- `engine/api/engine.py`

Not expected yet:
- loop algebra implementation
- fusion logic
- re-projection logic
- hypothesis files

---

## 9. RECOMMENDED NEXT STEP

Recommended next action after this note:
- `KROK 57 — Exclusion Rejection Signal Implementation`

Expected result type:
- technical conclusion

That step should:
- emit one explicit rejection signal
- keep rejection tied only to complete duplicate identity
- stay within stabilization-stage enforcement only

---

## 10. OUTCOME

KROK 56 is complete when:
- this rejection-point plan exists
- workflow memory points to the rejection-signal implementation step
- the engine-test grid identifies stabilization-stage rejection signaling
  as the next honest move

---

End of plan
