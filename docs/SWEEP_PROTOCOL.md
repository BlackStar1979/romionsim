# ROMION Sweep Protocol

**Version:** 2.0 (KROK 6 Compliant)  
**Date:** 2026-01-09  
**Status:** AUTHORITATIVE - Experiment Contract

---

## ⚠️ FUNDAMENTAL PRINCIPLE

> **Every result must be reproducible WITHOUT context from author's head.**

This protocol enforces complete, self-contained experimental records.

---

## 1. Run Structure (MANDATORY)

Each run MUST have ALL of these files:

```
<run_directory>/
├── config.json           # Full parameter set + hash
├── metadata.json         # Seed, timestamps, git info, system info
├── simulation.jsonl      # Evolution log
├── validation.json       # Fail-closed validation report
└── status.json          # Final completion status
```

**WITHOUT ALL FILES, RUN IS INCOMPLETE AND IGNORED BY ANALYSIS.**

### 1.1 config.json

**Purpose:** Complete reproducibility of simulation parameters

**Required fields:**
```json
{
  "params": {
    "spawn_threshold": 0.15,
    "decay": 0.008,
    "W_max": 2.5,
    "theta": 0.25,
    "wcluster": 0.02,
    "wdist": 0.005,
    "wbridge": 0.0,
    ...
  },
  "config_hash": "sha256_of_sorted_params",
  "n_nodes": 1000,
  "n_edges_initial": 10000,
  "init_w_range": [0.15, 0.5],
  "n_ticks": 600,
  "dump_graph_every": 100
}
```

**config_hash:** SHA256 of sorted parameters (deterministic)

### 1.2 metadata.json

**Purpose:** Provenance and reproducibility

**Required fields:**
```json
{
  "run_id": "2026-01-09T23:00:00Z_abc123",
  "seed": 42,
  "config_hash": "sha256...",
  "start_time": "2026-01-09T23:00:00Z",
  "end_time": "2026-01-09T23:05:00Z",
  "duration_seconds": 300.5,
  "git_commit": "abc123...",
  "git_branch": "main",
  "git_dirty": false,
  "python_version": "3.11.5",
  "platform": "Windows-10-...",
  "hostname": "machine-name",
  "experiment_name": "decay_sweep",
  "sweep_param": "decay",
  "sweep_value": 0.0056,
  "notes": "Testing decay sensitivity"
}
```

**CRITICAL:** seed and config_hash enable exact reproduction

### 1.3 simulation.jsonl

**Purpose:** Complete evolution log

**Required events:**
- STATE: Periodic system state (every 50 ticks)
- GRAPH: Graph dumps (configurable frequency)

**Each STATE must include:**
```json
{
  "type": "STATE",
  "tick": 100,
  "n_nodes": 1000,
  "n_edges": 8543,
  "total_weight": 1234.5,
  "seed": 42,
  "config_hash": "sha256..."
}
```

**Each GRAPH must include:**
```json
{
  "type": "GRAPH",
  "tick": 100,
  "n": 1000,
  "edges": [[u, v, w], ...]
}
```

### 1.4 validation.json

**Purpose:** Fail-closed validation report

**Required fields:**
```json
{
  "is_valid": true,
  "validation_status": "VALID",
  "reasons": [],
  "threshold_check": {
    "wcluster": 0.02,
    "wdist": 0.005,
    "wbridge": 0.0
  },
  "geometry_check": null,
  "validated_at": "2026-01-09T23:05:00Z"
}
```

**validation_status values:**
- VALID: All checks passed
- INVALID_TECH: Technical error (NaN, negative, etc)
- INVALID_THEORY: Methodology violation (threshold relations)
- PARTIAL: Warnings but usable

### 1.5 status.json

**Purpose:** Final completion status

**Required fields:**
```json
{
  "completed": true,
  "success": true,
  "error": null,
  "final_tick": 600,
  "final_n_edges": 7854,
  "freeze_detected": false,
  "freeze_tick": null,
  "validated": true,
  "validation_passed": true,
  "completed_at": "2026-01-09T23:05:00Z"
}
```

---

