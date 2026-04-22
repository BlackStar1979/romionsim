# LOOP DETECTION PLAN — KROK 43

Purpose:
Define the narrowest honest Stage 4 plan
for explicit loop detection and loop-state observables
in the current MVP engine.

This step does NOT implement loop detection yet.
It does NOT introduce loop classes.
It does NOT implement exclusion, propagation, or thaw.

---

## 1. CANONICAL BASIS

Relevant local sources:
- `docs/THEORY_V3.9.md` sections III.1–III.3
- `docs/MECHANICS_EMERGENCE.md` section 4
- `docs/SPEC_LOOP_CLASSES.md`
- `docs/ENGINE_MVP_SCOPE.md`
- `workflow/ENGINE_TEST_GRID.md`

Canonical constraints extracted from those files:
- Δ-loops are FRACTURE-level stabilized relational patterns,
  not particles and not new primitives.
- The first useful engine task is detection and tracking,
  not immediate classification.
- Loop observables must remain structural and reproducible.
- The implementation must not smuggle in geometry, field equations,
  or domain mappings.

---

## 2. WHY THIS STAGE IS NEXT

After KROK 42:
- freeze-side Stage 3 has a real non-synthetic control artifact,
- thaw remains intentionally deferred,
- Stage 4 is now the next blocked capability band with the best
  unlock-per-change ratio.

Without explicit loop detection, the engine still cannot honestly support:
- loop persistence tests,
- loop-class reproducibility checks,
- topological exclusion work,
- later phase-propagation and anisotropy work that depend on loop observables.

So the next honest move is:
- detect loops first,
- emit minimal loop observables,
- avoid overcommitting to loop identity or physics language.

---

## 3. MINIMUM DESIGN GOAL

Introduce one MVP-level loop-detection path that:
- derives a projected graph suitable for cycle analysis,
- detects simple loops in that graph,
- emits a small reproducible loop summary,
- remains fail-closed when the run regime is not suitable.

This stage does NOT require:
- full loop identity,
- niche identity,
- orientation or topological charge,
- bundle logic,
- class labels such as quark-like or lepton-like,
- exclusion events.

It only prepares the observables needed for later stages.

---

## 4. FIRST OPERATIONAL LOOP DEFINITION

For Stage 4 MVP, a detected loop should mean:

- a simple cycle in a FRACTURE-level projected graph,
- using undirected edges only,
- with no repeated internal vertex,
- length `>= 3`.

Important boundary:
- this is an analytical proxy for Δ-loop detection in the current MVP,
  not a claim that the engine already computes every canonical invariant
  from THEORY section III.

Preferred first projected graph for detection:
- the cluster-supporting subgraph
  using edges with `w >= w_cluster`

Why this graph first:
- `MECHANICS_EMERGENCE.md` ties loop stabilization to structure formation,
- `w_bridge` is already reserved for interaction channels,
- using bridge edges directly would blur Stage 4 with Stage 3 field behavior.

Fail-closed rule:
- if the run is not `projection_regime == canonical_separated`,
  loop observables must be absent or explicitly rejected,
  not guessed from contaminated or legacy runs.

---

## 5. FIRST LOOP OBSERVABLES

The first pass should stay small.

Recommended run-level / tick-level observables:
- `loop_count`
- `max_loop_length`
- `min_loop_length`
- `mean_loop_length`
- `loop_edge_coverage_ratio`

Definitions:
- `loop_count`:
  number of detected simple cycles after canonicalization
- `max_loop_length`:
  maximum topological cycle length in the detected set
- `min_loop_length`:
  minimum topological cycle length in the detected set
- `mean_loop_length`:
  arithmetic mean of detected cycle lengths
- `loop_edge_coverage_ratio`:
  fraction of cluster edges that belong to at least one detected loop

Why these first:
- they use only topological length `L0`-like information,
- they do not require geometry,
- they are enough to stop inferring loop behavior from `visible_ratio` alone.

