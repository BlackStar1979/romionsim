# 📁 Project Structure

**Complete ROMION O'LOGIC™ layout with descriptions**

**Updated:** 2026-01-11  
**Status:** POST-AUDIT - Operational Maturity

---

## 🏗️ TOP LEVEL

```
romionsim/
├── core/              # Simulation engine
├── analysis/          # Analysis tools + validation
├── scripts/           # Runners + validation tools
├── tests/             # Test suite + experiments
├── cfg/               # Configurations
├── docs/              # Documentation ⭐
├── archive/           # Historical files
├── session_reports/   # Session logs
├── research/          # Research notes
└── experiments/       # Exploratory scripts
```

---

## 🔧 CORE/ - Simulation Engine

```
core/
├── engine.py          # Main evolution loop
├── graph.py           # Hypergraph data structure
├── rules.py           # S1/S2/S3 evolution rules
├── metrics.py         # L1-CORE metrics computation
└── __init__.py
```

**Purpose:** ROMION O'LOGIC™ simulation core  
**Status:** Stable, MVP implementation  
**Note:** Schema v2.0 support partial (validation at analysis layer)

---

## 🔬 ANALYSIS/ - Analysis Tools

```
analysis/
├── gravity_test.py            # Main entry point (CLI wrapper)
└── gravity_test/              # ⭐ Modular analysis package
    ├── __init__.py           # Package exports
    ├── main.py               # CLI and orchestration (248 lines)
    ├── io.py                 # Log loading (63 lines)
    ├── clustering.py         # Cluster detection (138 lines)
    ├── metrics.py            # L3-INTERPRETATION metrics (246 lines)
    ├── distances.py          # Range calculation (111 lines)
    ├── channels.py           # Channel capacity (NEW)
    ├── validate_romion.py    # ⭐ Canonical metrics validation (550 lines)
    └── validate.py           # Legacy validation (superseded)
```

**Purpose:** Post-run analysis + validation  
**Main tool:** gravity_test (modular, <300 lines/file)  
**Key addition:** validate_romion.py (KROK 3, canonical metrics enforcement)

**Layer separation:**
- L1-CORE: core/metrics.py
- L2-FRACTURE: projection in gravity_test/main.py
- L3-INTERPRETATION: gravity_test/metrics.py (hub_share, coverage, R0, R2)

---

## 🛠️ SCRIPTS/ - Runners + Validation

```
scripts/
├── run_romion_extended.py     # Main simulator
├── run_from_config.py         # Config-based runner
├── run_romion_clean.py        # Baseline runner
├── run_with_frustration.py    # Frustration testing
├── run_metadata.py            # KROK 6 metadata runner
│
├── validate_log_schema.py     # ⭐ Schema v2.0 validator (650 lines)
├── validate_sweep.py          # ⭐ Sweep validator (enhanced)
├── validate_config.py         # Config validator
├── validate_simulation.py     # Simulation validator
├── validate.py                # Legacy validator
│
├── sweep_krok6.py             # ⭐ KROK 6 sweep runner
├── sweep_inprocess.py         # In-process sweep
├── batch_sweep.py             # Batch sweep runner
├── batch_test_c.py            # Test C batch
│
├── lint_results.py            # Results linter
├── analyze_sweep.py           # Sweep analysis
├── update_sweep_results.py    # Results updater
│
└── [other utilities]          # Various helpers
```

**Purpose:** Running simulations + validation  
**Main runners:** run_from_config.py, sweep_krok6.py  
**Key validators:** validate_log_schema.py (KROK 2), validate_sweep.py (KROK 6)

**Note:** Obsolete audit scripts removed (2026-01-11 cleanup)

---

## 🧪 TESTS/ - Test Suite

