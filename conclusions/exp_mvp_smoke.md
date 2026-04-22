# Conclusion: exp_mvp_smoke

Status: prerelease conclusion  
Source: experiments/exp_mvp_smoke (log + summary)

---

## What Was Tested

This was a smoke test of the new romionsim architecture.

The goal was to verify that:
- the engine can run end-to-end via API,
- schema-versioned logs are produced,
- minimal validation passes,
- minimal analysis can be computed and exported.

This experiment was not a scientific hypothesis test.

---

## Data Artifacts

- simulation log: experiments/exp_mvp_smoke/raw_logs/simulation_<run_id>.jsonl
- summary export: experiments/exp_mvp_smoke/analysis/summary.json

---

## Validity

- Log structure was validated against the minimal contract.
- The run completed with END.ok = true.
- The summary.json is consistent with the log content.

---

## Observations (From Summary)

FRACTURE visibility decreased over the run:
- fracture.visible_ratio_start = 0.6530612244897959
- fracture.visible_ratio_end = 0.018867924528301886

FRACTURE visible edges decreased:
- fracture.visible_edges_start = 32
- fracture.visible_edges_end = 1

CORE total weight decreased:
- core.total_weight_start = 1.363007454289892
- core.total_weight_end = 0.5616211971616101

The run included occasional edge additions,
but the overall FRACTURE visibility still decayed.

---

## Interpretation Boundary

These observations are expected under the current MVP rules:
- global multiplicative decay of weights
- fixed visibility threshold w_visible

This conclusion does not claim a physical explanation.
It only records observed behavior of the MVP engine.

---

## Next Step Recommendation

Create a second smoke experiment with altered parameters
to confirm that the trend is controllable, for example:
- increase p_add or decrease p_decay
- change w_visible

If the direction of the trend can be controlled,
then the engine is ready for the first hypothesis formulation.

---

End of conclusion