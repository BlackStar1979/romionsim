# EXCLUSION CONTRACT NARROWING PLAN — KROK 62

Purpose:
Define the next narrow Stage 5 step:
which exclusion-related claims are now strong enough
to be treated as contract expectations,
and which must remain validator-level only.

This step does NOT implement broader exclusion mechanics.
This step does NOT implement thaw, fusion, bundling, or re-projection handling.

---

## 1. WHY THIS STEP IS NEXT

Stage 5 now has:
- richer identity instrumentation,
- candidate-path signaling,
- explicit stabilization-stage rejection signaling,
- first post-signal outcome validation,
- first enforcement-level validation for uniqueness preservation
  in canonical stabilized output.

So the next blocker is no longer:
- whether a narrow exclusion-related claim can be validated.

The next blocker is:
- which of these validated claims may already become
  contract-level expectations for the engine,
- without pretending that full exclusion mechanics already exist.

---

## 2. CANONICAL BASIS

Relevant local sources:
- `docs/ENGINE_CONTRACT.md`
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/THEORY_REFRESH_2026-04-21_1653.md`
- `conclusions/EXCLUSION_REJECTION_SIGNAL_INTERIM.md`
- `conclusions/EXCLUSION_REJECTION_OUTCOME_INTERIM.md`
- `conclusions/EXCLUSION_MINIMAL_ENFORCEMENT_INTERIM.md`

Canonical constraints extracted from them:
- contract expectations must protect ontology, not replace it
- exclusion is structural and hard-constraint based
- validated narrow claims may support stricter engine expectations
- but missing broader mechanisms must remain explicitly out of scope

---

## 3. WHAT MAY ALREADY BE NARROWED TOWARD CONTRACT

The following now look strong enough
to be considered candidates for contract-level expectation:

1. complete duplicate identity is required before exclusion-related rejection
2. partial similarity must not trigger exclusion rejection
3. stabilization-stage rejection must remain an auditable event/process fact
4. canonical stabilized output must remain uniqueness-preserving
   at the rejection tick in the narrow MVP sense already validated

These are narrow and specific.
They do not yet imply full exclusion closure.

---

## 4. WHAT MUST REMAIN VALIDATOR-LEVEL ONLY

The following must remain below contract level for now:
- annihilation interpretations
- fusion / bundling consequences
- re-projection conflict handling
- any deeper-process claim about what happened before rejection
- any claim that exclusion is fully implemented across the engine

Reason:
- these areas are not yet closed by current Stage 5 capability work
- promoting them too early would repeat the same overreach pattern
  we have already been avoiding elsewhere in the repo

---

## 5. RECOMMENDED NARROW CONTRACT MOVE

The next honest move is not to rewrite `ENGINE_CONTRACT.md` broadly.

It is to prepare one minimal contract-oriented note
that says:

- what the engine must already preserve
  for narrow exclusion compliance,
- what still counts as missing feature rather than contract violation.

This should likely stay in workflow / conclusions first,
before any canonical-doc promotion.

---

## 6. MINIMAL TEST TARGET FOR THE NEXT STEP

The next validator/contract pass should answer one question:

- if a future run violates the already-validated narrow exclusion expectations,
  should that now be classified as:
  - implementation bug,
  - missing feature,
  - or still out of scope?

That classification boundary is the real goal of the next step.

---

## 7. WHAT NOT TO DO

Do NOT:
- silently harden all validated behavior into canonical contract
- rewrite `docs/ENGINE_CONTRACT.md` as if Stage 5 were already broadly closed
- treat validator success as proof of full exclusion implementation
- pull thaw or later exclusion branches into scope

---

## 8. RECOMMENDED NEXT STEP

Recommended next action after this note:
- `KROK 63 — Exclusion Contract Boundary Note`

Expected result type:
- technical conclusion

Why:
- the next closure is conceptual-architectural,
  not yet another broad mechanism pass
- and it should clarify future failure classification
  before Stage 5 grows further

---

## 9. OUTCOME

KROK 62 is complete when:
- this contract-narrowing plan exists
- workflow memory points to the contract-boundary note step
- restart notes and engine-test grid no longer point back to KROK 62

---

End of plan