```
tests/
├── test_canonical_metrics.py  # ⭐ Canonical metrics tests (9/9 pass)
├── test_v2_valid.jsonl        # Schema v2.0 test log
│
├── unit/                      # Unit tests
├── gravity_test/              # Analysis tests
│
├── test_c/                    # Historical: Parameter exploration
│   ├── README.md
│   ├── RESULTS.md
│   ├── cfg/                  # 6 configs (R0-R5)
│   └── results/              # Raw data
│
├── sweep_decay_inprocess/     # Historical: Decay sweep
│   ├── README.md
│   ├── FINAL_RESULTS.md
│   ├── cfg/
│   └── results/
│
└── [other test directories]   # Various experiments
```

**Purpose:** Test suite + historical experiments  
**Key test:** test_canonical_metrics.py (KROK 3, validates enforcement)  
**Note:** test_c/ and sweep_decay_inprocess/ are pre-audit (historical reference)

---

## ⚙️ CFG/ - Configurations

```
cfg/
├── baseline.cfg       # Default parameters
├── decay_slow.cfg     # decay×0.7
├── decay_optimal.cfg  # Optimal from sweeps
├── spawn_up.cfg       # spawn×1.2
├── tension_up.cfg     # tension×1.2
└── [other configs]    # Various parameter sets
```

**Purpose:** Reusable simulation configurations  
**Format:** INI-style with sections  
**Count:** 13+ configs

---

## 📚 DOCS/ - Documentation

```
docs/
├── README.md                         # ⭐ Documentation overview
├── STATUS.md                         # ⭐ Current status (post-audit)
├── ROADMAP.md                        # ⭐ Development roadmap
├── QUICK_REFERENCE.md                # ⭐ Quick navigation
├── STRUCTURE.md                      # This file
├── COMMANDS.md                       # Common commands
│
├── CANONICAL_LOG_CONTRACT.md         # ⭐⭐ Schema v2.0 (AUTHORITY)
├── CANONICAL_METRICS.md              # ⭐⭐ Metrics (AUTHORITY)
│
├── METHODOLOGY.md                    # Experimental standards
├── SWEEP_PROTOCOL.md                 # Sweep protocol (KROK 6)
├── RESULTS_HEADER_TEMPLATE.md        # Results format
│
├── THEORY.md                         # Theoretical foundation
├── LOG_SCHEMA_V2.md                  # Schema v2.0 technical
├── MIGRATION_V1_TO_V2.md             # Migration guide
│
├── IMPLEMENTATION_STATUS.md          # MVP vs SPEC
├── P0_CRITICAL_PATCHES.md            # P0 patches
├── GPT_ANNEXES_IMPLEMENTATION_SUMMARY.md  # Annexes status
│
├── AUDIT_GPT_VS_IMPLEMENTATION.md    # Historical: GPT audit
├── COSMOLOGY_MAPPING.md              # Cosmology framework
├── ANNEX_DOCUMENTATION_SUMMARY.md    # Annexes summary
├── QUESTIONS_FOR_CHATGPT.md          # Q&A
├── TASK_RUNNER.md                    # Task management
│
├── S2_TAIL_STATUS.md                 # S2 implementation status
├── SPEC_S2_TAIL.md                   # S2 specification
├── SPEC_THAW_SHOCK.md                # Shock specification
│
└── theory/                           # Detailed theory
    ├── INDEX.md                      # Theory index
    ├── GLOSSARY.md                   # Complete terminology
    ├── MEASUREMENT_THRESHOLDS.md     # Three-threshold system
    ├── HYPERGRAPH_TOPOLOGY.md        # Topological structures
    ├── PARTICLE_PHYSICS_LOOPS.md     # Loop algebra (SPEC)
    ├── PHOTON_ROMION.md              # Photon as phase mode
    ├── COSMOLOGICAL_SCHOOLS_CRITIQUE.md  # Cosmology critique
    ├── EXTENDED_THEORY_ENTANGLEMENT_GRAVITY.md  # Entanglement
    └── ROMION_COMPLETE_SUMMARY.md    # Theory summary
```

