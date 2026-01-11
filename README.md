# ROMION O'LOGIC™ Simulation

**Relational Ontology Model with Interaction-Oriented Networks**

Theoretical physics framework testing hypergraph → spacetime emergence.

---

## 🔒 Project Status: POST-AUDIT (Operational Maturity)

**Version:** 3.0.0  
**Updated:** 2026-01-11  
**Schema:** v2.0 (MANDATORY)  
**Audit:** ✅ 100% COMPLETE

### Audit Completion (2026-01-10/11)

**6/6 KROKÓW COMPLETE:**
- ✅ KROK 1: Semantyka - Philosophy locked (epistemological, not ontological)
- ✅ KROK 2: Kontrakt logów - Schema v2.0 enforced (CANONICAL_LOG_CONTRACT.md)
- ✅ KROK 3: Spójność metryk - Canonical metrics defined (CANONICAL_METRICS.md)
- ✅ KROK 4: Fail-closed validation - Invalid → reject, no silent degradation
- ✅ KROK 5: Rozdzielenie mechanizmów - S1/field/spark separation clear
- ✅ KROK 6: Kontrakt eksperymentu - Reproducibility enforced (seed+hash+git)

**Deliverables:**
- `docs/CANONICAL_LOG_CONTRACT.md` - Schema v2.0 authority
- `docs/CANONICAL_METRICS.md` - Metric definitions authority
- `scripts/validate_log_schema.py` - Schema enforcement
- `analysis/gravity_test/validate_romion.py` - Metrics enforcement
- `tests/test_canonical_metrics.py` - Test suite (9/9 passed)

**Status:** Theory locked, methodology fail-closed, contracts enforced

---

## ⚠️ Key Concept: Layer Separation

**L1-CORE / L2-FRACTURE / L3-INTERPRETATION - these are distinct ontological layers:**
- **L1-CORE:** Primary (what exists) - graph structure Δ(t)
- **L2-FRACTURE:** Derived (what is observed) - projection Πθ
- **L3-INTERPRETATION:** Interpretive (what we infer) - analysis patterns

**Critical Rules:**
- Projection MUST use metrics_post (after evolution U)
- No backreaction (L2 → L1 forbidden)
- Layer labels mandatory in schema v2.0

**See:** `docs/CANONICAL_METRICS.md` for complete layer specifications

---

## ⚙️ Schema v2.0 (MANDATORY)

All new simulations MUST use schema v2.0:

**Required in logs:**
- `schema_version: "2.0"` in first event
- `metrics_pre` (before U) and `metrics_post` (after U) separation
- `mean_frustration` in both metrics_pre and metrics_post
- Layer labels: `L1-CORE`, `L2-FRACTURE`
- `projection.uses_metrics_post: true` (CRITICAL!)

**Legacy v1.0 logs:**
- Readable with warnings
- Marked [LEGACY-V1] in results
- No mixing with v2.0 in analysis

**Validation:**
```bash
python scripts/validate_log_schema.py <log_file>
```

**See:** `docs/CANONICAL_LOG_CONTRACT.md` for complete schema specification

---

## 📁 Structure

```
romionsim/
├── core/              # Simulation engine
├── analysis/          # Analysis tools
│   └── gravity_test/  # Main analysis suite + validate_romion.py
├── scripts/           # Runners + validation
│   ├── validate_log_schema.py     # Schema v2.0 enforcement
│   ├── validate_sweep.py          # Entry gate validation
│   └── run_from_config.py         # Main runner
├── tests/             # Test suite
│   └── test_canonical_metrics.py  # Metrics validation tests
├── cfg/               # Configurations
├── docs/              # Documentation ⭐
│   ├── CANONICAL_LOG_CONTRACT.md  # Schema v2.0 (AUTHORITY)
│   ├── CANONICAL_METRICS.md       # Metrics (AUTHORITY)
│   ├── METHODOLOGY.md             # Standards
│   └── theory/                    # Theoretical foundation
├── archive/           # Historical files
└── session_reports/   # Session logs
    └── 2026-01-10/    # Audit completion reports
```

---

## 🚀 Quick Start

### Running Simulation:
```bash
# From config (recommended)
python scripts/run_from_config.py cfg/baseline.cfg

# Direct (advanced)
python scripts/run_romion_extended.py \
  --ticks 600 --seed 42 --out results/run1
```

