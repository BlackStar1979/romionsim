# PROJECT WORKING MEMORY — ROMION

Purpose:
Operational memory for ongoing experimental work.
This file should be enough to understand:
- current project state,
- active experiment phase,
- where important assets live,
- what must not be changed casually,
- what happens next.

Scope:
This is process memory, not canonical theory.
Canonical ontology and specifications live in `docs/`.

Update rule:
If the project state changes in a meaningful way,
update this file in the same session.

---

## 1. CURRENT STATE

Last verified: 2026-04-22

Current experiment status:
- KROK 25 complete: metric definition `FRACTURE_SURVIVAL_TIME`
- KROK 26 complete: coarse stability sweep
- KROK 27 complete: hypothesis H1 defined
- KROK 28 complete: refine falsification pass for `p_decay = 0.995`
- KROK 29 complete: define secondary metric `TAIL_MEAN_VISIBLE_RATIO_N20`
- KROK 30 complete: synthesize secondary-metric results
- KROK 31 complete: projection-layer separation plan written
- KROK 32 complete: minimal projection-layer separation implemented and validated
- KROK 33 complete: freeze/thaw stage plan written
- KROK 34 complete: explicit freeze detection implemented and validated
- KROK 35 complete: bridge-weight freeze refinement plan written
- KROK 36 complete: bridge-weight freeze refinement implemented and validated
- KROK 37 complete: frozen persistence plan written
- KROK 38 complete: frozen persistence validator implemented and validated
- KROK 39 complete: evolving frozen persistence plan written
- KROK 40 complete: evolving frozen persistence validator implemented and validated
- KROK 41 complete: evolving frozen persistence control plan written
- KROK 42 complete: evolving frozen persistence control family executed and validated
- KROK 43 complete: loop-detection plan written
- KROK 44 complete: minimal loop detection implemented and validated
- KROK 45 complete: loop-persistence plan written
- KROK 46 complete: loop-persistence validator implemented and validated
- KROK 47 complete: loop-identity plan written
- KROK 48 complete: loop-identity validator implemented and validated
- KROK 49 complete: exclusion-readiness plan written
- KROK 50 complete: exclusion-readiness audit implemented and validated
- KROK 51 complete: exclusion-ingredients plan written
- KROK 52 complete: exclusion-ingredient instrumentation plan written
- KROK 53 complete: exclusion-ingredient instrumentation implemented and validated
- KROK 54 complete: exclusion candidate-path plan written
- KROK 55 complete: exclusion candidate-path implementation implemented and validated
- KROK 56 complete: exclusion rejection-point plan written
- KROK 57 complete: exclusion rejection signal implemented and validated
- KROK 58 complete: exclusion rejection outcome plan written
- KROK 59 complete: exclusion rejection outcome validator implemented and validated
- KROK 60 complete: exclusion minimal enforcement plan written
- KROK 61 complete: exclusion minimal enforcement validator implemented and validated
- KROK 62 complete: exclusion contract narrowing plan written
- KROK 63 complete: exclusion contract boundary note written
- KROK 64 complete: exclusion contract promotion plan written
- KROK 65 complete: exclusion promotion candidate note written
- KROK 66 complete: exclusion promotion gate plan written
- KROK 67 complete: exclusion promotion gate assessment written
- KROK 68 complete: exclusion narrow contract proposal plan written
- KROK 69 complete: exclusion narrow contract proposal note written
- KROK 70 complete: exclusion contract patch candidate plan written
- KROK 71 complete: exclusion contract patch candidate note written
- KROK 72 complete: exclusion canonical patch gate plan written
- KROK 73 complete: exclusion canonical patch gate assessment written
- KROK 74 complete: exclusion human review packet plan written
- KROK 75 complete: exclusion human review packet note written
- KROK 76 complete: exclusion review handoff plan written
- KROK 77 complete: exclusion review handoff note written
- KROK 78 complete: workflow consolidation strategy written
- KROK 79 complete: workflow consolidation executed

Hard rule:
Only one active krok at a time.

Main-goal rule:
Each active krok must have one main goal only.

---

## 2. REPOSITORY DIGEST

### `engine/`
Simulation engine.

Subroles:
- `core/` → relational graph, evolution, metrics, RNG, params
- `boundary/` → stabilization rules at the CORE/FRACTURE boundary
- `fracture/` → observable FRACTURE state
- `api/` → public engine interface and log contract

Handling rule:
Do not change lightly.
Edits here affect reproducibility and theory compliance.

---

### `experiments/`
Executable experiments.
Each experiment should remain isolated and reproducible.

Expected local pattern:
- `params.json` → explicit configuration
- `run.py` → execution wrapper
- `validate.py` → validation gate
- `raw_logs/` → JSONL run logs
- `analysis/` → summaries, CSVs, derived artifacts

