# ROMION O'LOGIC™ - Quick Reference Card

**Updated:** 2026-01-11  
**Status:** POST-AUDIT - Operational Maturity  
**Schema:** v2.0 (MANDATORY)

---

## 🎯 ESSENTIAL COMMANDS

### Validation (FIRST PRIORITY)
```bash
# Validate log schema (entry gate)
python scripts/validate_log_schema.py results/run1/simulation.jsonl
# Output: VALID | LEGACY_V1 | INVALID

# Validate sweep results
python scripts/validate_sweep.py results/sweep_*/

# Run canonical metrics tests
python tests/test_canonical_metrics.py
```

### Run Simulation
```bash
# From config (recommended)
python scripts/run_from_config.py cfg/baseline.cfg

# Direct run
python scripts/run_romion_extended.py \
  --ticks 600 --seed 42 --out results/run1
```

### Analysis
```bash
# Basic analysis with canonical metrics
python analysis/gravity_test.py \
  --log results/run1/simulation.jsonl \
  --tick 400 \
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0

# With diagnostics
python analysis/gravity_test.py \
  --log results/run1/simulation.jsonl \
  --tick 400 \
  --channels --anisotropy
```

---

## 📋 CANONICAL CONTRACTS (MANDATORY)

### Schema v2.0
**Authority:** `docs/CANONICAL_LOG_CONTRACT.md`

**Required in logs:**
- `schema_version: "2.0"` in METADATA
- `metrics_pre` (L1-CORE, before U)
- `metrics_post` (L1-CORE, after U)
- `projection` (L2-FRACTURE, uses metrics_post)
- `mean_frustration` in both metrics_pre/post

**Critical check:**
```bash
grep "uses_metrics_post.*true" results/*/simulation.jsonl
# MUST be present for v2.0 compliance
```

### Canonical Metrics
**Authority:** `docs/CANONICAL_METRICS.md`

**20 metrics fully specified:**
- **L1-CORE (8):** mean_kappa, mean_pressure, mean_frustration, total_weight, n_edges, n_nodes, mean_tension, mean_emergent_time
- **L2-FRACTURE (3):** visible_edges, visible_ratio, mean_kappa_visible
- **L3-INTERPRETATION (4):** hub_share, coverage, R0, R2
- **Evolution (5):** spawn_new, spawn_reinf, field_tail_added, removed, norm_ops

---

## 🔍 THREE-THRESHOLD SEPARATION

**Authority:** `docs/theory/MEASUREMENT_THRESHOLDS.md`

```
wcluster (objects/matter)
    ↓
  Clusters (what exists as "things")
    
wdist (background/geometry)
    ↓
  Distance graph (how to measure range)
    
wbridge (field/interactions)
    ↓
  Bridge subgraph (connections between objects)
```

**CRITICAL RULE:** These thresholds MUST be measured separately. Never mix them!

**Standard values (pre-registered):**
- wcluster: 0.02
- wdist: 0.005
- wbridge: 0.0 (all positive)

---

## 📊 LAYER SEPARATION (MANDATORY)

**L1-CORE:** Primary (what exists)
- Graph structure Δ(t)
- Evolution operator U
- Independent of observation

**L2-FRACTURE:** Derived (what is observed)
- Projection Πθ
- MUST use metrics_post
- Depends on threshold θ

**L3-INTERPRETATION:** Interpretive (what we infer)
- Patterns, hypotheses
- NOT ontological claims
- Analysis artifacts

**RED FLAG:** Backreaction (L2 → L1) is FORBIDDEN

---

## ✅ VALIDATION CHECKLIST

### Before Running Analysis
- [ ] Log has schema_version: "2.0"
- [ ] Log validated with validate_log_schema.py
- [ ] Status: VALID (not LEGACY_V1 or INVALID)

### Before Reporting Results
- [ ] Thresholds explicit (wcluster, wdist, wbridge)
- [ ] Layer labels present (L1/L2/L3)
- [ ] projection.uses_metrics_post = true
- [ ] mean_frustration present (v2.0 requirement)
- [ ] No NaN/inf values (fail-closed)

### Before Claiming Findings
- [ ] Theory prediction stated first
- [ ] Derivation from ROMION principles shown
- [ ] Layer tagged correctly (CORE/FRACTURE/INTERPRETATION)
- [ ] No magic constants introduced
- [ ] Falsification condition stated

---

## 📁 KEY DOCUMENTATION

### Canonical Contracts (MUST READ)
- `docs/CANONICAL_LOG_CONTRACT.md` - Schema v2.0 authority
- `docs/CANONICAL_METRICS.md` - Metrics authority
- `docs/METHODOLOGY.md` - Experimental standards

### Theory
- `docs/THEORY.md` - Core foundations
- `docs/theory/GLOSSARY.md` - Complete terminology
- `docs/theory/MEASUREMENT_THRESHOLDS.md` - Three thresholds

