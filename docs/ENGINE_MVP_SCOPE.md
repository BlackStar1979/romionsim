# ENGINE MVP SCOPE — romionsim

Scope Version: v1  
Applies to Ontology Version: THEORY_V3.9  
Documentation Status: v1-prerelease

---

## Purpose

This document defines the **minimal viable scope**
for the reference simulation engine romionsim.

The purpose is not completeness,
but ontological correctness and testability.

---

## Definition of MVP

The engine is considered MVP-complete if it:

- implements the canonical ontology without extensions,
- preserves strict separation of CORE and FRACTURE,
- allows at least one hypothesis to be tested end-to-end.

Nothing more is required for MVP.

---

## What MUST Be Implemented (Mandatory)

### CORE Layer

The engine must implement:

- a relational structure without global boundary,
- local update rules operating without metric concepts,
- parameterized evolution without hidden constants.

CORE must not contain:
- distances,
- geometry,
- physical interpretations.

---

### Boundary Behavior

The engine must support:

- generation of relational configurations,
- stabilization selection rules,
- transition to observable structures.

The boundary is an engine of emergence,
not a threshold switch.

---

### FRACTURE Layer

The engine must implement:

- detection of stabilized relational structures,
- representation of clusters or loop-like patterns,
- basic observables derived from stabilization.

FRACTURE exists only after stabilization.

---

### Logging and Auditing

The engine must:

- log all parameters explicitly,
- allow run reproduction,
- support fail-closed behavior on invalid states.

---

## What MUST NOT Be Implemented (Explicitly Deferred)

The following are outside MVP scope:

- physical particle names,
- field equations,
- metric spacetime dynamics,
- quantum measurement formalism,
- cosmological expansion models,
- performance optimization,
- visualization tools.

Omitting these is correct and intended.

---

## Minimum Success Criteria

MVP is successful when:

- CORE and FRACTURE are distinguishable in execution,
- at least one HYPOTHESIS document can be tested,
- results can be audited against documentation,
- no ontology changes are required.

---

## Post-MVP Direction (Informational)

After MVP, future work may include:

- additional hypothesis support,
- richer FRACTURE observables,
- performance improvements,
- optional visualization layers.

These are not prerequisites for v1 release.

---

## Notes

Failure to implement deferred elements
does not indicate a problem.

Failure to respect ontology and separation
does.

---

End of ENGINE MVP SCOPE