Currently active experiment families:
- `exp_mvp_smoke`
- `exp_mvp_smoke_2`
- `exp_mvp_stability_sweep`
- `exp_mvp_stability_refine`
- `exp_mvp_frozen_persistence_control`

---

### `analysis/`
Analysis and automation only.
No engine logic should migrate here.

Important assets:
- `analysis/mvp_read_log.py`
- `analysis/automation/run_stability_sweep.py`
- `analysis/automation/generate_refine_runs.py`
- `analysis/automation/run_stability_refine.py`
- `analysis/metrics/FRACTURE_SURVIVAL_TIME_v1.md`
- `analysis/automation/add_tail_metric_to_csv.py`
- `analysis/metrics/TAIL_MEAN_VISIBLE_RATIO_v1.md`

Handling rule:
If analysis workflow changes, update this file and the workflow document.

---

### `validation/`
Validation scripts for log and regime checks.

Important assets:
- `validation/validate_log_minimal.py`
- `validation/validate_projection_modes.py`
- `validation/validate_freeze_modes.py`
- `validation/validate_frozen_persistence.py`
- `validation/validate_loop_modes.py`
- `validation/validate_loop_persistence.py`
- `validation/validate_loop_identity.py`
- `validation/validate_exclusion_readiness.py`
- `validation/validate_exclusion_ingredients.py`
- `validation/validate_exclusion_candidate_path.py`

---

### `hypotheses/`
Formalized hypotheses and their test documents.

Current files:
- `HYPOTHESIS_FRACTURE_STABILITY_V1.md`
- `HYPOTHESIS_FRACTURE_STABILITY_V1_TEST.md`

Handling rule:
Do not silently rewrite historical hypothesis intent.
Extend with test or revision documents when needed.

---

### `conclusions/`
Human-readable conclusions and interim summaries.
No raw logs, no executable logic.

Current focus:
- `FRACTURE_STABILITY_INTERIM.md`
- `FRACTURE_STABILITY_REFINE_INTERIM.md`
- `FRACTURE_STABILITY_SECONDARY_METRIC.md`
- `PROJECTION_LAYER_SEPARATION_INTERIM.md`
- `FREEZE_STATE_INTERIM.md`
- `FREEZE_STATE_REFINED_INTERIM.md`
- `FROZEN_PERSISTENCE_INTERIM.md`
- `EVOLVING_FROZEN_PERSISTENCE_INTERIM.md`
- `EVOLVING_FROZEN_PERSISTENCE_CONTROL_INTERIM.md`
- `LOOP_DETECTION_INTERIM.md`
- `LOOP_PERSISTENCE_INTERIM.md`
- `LOOP_IDENTITY_INTERIM.md`
- `EXCLUSION_READINESS_INTERIM.md`
- `EXCLUSION_INGREDIENT_INSTRUMENTATION_INTERIM.md`
- `EXCLUSION_CANDIDATE_PATH_INTERIM.md`
- `TICK_HORIZON_REASSESSMENT_INTERIM.md`

---

### `docs/`
Canonical documentation only:
ontology, architecture, theory, specs, glossary, public summary.

Handling rule:
Do not treat workflow notes or experimental summaries as canonical
unless they are deliberately promoted into `docs/`.

---

### `workflow/`
Operational coordination layer.

Contents:
- `PROJECT_WORKING_MEMORY.md` → current project state
- `EXPERIMENT_WORKFLOW.md` → workflow for running and extending experiments
- `ENGINE_TEST_GRID.md` → staged map from docs to engine-test sequence
- `EXCLUSION_CONTRACT_PROMOTION_TRACK.md` → active consolidated tracker for the Stage 5 contract-promotion lane
- `WORKFLOW_CONSOLIDATION_STRATEGY.md` → strategy for reducing active workflow fragmentation without losing history
- `PROJECTION_LAYER_SEPARATION_PLAN.md` → minimal design note for Stage 2 implementation
- `FREEZE_THAW_STAGE_PLAN.md` → minimal design note for Stage 3 freeze detection
- `BRIDGE_WEIGHT_FREEZE_REFINEMENT_PLAN.md` → minimal design note for Stage 3B freeze refinement
- `FROZEN_PERSISTENCE_PLAN.md` → minimal design note for Stage 3 frozen persistence support
- `EVOLVING_FROZEN_PERSISTENCE_PLAN.md` → minimal design note for interval-based frozen persistence over time
- `EVOLVING_FROZEN_PERSISTENCE_CONTROL_PLAN.md` → registered narrow path for one non-synthetic control family after validator closure
- `LOOP_DETECTION_PLAN.md` → narrow Stage 4 design note for explicit loop detection and loop-state observables
- `LOOP_INTERPRETATION_NOTE.md` → operational note separating loop ontology, stability proxies, and projection/expression proxies
- `TICK_HORIZON_ASSESSMENT.md` → methodological note on moving beyond the legacy 100-tick baseline
- `FIXED_PARAMETER_AUDIT.md` → audit of inherited fixed values, scope restrictions, and engine-side fallbacks
- `INHERITED_PARAMETER_ORIGINS.md` → reconstruction of which current fixed values came from old protocol and which are rebuild-local simplifications
- `SCAFFOLD_ROBUSTNESS_PLAN.md` → minimal sequence for testing whether Stage 1 stability survives seed, size, and scaffold changes
- `OLDIES_EVOLUTION_REVIEW.md` → synthesis of theory evolution, process failures, and empirical-history lessons extracted from `workflow/oldies/`
- `DOCS_WORKFLOW_CONSISTENCY_AUDIT_2026-04-21_0628.md` → active documentation audit covering `docs/` and active `workflow/` markdown files, with explicit exclusions for archives and generated artifacts
- `THEORY_REFRESH_2026-04-21_1653.md` → anti-drift note distilled from a full read-through of the active canonical `docs/` corpus before continuing Stage 5 work
- `LOOP_PERSISTENCE_PLAN.md` → narrow Stage 4B design note for summary-level loop persistence across ticks
- `LOOP_IDENTITY_PLAN.md` → narrow Stage 4C design note for operational loop identity / canonical signature across ticks

