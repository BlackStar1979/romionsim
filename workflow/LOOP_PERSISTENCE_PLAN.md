# LOOP PERSISTENCE PLAN — KROK 45

Purpose:
Define the next narrow Stage 4 plan
for loop-state persistence across ticks
after the first loop-detection slice is already in place.

This step does NOT implement loop identity yet.
It does NOT implement exclusion.
It does NOT introduce loop classes or thaw work.

---

## 1. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` sections III.1–III.3
- `docs/MECHANICS_EMERGENCE.md` section 4
- `docs/SPEC_LOOP_CLASSES.md`
- `workflow/LOOP_DETECTION_PLAN.md`
- `conclusions/LOOP_DETECTION_INTERIM.md`
- `workflow/ENGINE_TEST_GRID.md`

Canonical constraints extracted from those files:
- Δ-loops are stable relational patterns in FRACTURE.
- Stability matters before classification.
- Loop classes presuppose reproducible loop-state structure.
- Exclusion presupposes identity and niche semantics
  that do not yet exist in the current engine.

So the next honest question is narrower:
- can the engine detect persistence of loop-bearing structure over time
  without pretending it already knows full loop identity?

---

## 2. WHY THIS STAGE IS NEXT

After KROK 44:
- the engine can detect loops at a single tick,
- canonical and non-applicable regimes are already separated,
- but Stage 4 still lacks any explicit time-extended stability criterion.

Without a persistence pass, the engine still cannot honestly support:
- loop-state stability claims,
- later class reproducibility claims,
- later exclusion work that depends on durable structure.

So the next honest move is:
- define a persistence proxy over consecutive ticks,
- keep it weaker than true loop identity,
- record the interpretation boundary explicitly.

---

## 3. MINIMUM DESIGN GOAL

Introduce one validator-first persistence pass that answers:

Does a run contain a contiguous interval of ticks
in which loop-bearing structure remains present
at a reproducible summary level?

This stage does NOT require:
- proving that an individual canonicalized cycle
  is the same ontological loop across all ticks,
- niche tracking,
- orientation persistence,
- class persistence,
- bundle persistence.

It only prepares a minimal stability signal
for later stronger loop-state work.

---

## 4. FIRST PERSISTENCE DEFINITION

For Stage 4B MVP,
`loop persistence` should mean:

- a contiguous tick interval of length `L_loop`,
- in `projection_regime == canonical_separated`,
- with `loop_detection_regime == "canonical_cluster_graph"`,
- and `loop_count >= 1` at every tick in that interval.

This is the weakest acceptable definition
that still says more than a one-tick loop flash.

Important boundary:
- this is summary-level persistence,
  not proof of persistent loop identity.
- the same count at two ticks does not imply
  the same exact canonicalized cycles survived unchanged.

That stronger claim should remain blocked
until identity/signature machinery exists.

---

## 5. RECOMMENDED FIRST PARAMETER

Registered first persistence window:
- `L_loop = 3`

Why start small:
- current loop controls are short and local,
- this step is about defining a validator-level floor,
  not claiming mature loop stability already.

If `L_loop = 3` is too easy or always trivial,
the next step may raise it,
but this first pass should establish the contract first.

---

## 6. OPTIONAL STRONGER READING

If the same interval also preserves:
- `max_loop_length`
- `min_loop_length`

without change,
that may be recorded as stronger support,
but not yet as identity.

Recommended stronger derived class for later use:
- `supports_stable_loop_summary`

Meaning:
- contiguous `L_loop` interval
- `loop_count >= 1`
- and min/max length summaries remain constant

This stronger class should remain optional in the first pass.

---

## 7. IMPLEMENTATION SHAPE

Recommended code path:

1. `validation/`
   - add one dedicated loop-persistence validator
   - keep it independent of freeze validators

2. `workflow/loop_test_logs/`
   - reuse existing canonical loopy and acyclic controls
   - add a short synthetic control only if needed
     to separate weak persistence from no persistence

3. `conclusions/`
   - add one interim note stating exactly what this persistence pass
     proves and what it does not prove

Reason:
- KROK 44 already created the right observables,
- this step should reuse them before opening new engine complexity.

---

## 8. FIRST VALIDATOR CLASSES

Recommended initial classes:
- `supports_loop_persistence`
- `loop_present_but_not_persistent_enough`
- `no_loops_detected`
- `legacy_only`
- `not_applicable_contaminated`

Optional stronger class:
- `supports_stable_loop_summary`

The first pass does not need more.

---

## 9. MINIMAL TEST SET FOR THIS STAGE

### Test A — Persistent Canonical Loops

Preconditions:
- canonical-separated run
- `loop_count >= 1` across at least `L_loop` consecutive ticks

Expectation:
- validator returns `supports_loop_persistence`

---

### Test B — Acyclic Canonical Control

Preconditions:
- canonical-separated run
- `loop_count == 0` for all ticks

Expectation:
- validator returns `no_loops_detected`

---

### Test C — Legacy Rejection

Preconditions:
- legacy run

Expectation:
- validator returns `legacy_only`

---

### Test D — Contaminated Rejection

Preconditions:
- contaminated run

Expectation:
- validator returns `not_applicable_contaminated`

---

### Test E — Short Non-Persistent Loop Interval

Preconditions:
- canonical-separated run
- loop interval exists but is shorter than `L_loop`

Expectation:
- validator returns `loop_present_but_not_persistent_enough`

This may require a small synthetic control log
if no real short-interval case exists yet.

---

## 10. WHAT NOT TO DO IN THIS STAGE

Do NOT:
- claim persistent identity of individual loops
- open exclusion work
- introduce niche labels
- introduce loop classes
- infer cosmological meaning
- mix bridge/freeze logic into the persistence criterion by default

This step should remain
the smallest useful extension of Stage 4A.

---

## 11. CLOSURE ARTIFACTS

KROK 45 is complete when these artifacts exist:

1. this persistence plan
2. updated workflow memory
3. updated test-grid guidance

KROK 45 does NOT yet prove loop persistence in code.
It only registers the smallest honest path for doing so.

---

## 12. NEXT IMPLEMENTATION MOVE

Recommended next action after this note:
- implement one validator-first pass
  for summary-level loop persistence
  using `L_loop = 3`

That should become:
- `KROK 46 — Loop Persistence Validator`

Only after that should we decide whether:
- stronger summary stability is worth adding,
- loop identity work can start,
- or exclusion remains blocked.

---

End of plan
