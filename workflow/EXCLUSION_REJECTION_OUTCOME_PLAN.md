# EXCLUSION REJECTION OUTCOME PLAN — KROK 58

Purpose:
Define the narrowest honest next step
after the first explicit stabilization-stage exclusion rejection signal exists.

This step does NOT implement broader exclusion mechanics.
This step does NOT implement thaw, fusion, re-projection, or loop classes.

---

## 1. WHY THIS STEP IS NEXT

KROK 57 closed the signaling pass.

That means Stage 5 now has:
- richer identity instrumentation,
- explicit duplicate-candidate construction,
- explicit stabilization-stage rejection signaling
  for complete duplicate identity.

So the next blocker is no longer:
- "can the project signal structural rejection?"

but:
- "what exactly does that rejection mean,
  and what does it explicitly NOT mean yet?"

That is the smallest honest next planning question.

---

## 2. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` section III.4
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/THEORY_REFRESH_2026-04-21_1653.md`
- `workflow/EXCLUSION_REJECTION_POINT_PLAN.md`
- `conclusions/EXCLUSION_REJECTION_SIGNAL_INTERIM.md`

Canonical constraints extracted from them:
- exclusion is structural, not force-like
- a rejected duplicate candidate is not a second valid stabilized loop
- rejection at stabilization does not automatically explain the deeper fate
  of the rejected candidate
- process facts must remain auditable

---

## 3. WHAT THE CURRENT REJECTION SIGNAL MEANS

At the current MVP level,
the signal means only this:

- a complete duplicate-state candidate reached attempted stabilization
- the candidate was structurally rejected at stabilization
- the project must not treat that candidate as a valid coexisting stabilized loop

This is already meaningful,
but still narrow.

---

## 4. WHAT THE CURRENT REJECTION SIGNAL DOES NOT YET MEAN

It does NOT yet prove:
- annihilation
- fusion / bundling
- re-projection
- dissipation law
- identity transfer
- thaw-side recovery behavior

It also does NOT yet prove:
- that the candidate never existed anywhere in a deeper process sense
- that the project already has full exclusion closure

The signal only closes:
- stabilization-stage rejection as an explicit event-level fact

---

## 5. MINIMAL OUTCOME SEMANTICS TO REGISTER NEXT

The next implementation pass should classify the first post-rejection outcome
language as narrowly as possible.

Recommended outcome classes:

1. `rejection_signal_absent`
2. `rejection_signal_partial_nonrejected`
3. `rejection_signal_emitted`
4. `rejection_without_duplicate_persistence`

The next pass should focus on class 4.

---

## 6. NARROW NEXT QUESTION

The next honest question is:

- after a rejection signal is emitted,
  can the validator confirm that the rejected duplicate
  did NOT survive as a second valid stabilized duplicate state?

This is narrower than full exclusion enforcement,
but stronger than signaling alone.

---

## 7. MINIMAL TEST SET FOR THE NEXT STEP

### Test A — No Candidate Path

Expectation:
- no rejection
- no duplicate-persistence claim

### Test B — Partial Candidate Path

Expectation:
- no rejection
- no duplicate-persistence claim

### Test C — Complete Candidate Path With Rejection

Expectation:
- explicit rejection signal
- no evidence of a second valid stabilized duplicate loop

---

## 8. WHAT NOT TO DO

Do NOT:
- reinterpret rejection as annihilation
- reinterpret rejection as fusion
- add deep-process claims not present in the current logs
- move thaw into scope
- claim full exclusion closure after one post-signal pass

---

## 9. RECOMMENDED NEXT STEP

Recommended next action after this note:
- `KROK 59 — Exclusion Rejection Outcome Validator`

Expected result type:
- technical conclusion

---

## 10. OUTCOME

KROK 58 is complete when:
- this rejection-outcome plan exists
- workflow memory points to the outcome-validator step
- the engine-test grid no longer points back to the signaling step

---

End of plan