**Purpose:** Complete project documentation  
**Authority:** CANONICAL_LOG_CONTRACT.md, CANONICAL_METRICS.md  
**Organization:** <300 lines per file (maintained)

**Key documents (post-audit):**
- ⭐⭐ CANONICAL_LOG_CONTRACT.md - Schema v2.0 law (700 lines)
- ⭐⭐ CANONICAL_METRICS.md - Metrics law (1000 lines)
- STATUS.md - Current operational status
- ROADMAP.md - Next phase options

---

## 🗄️ ARCHIVE/ - Historical Files

```
archive/
├── README.md                  # Archive inventory
├── DEPRECATED_NOTICE.md       # Deprecation notice
│
├── pre_audit/                 # ⭐ Pre-audit docs (2026-01-11)
│   ├── AUDIT_MAIN_PY_CHANGES.md
│   ├── BUG_FIX_COMPLETE_SUMMARY.md
│   └── CRITICAL_BUG_FIX_20260108.md
│
├── sweep_decay_pilot_20260108/  # Historical sweep
│   ├── README.md
│   ├── RESULTS.md
│   ├── cfg/
│   └── results/
│
├── core_engine_old.py         # Old engine version
├── gravity_test_*.py          # Old analysis versions
├── run_romion_extended_old.py # Old runner
│
└── [many other historical files]
```

**Purpose:** Superseded/obsolete files  
**Recent addition:** archive/pre_audit/ (2026-01-11 cleanup)  
**Rule:** Don't use for current work (historical reference only)

---

## 📊 SESSION_REPORTS/ - Session Logs

```
session_reports/
├── README.md
│
├── 2026-01-10/               # ⭐ Audit completion
│   ├── KROK_2_INTEGRATION_COMPLETE.md
│   ├── KROK_2_SANITY_CHECK.md
│   ├── KROK_3_COMPLETE.md
│   ├── VALIDATOR_TEST_REPORT.md
│   └── STRATEGIC_PLAN_POST_EVAL.md
│
└── 2026-01-09/               # Pre-audit sessions
    ├── SESSION_100_PERCENT_COMPLETE.md
    ├── NEXT_SESSION_TODO.md
    └── [other session reports]
```

**Purpose:** Session documentation and audit trail  
**Key reports:** 2026-01-10/ (audit completion)

---

## 🔬 RESEARCH/ - Research Notes

```
research/
└── 2026-01-08_session/       # Session notes
    ├── cleanup_notes.md
    └── [other research notes]
```

**Purpose:** Research scratch space  
**Status:** Various states

---

## 🧪 EXPERIMENTS/ - Exploratory Scripts

```
experiments/
├── phase_sweep.py             # Phase space exploration
└── phase_sweep_complete.py    # Complete version
```

**Purpose:** Exploratory research scripts  
**Status:** Various states, not production

---

## 📊 FILE SIZE POLICY

### Limits (maintained):
- README.md: <300 lines
- STATUS.md: <300 lines
- Analysis modules: <300 lines per file
- Scripts: <300 lines per file

### Recent splits/additions:
- ✅ gravity_test.py → 5 modules (2026-01-08)
- ✅ validate_romion.py added (2026-01-11, 550 lines - canonical enforcement)
- ✅ validate_log_schema.py added (2026-01-10, 650 lines - schema enforcement)

### Large files (justified):
- CANONICAL_LOG_CONTRACT.md (700 lines) - Authoritative contract
- CANONICAL_METRICS.md (1000 lines) - Authoritative contract
- validate_log_schema.py (650 lines) - Complete schema enforcement
- validate_romion.py (550 lines) - Complete metrics enforcement

---

## 🔐 IGNORED FILES (.gitignore)

```
Results data:
- results/*/simulation.jsonl
- results/*/*.csv
- sweep_*/

Python:
- __pycache__/
- *.pyc

Temporary:
- *.log
- *.tmp

Archives (added 2026-01-11):
- *.zip
- *.tar.gz
```

---

