# ENGINE CONTRACT — Documentation vs romionsim

Contract Version: v1  
Applies to Ontology Version: THEORY_V3.9  
Documentation Status: v1-prerelease

---

## Purpose

This document defines the minimal and non-negotiable contract
between the ROMION documentation and the reference
simulation engine named romionsim.

The purpose of this contract is to:
- protect the canonical ontology,
- prevent ontology drift driven by implementation details,
- define what constitutes an implementation error.

---

## Primary Rule

romionsim is an implementation of the documentation.

The documentation is not a description of the implementation.

If behavior differs:
- the implementation is wrong,
- unless an explicit THEORY revision is undertaken.

---

## Ontology Authority

The following rules are absolute:

- THEORY_V3.9.md defines what exists.
- romionsim must not introduce new ontological entities.
- romionsim may not redefine CORE, FRACTURE, or boundary behavior.
- Failure to implement a mechanism does not invalidate the ontology.

---

## Layer Separation

romionsim must preserve strict layer separation:

- CORE logic operates without metric concepts.
- FRACTURE logic operates only on stabilized structures.
- INTERPRETATION may exist in analysis code only.

Backreaction from higher layers to lower layers is forbidden.

---

## Parameters and Metrics

All configurable parameters in romionsim must be:

- explicitly named,
- recorded in logs,
- stable across runs unless changed deliberately.

No hidden constants or implicit defaults
with ontological meaning are permitted.

---

## Failure Classification

Mismatch between documentation and behavior
must be classified as one of the following:

1. Implementation bug
2. Missing feature
3. Unsupported hypothesis
4. Explicit THEORY revision (rare)

Only case 4 permits changing documentation.

---

## Preconditions for Stable v1 Release

The documentation prerelease status is lifted when:

- romionsim implements CORE and FRACTURE separation
- at least one hypothesis is testable end-to-end
- engine behavior is auditable against documentation

Until then, romionsim is considered experimental.

---

## Scope

This contract applies only to documentation
and the reference simulation engine.

It does not define scientific correctness,
only architectural compliance.

---

End of ENGINE CONTRACT