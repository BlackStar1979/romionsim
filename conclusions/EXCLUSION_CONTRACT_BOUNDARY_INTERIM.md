# EXCLUSION CONTRACT BOUNDARY — INTERIM

Status:
Technical conclusion for KROK 63.

Purpose:
Record the current boundary between:
- narrow exclusion-compliance expectations that the engine should already preserve,
- and broader exclusion behavior that still counts as missing feature
  rather than contract violation.

---

## What now counts as narrow exclusion compliance

At the current Stage 5 level,
the following may already be treated as contract-facing expectations
for the engine in its narrow MVP scope:

1. complete duplicate identity is required before exclusion-related rejection
2. partial similarity must not trigger exclusion rejection
3. stabilization-stage rejection must remain explicit and auditable
4. canonical stabilized output must remain uniqueness-preserving
   at the rejection tick in the already validated narrow sense

If one of these is violated in a run that is otherwise within the same scope,
the default reading should now be:
- implementation bug
or
- broken narrow exclusion compliance

not merely:
- "future work someday"

---

## What still does NOT count as contract violation

The following still remain outside current narrow exclusion compliance:
- annihilation interpretation
- fusion / bundling consequences
- re-projection conflict handling
- deeper-process claims about what happened before rejection
- any claim of full exclusion closure across the engine

If these are missing,
the default reading should still be:
- missing feature

not:
- contract failure

---

## Why this boundary matters

Without this boundary,
the project risks two opposite mistakes:

1. being too weak:
   validated behavior never becomes enforceable expectation

2. being too strong:
   partially closed Stage 5 behavior gets over-promoted
   into a contract it does not yet deserve

This note is the narrow middle:
- validator-backed Stage 5 behavior can now constrain the engine a bit more,
- but the contract is still not pretending that full exclusion mechanics exist.

---

## Technical conclusion

KROK 63 closes successfully.

The project now has an explicit architectural boundary for exclusion work:
- some Stage 5 behavior is strong enough to count as narrow compliance expectation,
- but broader exclusion branches still remain missing feature rather than bug.

This is a contract-boundary clarification,
not a theory revision and not a claim of full exclusion completion.

End.
