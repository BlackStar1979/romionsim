# EXCLUSION REJECTION SIGNAL — INTERIM

Status:
Technical conclusion for KROK 57.

---

## Purpose

Close the first honest exclusion-enforcement pass
without pretending to implement full exclusion mechanics.

The target was narrower:
- emit one explicit stabilization-stage rejection signal,
- only for complete duplicate-state candidates,
- while preserving non-rejection for absent or partial candidate paths.

---

## What was added

- contract-level helper for a minimal rejection note in
  `engine/api/log_contract.py`
- validator:
  `validation/validate_exclusion_rejection_signal.py`
- updated targeted controls for:
  - partial candidate path with no rejection
  - complete candidate path with explicit rejection

The rejection signal remains outside `fracture`.
It is treated as a process/event fact, not a stable FRACTURE field.

---

## Validation classes

The validator now distinguishes:
- `legacy_only`
- `not_applicable_contaminated`
- `rejection_signal_absent`
- `rejection_signal_partial_nonrejected`
- `rejection_signal_emitted`

The emitted rejection signal is accepted only when all of the following hold:
- duplicate path exists
- duplicate identity is complete
- `rejection_stage = "stabilization"`
- `rejection_reason = "duplicate_niche_identity"`
- `rejection_identity_complete = true`

---

## Result

KROK 57 closes successfully at the signal level.

What is now supported:
- explicit auditable rejection signaling for a complete duplicate candidate
- explicit non-rejection for partial candidate identity
- explicit non-rejection when no candidate path exists

What is still NOT claimed:
- full exclusion enforcement
- fusion / bundling handling
- re-projection handling
- thaw work

---

## Technical conclusion

Stage 5 now has its first explicit exclusion-enforcement signal,
but still only as a narrow stabilization-stage event.

This is enough to show that exclusion is no longer only a future narrative.
It is now represented in the project as a distinct, auditable event-level fact.

It is not yet enough to claim full exclusion closure.

End.
