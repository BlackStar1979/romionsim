# EXCLUSION MINIMAL ENFORCEMENT PLAN — KROK 60

Purpose:
Define the smallest honest enforcement step
that can follow signaling and first post-signal outcome validation.

This step does NOT implement full exclusion mechanics.
This step does NOT implement thaw, fusion, bundling, or re-projection handling.

---

## 1. WHY THIS STEP IS NEXT

Stage 5 now has:
- richer identity instrumentation,
- candidate-path signaling,
- explicit stabilization-stage rejection signaling,
- first validator-backed outcome closure
  showing that rejection need not leave a second valid stabilized duplicate.

So the next blocker is no longer:
- whether rejection can be named,
- or whether its narrowest outcome can be audited.

The next blocker is:
- what the smallest real enforcement move is,
  beyond signaling and outcome description alone.

---

## 2. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` section III.4
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/THEORY_REFRESH_2026-04-21_1653.md`
- `workflow/EXCLUSION_REJECTION_POINT_PLAN.md`
- `workflow/EXCLUSION_REJECTION_OUTCOME_PLAN.md`
- `conclusions/EXCLUSION_REJECTION_OUTCOME_INTERIM.md`

Canonical constraints extracted from them:
- exclusion is structural, not force-like
- duplicate-state violation should be rejected, not merely narrated
- early enforcement may occur at creation / stabilization
- later branches such as fusion or re-projection must not be smuggled in early

---

## 3. WHAT COUNTS AS "MINIMAL ENFORCEMENT" HERE

For the current MVP,
minimal enforcement should mean:

- once a complete duplicate candidate is present,
- and a stabilization-stage rejection is emitted,
- the same tick must not be allowed to present
  two identical stabilized loop signatures
  as simultaneously valid canonical output.

Operational reading:
- this is a uniqueness guard at the stabilization-output level,
- not yet a deep-process law for everything that happened underneath.

---

## 4. WHAT THIS STEP STILL MUST NOT CLAIM

This step must NOT claim:
- annihilation
- fusion
- bundling
- re-projection handling
- full exclusion closure
- mature loop-class ontology

It also must NOT reinterpret:
- absence of a second stabilized duplicate
as
- proof that no deeper transient duplication attempt ever occurred.

---

## 5. RECOMMENDED FIRST ENFORCEMENT RULE

The first real enforcement rule should be:

- if a complete duplicate candidate reaches stabilization,
- and the rejection condition is satisfied,
- then canonical stabilized loop output must remain uniqueness-preserving
  at the rejection tick.

In practical MVP terms:
- no duplicate canonical loop signature may survive that tick
  as a second valid stabilized loop.

This keeps enforcement:
- narrow,
- auditable,
- and below broader exclusion mechanics.

---

## 6. WHERE THE ENFORCEMENT SHOULD APPEAR

Recommended first location:
- boundary / stabilization output contract

Reason:
- that is already where the rejection point was fixed,
- it avoids premature drift into broader engine semantics,
- it matches the current validator and control structure.

The first implementation may still use:
- event-level notes,
- validator-backed control logs,
- or one narrow canonical-output constraint,
as long as the claim remains explicit and limited.

---

## 7. MINIMAL TEST SET FOR THE NEXT STEP

### Test A — No Candidate Path

Expectation:
- no enforcement
- no duplicate-elimination claim

### Test B — Partial Candidate Path

Expectation:
- no enforcement
- no duplicate-elimination claim

### Test C — Complete Candidate Path With Rejection

Expectation:
- rejection signal present
- no second identical stabilized canonical loop survives

### Test D — Negative Control

Expectation:
- if duplicate persistence is still present,
  validator must detect it fail-closed

---

## 8. RECOMMENDED NEXT STEP

Recommended next action after this note:
- `KROK 61 — Exclusion Minimal Enforcement Validator`

Expected result type:
- technical conclusion

Why validator-first again:
- the project still needs a narrow capability closure,
- not yet a broad engine rewrite,
- and the current Stage 5 history keeps moving safely
  by proving one bounded claim at a time.

---

## 9. OUTCOME

KROK 60 is complete when:
- this plan exists
- workflow memory points to the minimal-enforcement validator step
- restart notes and the engine-test grid no longer point back to KROK 60

---

End of plan
