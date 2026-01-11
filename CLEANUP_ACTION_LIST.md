# ROMION CLEANUP - DETAILED ACTION LIST

**Date:** 2026-01-11  
**Status:** Ready for execution  
**Audit:** POST-AUDIT (100% complete)

---

## IMMEDIATE ACTIONS (Priority 1)

### DELETE FILES (9 items)

**Root:**
1. `romionsim_202501101114.zip` (44MB backup)
2. `romionsim_202501101490.zip` (48MB backup)
3. `temp_full_inventory.json` (temp file)
4. `md_files_inventory.json` (temp file, just created)

**Scripts (Obsolete audit tools):**
5. `scripts/audit_complete.py`
6. `scripts/audit_complete_fixed.py`
7. `scripts/audit_project.py`
8. `scripts/audit_root.py`
9. `scripts/deep_audit.py`
10. `scripts/systematic_docs_review.py`

**Total space saved:** ~92MB + temp files

---

## CRITICAL UPDATES (Priority 1)

### 1. README.md (Root)

**Current issues:**
- Version 2.4.0 (outdated)
- Date: 2026-01-09
- References Test C, Decay Sweep
- No audit mention

**New content should include:**
- Version 3.0.0 (post-audit)
- **Audit Status:** 100% complete
- **Schema:** v2.0 (CANONICAL_LOG_CONTRACT.md)
- **Metrics:** Canonical (CANONICAL_METRICS.md)
- **Operational Status:** Stable Core, Theory Locked
- Quick links to canonical contracts
- Updated structure (new files)

---

### 2. docs/STATUS.md

**Current issues:**
- Completely outdated (2026-01-09)
- Focuses on Test C, Decay Sweep
- Roadmap points to pre-audit work

**New content should include:**

```markdown
# Project Status

**Updated:** 2026-01-11  
**Phase:** POST-AUDIT - Operational Maturity  
**Schema:** v2.0

## Audit Status ✅

**6/6 KROKÓW COMPLETE:**
- KROK 1: Semantyka (100%)
- KROK 2: Kontrakt logów (100%)
- KROK 3: Spójność metryk (100%)
- KROK 4: Fail-closed validation (100%)
- KROK 5: Rozdzielenie mechanizmów (100%)
- KROK 6: Kontrakt eksperymentu (100%)

**Deliverables:**
- CANONICAL_LOG_CONTRACT.md (schema v2.0)
- CANONICAL_METRICS.md (metric definitions)
- validate_log_schema.py (enforcement)
- validate_romion.py (enhanced)
- Test suite (12/12 passed)

## Contracts Locked 🔒

**Schema v2.0 (MANDATORY):**
- metrics_pre/post separation
- mean_frustration required
- Layer labels (L1-CORE, L2-FRACTURE)
- projection.uses_metrics_post = true

**Canonical Metrics:**
- 20 metrics fully specified
- Bounds enforced
- Layer separation mandatory
- Cross-metric consistency checked

## Operational Status

**Mode:** STABLE CORE  
**Philosophy:** LOCKED  
**Methodology:** FAIL-CLOSED  
**Theory:** OPERATIONALLY MATURE

## Next Phase Options

(Deferred to separate decision)
1. P0 engine cleanup
2. Gravity re-evaluation
3. Cosmology/warp development
4. Paper freeze

## Documentation

**Core contracts:**
- docs/CANONICAL_LOG_CONTRACT.md
- docs/CANONICAL_METRICS.md
- docs/METHODOLOGY.md

**Audit reports:**
- session_reports/2026-01-10/

**Tests:**
- tests/test_canonical_metrics.py (9/9 passed)
```

---

### 3. docs/README.md

**Current issues:**
- Same as STATUS.md
- Structure outdated

**Updates needed:**
- Rewrite to reflect post-audit state
- Emphasize CANONICAL_*.md as core docs
- Update file listings
- Reference audit completion

---

### 4. docs/ROADMAP.md

**Current issues:**
- Focuses on Decay Sweep, Test C
- Phases 2-4 pre-audit planning
- No audit completion

**Updates needed:**
- Mark Phases 1-1.5 as HISTORICAL (archive reference)
- Update current phase to POST-AUDIT
- New roadmap sections:
  - **Phase 2A: P0 Engine Cleanup** (optional)
  - **Phase 2B: Gravity Re-evaluation** (on stable foundation)
  - **Phase 3: Cosmology** (warp, field theory)
  - **Phase 4: Paper** (freeze theory, publish)
- Reference audit completion as milestone

---

## MODERATE UPDATES (Priority 2)

### 5. docs/QUICK_REFERENCE.md

**Check for:**
- Outdated file references
- Missing CANONICAL_*.md
- Navigation accuracy

