# 💻 Common Commands

**Frequently used commands for ROMION O'LOGIC™**

**Updated:** 2026-01-11  
**Status:** POST-AUDIT - Schema v2.0

---

## ✅ VALIDATION COMMANDS (PRIORITY 1)

### Schema Validation (Entry Gate):
```bash
# Validate single log
python scripts/validate_log_schema.py results/run1/simulation.jsonl
# Output: VALID | LEGACY_V1 | INVALID

# Validate sweep
python scripts/validate_sweep.py results/sweep_*/
# Creates manifest with valid/legacy/invalid runs
```

### Metrics Test Suite:
```bash
# Run canonical metrics tests
python tests/test_canonical_metrics.py
# Expected: 9/9 tests passed

# Check specific validation
cd tests
python -c "from test_canonical_metrics import test_L1_valid; test_L1_valid()"
```

### Config Validation:
```bash
# Validate config file
python scripts/validate_config.py cfg/my_experiment.cfg
```

**RULE:** Always validate before analysis!

---

## ⚠️ THREE THRESHOLDS (MANDATORY SEPARATION)

**Authority:** `docs/theory/MEASUREMENT_THRESHOLDS.md`

| Threshold | Layer | Purpose | Default |
|-----------|-------|---------|---------|
| `--wcluster` | L1-CORE | Objects/matter definition | 0.02 |
| `--wdist` | L2-FRACTURE | Background geometry | 0.005 |
| `--wbridge` | L2-FRACTURE | Field/interactions | 0.0 |

**Critical Rules:**
- `wcluster ≥ wdist > 0` (objects more stable than background)
- `wbridge ≤ wcluster` (field weaker than matter)
- Distances computed on background graph (wdist), NEVER on bridges
- All three MUST be specified separately

**Fail-closed policy:**
- Invalid logs → rejected
- Missing thresholds → non-reproducible
- NaN/inf values → excluded

---

## 🚀 RUNNING SIMULATIONS

### From Config (RECOMMENDED):
```bash
# Using config file
python scripts/run_from_config.py cfg/baseline.cfg

# Test command (dry-run)
python scripts/run_from_config.py cfg/decay_slow.cfg --dry-run

# Override output directory
python scripts/run_from_config.py cfg/baseline.cfg --out results/my_output
```

### Direct Parameters:
```bash
python scripts/run_romion_extended.py \
  --ticks 600 \
  --decay-scale 0.7 \
  --seed 42 \
  --dump-graph-every 100 \
  --out results/my_test
```

### Full Options:
```bash
python scripts/run_romion_extended.py \
  --ticks 600 \
  --nodes 2000 \
  --init-edges 6000 \
  --seed 42 \
  --spawn-scale 1.0 \
  --decay-scale 0.7 \
  --tension-scale 1.0 \
  --dump-graph-every 100 \
  --log-interval 50 \
  --out results/my_test
```

**Note:** Current engine uses partial schema v2.0 (validation at analysis layer)

---

## 🔬 ANALYSIS (gravity_test)

### Basic Analysis:
```bash
python analysis/gravity_test.py \
  --log results/my_test/simulation.jsonl \
  --tick 400
```

### With All Three Thresholds (MANDATORY):
```bash
python analysis/gravity_test.py \
  --log results/my_test/simulation.jsonl \
  --tick 400 \
  --wcluster 0.02 \
  --wdist 0.005 \
  --wbridge 0.0
```

### With Diagnostics:
```bash
python analysis/gravity_test.py \
  --log results/my_test/simulation.jsonl \
  --tick 400 \
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0 \
  --channels --anisotropy
```

### Time Range:
```bash
python analysis/gravity_test.py \
  --log results/my_test/simulation.jsonl \
  --tick-range "100 600 100" \
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0
```

### CLI Reference:
| Parameter | Description |
|-----------|-------------|
| `--log` | Path to simulation.jsonl (required) |
| `--tick` | Single tick to analyze |
| `--tick-range` | Range: "start end step" |
| `--wcluster` | Threshold for clustering (L1-CORE objects) |
| `--wdist` | Threshold for background (L2-FRACTURE geometry) |
| `--wbridge` | Threshold for bridges (L2-FRACTURE field) |
| `--cluster-mode` | `threshold` or `topk` |
| `--min-cluster-size` | Min nodes per cluster |
| `--disconnected-policy` | `threshold` or `maxdist` |
| `--channels` | Enable channel capacity metrics |
| `--anisotropy` | Enable anisotropy metrics |

---

## 📋 COMPLETE WORKFLOW (POST-AUDIT)

### 1. Run Simulation:
```bash
python scripts/run_from_config.py cfg/my_experiment.cfg
```

### 2. Validate Log (MANDATORY):
```bash
python scripts/validate_log_schema.py results/my_experiment/simulation.jsonl
# Must show: VALID (not LEGACY_V1 or INVALID)
```

### 3. Analyze (if VALID):
```bash
python analysis/gravity_test.py \
  --log results/my_experiment/simulation.jsonl \
  --tick 400 \
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0
```

### 4. Document Results:
- Record: seed, config_hash, git_commit
- Cite: CANONICAL_METRICS.md for metric definitions
- Label: L1/L2/L3 layers explicitly
- Mark: Theory predictions vs observations

---

## 🧪 SWEEPS (KROK 6 Protocol)

### Run Sweep:
```bash
# KROK 6 compliant sweep
python scripts/sweep_krok6.py <sweep_config_dir>
```

### Validate Sweep:
```bash
python scripts/validate_sweep.py results/sweep_*/
# Creates manifest: valid_runs, legacy_runs, invalid_runs
```

