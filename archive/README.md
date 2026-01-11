# 📦 Archive

**Historical files worth preserving**

---

## 📋 CONTENTS:

### Audits (Historical Value):
- **AUDIT.md** (2025-01-06)
  - Initial audit from romionbygoogle transition
  - Documents clean implementation creation
  - Theory-code alignment baseline
  
- **AUDIT_2026_01_07.md** (2026-01-07)
  - Post-Test C Phase 1 audit
  - Methodological soundness verification
  - Tautology elimination documented

### Retracted Findings:
- **DISCOVERY_RANGE_2_RETRACTED.md**
  - Range=2 finding retracted (artifact)
  - Singleton noise geometry issue
  - Important methodological lesson

### Old Code (Reference):
- **core_engine_old.py**
  - Previous engine implementation
  - Backup before current version

- **run_romion_extended_old.py**
  - Previous runner version
  - Backup before --seed arg added

- **gravity_test_monolith.py**
  - Original 718-line version (v1.0)
  - Before modularization to gravity_test/ package

- **gravity_test_backup.py**
  - Old gravity_test version
  
- **gravity_test_before_chatgpt_fix.py**
  - Pre-bug-fix version (node2c=-1 leak)
  - Reference for bug comparison

### Old Cleanup:
- **CLEANUP_COMPLETE.md**
  - First cleanup (before restructure)
  - Superseded by RESTRUCTURING_COMPLETE.md

---

## 🗑️ CLEANED:

### Removed (2026-01-08):
**Session notes (obsolete):**
- INSTRUKCJA_DLA_CIEBIE.md
- FOR_CHATGPT_DONT_CREATE_NEW.md
- MESSAGE_TO_CHATGPT.md
- NOTATKA_NA_JUTRO_*.md
- SWEEP_INITIATED.md

**Wrong data (pre-bug-fix):**
- TEST_C_FINAL_RANKING_WRONG.md
- TEST_C_CLEAN_RESULTS_WRONG.md
- SESSION_COMPLETE_WRONG.md

**Old tests:**
- test_s2_*/ (3 directories)
- out_grav/
- simulation.jsonl

**Superseded docs:**
- FINAL_STATUS_20260107.md
- FIX_COMPLETE_20260108.md
- PILOT_SWEEP_*.md
- ANALYSIS_R2_TICK_400.md
- EXPERIMENTS_TEST_C.md
- PLAN_6_RUNOW.md
- SANITY_CHECK_M2_M3.md
- GRAVITY_TEST_FIXES.md
- RESTRUCTURING_*.md

**Total removed:** ~30 files, ~500MB

---

## 📤 MOVED TO DOCS:

**Specifications (still relevant):**
- SPEC_S2_TAIL.md → docs/
- SPEC_THAW_SHOCK.md → docs/
- S2_TAIL_STATUS.md → docs/

---

## 📝 RETENTION POLICY:

**Keep:**
- ✅ Audits (historical value)
- ✅ Retracted findings (lessons learned)
- ✅ Major methodology changes

**Remove:**
- ❌ Session notes
- ❌ Obsolete plans
- ❌ Wrong data (pre-bug-fix)
- ❌ Superseded summaries
- ❌ Old test data

---

## 🎯 CURRENT STATE:

Archive contains **9 files**:
- 2 audits (historical)
- 1 retracted finding (lesson)
- 4 old code backups (reference)
- 1 old cleanup doc
- 1 README (this file)

**Clean, minimal, valuable.** ✅

---

**Last cleaned:** 2026-01-08
