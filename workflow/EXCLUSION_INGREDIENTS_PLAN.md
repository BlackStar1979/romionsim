# EXCLUSION INGREDIENTS PLAN — KROK 51

Purpose:
Define the narrowest honest next step after the Stage 5 readiness audit.

This step does NOT implement exclusion.
This step does NOT implement loop classes.
This step does NOT introduce thaw work.

---

## 1. WHY THIS STEP IS NEXT

KROK 50 closed the audit layer.

The audit proved three things:
- operational identity already exists,
- summary-level sameness does not imply structural identity,
- real canonical runs are still blocked before exclusion.

The current blocker is no longer vague.
It has two concrete parts:
- richer exclusion-relevant identity fields are not emitted,
- no real duplicate-state creation path exists yet.

So the next honest move is not:
- exclusion implementation

and not:
- broad speculative redesign

but:
- one narrow plan for how to introduce the missing ingredients
  without overclaiming readiness.

---

## 2. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` section III.2–III.4
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/EXCLUSION_READINESS_PLAN.md`
- `conclusions/EXCLUSION_READINESS_INTERIM.md`
- `workflow/ENGINE_TEST_GRID.md`

The local canon is consistent on one key point:
- exclusion requires complete identity,
- and complete identity needs more than loop signature alone.

The required attributes are:
- canonical topological signature
- orientation `sigma`
- topological charge `Q_T`
- excitation index `n`
- niche anchor

---

## 3. WHAT KROK 50 TAUGHT US

The audit separated three levels cleanly:

1. Operational identity only
   - already available
   - enough for strict tracked continuity
   - not enough for exclusion

2. Exclusion-candidate identity
   - possible in synthetic controls
   - requires richer fields plus duplicate-creation path

3. Exclusion execution
   - still absent
   - must remain blocked

This is valuable because it prevents a false jump
from "identity exists" to "exclusion exists".

---

## 4. SMALLEST HONEST NEXT TARGET

The next target should be:

- one instrumentation-oriented pass
  for exclusion-relevant identity ingredients

not yet:
- rejection logic
- rejection events
- degeneracy resolution

So the next stage after this plan should aim to answer:

"Can the engine emit the minimum exclusion-relevant identity layer
and one explicit candidate duplicate-creation path
without pretending exclusion is already enforced?"

---

## 5. REQUIRED INGREDIENTS TO ADD EXPLICITLY

### 5.1 Identity fields

The smallest useful explicit fields are:
- `loop_orientation`
- `loop_charge`
- `loop_excitation_index`
- `loop_niche_anchor`

These should be treated as:
- experimental identity ingredients,
- not yet final proof of full ontology,
- but explicit enough for validator-first readiness work.

### 5.2 Duplicate-creation path

The engine also needs one explicit path
that can produce a candidate duplicate-state attempt.

This does NOT yet need to be a full exclusion event.

It only needs to be:
- pre-registered,
- reproducible,
- logged clearly enough for audit and future rejection checks.

---

## 6. ORDER OF WORK

The most economical order is:

1. plan the minimal richer identity layer
2. plan one narrow duplicate-creation path
3. validate that the new fields are emitted consistently
4. only then consider an actual exclusion implementation

Reason:
- if duplicate creation exists without richer identity,
  the result is still underdetermined
- if richer identity exists without duplicate creation,
  exclusion still cannot be exercised
- both ingredients must exist before exclusion can be tested honestly

---

## 7. WHAT NOT TO DO

Do NOT:
- infer exclusion from summary metrics
- treat synthetic candidate readiness as real engine closure
- implement rejection before candidate identity is explicit
- backfill orientation or charge from narrative convenience
- claim Stage 5 closure before auditable candidate conflicts exist

---

## 8. RECOMMENDED NEXT IMPLEMENTATION STEP

Recommended next step after this note:
- `KROK 52 — Exclusion Ingredient Instrumentation Planning`

That step should define:
- the minimal semantics for each richer identity field
- the smallest honest duplicate-creation control path
- where those fields should live in `fracture`
- how legacy and contaminated regimes remain fail-closed

This is the narrowest route
that moves Stage 5 forward without pretending exclusion already works.

---

## 9. OUTCOME OF THIS PLAN

KROK 51 is complete when:
- this plan exists,
- workflow memory points to the instrumentation-planning step,
- the engine-test grid no longer treats Stage 5 as only "audit next",
  but as "ingredient instrumentation next".

---

End of plan