### Validation:
```bash
# Validate log schema
python scripts/validate_log_schema.py results/run1/simulation.jsonl

# Validate metrics
python tests/test_canonical_metrics.py
```

### Analysis:
```bash
python analysis/gravity_test.py \
  --log results/run1/simulation.jsonl \
  --tick 400 \
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0
```

---

## 📖 Documentation

**Start here:**
- `docs/README.md` - Documentation overview
- `docs/STATUS.md` - Current status (post-audit)
- `docs/QUICK_REFERENCE.md` - Navigation guide

**Canonical Contracts (AUTHORITY):**
- `docs/CANONICAL_LOG_CONTRACT.md` - Schema v2.0 specification
- `docs/CANONICAL_METRICS.md` - Metric definitions

**Theory:**
- `docs/METHODOLOGY.md` - Experimental standards
- `docs/theory/` - Theoretical foundations
- `docs/THEORY.md` - Core concepts

**Audit Reports:**
- `session_reports/2026-01-10/` - Audit completion (KROK 2, KROK 3)

---

## ✅ Contracts Enforced

### Schema v2.0
- ✅ metrics_pre/post separation
- ✅ mean_frustration required
- ✅ Layer labels (L1-CORE, L2-FRACTURE)
- ✅ projection.uses_metrics_post = true
- ✅ Validation: fail-closed (invalid → reject)

### Canonical Metrics (20 metrics)
- ✅ L1-CORE: mean_kappa, mean_pressure, mean_frustration, total_weight, n_edges, n_nodes
- ✅ L2-FRACTURE: visible_edges, visible_ratio, mean_kappa_visible
- ✅ L3-INTERPRETATION: hub_share, coverage, R0, R2
- ✅ Evolution: spawn_new, spawn_reinf, field_tail_added, removed, norm_ops
- ✅ Bounds enforced, cross-metric consistency checked

**See:** `docs/CANONICAL_METRICS.md` for complete specifications

---

## 🎯 Next Phase (Deferred)

Options available (separate decision):
1. **P0 Engine Cleanup** - Mechanical code improvements
2. **Gravity Re-evaluation** - Field theory on stable foundation
3. **Cosmology/Warp** - New chapter, stable base
4. **Paper Freeze** - Theory publication

**Current mode:** STABLE CORE, WAITING FOR DIRECTION

---

## 📋 Key Files

**Simulation:**
- `core/engine.py` - Main simulation loop
- `core/rules.py` - S1/S2/S3 evolution rules
- `core/metrics.py` - Metric computation

**Validation:**
- `scripts/validate_log_schema.py` - Schema v2.0 validator
- `analysis/gravity_test/validate_romion.py` - Metrics validator
- `scripts/validate_sweep.py` - Sweep validation (with schema check)

**Analysis:**
- `analysis/gravity_test/main.py` - Main analysis entry
- `analysis/gravity_test/metrics.py` - L3 metrics (hub_share, coverage, R0, R2)
- `analysis/gravity_test/clustering.py` - Cluster detection

**Tests:**
- `tests/test_canonical_metrics.py` - Metrics validation (9/9 passed)

---

## 🔧 Requirements

- Python 3.11+
- Dependencies: networkx, numpy, matplotlib (for analysis)
- No external physics libraries (theory-driven only)

---

## 📚 References

**Canonical Documentation:**
- CANONICAL_LOG_CONTRACT.md - Schema v2.0 law
- CANONICAL_METRICS.md - Metrics law
- METHODOLOGY.md - Experimental standards

**Theory:**
- theory/GLOSSARY.md - Complete terminology
- theory/MEASUREMENT_THRESHOLDS.md - Three-threshold system
- THEORY.md - Foundations

**Audit:**
- session_reports/2026-01-10/ - Completion reports

---

## 💬 Notes

- **Theory-first:** No magic constants, no data fitting
- **Fail-closed:** Invalid metrics → reject run
- **Reproducibility:** seed + config_hash + git_commit required
- **Layer separation:** L1/L2/L3 enforced contractually
- **Schema v2.0:** MANDATORY for all new work

---

**Project Status:** OPERATIONAL MATURITY ✅  
**Theory:** LOCKED 🔒  
**Methodology:** FAIL-CLOSED ⚠️  
**Ready for:** Next phase (decision pending)

**Full documentation:** See `docs/` directory  
**Audit reports:** See `session_reports/2026-01-10/`