## 🎯 ORGANIZATION PRINCIPLES

### 1. Single Source of Truth
- CANONICAL_LOG_CONTRACT.md = schema authority
- CANONICAL_METRICS.md = metrics authority
- No scattered definitions

### 2. Layer Separation
- L1-CORE: core/metrics.py
- L2-FRACTURE: analysis projection
- L3-INTERPRETATION: analysis/gravity_test/metrics.py
- Labels mandatory (enforced by validators)

### 3. Fail-Closed Validation
- validate_log_schema.py = entry gate (schema v2.0)
- validate_romion.py = metrics bounds/consistency
- validate_sweep.py = sweep-level validation
- Invalid → reject (no silent degradation)

### 4. Test Self-Containment
Each test/ directory:
- README (description)
- cfg/ (configs)
- results/ (data)
- Analysis docs

### 5. Config-First
- Every run from .cfg file
- Reproducible (seed + config_hash + git_commit)
- Easy to modify

### 6. Documentation Hierarchy
- docs/ = project-level
- tests/*/ = test-specific
- session_reports/ = audit trail
- archive/ = historical

---

## 📋 KEY FILES BY FUNCTION

### Canonical Contracts (AUTHORITY)
- `docs/CANONICAL_LOG_CONTRACT.md` - Schema v2.0
- `docs/CANONICAL_METRICS.md` - Metrics

### Validation (Entry Gates)
- `scripts/validate_log_schema.py` - Schema enforcement
- `analysis/gravity_test/validate_romion.py` - Metrics enforcement
- `scripts/validate_sweep.py` - Sweep validation

### Simulation
- `core/engine.py` - Evolution loop
- `core/rules.py` - S1/S2/S3 rules
- `scripts/run_from_config.py` - Main runner

### Analysis
- `analysis/gravity_test/main.py` - Analysis orchestration
- `analysis/gravity_test/metrics.py` - L3 metrics
- `analysis/gravity_test/clustering.py` - Cluster detection

### Testing
- `tests/test_canonical_metrics.py` - Metrics validation tests (9/9 pass)
- `tests/unit/` - Unit tests

### Documentation
- `docs/STATUS.md` - Current status
- `docs/ROADMAP.md` - Next phase
- `docs/QUICK_REFERENCE.md` - Navigation

---

## 🔄 RECENT CHANGES (2026-01-10/11)

### Added:
- ✅ CANONICAL_LOG_CONTRACT.md (schema v2.0 authority)
- ✅ CANONICAL_METRICS.md (metrics authority)
- ✅ validate_log_schema.py (schema enforcement)
- ✅ validate_romion.py enhancement (metrics enforcement)
- ✅ test_canonical_metrics.py (validation tests)
- ✅ archive/pre_audit/ (pre-audit docs)

### Removed:
- ✅ Obsolete audit scripts (6 files)
- ✅ Backup ZIPs (92MB)
- ✅ Temp files

### Updated:
- ✅ README.md (post-audit status)
- ✅ STATUS.md (operational maturity)
- ✅ ROADMAP.md (next phase options)
- ✅ docs/README.md (documentation overview)
- ✅ QUICK_REFERENCE.md (canonical contracts, validation)
- ✅ STRUCTURE.md (this file)

---

## 📖 NAVIGATION

**Want to know...?**

- **Current status?** → docs/STATUS.md
- **Project structure?** → This file (STRUCTURE.md)
- **Quick commands?** → docs/QUICK_REFERENCE.md
- **Schema v2.0?** → docs/CANONICAL_LOG_CONTRACT.md
- **Metric definitions?** → docs/CANONICAL_METRICS.md
- **Theory?** → docs/THEORY.md, docs/theory/
- **Audit results?** → session_reports/2026-01-10/

---

**For navigation:** QUICK_REFERENCE.md  
**For commands:** COMMANDS.md  
**For status:** STATUS.md  
**For contracts:** CANONICAL_*.md
