# FROZEN PERSISTENCE PLAN — KROK 37

Purpose:
Define the minimum honest plan for testing the Stage 3 claim that
frozen structure persists without observable propagation.

This step does NOT implement thaw.
It does NOT create a new hypothesis document.

---

## 1. CANONICAL BASIS

Relevant local sources:
- `docs/FOUNDATION_PROJECTION.md` section 8
- `docs/MECHANICS_EMERGENCE.md` section 7
- `docs/THEORY_V3.9.md` section II.4
- `workflow/ENGINE_TEST_GRID.md`
- `conclusions/FREEZE_STATE_REFINED_INTERIM.md`

Canonical statements already present in docs:
- freeze is not annihilation
- frozen configurations still exist relationally
- during freeze, structure persists
- during freeze, no propagation occurs

Current engine after KROK 36 can already log:
- `visible_edges`
- `visible_weight`
- `visible_ratio`
- `bridge_edges`
- `bridge_weight`
- `freeze_state`
- `freeze_reason`

So the next honest question is not:
- can freeze be labeled?

But:
- can frozen structure be distinguished from disappearance
  using current observables?

---

## 2. WHAT MUST BE SHOWN

To support frozen persistence at the current MVP level,
the engine does NOT need full thaw or propagation modeling yet.

It only needs to support one narrower claim:

When `freeze_state == true`,
some structural observables remain present and non-invalid.

Minimum acceptable persistence reading:
- `freeze_state == true`
- AND structure-bearing observables remain non-zero

Recommended MVP persistence proxy:
- `visible_edges > 0`

Optional supporting proxies:
- `visible_ratio > 0`
- `cluster_edges > 0`

What this means:
- freeze can coexist with structure
- structure is not automatically annihilated by freeze

What this does NOT yet prove:
- long-run persistence under varying dynamics
- loop persistence
- recovery
- propagation absence as a measured field process

---

## 3. RECOMMENDED MVP TEST TARGET

Define one narrow Stage 3 target:

### Frozen-Not-Annihilated Persistence Target

For a run or controlled log segment:
- if `freeze_state == true`
- and `visible_edges > 0`

then the state is classified as:
- frozen but structurally persistent

This target is compatible with current engine capabilities,
because it uses already logged observables only.

---

## 4. REQUIRED SEMANTIC GUARDRAILS

The following must hold:

1. `freeze_state == true` must not automatically imply:
   - `visible_edges == 0`
   - `visible_ratio == 0`

2. A run with:
   - `freeze_state == true`
   - `visible_edges == 0`
   is not automatically invalid,
   but it does NOT support the persistence claim.

3. Persistence support must remain separate from:
   - thaw semantics
   - propagation modeling
   - loop ontology

4. Diagnostic contaminated runs may be used for diagnostics only,
   not as canonical support.

---

## 5. IMPLEMENTATION OPTIONS

Two honest options exist.

### Option A — Validator First

Add a validator that checks whether a log contains at least one
frozen tick with retained structure.

Recommended result classes:
- `supports_persistence`
- `frozen_without_persistence_support`
- `not_frozen`

Advantage:
- minimal scope
- works with current logs
- no engine changes required

### Option B — Controlled Experiment Wrapper

Create one tiny controlled run configuration
designed to enter freeze while retaining non-zero visible structure.

Advantage:
- produces a concrete canonical control artifact

Risk:
- may require parameter tuning and could blur into experiment design

Recommended order:
- do Option A first
- do Option B only if needed

---

## 6. RECOMMENDED VALIDATOR LOGIC

For each non-legacy tick:

1. Read:
   - `freeze_state`
   - `freeze_reason`
   - `visible_edges`
   - optional `cluster_edges`

2. Classify:
   - if `freeze_state != true` -> `not_frozen`
   - if `freeze_state == true` and `visible_edges > 0` -> `supports_persistence`
   - if `freeze_state == true` and `visible_edges == 0` -> `frozen_without_persistence_support`

3. Reject only on schema / semantic inconsistency,
   not on the absence of persistence support itself.

This keeps the validator observational rather than interpretive.

---

## 7. MINIMAL TEST SET

### Test A — Frozen with persistence support

Preconditions:
- canonical-separated run or controlled log
- `freeze_state == true`
- `visible_edges > 0`

Expectation:
- validator returns `supports_persistence`

---

### Test B — Frozen without persistence support

Preconditions:
- frozen run or synthetic control
- `freeze_state == true`
- `visible_edges == 0`

Expectation:
- validator returns `frozen_without_persistence_support`
- no invalid-state claim is made automatically

---

### Test C — Not frozen

Preconditions:
- active run

Expectation:
- validator returns `not_frozen`

---

### Test D — Legacy compatibility

Preconditions:
- `legacy_visible_only`

Expectation:
- validator does not fabricate persistence semantics for legacy logs

---

## 8. WHAT NOT TO DO YET

Do NOT in this step:
- implement thaw
- require propagation metrics
- require loop detection
- promote persistence to a new hypothesis
- infer ontology from a single diagnostic contaminated log

This remains a capability-closure step for Stage 3.

---

## 9. CLOSURE ARTIFACTS

KROK 37 is complete when these artifacts exist:

1. this plan
2. updated workflow memory
3. updated test-grid guidance

KROK 37 does NOT yet prove persistence.
It only defines the narrowest honest test target for it.

---

## 10. NEXT IMPLEMENTATION MOVE

Recommended next action after this note:
- implement one validator for frozen persistence support
  using current log fields only

That should become KROK 38.

Only after that should we decide
whether a controlled persistence experiment is still needed.

---

End of plan