**Update:**
- Add canonical contracts section
- Update file tree if needed

---

### 6. docs/STRUCTURE.md

**Updates:**
- Add new files (CANONICAL_*.md, validate_log_schema.py, test_canonical_metrics.py)
- Update scripts/ listing (remove audit tools)
- Verify directory structure current

---

### 7. docs/IMPLEMENTATION_STATUS.md

**Updates:**
- Mark audit items complete
- Update MVP/SPEC status
- Reference canonical contracts

---

### 8. docs/P0_CRITICAL_PATCHES.md

**Updates:**
- Mark completed patches
- Add "POST-AUDIT" status
- Reference canonical enforcement

---

## MINOR UPDATES (Priority 3)

### 9. docs/COMMANDS.md

**Check:**
- Commands still work
- Add validation commands:
  ```bash
  python scripts/validate_log_schema.py <log>
  python tests/test_canonical_metrics.py
  ```

---

### 10. docs/METHODOLOGY.md

**Check:**
- Alignment with CANONICAL_METRICS.md
- Layer separation (L1/L2/L3) referenced
- Cross-reference canonical contracts

---

### 11. docs/theory/GLOSSARY.md

**Updates:**
- Add terms: L1-CORE, L2-FRACTURE, L3-INTERPRETATION
- Add: schema v2.0, canonical metrics
- Update date to 2026-01-11

---

## ARCHIVE CANDIDATES

### Move to archive/pre_audit/

**Documentation:**
- docs/AUDIT_MAIN_PY_CHANGES.md → archive/pre_audit/
- docs/BUG_FIX_COMPLETE_SUMMARY.md → archive/pre_audit/
- docs/CRITICAL_BUG_FIX_20260108.md → archive/pre_audit/

**Rationale:** Historical value, but superseded by audit

---

## FILES TO REVIEW (Check Relevance)

### Keep or Archive?

1. **docs/AUDIT_GPT_VS_IMPLEMENTATION.md**
   - **Decision:** KEEP (historical reference, GPT audit points)
   - Mark as [HISTORICAL - Pre-Audit]

2. **docs/GPT_ANNEXES_IMPLEMENTATION_SUMMARY.md**
   - **Review:** Check if still relevant
   - **Likely:** KEEP (implementation status)

3. **docs/S2_TAIL_STATUS.md**
   - **Review:** Still relevant post-audit?
   - **Check:** Does it conflict with canonical contracts?

4. **docs/SPEC_S2_TAIL.md, docs/SPEC_THAW_SHOCK.md**
   - **Review:** Spec files - keep unless superseded

---

## VERIFICATION CHECKLIST

After updates, verify:

- [ ] README.md reflects audit completion
- [ ] STATUS.md current (2026-01-11)
- [ ] ROADMAP.md post-audit
- [ ] No broken links in documentation
- [ ] All references to deleted files removed
- [ ] CANONICAL_*.md referenced in main docs
- [ ] Test suite runs (test_canonical_metrics.py)
- [ ] No temp files remain
- [ ] Backup zips deleted

---

## EXECUTION PLAN

**Step 1: BACKUP**
```bash
# Create safety backup
git status
git commit -am "Pre-cleanup commit (2026-01-11)"
```

**Step 2: DELETE**
```bash
# Root
rm romionsim_202501101114.zip
rm romionsim_202501101490.zip
rm temp_full_inventory.json
rm md_files_inventory.json

# Scripts
cd scripts
rm audit_complete.py audit_complete_fixed.py audit_project.py
rm audit_root.py deep_audit.py systematic_docs_review.py
```

**Step 3: ARCHIVE**
```bash
mkdir -p archive/pre_audit
mv docs/AUDIT_MAIN_PY_CHANGES.md archive/pre_audit/
mv docs/BUG_FIX_COMPLETE_SUMMARY.md archive/pre_audit/
mv docs/CRITICAL_BUG_FIX_20260108.md archive/pre_audit/
```

**Step 4: UPDATE DOCS**
- Rewrite README.md (root)
- Rewrite STATUS.md
- Rewrite docs/README.md
- Update ROADMAP.md
- Update others per priority

**Step 5: VERIFY**
- Run tests
- Check links
- Review structure

**Step 6: COMMIT**
```bash
git add -A
git commit -m "Post-audit cleanup (2026-01-11): Remove obsolete files, update documentation"
```

---

## SUMMARY METRICS

**Files to delete:** 10
**Files to archive:** 3
**Files to update (critical):** 4
**Files to update (moderate):** 4
**Files to update (minor):** 3
**Files to review:** 4

**Space saved:** ~92MB
**Time estimate:** 2-3 hours

---

**Status:** READY FOR EXECUTION  
**Approval:** Awaiting user confirmation

**Next:** Execute cleanup with user pushes