### Analyze Valid Runs:
```bash
# Use manifest to analyze only valid runs
python scripts/analyze_sweep.py results/sweep_*/manifest.json
```

**Authority:** `docs/SWEEP_PROTOCOL.md`

---

## 🔍 INSPECTION

### Check Log Status:
```bash
# Quick check
head -1 results/run1/simulation.jsonl | python -m json.tool

# Check schema version
grep '"schema_version"' results/run1/simulation.jsonl | head -1

# Count events
grep '"type":"STATE"' results/run1/simulation.jsonl | wc -l
grep '"type":"GRAPH"' results/run1/simulation.jsonl | wc -l
```

### Check Metrics:
```bash
# Extract metrics_post from tick 400
jq 'select(.type=="STATE" and .tick==400) | .metrics_post' \
  results/run1/simulation.jsonl

# Check projection
jq 'select(.type=="STATE" and .tick==400) | .projection' \
  results/run1/simulation.jsonl
```

### Check Canonical Compliance:
```bash
# Verify frustration present
jq 'select(.type=="STATE") | .metrics_post.mean_frustration' \
  results/run1/simulation.jsonl | head -5

# Verify uses_metrics_post
jq 'select(.type=="STATE") | .projection.uses_metrics_post' \
  results/run1/simulation.jsonl | head -5
```

---

## 🧪 TEST REPRODUCTION

### Historical Tests (Pre-Audit):
**Note:** These may not meet schema v2.0 standards

```bash
# Test C baseline (historical reference)
python scripts/run_romion_extended.py \
  --config tests/test_c/cfg/R0_baseline.cfg

# Analysis (historical)
python analysis/gravity_test.py \
  --log tests/test_c/results/R0_base/simulation.jsonl \
  --tick 400 --wcluster 0.02 --wdist 0.005 --wbridge 0.0
```

**Recommendation:** Re-run experiments with schema v2.0 compliance

---

## 📊 BATCH OPERATIONS

### Batch Analysis:
```bash
# Analyze multiple runs
python scripts/batch_test_c.py

# Update sweep results
python scripts/update_sweep_results.py --prefix my_sweep
```

### Lint Results:
```bash
# Check results format
python scripts/lint_results.py
```

---

## 🔧 DEBUGGING

### Verbose Output:
```bash
# Enable debug logging
python scripts/run_romion_extended.py \
  --ticks 100 --seed 42 --out results/debug \
  --log-interval 1 --dump-graph-every 10
```

### Check Validation:
```bash
# Test validators
python -c "from scripts.validate_log_schema import validate_log_schema; \
           print(validate_log_schema('results/run1/simulation.jsonl'))"

# Test canonical metrics
python -c "from analysis.gravity_test.validate_romion import validate_L1_metrics; \
           metrics = {'mean_kappa': 0.5, 'mean_pressure': 1.0, 'mean_frustration': 0.1, \
                      'total_weight': 1000, 'n_edges': 100, 'n_nodes': 50}; \
           print(validate_L1_metrics(metrics, '2.0'))"
```

---

## 📚 REFERENCE

### Key Files:
- **Canonical Contracts:**
  - `docs/CANONICAL_LOG_CONTRACT.md` - Schema v2.0 authority
  - `docs/CANONICAL_METRICS.md` - Metrics authority

- **Protocols:**
  - `docs/METHODOLOGY.md` - Experimental standards
  - `docs/SWEEP_PROTOCOL.md` - Sweep protocol (KROK 6)

- **Theory:**
  - `docs/theory/MEASUREMENT_THRESHOLDS.md` - Three thresholds
  - `docs/theory/GLOSSARY.md` - Complete terminology

### Quick Navigation:
- Structure: `docs/STRUCTURE.md`
- Quick reference: `docs/QUICK_REFERENCE.md`
- Current status: `docs/STATUS.md`

---

## ⚡ COMMON PATTERNS

### Pattern 1: Quick Test
```bash
# Run + validate + analyze
python scripts/run_from_config.py cfg/baseline.cfg && \
python scripts/validate_log_schema.py results/baseline/simulation.jsonl && \
python analysis/gravity_test.py --log results/baseline/simulation.jsonl --tick 400
```

### Pattern 2: Sweep Workflow
```bash
# Run sweep
python scripts/sweep_krok6.py configs/my_sweep/

# Validate
python scripts/validate_sweep.py results/my_sweep/

# Analyze valid runs from manifest
python scripts/analyze_sweep.py results/my_sweep/manifest.json
```

### Pattern 3: Debugging
```bash
# Verbose run + immediate check
python scripts/run_romion_extended.py --ticks 100 --out results/debug --log-interval 1 && \
python scripts/validate_log_schema.py results/debug/simulation.jsonl && \
jq 'select(.type=="STATE") | .metrics_post.mean_frustration' results/debug/simulation.jsonl
```

---

## 🚨 COMMON ERRORS

### "Log schema INVALID"
→ Check schema_version field, metrics_pre/post separation, mean_frustration presence

### "Legacy v1.0 detected"
→ Old log format, needs upgrade or explicit [LEGACY-V1] marking

### "Missing uses_metrics_post"
→ Critical: projection must use metrics_post (v2.0 requirement)

### "Threshold not specified"
→ wcluster, wdist, wbridge all MUST be explicit (reproducibility)

### "NaN/inf in metrics"
→ Fail-closed: run is INVALID, check simulation parameters

---

**For complete documentation:** `docs/README.md`  
**For validation details:** `docs/CANONICAL_LOG_CONTRACT.md`  
**For metric specs:** `docs/CANONICAL_METRICS.md`  
**For quick reference:** `docs/QUICK_REFERENCE.md`
