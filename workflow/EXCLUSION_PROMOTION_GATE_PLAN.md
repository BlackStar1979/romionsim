# EXCLUSION PROMOTION GATE PLAN — KROK 66

Purpose:
Define the narrow gate that any exclusion promotion candidate
must still pass before becoming an actual contract-facing proposal.

This step does NOT rewrite `docs/ENGINE_CONTRACT.md`.
This step does NOT broaden exclusion mechanics.
This step does NOT implement thaw, fusion, bundling, or re-projection handling.

---

## 1. WHY THIS STEP IS NEXT

KROK 65 already identified the candidate set.

So the next blocker is:
- what additional evidence or stability must exist
  before promotion is justified?

That is a gate question.

---

## 2. GATE PRINCIPLE

No exclusion item should be promoted closer to contract status
only because it has one validator and one conclusion artifact.

Promotion should require:
- stability,
- repeatability,
- clean failure classification,
- and low risk of near-term reversal.

This is stricter than candidacy.

---

## 3. MINIMAL PROMOTION GATE

Before any current candidate advances beyond workflow/conclusion status,
it should satisfy all of the following:

1. validator-backed in at least one positive path
2. validator-backed in at least one negative or fail-closed control
3. already classified as narrow compliance expectation
4. not contradicted by current stored control logs
5. unlikely to be invalidated by the next immediate Stage 5 step
6. expressible without expanding ontology or importing broader mechanics

If one of these is missing:
- gate not passed

---

## 4. WHAT THIS GATE STILL DOES NOT AUTHORIZE

Passing the gate would still NOT automatically authorize:
- broad `ENGINE_CONTRACT.md` rewrite
- theory revision
- full exclusion-compliance claim
- promotion of fusion / re-projection / annihilation language

At most, it authorizes:
- one narrow contract-facing proposal
- for one already validated exclusion expectation

---

## 5. RECOMMENDED NEXT STEP

Recommended next action after this note:
- `KROK 67 — Exclusion Promotion Gate Assessment`

Expected result type:
- technical conclusion

That step should answer:
- which current candidates pass the gate,
- which fail it,
- and why.

It should still NOT rewrite canonical docs directly.

---

## 6. OUTCOME

KROK 66 is complete when:
- this promotion-gate plan exists
- workflow memory points to a gate-assessment step
- restart notes no longer point back to KROK 66

---

End of plan
