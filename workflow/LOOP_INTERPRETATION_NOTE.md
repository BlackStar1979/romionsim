# LOOP INTERPRETATION NOTE

Purpose:
Clarify how to read loop-related quantities during the current rebuild,
without promoting any new claims into canonical theory.

This note is operational and interpretive.
It does NOT modify `docs/THEORY_V3.9.md`.

---

## 1. THREE DIFFERENT THINGS

When reading loop results, keep these three layers separate:

1. ontological property
2. stability proxy
3. projection / expression proxy

Confusing them creates fake certainty.

---

## 2. ONTOLOGICAL PROPERTY

At the theory level, a Δ-loop is:
- a stabilized relational pattern in FRACTURE,
- formally represented as a closed path,
- described by canonical quantities such as:
  - `L0`
  - `L1`
  - `LT`
  - `mu(C)`
  - `sigma(C)`
  - `QT`

In this sense:
- `L0` is not “stability”
- `L0` is not “visibility”
- `L0` is a structural property of the loop itself

The safest current reading:
- length belongs to what the loop is structurally,
  not yet to what it proves dynamically.

---

## 3. STABILITY PROXY

Stability is a different question:
- does the loop-bearing structure persist?
- does it resist dissolution?
- does it recur or remain present across ticks?

In theory, the more direct stability-side quantity is:
- `mu(C)`

But the current MVP engine does not yet compute full canonical `mu(C)`.

So in the rebuild, current stability-related readings are only proxies, for example:
- persistence of `loop_count >= 1`
- persistence of min/max loop length summaries
- persistence across a contiguous interval of ticks

This means:
- loop length may correlate with stability,
- but loop length is not itself the stability claim.

Safe wording:
- “loop length may co-determine stability”

Unsafe wording:
- “longer loop = more stable loop”

That stronger rule has not been established.

---

## 4. PROJECTION / EXPRESSION PROXY

“Expression” is best treated as a FRACTURE-side observational issue:
- how strongly the structure appears in the projected layer,
- how clearly it survives thresholds,
- how visible its consequences are in the logged observables.

This is not the same as ontology.
It is also not automatically the same as stability.

A loop may:
- exist structurally,
- yet project weakly,
- or project intermittently,
- or be hidden by thresholding choices.

So expression belongs closer to:
- observability,
- threshold passage,
- persistence in logged summaries,
- later bridge / cluster context

than to the bare ontological definition of the loop.

---

## 5. CURRENT SAFE INTERPRETATION

For the current project stage, the safest interpretation is:

- `L0`:
  structural/topological property
- loop persistence across ticks:
  provisional stability proxy
- visibility in logged FRACTURE summaries:
  provisional expression / projection proxy

So a sentence like this is currently acceptable:

`topological length may influence both stability and expression,`
`but the current engine does not yet justify a simple one-variable law.`

That is the clean middle ground:
- more informative than saying “we know nothing,”
- more honest than claiming a finished ontology-to-observable rule.

---

## 6. PRACTICAL RULE FOR FUTURE STEPS

When writing conclusions or plans:

- if the statement is about what a loop is:
  use structural language
- if the statement is about persistence over ticks:
  use stability-proxy language
- if the statement is about what appears in logs:
  use projection/expression language

Do not collapse these into one sentence
unless the supporting experiment really tested the link explicitly.

---

## 7. WHAT THIS SUGGESTS FOR FUTURE TESTS

The current interpretation naturally suggests later tests such as:

- relation between `L0` and persistence interval
- relation between `L0` and loop edge coverage
- relation between loop-bearing structure and freeze/frozen persistence
- later, relation between richer invariants and class structure

But these remain future tests,
not current conclusions.

---

End.