## 2. Running Sweeps

### 2.1 Using sweep_krok6.py

**Correct way to run sweeps:**

```bash
python scripts/sweep_krok6.py
```

This creates complete run structure automatically.

**Manual sweep (advanced):**

```python
from scripts.sweep_krok6 import run_simulation

run_simulation(
    params=my_params,
    seed=42,
    n_ticks=600,
    dump_graph_every=100,
    output_dir=Path("experiments/my_run"),
    experiment_name="my_experiment",
    sweep_param="decay",
    sweep_value=0.0056,
    notes="Testing hypothesis H1"
)
```

### 2.2 Pre-Registration (REQUIRED)

Before running sweep, document:

```markdown
## Pre-Registration

### Hypothesis [L2]
H1: decay < 0.006 produces bridges_count > 0 at tick 400

### Parameters
- Sweep: decay ∈ [0.004, 0.008] (5 points)
- Fixed: wcluster=0.02, wdist=0.005, wbridge=0.0
- Seeds: [42, 123, 456]
- Total runs: 15

### Success Criteria
- bridges_count@400 > 0 for decay ≤ 0.006
- Replicated across all 3 seeds

### Falsification
H1 falsified if any seed with decay=0.006 has bridges=0
```

Save as `experiments/<name>/PRE_REGISTRATION.md`

---

## 3. Validation (MANDATORY BEFORE ANALYSIS)

### 3.1 Run Validator

```bash
python scripts/validate_sweep.py experiments/decay_sweep_krok6
```

**Output:**
- Lists all runs with status (VALID/INVALID/INCOMPLETE)
- Creates `valid_runs_manifest.json` with ONLY valid runs
- Exit code 0 if any valid runs, 1 if none

**Example output:**
```
SWEEP VALIDATION - decay_sweep_krok6
======================================================================
Total directories: 27

Checking: decay_0.008_seed_42
  ✓ VALID
Checking: decay_0.008_seed_123
  ✗ INCOMPLETE - missing: status.json
Checking: decay_0.0072_seed_42
  ✗ INVALID
      - Run not completed
      
VALIDATION SUMMARY
======================================================================
Total runs: 27
  ✓ Valid:      20 (74.1%)
  ✗ Invalid:    5 (18.5%)
  ✗ Incomplete: 2 (7.4%)

✓ 20 runs ready for analysis

Manifest saved: experiments/decay_sweep_krok6/valid_runs_manifest.json
```

### 3.2 Valid Runs Manifest

**Purpose:** Analysis ONLY processes runs in manifest

**Structure:**
```json
{
  "valid_runs": [
    {
      "path": "experiments/decay_sweep_krok6/decay_0.008_seed_42",
      "run_id": "2026-01-09T...",
      "seed": 42,
      "config_hash": "sha256...",
      "sweep_param": "decay",
      "sweep_value": 0.008,
      "final_tick": 600,
      "freeze_detected": false
    },
    ...
  ],
  "total": 20,
  "created_at": "2026-01-09T23:10:00Z"
}
```

**CRITICAL:** Analysis scripts load manifest, IGNORE runs not listed.

---

## 4. Analysis Protocol

### 4.1 Using Manifest (REQUIRED)

```python
import json
from pathlib import Path

# Load manifest
with open('experiments/decay_sweep/valid_runs_manifest.json') as f:
    manifest = json.load(f)

# Process ONLY valid runs
for run_info in manifest['valid_runs']:
    run_dir = Path(run_info['path'])
    
    # Load metadata
    config = load_config(run_dir / 'config.json')
    metadata = load_metadata(run_dir / 'metadata.json')
    
    # Analyze...
```

**DO NOT iterate over directories directly** - use manifest!

### 4.2 Analysis Output Structure

```
experiments/<name>/
├── runs/                    # Individual runs
│   ├── <run_id>/
│   │   ├── config.json
│   │   ├── metadata.json
│   │   ├── simulation.jsonl
│   │   ├── validation.json
│   │   └── status.json
│   └── ...
├── PRE_REGISTRATION.md      # Pre-registration
├── valid_runs_manifest.json # Valid runs only
└── analysis/
    ├── summary.csv          # Aggregate results
    ├── plots/               # Visualizations
    └── REPORT.md            # Final report
```