Active-reading rule:
- use the central workflow files plus the current consolidated tracker and synthesis note
- treat old Stage 5 contract-promotion micro-files as preserved support material, not default active context
- `EXCLUSION_READINESS_PLAN.md` → narrow Stage 5 readiness note for the gap between operational identity and exclusion mechanics
- `EXCLUSION_INGREDIENTS_PLAN.md` → narrow Stage 5 note for the smallest explicit richer-identity and duplicate-path layer before real exclusion
- `EXCLUSION_INGREDIENT_INSTRUMENTATION_PLAN.md` → minimal Stage 5 implementation note for emitting richer identity fields before any exclusion logic
- `EXCLUSION_CANDIDATE_PATH_PLAN.md` → narrow Stage 5 note for a real duplicate-state candidate path before any exclusion enforcement
- `EXCLUSION_REJECTION_POINT_PLAN.md` → narrow Stage 5 note for where stabilization-stage exclusion rejection should occur before broader mechanics are attempted
- `EXCLUSION_REJECTION_OUTCOME_PLAN.md` → narrow Stage 5 note for what stabilization-stage rejection does and does not imply before broader exclusion mechanics
- `EXCLUSION_MINIMAL_ENFORCEMENT_PLAN.md` → narrow Stage 5 note for the smallest real enforcement move beyond signaling and first post-signal outcome closure
- `EXCLUSION_CONTRACT_NARROWING_PLAN.md` → narrow Stage 5 note for which validated exclusion claims may already be treated as contract expectations
- `EXCLUSION_CONTRACT_PROMOTION_PLAN.md` → narrow Stage 5 note for when a validated exclusion expectation is mature enough to move closer to contract-facing status
- `EXCLUSION_PROMOTION_GATE_PLAN.md` → narrow Stage 5 note for the additional evidence and stability required before any candidate can be treated as promotion-ready
- `conclusions/EXCLUSION_CONTRACT_BOUNDARY_INTERIM.md` → current boundary between narrow exclusion-compliance expectation and still-missing Stage 5 feature work
- `conclusions/EXCLUSION_PROMOTION_CANDIDATE_INTERIM.md` → current set of narrow exclusion behaviors that are credible promotion candidates, without yet promoting them into the canonical contract
- `workflow/exclusion_rejection_test_logs/` → targeted controls for post-signal exclusion outcome semantics, including explicit duplicate-persistence detection
- `workflow/tick_reassessment/` → rerun artifacts comparing 100-tick and longer-horizon behavior
- `workflow/loop_identity_test_logs/` → targeted controls for strict loop identity continuity, births, dissolutions, and identity breaks
- `workflow/exclusion_readiness_test_logs/` → targeted controls for exclusion-readiness states, including partial-readiness and candidate-ready synthetic cases
- `workflow/exclusion_ingredient_test_logs/` → fresh engine-generated canonical controls for richer Stage 5 identity instrumentation
- `workflow/exclusion_candidate_path_test_logs/` → targeted controls for absent, partial, and complete duplicate-state candidate signaling
- `analysis/README.md` → quick index for analysis and automation scripts with typical entrypoints
- `validation/README.md` → quick index for validator scripts, their purpose, and typical log sources
- `experiments/README.md` → quick index for executable experiment wrappers and how to run them
- `PROJECT_MAP_FULL.md`
- `PROJECT_MAP_FULL.json`

---

## 3. CURRENT RESULTS WORTH PRESERVING

Primary metric:
- `FRACTURE_SURVIVAL_TIME(theta = 0.1)`

