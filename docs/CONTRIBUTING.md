# CONTRIBUTING — ROMION Documentation

## Role

This document defines the rules for contributing to ROMION documentation.

Its purpose is to:
- protect the canonical ontology,
- enforce strict epistemic separation,
- prevent uncontrolled speculative growth,
- ensure long-term internal consistency.

These rules apply to all documentation files.

---

## 1. Fundamental Principle

Ontology is not negotiable by accident.

ROMION strictly separates:
- existence (ontology),
- emergence mechanics,
- interpretation and mapping,
- hypotheses and predictions.

Any contribution that violates this separation is invalid.

---

## 2. Epistemic Categories (Non-Negotiable)

Every document belongs to exactly one epistemic category,
determined by its filename prefix.

THEORY_
- Canonical Ontology
- May define existence and rules of being
- Must NOT use domain language or introduce hypotheses

FOUNDATION_
- Formal Bases
- May explain axioms
- Must NOT add entities or dynamics

MECHANICS_
- Deductive
- May derive behavior from THEORY
- Must NOT modify ontology

SPEC_
- Structural Extensions
- May define operators and structure
- Must NOT redefine existence

MAP_
- Interpretation
- May use physics or cosmology language
- Must NOT assert ontological truth

HYPOTHESIS_
- Testable Claims
- Must define H1, H0, and falsification criteria
- Must NOT claim explanation or truth

POTENTIALS
- Orientational
- May list possibilities
- Must NOT assert claims or hypotheses

GLOSSARY
- Terminology
- May align language
- Must NOT define ontology

If a contribution cannot be clearly assigned to one category,
it must not be merged.

---

## 3. Rules for Modifying THEORY_V3.9.md

THEORY_V3.9.md is the sole ontological authority.

Allowed:
- Explicitly versioned changes (for example V4.0)
- Formal tightening of definitions
- Removal of ambiguity

Forbidden:
- Examples, metaphors, or narratives
- Domain language (particles, fields, Lambda, etc.)
- Hypotheses, predictions, interpretations
- Silent edits without version increment

If in doubt, do not modify THEORY.

---

## 4. Creating or Modifying Other Documents

FOUNDATION, MECHANICS, SPEC:
- Must reference relevant THEORY sections
- Must not override ontological commitments
- May evolve independently of THEORY

MAP:
- May use external physics and cosmology terminology
- Must explicitly declare interpretative status
- Must never be cited as ontological authority

HYPOTHESIS:
Every hypothesis document must define:
- H1
- H0
- falsification criteria
- required observables or metrics
- validity and failure conditions

No hypothesis may claim explanation or truth.

POTENTIALS:
- Serves as an inventory of possible explanations or predictions
- Makes no claims
- Does not assert hypotheses
- Guides future MAP or HYPOTHESIS development

---

## 5. Domain-Leakage Prohibition

This rule is absolute.

Domain-specific terms (for example electron, photon, dark matter, inflation)
are forbidden outside:
- MAP files
- HYPOTHESIS files
- POTENTIALS.md

Violations require immediate correction.

---

## 6. Measurement and Validity Rules

All measurement-related content must obey:

Fail-Closed Principle:
Invalid data invalidates the entire result.

Parameter Explicitness Rule:
No unnamed parameters, thresholds, or flags.

Pre-Registered Exploration Rule:
Post-hoc scanning or tuning is invalid.

These rules apply globally.

---

## 7. Units: SI and RI

Every quantitative value must declare its unit system.

SI:
- Observable physical units

RI (Relational Internal):
- Internal relational units

Examples:
- L1(C) = 1.2 SI
- mu(C) = 0.42 RI

Mixing SI and RI without explicit declaration is prohibited.

---

## 8. Proper Lifecycle of New Ideas

Correct progression of ideas:

1. Idea exists informally
2. Idea is listed in POTENTIALS as a possibility
3. Idea may be interpreted in MAP
4. Idea may become a testable HYPOTHESIS
5. Only if absolutely unavoidable, THEORY may be revised in a new version

Skipping steps is not allowed.

---

## 9. Style and Language

- Use precise, declarative language
- Avoid metaphors and persuasion
- Avoid narrative framing
- Maintain neutral, technical tone

ROMION documentation is not a manifesto.

---

## 10. Final Rule

If you are unsure where something belongs,
it does not belong in the documentation yet.

---

End of CONTRIBUTING