---

## 5. Fail-Closed Validation Rules

### 5.1 Run Completeness

**Required:**
- ✅ All 5 files present (config, metadata, log, validation, status)
- ✅ Config has hash
- ✅ Metadata has seed + timestamps
- ✅ Status shows completed=true, success=true
- ✅ Validation shows is_valid=true

**If ANY missing → RUN EXCLUDED**

### 5.2 Threshold Relations

**Required (from METHODOLOGY.md):**
- wcluster ≥ wdist > 0
- wbridge ≤ wcluster
- All positive

**If violated → INVALID_THEORY → RUN EXCLUDED**

### 5.3 Technical Validation

**Required:**
- No NaN/Inf in metrics
- hub_share, coverage ∈ [0, 100]
- Counts ≥ 0

**If violated → INVALID_TECH → RUN EXCLUDED**

---

## 6. Reproducibility Checklist

Before claiming result is reproducible:

- [ ] All runs have 5 required files
- [ ] Pre-registration document exists
- [ ] Validation passed (valid_runs_manifest.json created)
- [ ] Config hashes recorded
- [ ] Seeds recorded
- [ ] Git commit recorded (if available)
- [ ] Analysis uses manifest (not directory iteration)
- [ ] Report references config hashes and seeds

**Without ALL checks: RESULT IS NOT REPRODUCIBLE**

---

## 7. Common Mistakes (DO NOT)

### ❌ Missing Files
```
experiments/my_run/
└── simulation.jsonl          # INCOMPLETE - other files missing
```

**Analysis will ignore this run.**

### ❌ No Validation
```bash
# Running analysis without validation
python analyze_sweep.py experiments/my_sweep  # WRONG
```

**Must run validate_sweep.py first!**

### ❌ Directory Iteration
```python
# WRONG - ignores validation
for run_dir in Path('experiments/sweep').iterdir():
    analyze(run_dir)  # May include invalid runs!
```

**Use manifest instead:**
```python
# CORRECT
manifest = load_manifest('experiments/sweep/valid_runs_manifest.json')
for run_info in manifest['valid_runs']:
    analyze(run_info['path'])
```

### ❌ No Pre-Registration
Running sweep without documenting hypothesis first.

**Post-hoc analysis ≠ hypothesis testing**

---

## 8. Quick Reference

**Run sweep:**
```bash
python scripts/sweep_krok6.py
```

**Validate:**
```bash
python scripts/validate_sweep.py experiments/<name>
```

**Analyze (use manifest):**
```python
manifest = load_manifest('experiments/<name>/valid_runs_manifest.json')
for run in manifest['valid_runs']:
    ...
```

**Check run:**
```bash
ls experiments/<name>/<run_id>/
# Should see: config.json, metadata.json, simulation.jsonl, 
#             validation.json, status.json
```

---

## 9. Migration from Old Sweeps

**Old sweep (incomplete):**
```
experiments/old_sweep/
└── d0.7_s42/
    └── simulation.jsonl      # Only log, no metadata
```

**Action required:**
1. Mark as [LEGACY] or [INCOMPLETE]
2. Do NOT use for publication
3. Re-run with sweep_krok6.py if needed

**NEVER mix old + new runs in analysis**

---

## 10. Publication Checklist

Before submitting results:

- [ ] All runs validated (manifest exists)
- [ ] Pre-registration document included
- [ ] Config hashes in paper/SI
- [ ] Seeds in paper/SI
- [ ] Git commit in SI (if available)
- [ ] Archive uploaded (with all 5 files per run)
- [ ] README explains file structure
- [ ] Reproduction instructions tested

**Without complete records: RESULTS NOT PUBLISHABLE**

---

**Status:** AUTHORITATIVE PROTOCOL  
**Version:** 2.0 (KROK 6 compliant)  
**Enforcement:** Scripts validate_sweep.py, sweep_krok6.py  
**Maintenance:** Update when adding new validation rules
