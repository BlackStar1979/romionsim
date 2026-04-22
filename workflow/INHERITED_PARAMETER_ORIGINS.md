# INHERITED PARAMETER ORIGINS — What Came From Where

Purpose:
Trace the origin of the main fixed values inherited from older ROMION work,
using only locally available old project materials.

This note answers a narrower question than `FIXED_PARAMETER_AUDIT.md`:
not just which fixed values exist now,
but why earlier models may have treated them as natural.

---

## 1. EXECUTIVE RESULT

The inherited values do NOT all come from one source.

They split into four origin classes:

1. old-engine baseline protocol values
2. old reproducibility protocol values
3. old analysis-threshold values
4. new-MVP simplification values

This means the current repo inherits some values honestly,
but it also compresses an older, richer protocol into a much smaller engine.
That compression explains why some parameters survived
without their original rationale remaining visible.

---

## 2. WHAT THE OLD PROJECT CLEARLY SHOWS

### Old baseline was not the current MVP baseline

In `workflow/oldies/romionsim_old_2/cfg/baseline.cfg`,
the old baseline was:
- `ticks = 1000`
- `nodes = 2000`
- `init_edges = 6000`
- `seed = 42`
- `spawn_scale = 1.0`
- `decay_scale = 1.0`
- `tension_scale = 1.0`
- many deeper parameters such as:
  - `spawn_threshold = 0.15`
  - `spawn_samples = 1500`
  - `spawn_damping = 0.55`
  - `spawn_cap = 1500`
  - `reinforce_factor = 0.05`
  - `decay = 0.008`
  - `min_weight = 0.005`
  - `W_max = 2.5`
  - `theta = 0.25`
  - `beta_2hop = 0.25`

So the current MVP values were NOT simply copied from the old main baseline.

---

### Seed 42 came from reproducibility protocol, not from theory

The old project repeatedly uses `seed = 42` in:
- `cfg/baseline.cfg`
- `cfg/decay_slow.cfg`
- `scripts/run_romion_extended.py`
- many sweep and report artifacts

But the same old project also explicitly used multi-seed checks:
- `seeds = [42, 123]`

This appears in:
- `archive/old_sweep_tests/sweep_decay_channels/PROTOCOL.md`
- `archive/old_sweep_tests/sweep_decay_channels/STATUS.md`
- `archive/old_sweep_tests/sweep_decay_inprocess/STATUS.md`
- `scripts/batch_sweep.py`

Conclusion:
- `42` was a baseline reproducibility seed
- not a claim that one seed is sufficient
- the old methodology expected later robustness checks across more than one seed

Implication for current repo:
- inheriting `seed = 42` alone is only half of the old protocol
- the other half, multi-seed robustness, was dropped in the MVP rebuild

---

### 600/1000 ticks in the old project were deliberate observation horizons

The old project repeatedly uses:
- `ticks = 1000` for main baseline and exploratory runs
- `ticks = 600` for sweep work and freeze/channel diagnostics

This is visible in:
- `cfg/baseline.cfg`
- `cfg/decay_slow.cfg`
- `scripts/run_romion_extended.py`
- `archive/old_sweep_tests/sweep_decay_inprocess/STATUS.md`
- `archive/old_sweep_tests/sweep_decay_inprocess/FINAL_RESULTS.md`
- `archive/old_sweep_tests/sweep_decay_channels/STATUS.md`

These longer horizons were tied to the old engine's questions:
- SOC window
- freeze diagnostics
- time evolution at checkpoints
- channel / anisotropy analysis

Conclusion:
- the old project did not treat `100` as a natural default
- the current `100` belongs to the rebuilt MVP phase, not to the older baseline tradition

---

### `wcluster = 0.02`, `wdist = 0.005`, `wbridge = 0.0` came from old analysis protocol

These values recur consistently in old gravity/channel analysis:
- `archive/old_sweep_tests/sweep_decay_channels/PROTOCOL.md`
- `archive/old_sweep_tests/sweep_decay_inprocess/FINAL_RESULTS.md`
- `archive/gravity_test_monolith.py`
- `archive/gravity_test_before_chatgpt_fix.py`
- multiple analysis helper scripts

Interpretation:
- these were not random leftovers
- they were old analysis-threshold conventions tied to the three-threshold separation

