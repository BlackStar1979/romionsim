# EXCLUSION READINESS PLAN — KROK 49

Purpose:
Define the narrowest honest Stage 5 readiness note
for the gap between current operational loop identity
and actual topological exclusion mechanics.

This step does NOT implement exclusion.
This step does NOT introduce loop classes.
This step does NOT change canonical theory.

---

## 1. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` section III.4
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/LOOP_IDENTITY_PLAN.md`
- `conclusions/LOOP_IDENTITY_INTERIM.md`
- `workflow/ENGINE_TEST_GRID.md`

Canonical constraints extracted from those files:
- exclusion is triggered only by complete identity,
- complete identity requires more than summary similarity,
- exclusion is a hard structural constraint, not a force,
- partial similarity must not be treated as exclusion.

So the next honest question is:
- what exactly is still missing before the engine can even attempt
  a fail-closed exclusion pass?

---

## 2. WHY THIS STAGE IS NEXT

After KROK 48:
- loop detection exists,
- summary-level persistence exists,
- strict operational identity exists,
- but exclusion still remains intentionally blocked.

That is correct,
because the current identity layer is still weaker than the full identity
required by `SPEC_EXCLUSION_MECHANICS.md`.

So the next honest move is not:
- implement exclusion immediately

but rather:
- map the missing exclusion-relevant attributes explicitly
- and register the smallest readiness check.

---

## 3. WHAT WE ALREADY HAVE

Current engine-ready ingredients:
- canonicalized cycle representative
- strict exact-signature tracking across ticks
- birth / dissolution / identity-break detection
- explicit separation between summary persistence and individual identity

These are real prerequisites.

Without them,
Stage 5 would still be premature.

---

## 4. WHAT IS STILL MISSING

From `SPEC_EXCLUSION_MECHANICS.md`,
full exclusion-relevant identity requires:
- canonical topological signature
- orientation `sigma`
- topological charge `Q_T`
- excitation index `n`
- core cluster / niche anchor

Current gap:

1. We have only a conservative exact cycle representative,
   not a richer canonical topological signature layer.

2. We do not compute:
   - `sigma`
   - `Q_T`
   - excitation index

3. We do not compute niche anchor explicitly.

4. We do not yet model attempted duplicate-state creation,
   so we cannot test actual structural rejection.

This means:
- current identity is enough for conservative tracking,
- but not yet enough for exclusion enforcement.

---

## 5. MOST IMPORTANT READINESS PRINCIPLE

The core readiness rule should be:

`statistical similarity must never be treated as exclusion identity`

Only explicit exclusion-relevant identity attributes
may trigger exclusion.

Operational consequence:
- if two loop-bearing structures share the same summary metrics
  but differ in tracked signature,
  they must currently remain non-identical.

This protects the project from collapsing back
into a merely averaged-statistical reading.

---

## 6. READINESS TARGET FOR THE NEXT STEP

The smallest useful readiness target is not exclusion itself.

It is:
- one explicit exclusion-identity audit layer
  that says for a given run or synthetic case:
  - which exclusion-relevant attributes are present
  - which are missing
  - whether exclusion is:
    - `not_ready`
    - `partially_ready`
    - or `ready_for_candidate_test`

At the current stage,
the expected honest answer is probably:
- `not_ready`

But writing that down explicitly is better
than silently pretending readiness.

---

## 7. RECOMMENDED FIRST READINESS CLASSES

For the next validator-first pass,
the following readiness classes are enough:

- `not_ready_missing_orientation`
- `not_ready_missing_charge`
- `not_ready_missing_excitation_index`
- `not_ready_missing_niche_anchor`
- `not_ready_missing_duplicate_creation_path`
- `partially_ready_operational_identity_only`
- `candidate_ready_for_exclusion_test`

This is intentionally an audit language,
not yet an exclusion language.

---

## 8. MINIMAL TEST SET FOR READINESS

### Test A — Current Canonical Identity Case

Preconditions:
- strict operational identity exists
- no orientation / charge / niche fields exist

Expectation:
- validator reports partial readiness only

---

### Test B — Similar Summary, Different Structure

Preconditions:
- same summary-level metrics
- different tracked signatures

Expectation:
- validator confirms non-identity
- and blocks exclusion interpretation

---

### Test C — Missing Duplicate-Creation Path

Preconditions:
- no actual candidate duplicate-state creation event exists

Expectation:
- validator reports not ready for exclusion execution

---

## 9. WHAT NOT TO DO IN THIS STAGE

Do NOT:
- implement exclusion events yet
- infer orientation heuristically without support
- derive charge from summary metrics
- derive niche anchor from convenience shortcuts
- treat operational identity as already exclusion-ready

This step should remain a readiness map only.

---

## 10. CLOSURE ARTIFACTS

KROK 49 is complete when these artifacts exist:

1. this readiness plan
2. updated workflow memory
3. updated test-grid guidance

KROK 49 does NOT yet prove exclusion is ready.
It only registers the smallest honest path for testing readiness.

---

## 11. NEXT IMPLEMENTATION MOVE

Recommended next action after this note:
- implement one validator-first exclusion-readiness audit
  over the current identity layer

That should become:
- `KROK 50 — Exclusion Readiness Audit`

Only after that should we decide whether:
- richer identity fields must be added first,
- a duplicate-state creation path is the next blocker,
- or a true exclusion implementation can begin.

---

End of plan
