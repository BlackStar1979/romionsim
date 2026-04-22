# EXPERIMENT ENTRYPOINTS

Purpose:
Minimal index for executable experiment wrappers.

General pattern:
- `params.json` defines the run
- `run.py` executes
- `validate.py` executes and validates

Run from repository root:

```powershell
cd C:\Work\romionsim
```

---

## Smoke

- `experiments/exp_mvp_smoke/run.py`

```powershell
python .\experiments\exp_mvp_smoke\run.py
```

- `experiments/exp_mvp_smoke/validate.py`

```powershell
python .\experiments\exp_mvp_smoke\validate.py
```

## Larger families

For families such as:
- `exp_mvp_stability_sweep`
- `exp_mvp_stability_refine`
- `exp_mvp_frozen_persistence_control`

start from:
- experiment-local `spec.md`
- `analysis/README.md`

End.