Important limit:
- they belong to the old richer analysis layer,
  not automatically to the current rebuilt engine semantics

---

## 3. WHAT THE CURRENT MVP SEEMS TO HAVE INTRODUCED ANEW

The current MVP stability scaffold:
- `n_nodes = 50`
- `w_init_min = 0.01`
- `w_init_max = 0.05`
- `p_add = 0.05`
- `p_decay = 0.99 / 0.995 / 0.999`
- `w_prune = 0.0`
- `w_visible = 0.015 .. 0.030`

does NOT appear as a documented old canonical baseline in the local old project.

The closest old analogies are:
- `reinforce_factor = 0.05`
- some old weak-weight scales near `0.02`
- old threshold conventions in analysis

But the current MVP tuple as a whole looks like a rebuild-specific simplification,
not an old, explicitly justified experimental law.

Conclusion:
- current MVP scaffold values are mostly new simplifications,
  not faithful imports of the old baseline protocol

---

## 4. MOST IMPORTANT ORIGIN JUDGMENTS

### A. `seed = 42`
Origin:
- old reproducibility baseline convention

Verdict:
- inherited honestly
- but incompletely, because the old project paired it with multi-seed checks

### B. `ticks = 100`
Origin:
- not supported by old baseline materials
- belongs to new MVP simplification

Verdict:
- inherited from recent rebuild behavior, not from deep old protocol
- already revised in the current repo

### C. `spawn_scale = 1.0`, `decay_scale = 1.0`
Origin:
- old phase-control baseline conventions

Verdict:
- inherited honestly as neutral scale multipliers
- acceptable as baseline controls

### D. `n_nodes = 50`
Origin:
- no clear support in the local old project as a canonical baseline
- old project used `1000` and `2000` node systems for substantive experiments

Verdict:
- current MVP convenience choice
- should be treated as strictly local scaffold, not inherited experimental law

### E. `w_init_min = 0.01`, `w_init_max = 0.05`, `p_add = 0.05`, `w_prune = 0.0`
Origin:
- no explicit old baseline source found for this exact package

Verdict:
- rebuild-specific simplification values until proven otherwise
- they should be treated as provisional scaffold choices

### F. `theta = 0.1` in the current stability metric
Origin:
- not the same as old engine `theta = 0.25`
- current value is a new metric-definition choice for MVP

Verdict:
- not inherited from old canonical thresholding
- valid only as current metric version, not historical carry-over

### G. `wcluster = 0.02`, `wdist = 0.005`, `wbridge = 0.0`
Origin:
- old analysis-threshold protocol

Verdict:
- inherited with real historical grounding
- but grounded in old analysis tooling, not automatically in current engine ontology

---

## 5. PRACTICAL CONSEQUENCE FOR THE CURRENT REPO

The current project should treat inherited values in three buckets:

### Historically grounded and still understandable
- `seed = 42` as reproducibility baseline seed
- neutral scales `spawn_scale = 1.0`, `decay_scale = 1.0`
- projection-analysis thresholds like `wcluster = 0.02`, `wdist = 0.005`

### Historically grounded, but incomplete if used alone
- `seed = 42`
because the older protocol expected multi-seed follow-up

### Rebuild-local simplifications that need fresh justification
- `n_nodes = 50`
- `w_init_min = 0.01`
- `w_init_max = 0.05`
- `p_add = 0.05`
- `w_prune = 0.0`
- the former universal use of `ticks = 100`
- current metric threshold choice `theta = 0.1`

---

## 6. DECISION RULE GOING FORWARD

When a current fixed value is questioned:

1. if old local materials show a protocol role, preserve that history explicitly
2. if old local materials do not support it, treat it as a rebuild-local scaffold
3. if old protocol also required a second guardrail, preserve both, not just one

Example:
- `seed = 42` should not be read alone
- the old meaning was closer to:
  "start with 42, then verify with additional seeds"

---

## 7. WHAT THIS NOTE DOES NOT YET PROVE

This note reconstructs origins from local old materials only.

It does NOT prove:
- that all old justifications were correct
- that all missing justifications never existed elsewhere
- that every current scaffold value is wrong

It only establishes:
- what is historically supported in local oldies
- and what currently lacks that support

End of origin note