Secondary metric:
- `TAIL_MEAN_VISIBLE_RATIO_N20`

Established result from current passes:
- completed 100-tick experiments remain valid as short-horizon baselines
- after horizon reassessment, the earlier `p_decay = 0.995` plateau claim over `w_visible ∈ [0.018, 0.026]`
  is treated as right-censored rather than canonical
- broad degradation with increasing `w_visible` remains real,
  but earlier sharp-boundary language has been revised
- all currently preserved stability findings are conditional on the fixed prerelease scaffold:
  `seed = 42`, `n_nodes = 50`, `spawn_scale = 1.0`, `decay_scale = 1.0`,
  `w_init_min = 0.01`, `w_init_max = 0.05`, `p_add = 0.05`, `w_prune = 0.0`

Evidence files:
- `experiments/exp_mvp_stability_sweep/analysis/stability_table_auto.csv`
- `experiments/exp_mvp_stability_refine/analysis/stability_table_auto.csv`
- `workflow/tick_reassessment/tick_reassessment_100_vs_300.csv`

Status note:
These are current experimental findings, not yet canonical theory.

---

## 4. NEXT REQUIRED STEP

Hygiene rule:
- this section may contain only the currently active krok band and must end immediately before `## 5. NON-NEGOTIABLE OPERATING RULES`

### KROK 58 — Exclusion Rejection Outcome Planning

Goal:
Prepare one narrow Stage 5 note
for what the rejected duplicate candidate means operationally
after the stabilization-stage rejection signal now exists.

Reason selected:
- KROK 57 now gives the project an explicit rejection signal,
- the next honest blocker is no longer whether rejection is signaled,
- it is what rejection does and does not imply structurally.

Required output:
- one narrow rejection-outcome plan
- no broader exclusion enforcement yet
- no thaw work yet

Status:
- complete

---

### KROK 59 — Exclusion Rejection Outcome Validator

Goal:
Validate the first narrow post-signal claim:
that a rejected complete duplicate candidate
does not survive as a second valid stabilized duplicate loop.

Reason selected:
- KROK 57 closed signaling,
- KROK 58 now defines what that signal does and does not mean,
- the next honest move is validator-first again,
  not broader exclusion execution.

Required output:
- one validator or validator extension
- one technical conclusion artifact
- no thaw implementation yet

Status:
- complete

---

### KROK 60 — Exclusion Minimal Enforcement Planning

Goal:
Prepare the next narrow Stage 5 note
for the smallest real enforcement step beyond signaling and immediate outcome validation.

Reason selected:
- KROK 57 closed signaling,
- KROK 59 now closes the first post-signal outcome claim,
- the next honest blocker is how far minimal enforcement can go
  without overclaiming full exclusion mechanics.

Required output:
- one narrow Stage 5 planning note
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 61 — Exclusion Minimal Enforcement Validator

Goal:
Validate the smallest real enforcement claim
beyond signaling and first outcome closure.

Reason selected:
- KROK 60 now defines the narrowest honest enforcement target,
- the next move should again be validator-first,
  not broad Stage 5 execution.

Required output:
- one validator or validator extension
- one technical conclusion artifact
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 62 — Exclusion Contract Narrowing Plan

Goal:
Prepare the next narrow Stage 5 note
for what can already be promoted from validator-level enforcement
into a stricter contract expectation.

Reason selected:
- KROK 61 now closes the first enforcement-level validator claim,
- the next blocker is how much of that claim can be treated as contract
  without pretending to have full exclusion mechanics.

Required output:
- one narrow Stage 5 planning note
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 63 — Exclusion Contract Boundary Note

Goal:
Clarify what already counts as a narrow exclusion-compliance expectation
and what still remains missing feature rather than contract violation.

Reason selected:
- KROK 62 now defines the narrowing logic,
- the next honest move is to record the contract boundary explicitly,
  not yet to broaden exclusion mechanics.

Required output:
- one narrow contract-boundary note
- one technical conclusion artifact
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 64 — Exclusion Contract Promotion Planning

Goal:
Prepare the next narrow step for deciding
whether any Stage 5 exclusion expectations should be promoted
from workflow/conclusions into a more formal contract-facing registry.

Reason selected:
- KROK 63 now defines the boundary,
- the next honest blocker is whether anything should be promoted further,
  not whether the boundary exists.

Required output:
- one narrow planning note
- no broad `docs/ENGINE_CONTRACT.md` rewrite yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 65 — Exclusion Promotion Candidate Note

Goal:
Record which current narrow exclusion behaviors
are credible promotion candidates
and which must remain below contract-facing status for now.

Reason selected:
- KROK 64 now defines the promotion test,
- the next honest move is to apply that test explicitly,
  not yet to rewrite canonical docs.

Required output:
- one narrow technical note
- one technical conclusion artifact
- no broad `docs/ENGINE_CONTRACT.md` rewrite yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 66 — Exclusion Promotion Gate Plan

