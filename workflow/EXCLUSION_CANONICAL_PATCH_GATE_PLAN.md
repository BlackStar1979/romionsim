# EXCLUSION CANONICAL PATCH GATE PLAN — KROK 72

Purpose:
Prepare one narrow gate
for deciding when a contract-patch candidate
is mature enough to justify direct canonical contract editing.

This step does NOT edit `docs/ENGINE_CONTRACT.md`.
This step does NOT broaden exclusion mechanics.

---

## 1. WHY THIS STEP IS NEXT

KROK 71 closes the smallest safe contract-patch candidate shape.

That means the next blocker is:
- what additional gate must still be passed
  before direct canonical editing is justified?

---

## 2. GATE IDEA

A patch candidate should not reach canonical docs
only because it is neat and narrow.

Before canonical editing,
it should satisfy at least:

1. validator-backed narrow scope
2. stable across current control set
3. no contradiction with `docs/ENGINE_CONTRACT.md`
4. low risk of immediate reversal by the next nearby Stage 5 step
5. explicit human review readiness

---

## 3. RECOMMENDED NEXT STEP

Recommended next action after this plan:
- `KROK 73 — Exclusion Canonical Patch Gate Assessment`

Expected result type:
- technical conclusion

That step should:
- assess whether the current patch candidate passes this stricter gate
- still stop before any direct canonical contract edit

---

## 4. OUTCOME

KROK 72 is complete when:
- this gate plan exists
- workflow memory points to KROK 73
- restart notes no longer point back to KROK 72

---

End of plan