### Status
- `docs/STATUS.md` - Current project status (post-audit)
- `docs/ROADMAP.md` - Next phase options
- `session_reports/2026-01-10/` - Audit completion reports

### Protocols
- `docs/SWEEP_PROTOCOL.md` - Parameter sweep protocol (KROK 6)
- `docs/RESULTS_HEADER_TEMPLATE.md` - Results format

---

## 🚨 FAIL-CLOSED RULES

### Invalid Data (REJECT)
- NaN values → INVALID
- Inf values → INVALID
- Out-of-bounds metrics → INVALID
- Missing required fields (v2.0) → INVALID

### Layer Violations (FORBIDDEN)
- L2 → L1 backreaction → FORBIDDEN
- L3 treated as L1 ontology → FORBIDDEN
- Projection using metrics_pre → CRITICAL ERROR

### Methodology Violations (STOP)
- Magic constants without derivation → STOP
- Data fitting without theory → STOP
- Post-hoc parameter changes → STOP
- Unfalsifiable claims → STOP

---

## 🎓 COMMON WORKFLOWS

### Workflow 1: Run Single Simulation
```bash
# 1. Create/verify config
vim cfg/my_experiment.cfg

# 2. Run simulation
python scripts/run_from_config.py cfg/my_experiment.cfg

# 3. Validate log
python scripts/validate_log_schema.py results/my_experiment/simulation.jsonl

# 4. Analyze (if VALID)
python analysis/gravity_test.py --log results/my_experiment/simulation.jsonl --tick 400
```

### Workflow 2: Parameter Sweep
```bash
# 1. Create sweep configs (multiple .cfg files)
# 2. Run sweep
python scripts/sweep_krok6.py <sweep_dir>

# 3. Validate sweep
python scripts/validate_sweep.py <sweep_dir>/results/

# 4. Analyze valid runs only
# (validate_sweep.py creates manifest with valid runs)
```

### Workflow 3: Validate Existing Data
```bash
# Schema check
python scripts/validate_log_schema.py <log>

# Metrics check (if implementing analysis)
# Use validate_romion.py functions in code
```

---

## 🔬 RESEARCH PRINCIPLES

### Theory-First (MANDATORY)
1. State theoretical expectation (from ROMION)
2. Derive expected functional form
3. Predict observable consequences
4. Design experiment
5. Compare results
6. Accept/reject/refine (with rationale)

### Forbidden Approaches
- ❌ Run experiment → see pattern → invent formula
- ❌ Fit data → claim theory predicted it
- ❌ Introduce constants to match results
- ❌ Use ROMION to "explain everything"

---

## 📖 LEARN MORE

### Audit Reports (Historical)
- `session_reports/2026-01-10/KROK_2_INTEGRATION_COMPLETE.md`
- `session_reports/2026-01-10/KROK_3_COMPLETE.md`
- `session_reports/2026-01-10/VALIDATOR_TEST_REPORT.md`

### Pre-Audit Work (Historical Reference)
- `archive/pre_audit/` - Pre-audit documentation
- `session_reports/2026-01-09/` - Pre-audit sessions
- Note: May not meet schema v2.0 standards

### Navigation
- `docs/README.md` - Documentation overview
- `docs/STRUCTURE.md` - Project organization
- `docs/QUICK_REFERENCE.md` - This file

---

## 💡 QUICK TIPS

**Finding specific info:**
- Schema v2.0 details → CANONICAL_LOG_CONTRACT.md
- Metric definitions → CANONICAL_METRICS.md
- Layer separation → METHODOLOGY.md section 3
- Three thresholds → theory/MEASUREMENT_THRESHOLDS.md
- Current status → STATUS.md
- Next steps → ROADMAP.md

**Common issues:**
- "Invalid schema" → Check schema_version field
- "Missing frustration" → v2.0 requires mean_frustration
- "Uses metrics_pre" → CRITICAL: must use metrics_post
- "Legacy warning" → v1.0 log, needs upgrade or explicit [LEGACY-V1] marking

**Getting help:**
- Start with docs/README.md
- Check CANONICAL_*.md for contracts
- Review session_reports/2026-01-10/ for audit details

---

## 🎯 PROJECT STATUS SUMMARY

**Version:** 3.0.0 (post-audit)  
**Schema:** v2.0 (MANDATORY)  
**Audit:** 100% COMPLETE ✅  
**Theory:** LOCKED 🔒  
**Mode:** STABLE CORE

**Next phase:** Deferred (options: P0/gravity/cosmology/paper)

---

**For complete documentation:** See `docs/` directory  
**For current status:** See `docs/STATUS.md`  
**For contracts:** See `CANONICAL_LOG_CONTRACT.md` and `CANONICAL_METRICS.md`

---

**END QUICK REFERENCE**
