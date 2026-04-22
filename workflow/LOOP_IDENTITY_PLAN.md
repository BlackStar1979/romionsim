# LOOP IDENTITY PLAN — KROK 47

Purpose:
Define the next narrow Stage 4 plan
for loop identity / canonical signature across ticks
after summary-level loop persistence is already validated.

This step does NOT implement exclusion yet.
It does NOT implement loop classes.
It does NOT claim full ontological identity in the strongest sense.

---

## 1. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` sections III.2–III.4
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `workflow/LOOP_INTERPRETATION_NOTE.md`
- `workflow/LOOP_PERSISTENCE_PLAN.md`
- `conclusions/LOOP_PERSISTENCE_INTERIM.md`
- `workflow/ENGINE_TEST_GRID.md`

Canonical constraints extracted from those files:
- exclusion requires identity,
- identity depends on a signature,
- the current engine does not yet expose full canonical invariants
  such as orientation, charge, excitation index, or niche.

So the next honest question is:
- what is the minimal operational signature
  that allows tracking loop-like individuals across ticks
  without falsely claiming complete canonical identity?

---

## 2. WHY THIS STAGE IS NEXT

After KROK 46:
- loop detection exists,
- summary-level loop persistence exists,
- but time-extended claims still speak only about loop-bearing structure,
  not about identifiable loop individuals.

Without an identity layer, the engine still cannot honestly support:
- per-loop persistence claims,
- loop lineage across ticks,
- niche-based exclusion checks,
- class reproducibility for specific loop states.

So the next honest move is:
- define a minimal identity contract,
- make its epistemic limitation explicit,
- keep exclusion still blocked.

---

## 3. MINIMUM DESIGN GOAL

Introduce one MVP-level identity concept
that is strong enough for tracking
but weaker than full canonical identity in THEORY.

This stage should aim to define:
- a canonical loop signature,
- a per-tick loop record format,
- a minimal rule for saying
  “this loop at tick t is the same tracked individual as at tick t+1”.

This stage does NOT require:
- orientation,
- topological charge,
- excitation index,
- niche identity,
- bundle identity,
- exclusion enforcement.

It only prepares the smallest honest identity layer.

---

## 4. OPERATIONAL IDENTITY VS FULL IDENTITY

This distinction must remain explicit.

### Full canonical identity (not yet available)

Theory-side full identity would eventually depend on things such as:
- canonical topological signature,
- `sigma`,
- `Q_T`,
- excitation index,
- core-cluster niche anchor.

The current engine does not yet compute that full set.

### Operational identity (Stage 4C target)

For the current rebuild,
the first identity layer should be framed as:
- operational tracked identity
- suitable for continuity checks across ticks
- explicitly weaker than full exclusion-ready identity

Safe wording:
- `tracked loop identity`
- `operational loop signature`

Unsafe wording:
- `complete loop identity`
- `exclusion-ready identity`

---

## 5. FIRST CANDIDATE SIGNATURE

Recommended first signature ingredients:
- canonicalized cycle node-set / node-sequence representative
- `L0` (topological length)
- cluster anchor placeholder

Most minimal workable signature for the current engine:
- canonicalized undirected cycle representative itself

Reason:
- KROK 44 already canonicalizes simple cycles,
- this is the strongest identity handle we currently have
  without inventing orientation or charge.

Important boundary:
- if the exact canonicalized cycle changes by one node,
  the tracked identity should currently be treated as changed,
  even if the summary looks similar.

This may be too strict,
but strictness is safer than false continuity
at this stage.

---

## 6. FIRST MATCHING RULE ACROSS TICKS

Recommended first rule:

A loop at tick `t+1` is the same tracked loop as at tick `t`
iff the canonicalized cycle representative is identical.

This is intentionally conservative.

Consequences:
- stable exact cycles can be tracked honestly,
- near-miss variants are not silently merged,
- later relaxed matching rules can be introduced explicitly if needed.

This rule should be described as:
- fail-closed,
- continuity-conservative,
- not yet topologically tolerant.

---

## 7. FIRST IDENTITY-LEVEL OBSERVABLES

Once identity is introduced,
the next validator-facing observables should be minimal:

- `tracked_loop_count`
- `persisting_loop_count`
- `new_loop_count`
- `dissolved_loop_count`
- optional `max_tracked_loop_age`

These should remain per-tick or run-summary observables,
not yet domain interpretations.

Why these first:
- they connect naturally to Stage 4 persistence,
- they stay below exclusion complexity,
- they give us the first honest loop-lineage signal.

---

## 8. IMPLEMENTATION SHAPE

Recommended code path for the next step after this note:

1. `engine/boundary/`
   - expose canonicalized cycles as internal structures,
     not only aggregated counts

2. `engine/boundary/stabilization.py`
   - derive per-tick tracked signatures
   - optionally compare with previous tick state

3. `engine/fracture/state.py`
   - accept minimal identity-level summary fields

4. validation
   - add one validator for tracked loop continuity

Reason:
- identity must remain a FRACTURE/boundary construct,
- CORE should still stay free of loop-individual semantics.

---

## 9. MINIMAL TEST SET FOR THIS STAGE

### Test A — Exact Persistent Loop

Preconditions:
- the same canonicalized cycle appears in consecutive ticks

Expectation:
- validator counts it as the same tracked loop

---

### Test B — Loop Dissolution

Preconditions:
- a canonicalized cycle disappears at the next tick

Expectation:
- validator counts one dissolved loop

---

### Test C — New Loop Birth

Preconditions:
- a canonicalized cycle appears that was absent in the prior tick

Expectation:
- validator counts one new loop

---

### Test D — Similar but Not Identical Loop

Preconditions:
- summary metrics stay similar,
  but the canonicalized cycle representative changes

Expectation:
- validator treats this as identity break,
  not silent continuity

This test is especially important
to prevent false carryover from summary persistence to individual persistence.

---

## 10. WHAT NOT TO DO IN THIS STAGE

Do NOT:
- implement exclusion yet
- invent tolerant graph-matching heuristics and call them canonical
- introduce orientation or charge placeholders without data support
- infer niche identity from summary metrics alone
- collapse operational identity into full ontological identity

This stage should remain
the narrowest honest bridge from persistence to identity.

---

## 11. CLOSURE ARTIFACTS

KROK 47 is complete when these artifacts exist:

1. this identity plan
2. updated workflow memory
3. updated test-grid guidance

KROK 47 does NOT yet prove loop identity in code.
It only registers the smallest honest path for implementing it.

---

## 12. NEXT IMPLEMENTATION MOVE

Recommended next action after this note:
- implement one validator-first pass
  for tracked loop identity continuity
  using strict exact-signature matching

That should become:
- `KROK 48 — Loop Identity Validator`

Only after that should we decide whether:
- identity is strong enough to support exclusion planning,
- relaxed matching is needed,
- or richer invariants must come first.

---

End of plan