Goal:
Prepare the next narrow step
for deciding what additional evidence or stability is required
before any promotion candidate can become an actual contract-facing proposal.

Reason selected:
- KROK 65 now identifies the candidate set,
- the next honest blocker is not "what are the candidates?"
- but "what gate must they pass before promotion is justified?"

Required output:
- one narrow planning note
- no broad `docs/ENGINE_CONTRACT.md` rewrite yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 67 — Exclusion Promotion Gate Assessment

Goal:
Assess which current promotion candidates
actually pass the narrow promotion gate
and which still fail it.

Reason selected:
- KROK 66 now defines the gate,
- the next honest move is to apply it explicitly,
  not yet to promote anything.

Required output:
- one narrow technical note
- one technical conclusion artifact
- no broad `docs/ENGINE_CONTRACT.md` rewrite yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 68 — Exclusion Narrow Contract Proposal Plan

Goal:
Prepare one narrow Stage 5 note
for how the gate-passing exclusion candidates
should be framed as a contract-facing proposal
without rewriting canonical contract docs yet.

Reason selected:
- KROK 67 now applies the promotion gate explicitly,
- the next honest move is to prepare one narrow proposal layer,
  not yet to promote it directly into canonical docs.

Required output:
- one narrow planning note
- no broad `docs/ENGINE_CONTRACT.md` rewrite yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 69 — Exclusion Narrow Contract Proposal Note

Goal:
Record the narrow proposal-ready exclusion expectations
that may later be carried toward contract-facing status,
still without rewriting canonical contract docs.

Reason selected:
- KROK 68 now defines the proposal frame,
- the next honest move is to state the narrow proposal explicitly,
  not yet to modify canonical contract documentation.

Required output:
- one narrow technical note
- one technical conclusion artifact
- no broad `docs/ENGINE_CONTRACT.md` rewrite yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 70 — Exclusion Contract Patch Candidate Plan

Goal:
Prepare one narrow plan
for how the proposal-ready exclusion expectations
could later be represented as a contract patch candidate,
still without editing canonical contract docs.

Reason selected:
- KROK 69 now closes the proposal-ready narrow exclusion set,
- the next honest move is to define a safe patch shape,
  not yet to modify canonical contract documentation.

Required output:
- one narrow planning note
- no broad `docs/ENGINE_CONTRACT.md` rewrite yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 71 — Exclusion Contract Patch Candidate Note

Goal:
Record the smallest safe contract-patch candidate shape
for the proposal-ready exclusion expectations,
still below direct canonical contract editing.

Reason selected:
- KROK 70 now defines the patch-candidate frame,
- the next honest move is to state that frame explicitly,
  not yet to edit canonical contract docs.

Required output:
- one narrow technical note
- one technical conclusion artifact
- no broad `docs/ENGINE_CONTRACT.md` rewrite yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 72 — Exclusion Canonical Patch Gate Plan

Goal:
Prepare one narrow gate
for deciding when the current contract-patch candidate
would be mature enough for direct canonical contract editing.

Reason selected:
- KROK 71 now defines the smallest safe patch candidate shape,
- the next honest move is to define the final gate before canonical editing,
  not yet to edit canonical docs.

Required output:
- one narrow planning note
- no direct `docs/ENGINE_CONTRACT.md` edit yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 73 — Exclusion Canonical Patch Gate Assessment

Goal:
Assess whether the current contract-patch candidate
passes the stricter gate for direct canonical contract editing,
while still stopping short of editing canonical docs.

Reason selected:
- KROK 72 now defines that stricter gate,
- the next honest move is to assess it explicitly,
  not yet to patch canonical docs.

Required output:
- one narrow technical note
- one technical conclusion artifact
- no direct `docs/ENGINE_CONTRACT.md` edit yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 74 — Exclusion Human Review Packet Plan

Goal:
Prepare one narrow plan
for packaging the exclusion contract-patch candidate
for explicit human review,
still before direct canonical contract editing.

Reason selected:
- KROK 73 now closes the stricter canonical-patch gate,
- the next honest move is to define the review packet shape,
  not yet to edit canonical docs.

Required output:
- one narrow planning note
- no direct `docs/ENGINE_CONTRACT.md` edit yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 75 — Exclusion Human Review Packet Note

Goal:
Record the smallest human-review-facing packet
for the current exclusion contract-patch candidate,
still below direct canonical contract editing.

Reason selected:
- KROK 74 now defines the review-packet frame,
- the next honest move is to state that frame explicitly,
  not yet to edit canonical docs.

Required output:
- one narrow technical note
- one technical conclusion artifact
- no direct `docs/ENGINE_CONTRACT.md` edit yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 76 — Exclusion Review Handoff Plan

Goal:
Prepare one narrow handoff plan
for moving the exclusion review packet
into explicit human decision space,
still before direct canonical contract editing.

