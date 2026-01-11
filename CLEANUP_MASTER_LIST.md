# ROMION PROJECT - COMPREHENSIVE CLEANUP PLAN

**Date:** 2026-01-11  
**Context:** Post-Audit (100% Complete)  
**Goal:** Remove obsolete files, update outdated documentation

---

## PHASE 1: FILES TO DELETE

### Root Directory
- [ ] `romionsim_202501101114.zip` - Backup archive (44MB)
- [ ] `romionsim_202501101490.zip` - Backup archive (48MB)
- [ ] `temp_full_inventory.json` - Temporary inventory file

### Scripts (Obsolete Audit Tools)
- [ ] `scripts/audit_complete.py` - Pre-audit tool
- [ ] `scripts/audit_complete_fixed.py` - Pre-audit tool
- [ ] `scripts/audit_project.py` - Pre-audit tool
- [ ] `scripts/audit_root.py` - Pre-audit tool
- [ ] `scripts/deep_audit.py` - Pre-audit tool
- [ ] `scripts/systematic_docs_review.py` - Pre-audit tool

**Rationale:** Audit is complete, these tools served their purpose.

---

## PHASE 2: FILES TO UPDATE (CRITICAL)

### Root
- [ ] **README.md** - Update to reflect audit completion, schema v2.0, canonical contracts
  - Current: 2026-01-09 (Test C, Decay Sweep)
  - Needed: 2026-01-11 (Audit complete, stable core)

### Documentation (docs/)

#### HIGH PRIORITY (Completely Outdated)
- [ ] **STATUS.md** - REWRITE
  - Current: Test C, Decay Sweep status
  - Needed: Audit status, canonical contracts, operational maturity

- [ ] **README.md** - REWRITE
  - Current: Pre-audit documentation structure
  - Needed: Post-audit structure with CANONICAL_*.md

- [ ] **ROADMAP.md** - REWRITE
  - Current: Decay sweep, Test C, Phase 2-4 plans
  - Needed: Post-audit roadmap (P0 patches, gravity, cosmology, paper)

#### MEDIUM PRIORITY (Partial Updates)
- [ ] **QUICK_REFERENCE.md** - CHECK & UPDATE
  - Verify navigation matches current state
  - Add CANONICAL_*.md references

- [ ] **STRUCTURE.md** - CHECK & UPDATE
  - Verify directory structure current
  - Add new files (CANONICAL_*, validate_log_schema.py, etc)

- [ ] **METHODOLOGY.md** - CHECK
  - Verify alignment with CANONICAL_METRICS.md
  - Cross-reference layer separation (L1/L2/L3)

#### LOW PRIORITY (Minor Updates)
- [ ] **COMMANDS.md** - CHECK
  - Verify commands still work
  - Add new validation commands

- [ ] **IMPLEMENTATION_STATUS.md** - UPDATE
  - Mark audit items as complete
  - Update MVP/SPEC status

---

## PHASE 3: FILES TO REVIEW (Audit Status)

### Documentation (docs/)

#### Audit-Related (Check Relevance)
- [ ] **AUDIT_GPT_VS_IMPLEMENTATION.md** - Keep or archive?
  - Content: GPT audit points
  - Status: Complete, historical value
  - **Decision:** KEEP (historical reference)

- [ ] **AUDIT_MAIN_PY_CHANGES.md** - Keep or archive?
  - Content: Changes to main.py
  - **Decision:** ARCHIVE (historical, pre-audit)

- [ ] **BUG_FIX_COMPLETE_SUMMARY.md** - Archive?
  - Content: Bug fixes pre-audit
  - **Decision:** ARCHIVE (superseded by audit)

- [ ] **CRITICAL_BUG_FIX_20260108.md** - Archive?
  - **Decision:** ARCHIVE (historical)

- [ ] **GPT_ANNEXES_IMPLEMENTATION_SUMMARY.md** - Keep or update?
  - Content: Annex implementation status
  - **Decision:** CHECK if still relevant post-audit

