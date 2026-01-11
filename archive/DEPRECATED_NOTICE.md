# ⚠️ ARCHIVE DIRECTORY - ALL FILES DEPRECATED

**Date:** 2026-01-09  
**Status:** ARCHIVE - Historical reference only

---

## ⚠️⚠️⚠️ DO NOT USE FILES IN THIS DIRECTORY ⚠️⚠️⚠️

All Python files in `archive/` are DEPRECATED and should NOT be used for experiments.

### Archived Files

**Gravity Test Versions:**
- `gravity_test_backup.py` - Old backup (pre-refactor)
- `gravity_test_before_chatgpt_fix.py` - Before ChatGPT fixes
- `gravity_test_monolith.py` - Monolithic version (pre-split)

**Engine Versions:**
- `core_engine_old.py` - Old engine implementation
- `run_romion_extended_old.py` - Old runner script

### Why Deprecated?

These files:
- Use outdated methodology
- May violate three-threshold separation (wcluster/wdist/wbridge)
- Contain bugs that were fixed in current versions
- Are not compatible with current ROMION O'LOGIC™ v2.0

### What to Use Instead

**Current implementations:**
- **Gravity Test:** `analysis/gravity_test.py` (wrapper to `gravity_test/` package)
- **Core Engine:** `core/engine.py`
- **Runner:** `scripts/run_romion_clean.py`

### Archive Policy

**Keep for:**
- Historical reference
- Understanding evolution of codebase
- Regression testing (comparing old vs new)

**DO NOT:**
- Run archived scripts for experiments
- Copy code from archived files
- Reference archived files in documentation

---

## If You Accidentally Used Archived Code

**Your results are INVALID** if you used:
- Any file in `archive/`
- Any file with `_backup` or `_old` suffix
- `gravity_test_before_split.py`
- `gravity_test_backup_20260107.py`

**Action required:**
1. Mark results as [INVALID-ARCHIVE]
2. Re-run with current implementation
3. Compare to verify methodology differences

---

## Documentation Status

**This notice:** AUTHORITATIVE  
**All archived .py files:** DEPRECATED  
**Effective date:** 2026-01-09 (ROMION v2.0 refactor)