Reason selected:
- KROK 75 now closes the smallest review-ready packet,
- the next honest move is to define the handoff shape,
  not yet to edit canonical docs.

Required output:
- one narrow planning note
- no direct `docs/ENGINE_CONTRACT.md` edit yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 77 — Exclusion Review Handoff Note

Goal:
Record the smallest safe handoff form
for the current exclusion review packet,
still below direct canonical contract editing.

Reason selected:
- KROK 76 now defines the handoff frame,
- the next honest move is to state that handoff explicitly,
  not yet to edit canonical docs.

Required output:
- one narrow technical note
- one technical conclusion artifact
- no direct `docs/ENGINE_CONTRACT.md` edit yet
- no thaw implementation yet
- no fusion or re-projection implementation yet

Status:
- complete

---

### KROK 78 — Workflow Consolidation Plan

Goal:
Prepare one narrow plan
for reducing Stage 5 workflow fragmentation
without losing restart safety or history.

Reason selected:
- KROK 77 now closes the review-handoff lane,
- the next honest move is to reduce workflow overhead
  before opening further adjacent micro-files.

Required output:
- one narrow planning note
- preserve historical files
- reduce active reading surface

Status:
- complete

---

### KROK 79 — Workflow Consolidation Execution

Goal:
Execute the first controlled consolidation pass
for the Stage 5 contract-promotion micro-chain,
while preserving restart safety and history.

Reason selected:
- KROK 78 now defines the consolidation strategy,
- the next honest move is to implement it deliberately,
  not to keep accumulating adjacent micro-files.

Required output:
- one controlled workflow consolidation pass
- one audit of the new active-reading path
- preserved history without active-surface bloat

Status:
- complete

---

### KROK 80 — Local Git Bootstrap Execution

Goal:
Execute the first local Git bootstrap pass
for the rebuilt repository,
following the already written GitHub preparation plan.

Reason selected:
- KROK 79 reduced workflow overhead,
- the next practical blocker is repository identity, not more workflow notes,
- and the GitHub preparation direction is already defined.

Required output:
- minimal `.gitignore`
- local Git initialization
- first local status inspection
- no remote replacement yet

Status:
- complete

---

### KROK 81 — Initial Git Snapshot Plan

Goal:
Prepare one narrow plan
for the first local snapshot commit,
based on the now-observed Git status.

Reason selected:
- KROK 80 now created a real local repository identity,
- the next honest move is to define the first snapshot scope
  before making any commit or touching the remote.

Required output:
- one narrow repo-hygiene planning note
- explicit first-snapshot scope
- no remote replacement yet

---

## 5. NON-NEGOTIABLE OPERATING RULES

1. Do not manually edit CSV outputs or raw logs.
2. Do not retroactively change the meaning of an existing hypothesis.
3. Only one krok can be active at a time.
4. Structural repository changes require refreshing the project map.
5. If process ambiguity appears, resolve it in the workflow files immediately.
6. If repository understanding becomes uncertain, stop and restore clarity before making structural edits.
7. Workflow overhead must stay smaller than the experiment itself.

Short risk check before substantial work:
- What is most likely to break?
- What would be expensive to misunderstand?
- What must not be modified casually?

Tick-horizon rule:
- `100` ticks is a legacy baseline for smoke checks and historical reproducibility
- `300` ticks is the default for new exploratory runs
- `500` ticks should be used when a run still saturates the horizon at `300`
  or when persistence itself is part of the question

Fixed-scaffold rule:
- when only some parameters are swept, conclusions must state the remaining fixed scaffold explicitly
- engine-side fallbacks are compatibility behavior only and must not be treated as recommended defaults
- if a fixed value is historically inherited, preserve its original protocol meaning,
  not only the bare number
- when robustness work begins, test seed first, then node count, then injection rate,
  unless a stronger local reason is documented

---

## 6. MAINTENANCE PROTOCOL

After a meaningful structural change, run:

```powershell
python .\rebuild_project_map.py
```

After a meaningful experimental change:
- update `PROJECT_WORKING_MEMORY.md`,
- update `EXPERIMENT_WORKFLOW.md` if the process changed,
- append one short note to the log below.

---

## 7. APPEND-ONLY LOG

Rules:
- append only,
- 1 to 3 short lines per entry,
- no deletions of prior entries.

<!-- APPEND_LOG_START -->