Not yet required in Stage 4 MVP:
- `L1`
- `LT`
- `mu(C)`
- `sigma(C)`
- `QT`

Those remain future extensions once the engine can carry
the necessary semantics honestly.

---

## 6. CANONICALIZATION RULE

Cycle detection can overcount the same undirected loop
through rotation and reversal.

So Stage 4 MVP needs one explicit canonicalization rule:
- treat cycles as identical under:
  - rotation
  - reversal
- keep only one canonical representative per undirected simple cycle

This is required before any metric based on `loop_count`
can be considered reproducible.

---

## 7. WHERE THE IMPLEMENTATION SHOULD LIVE

Recommended code path:

1. `engine/boundary/`
   - add a small loop-detection helper over the projected cluster graph

2. `engine/boundary/stabilization.py`
   - compute loop summary only for `canonical_separated`
   - attach the summary to the fracture snapshot

3. `engine/fracture/state.py`
   - accept optional loop summary fields fail-closed

4. `engine/core/evolution.py`
   - thread the richer boundary output into FRACTURE state

5. validation
   - add one dedicated loop-summary validator

Reason:
- keeps CORE free of FRACTURE semantics,
- keeps projection-derived loop analysis at the boundary/FRACTURE layer,
- avoids pretending that CORE itself contains loops as metric objects.

---

## 8. LOGGING PLAN

Do not change event order.
Keep:
- `METADATA`
- `PARAMS`
- `TICK`
- `END`

Extend only `TICK.fracture`.

Recommended optional fields for Stage 4 MVP:
- `loop_count`
- `max_loop_length`
- `min_loop_length`
- `mean_loop_length`
- `loop_edge_coverage_ratio`
- `loop_detection_regime`

Recommended `loop_detection_regime` values:
- `canonical_cluster_graph`
- `not_applicable_legacy`
- `not_applicable_contaminated`

This keeps loop summaries auditable
and prevents misreading diagnostic runs as canonical loop support.

---

## 9. MINIMAL TEST SET FOR THIS STAGE

These tests should be enough to close the first Stage 4 pass.

### Test A — Loop Detection Sanity

Preconditions:
- canonical-separated run
- projected cluster graph contains at least one simple cycle

Expectation:
- `loop_count >= 1`
- length metrics are finite and consistent

---

### Test B — Acyclic Control

Preconditions:
- canonical-separated run
- projected cluster graph is acyclic

Expectation:
- `loop_count == 0`
- coverage ratio is `0`
- no fake loop metrics appear

---

### Test C — Regime Rejection

Preconditions:
- `legacy_visible_only` or `diagnostic_contaminated`

Expectation:
- loop summary is absent
  or explicitly marked not applicable
- validator does not allow these runs
  to count as canonical Stage 4 support

---

### Test D — Reproducible Canonicalization

Preconditions:
- one graph containing the same undirected loop
  discoverable through multiple traversals

Expectation:
- the loop is counted once only

---

## 10. WHAT NOT TO DO IN THIS STAGE

Do NOT:
- introduce loop classes
- introduce particle names
- compute orientation or charge heuristically and call it canonical
- mix bridge edges into the first canonical loop graph
- open exclusion work yet
- open thaw work yet
- claim cosmological meaning from loop counts

This stage should remain
the narrowest possible observability-enabling layer.

---

## 11. CLOSURE ARTIFACTS

KROK 43 is complete when these artifacts exist:

1. this design note
2. updated workflow memory
3. updated test-grid guidance

KROK 43 does NOT yet prove that loop detection works in code.
It only registers the smallest honest path for doing so.

---

## 12. NEXT IMPLEMENTATION MOVE

Recommended next action after this note:
- implement one minimal loop-summary path
  over the canonical cluster graph
  with validator-backed sanity checks

That should become:
- `KROK 44 — Loop Detection Implementation`

The first useful vertical slice is:
- detect canonicalized simple cycles,
- emit topological-length summaries,
- validate canonical vs non-applicable regimes,
- stop there before any loop classes or exclusion logic.

---

End of plan
