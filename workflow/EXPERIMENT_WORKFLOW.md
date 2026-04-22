# EXPERIMENT WORKFLOW — ROMION

Purpose:
Define the working procedure for experimental development in `romionsim`.
This workflow is for executable experiment work,
not for canonical ontology changes.

Principle:
Every experimental result must be reproducible from repository state,
explicit parameters, logged outputs, and a readable conclusion trail.

Design rule:
The workflow must stay smaller than the experiment itself.
If process overhead starts growing faster than experimental clarity,
simplify the workflow before adding new control layers.

---

## 1. WHEN TO USE THIS WORKFLOW

Use this workflow when work touches any of the following:
- `experiments/`
- `analysis/`
- `validation/`
- `hypotheses/`
- `conclusions/`
- `workflow/`

If work changes ontology, theory, or canonical spec meaning,
pause and treat that as a `docs/` governance task instead.

---

## 1A. SINGLE MAIN GOAL

Each active krok must have one main goal only.

That goal should be expressible in one short sentence, for example:
- define one metric,
- run one sweep,
- validate one hypothesis test document,
- write one conclusion update.

Do not bundle multiple goals into one krok.
If the work naturally splits into separate goals,
create the next krok instead of widening the current one.

---

## 2. EXPERIMENT LIFECYCLE

### Phase A — Frame the question

Before writing code or running a sweep, define:
- what is being tested,
- whether it is technical validation or hypothesis testing,
- which metric is primary,
- what counts as failure,
- which existing logs or scripts can be reused.

Required outputs:
- experiment `spec.md` or hypothesis test note,
- explicit decision about the single active krok.

Minimal framing check:
- one main goal,
- one primary metric or validation target,
- one reason this krok matters now.

---

### Phase B — Prepare the run

Create or update the experiment package under `experiments/`.

Minimum required files:
- `params.json`
- `run.py`
- `validate.py`
- `spec.md`

Rules:
- parameters must be explicit in `params.json`,
- wrappers may stay minimal,
- validation must be separate from execution,
- no manual precomputation hidden outside the repo.

Scaffold rule:
- every experiment must distinguish:
  - swept variables,
  - fixed scaffold parameters,
  - metric-version defaults used for interpretation
- if only a subset is varied,
  conclusions must say explicitly that the result is conditional
  on the remaining fixed scaffold

Tick-horizon rule:
- `ticks = 100` is reserved for:
  - smoke checks,
  - contract validation,
  - reproducing already completed historical baselines
- `ticks = 300` is the default for new exploratory runs
  unless there is a documented reason to choose otherwise
- `ticks = 500` should be used when:
  - the run still saturates the observation horizon at `300`,
  - or late-time persistence is itself part of the question

Required discipline:
- every new experiment spec should state why its tick horizon is appropriate
- do not use 100-tick runs alone for long-horizon stability claims
- do not let engine-side compatibility fallbacks define experiment meaning

---

### Phase C — Execute

Run the experiment through its wrapper or approved automation.

Expected outputs:
- JSONL log in `raw_logs/`
- validator pass
- reproducible `run_id`

Rules:
- do not edit logs by hand,
- do not overwrite conclusions before validation,
- if execution fails, fix the pipeline before interpretation.

Execution honesty rule:
If the current repository state is no longer understood well enough
to predict the effect of a change, stop and restore clarity first.
Do not improvise across unclear dependencies.

---

### Phase D — Validate

Validation is mandatory before analysis.

Validation layers:
- schema/log validation via `validation/validate_log_minimal.py`
- experiment-specific validation via local `validate.py`

A run is not usable for conclusions if validation fails.

---

### Phase E — Analyze

Convert validated logs into derived artifacts.

Allowed analysis outputs:
- `summary.json`
- CSV tables
- metric comparison outputs
- compact derived notes

Rules:
- analysis must be derived from logs,
- analysis scripts must not mutate engine behavior,
- derived metrics should be documented before becoming decision criteria.

---

### Phase F — Conclude

Write human-readable conclusions only after:
- execution is reproducible,
- validation passes,
- analysis artifacts exist.

Write conclusions in `conclusions/`.

Rules:
- separate observed results from interpretation,
- state scope and limits,
- avoid promoting results to canonical claims automatically.
- if a result was obtained under a frozen scaffold,
  say so explicitly in the conclusion artifact

---

## 3. SINGLE-KROK RULE

Only one krok may be active at a time.

Operational meaning:
- do not define a new sweep while the current metric is unresolved,
- do not mix technical validation with hypothesis interpretation in one step,
- do not start result synthesis before the required metric work is complete.

--- 

## 3A. LIGHTWEIGHT RISK CHECK

Before substantial work, do a short risk check in plain language.

Minimum questions:
- What is most likely to break?
- What would be expensive to misunderstand?
- What must not be modified casually?

Typical answers in this repo:
- shared automation,
- validator behavior,
- engine semantics,
- interpretation accidentally presented as canonical.

If any of these risks are active,
name them in the working memory before proceeding.

---

## 4. WHAT CAN CHANGE IN EACH AREA

### Safe to change during experiment work
- experiment wrappers
- experiment params
- analysis scripts
- workflow notes
- conclusions
- hypothesis test documents

### Change carefully
- shared validators
- reusable automation scripts

### Escalate before changing
- engine semantics
- log contract semantics
- canonical docs meaning

---

## 5. REQUIRED ARTIFACT CHAIN

For a result to count as usable, the chain should be complete:

1. `spec.md` or hypothesis-test framing
2. explicit `params.json`
3. executable run
4. validated `raw_logs`
5. derived `analysis/` artifact
6. conclusion note
7. workflow memory update

If one link is missing, the result is provisional.

---

## 6. FAILURE HANDLING

If a run fails:
- preserve the error context,
- identify whether failure is in engine, wrapper, validation, or analysis,
- fix the earliest broken layer first,
- rerun end to end.

If results are ambiguous:
- do not reinterpret theory to save the run,
- tighten the metric or experiment framing first,
- record the ambiguity in workflow memory.

If context handling fails:
- stop making structural edits,
- read the relevant source files again,
- update workflow memory with what is known and unknown,
- resume only after the ambiguity is reduced.

---

## 7. UPDATE DISCIPLINE

After process changes:
- update this workflow,
- update `PROJECT_WORKING_MEMORY.md`,
- regenerate project map if structure changed.
- after updating `PROJECT_WORKING_MEMORY.md`, verify that `## 4. NEXT REQUIRED STEP` contains only the active krok band and ends immediately before `## 5. NON-NEGOTIABLE OPERATING RULES`.

Use:

```powershell
python .\rebuild_project_map.py
```

For longer work, leave a compact checkpoint in the workflow memory:
- what changed,
- what remains true,
- what comes next.

If the work uncovers inherited fixed values that were being treated too casually:
- document them in workflow memory or a dedicated workflow note immediately,
- revise any over-broad conclusion wording in the same session.

---

## 8. CURRENT PRIORITY

Current priority must be read from:
- `workflow/PROJECT_WORKING_MEMORY.md`

Reason:
- this workflow defines procedure,
- the working memory defines the currently active krok.

--- 

End of workflow