- [ ] **P0_CRITICAL_PATCHES.md** - Update or archive?
  - Content: P0 patch list
  - **Decision:** UPDATE with audit completion status

#### Theory Files (Check Currency)
- [ ] **THEORY.md** - Verify alignment with CANONICAL_METRICS.md
- [ ] **theory/GLOSSARY.md** - Check for new terms from audit
- [ ] **theory/MEASUREMENT_THRESHOLDS.md** - Verify accuracy

#### Legacy/Spec Files
- [ ] **S2_TAIL_STATUS.md** - Still relevant?
- [ ] **SPEC_S2_TAIL.md** - Update with current understanding?
- [ ] **SPEC_THAW_SHOCK.md** - Still valid?

---

## PHASE 4: FILES TO CREATE

### Root
- [ ] **VERSION.txt** or version in README
  - Current version post-audit (3.0.0?)
  - Schema version (v2.0)
  - Audit status

### Documentation (docs/)
- [ ] **CHANGELOG.md** (optional)
  - Major changes log
  - Audit completion entry
  - Schema v2.0 migration

- [ ] **POST_AUDIT_STATUS.md** (or update STATUS.md)
  - Current operational status
  - What's locked (contracts)
  - What's next (P0, gravity, cosmology)

---

## PHASE 5: ARCHIVE CANDIDATES

### Move to archive/ (Historical Value)

#### Documentation
- [ ] `docs/AUDIT_MAIN_PY_CHANGES.md` → `archive/audit/`
- [ ] `docs/BUG_FIX_COMPLETE_SUMMARY.md` → `archive/bug_fixes/`
- [ ] `docs/CRITICAL_BUG_FIX_20260108.md` → `archive/bug_fixes/`

#### Scripts (if not deleted)
- [ ] Old audit scripts → `archive/scripts/audit_tools/`

---

## PHASE 6: STRUCTURE VERIFICATION

### Verify Directory Structure
- [ ] `core/` - Engine code (check for obsolete files)
- [ ] `analysis/` - Analysis tools (check for duplicates)
- [ ] `scripts/` - Active scripts only
- [ ] `tests/` - Current tests + canonical metrics test
- [ ] `docs/` - Updated documentation
- [ ] `archive/` - Historical files properly organized

### Check for Duplicates
- [ ] Search for backup files (*_old.py, *_backup.py)
- [ ] Search for temp files (*.tmp, temp_*)
- [ ] Search for test outputs (results/, sweep_*)

---

## PHASE 7: VALIDATION

### Post-Cleanup Checks
- [ ] All imports work (no broken references)
- [ ] README.md accurate
- [ ] STATUS.md current
- [ ] ROADMAP.md reflects post-audit state
- [ ] CANONICAL_*.md referenced in main docs
- [ ] No dangling references to deleted files

### Test Suite
- [ ] Run test_canonical_metrics.py
- [ ] Run any other active tests
- [ ] Verify validation tools work

---

## EXECUTION ORDER

1. **BACKUP FIRST** (create zip of current state)
2. **DELETE** (Phase 1 - remove obsolete files)
3. **ARCHIVE** (Phase 5 - move historical files)
4. **UPDATE** (Phase 2 - rewrite outdated docs)
5. **CREATE** (Phase 4 - new status files)
6. **VERIFY** (Phase 6-7 - structure + tests)

---

## NOTES

- **Principle:** Preserve history (archive/), remove clutter (delete)
- **Priority:** Documentation accuracy > File cleanup
- **Safety:** Test after each phase
- **Audit:** This cleanup is post-audit maintenance, not pre-audit repair

---

## METRICS

### Current State
- Total files: ~2000+ (with results)
- Documentation files: ~30 in docs/
- Scripts: ~30 in scripts/
- Obsolete audit tools: ~6
- Backup zips: 2 (92MB total)

### Target State
- Remove: ~8-10 files
- Update: ~10 docs
- Archive: ~5 files
- Create: ~2 new status files

**Space saved:** ~92MB (zips) + cleanup

---

**Status:** PLAN CREATED  
**Next:** Execute cleanup with user approval
