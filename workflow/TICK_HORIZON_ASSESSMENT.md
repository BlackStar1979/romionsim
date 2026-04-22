# TICK HORIZON ASSESSMENT — 100 vs Longer Runs

Purpose:
Record the current evidence on whether `ticks = 100`
is still a reasonable default under the rebuilt engine.

This is a methodological note only.
It does NOT retroactively alter completed experiments.

---

## 1. CURRENT REPO FACTS

Observed from local files:
- all current experiment `params.json` files use `ticks = 100`
- current metric definitions were written around that practice:
  - `FRACTURE_SURVIVAL_TIME_v1.md`
  - `TAIL_MEAN_VISIBLE_RATIO_v1.md`

Important boundary:
- `ticks = 100` is not required by:
  - `docs/ENGINE_MVP_SCOPE.md`
  - `docs/ENGINE_CONTRACT.md`
  - canonical theory documents

So `100` is an experimental convention,
not an ontological or contractual requirement.

---

## 2. WHY 100 SHOULD BE RECHECKED

The earlier choice of `100` came from an older engine context
where longer runs were operationally expensive.

Under the current rebuilt engine,
that assumption needed to be verified again
instead of being carried forward by inertia.

---

## 3. CURRENT PROBE RESULTS

Probe runs were executed under the current engine
for representative cases at:
- 100 ticks
- 200 ticks
- 300 ticks
- 500 ticks
- and selected 1000-tick controls

Representative runtime observation:
- 100 ticks: about `0.01 s` per run
- 500 ticks: about `0.05 s` per run
- 1000 ticks: about `0.10 s` per run

Practical conclusion:
- current runtime growth is roughly linear
- the rebuilt engine does NOT show the old severe 100-tick pressure

---

## 4. INTERPRETIVE FINDINGS

### Case A — `p_decay = 0.99`, `w_visible = 0.02`

- `T_survival(0.1)` stays at about `78`
- extending horizon adds little to the primary boundary reading

Conclusion:
- `100` is already sufficient for this clearly decaying regime

---

### Case B — `p_decay = 0.995`, `w_visible = 0.026`

- at `100` ticks, `T_survival(0.1) = 99`
- at longer horizons, first sub-threshold occurs around tick `104`

Conclusion:
- `100` slightly censors this boundary-near stable case
- the distortion is real but modest

---

### Case C — `p_decay = 0.995`, `w_visible = 0.027`

- already declines before the `100`-tick cutoff

Conclusion:
- `100` is broadly enough to distinguish the boundary transition here

---

### Case D — `p_decay = 0.999`, `w_visible = 0.02`

- at `100` ticks, `T_survival(0.1) = 99`
- at `200`, `300`, `500`, and even `1000` ticks,
  the run still remains above the threshold

Conclusion:
- `100` heavily censors high-stability regimes
- for this class of run, `100` is too short for horizon-sensitive conclusions

---

## 5. METHODOLOGICAL CONSEQUENCE

Under the rebuilt engine,
`ticks = 100` is no longer justified as a default by runtime cost alone.

The real tradeoff is now methodological:
- shorter runs are still fine for smoke checks and coarse decays
- but they can censor genuinely persistent regimes

So the question is no longer:
- \"can the engine afford more than 100?\"

The current answer is:
- yes, easily

The better question is:
- \"what horizon is appropriate for the experimental claim?\"

---

## 6. RECOMMENDATION

### Keep `100` for:
- smoke / contract validation
- very cheap sanity checks
- reproducing already completed prerelease results without changing protocol

### Use `300` as the new default for:
- new exploratory stability runs
- Stage 3 capability experiments
- future preregistered checks where late-time behavior matters

Why `300`:
- materially reduces right-censoring vs `100`
- remains operationally cheap under current engine
- avoids jumping immediately to overly long horizons everywhere

### Use `500` for:
- high-stability regimes (for example `p_decay >= 0.999`)
- persistence-oriented runs
- cases where `T_survival` still saturates at `ticks - 1` under `300`

---

## 7. METRIC NOTE

If future experiments move beyond `100` ticks,
current metrics remain usable,
but one nuance matters:

- `FRACTURE_SURVIVAL_TIME` is horizon-sensitive by design
- `TAIL_MEAN_VISIBLE_RATIO_N20` remains valid,
  but its tail window becomes a smaller fraction of the run

Therefore:
- existing v1 metrics do not need immediate replacement
- but a future metric revision may want a horizon-relative tail window

This is not required yet for Stage 3 work.

---

## 8. PRACTICAL RULE

Recommended rule for current project work:

1. Do not rewrite or reinterpret completed 100-tick experiments retroactively.
2. Treat `100` as a legacy baseline, not as the universal default.
3. For new runs:
   - start at `300`
   - escalate to `500` when stability still saturates the horizon

---

End of assessment