- [2026-04-22] GitHub remote `BlackStar1979/romionsim` was archived locally and on branch `archive/pre-rebuild-2026-04-22`; remote `main` is now a clean placeholder ready for rebuilt import after the first local snapshot
- [2026-04-22] Morning session audit 05:48 found no new hard inconsistencies; Stage 5 and GitHub preparation plan remain aligned at KROK 75
- [2026-04-21] Afternoon session audit 17:48 found no new hard inconsistencies; freeze state is clean for restart at KROK 69
- [2026-04-19] KROK 28 complete; refine confirms continuous stability region at p_decay=0.995
- [2026-04-19] PROJECT_MAP generated; working memory restructured
- [2026-04-19] KROK 29 defined TAIL_MEAN_VISIBLE_RATIO_N20 as the secondary metric with automation for sweep and refine CSVs
- [2026-04-19] KROK 30 added secondary-metric synthesis confirming the same stability boundary near w_visible = 0.027
- [2026-04-19] Hypothesis test H1 extended with secondary support from TAIL_MEAN_VISIBLE_RATIO_N20
- [2026-04-19] Added ENGINE_TEST_GRID.md mapping canonical docs to staged engine-test closures; next recommended stage is projection-layer separation
- [2026-04-19] KROK 31 completed with PROJECTION_LAYER_SEPARATION_PLAN.md, informed by oldies but scoped to the current MVP engine
- [2026-04-19] KROK 32 implemented projection-layer separation with explicit regimes and validation for legacy, canonical, and contaminated runs
- [2026-04-20] KROK 33 completed with FREEZE_THAW_STAGE_PLAN.md; freeze will be implemented before any thaw mechanics
- [2026-04-20] KROK 34 implemented explicit freeze_state/freeze_reason, validated legacy compatibility, and closed freeze detection at Stage 3A only
- [2026-04-20] KROK 35 completed with BRIDGE_WEIGHT_FREEZE_REFINEMENT_PLAN.md, defining Stage 3B before any thaw work
- [2026-04-20] KROK 36 implemented explicit bridge_weight and refined freeze semantics; zero_bridge_weight is validated semantically but is not yet a natural canonical run regime
- [2026-04-20] KROK 37 completed with FROZEN_PERSISTENCE_PLAN.md, choosing validator-first closure for the frozen-not-annihilated claim
- [2026-04-20] KROK 38 implemented validate_frozen_persistence.py and confirmed that freeze does not automatically imply annihilation
- [2026-04-20] KROK 39 completed with EVOLVING_FROZEN_PERSISTENCE_PLAN.md, choosing interval-based validator logic before any dedicated long-run control experiment
- [2026-04-20] Tick-horizon reassessment found that 100-tick plateau claims were right-censored; 300 is now the default for new exploratory runs and old refine conclusions were revised accordingly
- [2026-04-20] Tick-horizon assessment concluded that 100 ticks is a legacy baseline; recommend 300 for new exploratory runs and 500 for high-stability or persistence-focused runs
- [2026-04-20] Fixed-parameter audit classified metric defaults, fixed scaffold parameters, and engine fallbacks; current stability conclusions are now explicitly scoped to the prerelease scaffold
- [2026-04-20] Inherited-parameter origin review found that seed=42 and neutral scales have old protocol roots, while much of the current MVP scaffold is rebuild-local rather than faithfully inherited from the old baseline
- [2026-04-20] Scaffold robustness plan set the smallest useful follow-up order as seed -> node count -> p_add -> init band -> mild prune, while keeping KROK 40 as the active next engine step
- [2026-04-20] KROK 40 was explicitly gated on a structured review of workflow/oldies so the next validator step can absorb lessons from the full historical evolution of the project
- [2026-04-20] Structured oldies review completed; strongest retained lessons are layer discipline, anti-data-fitting guardrails, and the rule that historical datasets and speculative expansions must not silently steer current MVP engine semantics
- [2026-04-20] KROK 40 extended validate_frozen_persistence.py with interval-based evolving mode; validator classes now distinguish short frozen persistence from interval-level support at L_persist=20
- [2026-04-20] KROK 41 registered a narrow Stage 3C control path: one canonical-separated, non-synthetic experiment family with a 3-run w_bridge lane at 300 ticks before any broader search or thaw work
- [2026-04-20] KROK 42 executed the first Stage 3C control family; w_bridge=0.0225 and 0.0250 produced supports_evolving_persistence after an earlier active phase, so real non-synthetic frozen persistence is now established at control level
- [2026-04-20] KROK 43 completed with LOOP_DETECTION_PLAN.md, fixing the first Stage 4 scope to canonicalized simple-cycle detection on the cluster graph before any classes, exclusion, or thaw work
- [2026-04-20] KROK 44 implemented minimal loop detection with validate_loop_modes.py; canonical runs now emit cluster-graph loop summaries while legacy remains unchanged and contaminated runs stay non-applicable
- [2026-04-20] KROK 45 completed with LOOP_PERSISTENCE_PLAN.md, explicitly limiting the next Stage 4 step to summary-level loop persistence across ticks before any identity, class, or exclusion claims
- [2026-04-20] KROK 46 implemented validate_loop_persistence.py; Stage 4 now supports summary-level loop persistence, and the canonical loopy control already reaches the stronger stable-summary subclass
- [2026-04-20] KROK 47 completed with LOOP_IDENTITY_PLAN.md, limiting the next identity step to strict exact-signature tracking before any exclusion or full ontological identity claims
- [2026-04-20] KROK 48 implemented validate_loop_identity.py; Stage 4 now supports strict operational loop identity continuity, including births, dissolutions, and explicit identity-break detection
- [2026-04-20] KROK 49 completed with EXCLUSION_READINESS_PLAN.md, explicitly separating operational identity from exclusion-ready identity and blocking any premature exclusion implementation
- [2026-04-20] KROK 50 implemented validate_exclusion_readiness.py; Stage 5 now has an explicit audit language showing that real canonical runs remain blocked before exclusion while same-summary non-equivalent structures stay non-identical
- [2026-04-20] KROK 51 completed with EXCLUSION_INGREDIENTS_PLAN.md, setting richer identity fields plus a duplicate-state candidate path as the next honest pre-exclusion target
- [2026-04-20] KROK 52 completed with EXCLUSION_INGREDIENT_INSTRUMENTATION_PLAN.md, fixing the first richer-identity semantics as explicit provisional instrumentation rather than premature exclusion mechanics
- [2026-04-21] KROK 53 implemented richer Stage 5 identity instrumentation plus validate_exclusion_ingredients.py; canonical runs now emit provisional orientation, charge, excitation, anchor, and explicit candidate regime without claiming exclusion yet
- [2026-04-21] KROK 54 completed with EXCLUSION_CANDIDATE_PATH_PLAN.md, setting the next blocker as structured duplicate-candidate construction rather than exclusion enforcement
- [2026-04-21] KROK 55 implemented validate_exclusion_candidate_path.py and targeted controls; Stage 5 now distinguishes absent, partial, and complete duplicate-state candidates without enforcing exclusion yet
- [2026-04-21] KROK 56 completed with EXCLUSION_REJECTION_POINT_PLAN.md, fixing the first exclusion enforcement point at stabilization-stage rejection rather than jumping to broader mechanics
- [2026-04-21] Active docs/workflow audit completed; active markdown documentation is coherent for continuation from KROK 56, with `workflow/oldies/` and generated artifacts explicitly excluded from semantic audit scope
- [2026-04-21] Full canonical docs refresh completed; `THEORY_REFRESH_2026-04-21_1653.md` records the anti-drift guardrails before continuing Stage 5 exclusion work
- [2026-04-21] KROK 57 implemented validate_exclusion_rejection_signal.py and the first explicit stabilization-stage rejection signal for complete duplicate candidates, while preserving non-rejection for absent and partial paths
- [2026-04-21] KROK 58 completed with EXCLUSION_REJECTION_OUTCOME_PLAN.md; next blocker is now post-signal outcome validation rather than signaling itself
- [2026-04-21] KROK 59 implemented validate_exclusion_rejection_outcome.py and confirmed the first narrow post-signal claim: rejection need not leave a second valid stabilized duplicate loop
- [2026-04-21] KROK 60 completed with EXCLUSION_MINIMAL_ENFORCEMENT_PLAN.md; next blocker is now the smallest validator-backed enforcement claim beyond signaling and outcome semantics
- [2026-04-21] KROK 61 implemented validate_exclusion_minimal_enforcement.py and closed the first validator-backed enforcement claim: uniqueness of canonical stabilized output after rejection
- [2026-04-21] KROK 62 completed with EXCLUSION_CONTRACT_NARROWING_PLAN.md; next blocker is now the explicit contract boundary between narrow exclusion compliance and still-missing Stage 5 features
- [2026-04-21] KROK 63 completed with EXCLUSION_CONTRACT_BOUNDARY_INTERIM.md, clarifying which current exclusion behaviors now count as narrow compliance expectation and which still remain missing feature
- [2026-04-21] KROK 64 completed with EXCLUSION_CONTRACT_PROMOTION_PLAN.md, defining promotion tiers and a minimal maturity test before any narrow exclusion expectation moves closer to contract-facing status
- [2026-04-21] KROK 65 completed with EXCLUSION_PROMOTION_CANDIDATE_INTERIM.md, identifying which current exclusion behaviors are real promotion candidates and which still must remain below contract-facing status
- [2026-04-21] KROK 66 completed with EXCLUSION_PROMOTION_GATE_PLAN.md, defining the additional gate that candidates must pass before any contract-facing promotion is justified


<!-- AUTO:PROJECT_MAP_START -->
## PROJECT STRUCTURE SNAPSHOT (AUTO)
Updated: 2026-04-22T18:24:04

- Files: 2713
- Dirs: 546
- Map MD: workflow\PROJECT_MAP_FULL.md
- Map JSON: workflow\PROJECT_MAP_FULL.json

<!-- AUTO:PROJECT_MAP_END -->





























































