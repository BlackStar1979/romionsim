# VALIDATION SCRIPTS

Purpose:
Quick index for the validator layer: what each script checks and where it is usually used.

Run from repository root:

```powershell
cd C:\Work\romionsim
python .\validation\<script_name>.py --log <path-to-simulation.jsonl>
```

---

## Contract

- `validate_log_minimal.py`
  Minimal JSONL contract, event order, required `core` and `fracture`.

## Projection / freeze

- `validate_projection_modes.py`
  Projection regimes: legacy, canonical, contaminated.
- `validate_freeze_modes.py`
  Freeze semantics: `no_bridges`, `zero_bridge_weight`, `active`.
- `validate_frozen_persistence.py`
  Snapshot and evolving frozen persistence classes.

## Loops

- `validate_loop_modes.py`
  Loop detection regime and applicability.
- `validate_loop_persistence.py`
  Summary-level loop persistence across ticks.
- `validate_loop_identity.py`
  Strict exact-signature continuity, births, dissolutions, identity breaks.

## Exclusion

- `validate_exclusion_readiness.py`
  Not-ready / partially-ready / candidate-ready states.
- `validate_exclusion_ingredients.py`
  Richer identity instrumentation.
- `validate_exclusion_candidate_path.py`
  Absent / partial / complete duplicate-candidate path.
- `validate_exclusion_rejection_signal.py`
  Explicit stabilization-stage rejection signal and allowed non-rejection.
- `validate_exclusion_rejection_outcome.py`
  First post-signal outcome check: no second valid stabilized duplicate after rejection.
- `validate_exclusion_minimal_enforcement.py`
  First enforcement-level check: canonical stabilized output remains uniqueness-preserving after rejection.

Typical log sources:
- `workflow/projection_test_logs/`
- `workflow/freeze_test_logs*/`
- `workflow/loop*_test_logs/`
- `workflow/exclusion*_test_logs/`

End.
