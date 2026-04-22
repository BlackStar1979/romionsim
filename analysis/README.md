# ANALYSIS SCRIPTS

Purpose:
Quick index for analysis and automation helpers.

Run from repository root:

```powershell
cd C:\Work\romionsim
```

---

## Root analysis

- `mvp_read_log.py`
  Read one simulation log and emit a small summary JSON.

## Automation

- `automation/run_stability_sweep.py`
  Run registered sweep validations and refresh `stability_table_auto.csv`.
- `automation/run_stability_refine.py`
  Run registered refine validations and refresh `stability_table_auto.csv`.
- `automation/generate_refine_runs.py`
  Generate the refine run layout from the registered lane.
- `automation/add_tail_metric_to_csv.py`
  Compute `TAIL_MEAN_VISIBLE_RATIO_N20` and update the sweep/refine CSVs.

Interpretation rule:
These scripts are analysis-only. They must not become a shadow engine.

End.
