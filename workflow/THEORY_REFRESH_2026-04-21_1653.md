# THEORY REFRESH — 2026-04-21 16:53

Purpose:
Anti-drift note written after a full read-through of the active canonical
`docs/` corpus.
This file does not add theory.
It records the constraints that must remain visible while implementing the
current engine stages.

Scope reviewed:
- `docs/README.md`
- `docs/INDEX.md`
- `docs/ARCHITECTURE.md`
- `docs/THEORY_V3.9.md`
- `docs/FOUNDATION_HYPERGRAPH.md`
- `docs/FOUNDATION_PROJECTION.md`
- `docs/MECHANICS_EMERGENCE.md`
- `docs/SPEC_LOOP_CLASSES.md`
- `docs/SPEC_LOOP_ALGEBRA.md`
- `docs/SPEC_EXCLUSION_MECHANICS.md`
- `docs/POTENTIALS.md`
- `docs/MAP_PARTICLE_PHYSICS.md`
- `docs/MAP_INTERACTIONS.md`
- `docs/MAP_COSMOLOGY.md`
- `docs/HYPOTHESIS_PHASE_PROPAGATION.md`
- `docs/HYPOTHESIS_CWD_DIPOLE.md`
- `docs/GLOSSARY.md`
- `docs/PUBLIC_SUMMARY.md`
- `docs/FAQ.md`
- `docs/ENGINE_MVP_SCOPE.md`
- `docs/ENGINE_CONTRACT.md`
- `docs/PRE_RELEASE.md`
- `docs/CONTRIBUTING.md`
- `docs/CHANGELOG.md`

Reviewed on:
- 2026-04-21

---

## 1. Canonical constraints that must stay fixed

1. The ontology remains strictly relational.
   No objects, particles, spacetime points, or fields may be treated as
   fundamental engine entities.

2. CORE is pre-spatial, pre-temporal, and pre-object.
   Any metric, geometry, distance, or object language belongs only to
   projection / FRACTURE-level emergence.

3. FRACTURE is not a second ontology.
   It is an emergent, projection-bound observable regime produced through
   stabilization at the active CORE/FRACTURE boundary.

4. Projection is selective and lossy stabilization.
   It must not silently drift into:
   - coarse-graining,
   - collapse,
   - embedding,
   - direct readout of hidden objects.

5. Exclusion is a structural constraint, not a force.
   The exclusion documents support treating rejection as a topological /
   structural impossibility, not as repulsion, collision, or interaction law.

6. Layer discipline is canonical, not stylistic.
   The project only stays coherent if:
   - `THEORY` states existence,
   - `FOUNDATION` states assumptions,
   - `MECHANICS` states dynamics,
   - `SPEC` states structural extensions,
   - `MAP` states interpretation,
   - `HYPOTHESIS` states falsifiable claims,
   - `POTENTIALS` states possibilities only.

---

## 2. Implementation guardrails derived from docs

1. Do not let `MAP_*`, `POTENTIALS.md`, or public-summary language leak into
   engine semantics.
   Those files may guide orientation, but they do not authorize ontology.

2. Do not let workflow notes overrule canonical `docs/`.
   Workflow can constrain process and scope, but not redefine theory.

3. Keep CORE/FRACTURE separation fail-closed.
   If a field or metric mixes projection layers, identity layers, or canonical
   vs contaminated regimes ambiguously, the implementation should reject or mark
   it explicitly instead of guessing.

4. Keep exclusion narrow until the ingredients are real.
   The canon supports an early stabilization-stage rejection point, but not
   broad exclusion mechanics before richer identity ingredients exist.

5. Keep thaw deferred.
   Nothing in the reviewed docs justifies jumping ahead of:
   - exclusion instrumentation,
   - rejection signaling,
   - later structural conflict handling.

6. Keep loop claims modest.
   Current engine work may support:
   - loop detection,
   - summary persistence,
   - operational tracked identity.
   It does not yet justify full ontological identity claims or mature loop
   classes.

7. Keep prerelease language conservative.
   Existing code and validators do not by themselves lift prerelease status.
   The docs still require an approved reference engine and end-to-end
   hypothesis testability.

---

## 3. Practical reading of the current stage sequence

Current engine work remains aligned with canon if read this way:
- Stage 2 = projection hygiene
- Stage 3 freeze-side = bridge-mediated activity distinction
- Stage 4 = loop observability before class ontology
- Stage 5 = richer structural identity before exclusion

That means the current next step:
- `KROK 57 — Exclusion Rejection Signal Implementation`

is still a legitimate next move, because:
- `SPEC_EXCLUSION_MECHANICS.md` supports structural rejection,
- the current repo already has preconditions for a narrow signal,
- and the step can stay below full exclusion enforcement.

---

## 4. Things most likely to cause future drift

1. Treating projection summaries as if they were ontology.
2. Treating operational identity as if it were full ontological identity.
3. Treating contaminated regimes as if they were canonical evidence.
4. Treating interpretive maps as implementation specs.
5. Treating prerelease MVP success as if it already closed the theory.
6. Treating future-facing `POTENTIALS` language as permission to skip stages.

---

## 5. Operational conclusion

This review does not change the current plan.
It confirms that the active path remains coherent if we keep:
- layer separation strict,
- exclusion structural,
- thaw deferred,
- interpretation subordinate to canon,
- and every new capability explicitly marked by regime.

End.
