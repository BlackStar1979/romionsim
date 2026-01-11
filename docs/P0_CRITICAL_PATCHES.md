# P0 Critical Patches - Status Report

**Updated:** 2026-01-11  
**Status:** POST-AUDIT - Review Required  
**Context:** Audit complete, patches need re-evaluation

---

## Overview

This document originally identified critical semantic errors in gravity_test (2026-01-08).

**POST-AUDIT STATUS (2026-01-11):**
- **Audit completed:** 6/6 KROKÓW (100%)
- **Contracts locked:** CANONICAL_LOG_CONTRACT.md, CANONICAL_METRICS.md
- **Validation enforced:** Schema v2.0, canonical metrics
- **Theory stable:** Philosophy locked, methodology fail-closed

**QUESTION:** Are P0 patches still relevant, or superseded by audit work?

**DECISION:** Deferred to next phase (Option A: P0 Engine Cleanup)

---

## Original P0 Issues (2026-01-08)

### Patch 1: CLI Semantics ⚠️
**Problem:** `--wcluster` alias overwrote `--wdist`  
**Impact:** All "wdist=0.005" runs actually used 0.02  
**Status:** NEEDS VERIFICATION (may be fixed in analysis refactor)

### Patch 2: Background Distance Graph ⚠️
**Problem:** Range computed on bridge graph, not background  
**Impact:** "dist=2" meaningless for ROMION geometry  
**Status:** NEEDS VERIFICATION (distances.py may be correct now)

### Patch 3: Clustering ⚠️
**Problem:** Fragile max_node calculation  
**Impact:** Index errors with filtered clusters  
**Status:** NEEDS VERIFICATION (clustering.py may be robust now)

### Patch 4: Unassigned Reporting ⚠️
**Problem:** Edge count reported as node count  
**Impact:** Misleading diagnostics  
**Status:** NEEDS VERIFICATION (metrics.py may be clear now)

### Patch 5: Batch Runner ⚠️
**Problem:** Batch scripts need correct semantics  
**Status:** NEEDS VERIFICATION (batch scripts may be updated)

---

## Post-Audit Context

### What Changed (2026-01-10/11)

**Audit deliverables:**
1. ✅ CANONICAL_LOG_CONTRACT.md - Schema v2.0 authority
2. ✅ CANONICAL_METRICS.md - Metrics authority (20 metrics specified)
3. ✅ validate_log_schema.py - Schema enforcement (entry gate)
4. ✅ validate_romion.py - Metrics enforcement (bounds, consistency)
5. ✅ validate_sweep.py - Sweep validation (schema check)
6. ✅ Test suite - 12/12 tests passed

**What's locked:**
- Philosophy (epistemological foundation)
- Schema v2.0 (MANDATORY for all new work)
- Layer separation (L1/L2/L3 enforced)
- Fail-closed validation (invalid → reject)

**What's safe:**
- P0 cleanup now epistemologically safe (contracts prevent violations)
- Methodology locked (no semantic drift possible)
- Any fixes must conform to CANONICAL_*.md

---

## Re-Evaluation Required

### Questions to Answer:

1. **Are CLI semantics correct now?**
   - Check: analysis/gravity_test/main.py argument parsing
   - Verify: wcluster, wdist, wbridge are separate
   - Test: Does changing wdist affect range (not clusters)?

2. **Is background graph correct?**
   - Check: analysis/gravity_test/distances.py
   - Verify: Uses background, not bridges
   - Test: Range computation independent of wbridge?

3. **Is clustering robust?**
   - Check: analysis/gravity_test/clustering.py
   - Verify: assign_clusters() takes n_nodes explicitly
   - Test: No index errors with filtered clusters?

4. **Is unassigned reporting clear?**
   - Check: analysis/gravity_test/metrics.py
   - Verify: Separate unassigned_nodes from skipped_edges
   - Test: Reports are semantically correct?

5. **Are batch scripts updated?**
   - Check: scripts/batch_*.py
   - Verify: Use correct threshold semantics
   - Test: Reproducible with correct parameters?

---

## Verification Protocol (If Proceeding)

### Step 1: Code Review
```bash
# Check current implementation
view analysis/gravity_test/main.py | grep -A20 "add_argument.*wcluster"
view analysis/gravity_test/distances.py | grep -A30 "background"
view analysis/gravity_test/clustering.py | grep -A20 "assign_clusters"
view analysis/gravity_test/metrics.py | grep -A20 "count_bridges"
```

### Step 2: Semantic Test
```bash
# Test threshold independence
python analysis/gravity_test.py \
  --log test.jsonl --tick 100 \
  --wcluster 0.02 --wdist 0.005 --wbridge 0.0

# Change wdist, verify range changes (not clusters)
python analysis/gravity_test.py \
  --log test.jsonl --tick 100 \
  --wcluster 0.02 --wdist 0.010 --wbridge 0.0
```

### Step 3: Regression Test
```bash
# Verify canonical metrics still work
python tests/test_canonical_metrics.py

# Verify schema validation still works
python scripts/validate_log_schema.py test.jsonl
```

---

## Integration with Canonical Contracts

### If P0 Patches Are Applied:

**Must conform to:**
1. **CANONICAL_METRICS.md** - Three-threshold separation
   - wcluster (L1-CORE: objects)
   - wdist (L2-FRACTURE: background geometry)
   - wbridge (L2-FRACTURE: field interactions)

2. **CANONICAL_LOG_CONTRACT.md** - Schema v2.0
   - No changes to log format
   - Fixes are analysis-layer only

3. **Layer separation** - Enforced
   - L1-CORE: Graph structure (independent of thresholds)
   - L2-FRACTURE: Projection (depends on θ, uses metrics_post)
   - L3-INTERPRETATION: Analysis (hub_share, coverage, R0, R2)

4. **Fail-closed validation**
   - Invalid parameters → reject
   - Out-of-bounds → reject
   - Inconsistent → reject

**Validation:**
- validate_romion.py checks three-threshold separation
- validate_L2_metrics() checks projection uses metrics_post
- Cross-metric consistency enforced

---

## Recommendation (POST-AUDIT)

### Option 1: Defer to "Option A: P0 Engine Cleanup"
**Rationale:**
- Audit complete, theory stable
- P0 patches are mechanical fixes
- Should be part of systematic engine cleanup
- No rush (theory locked, methodology safe)

**Timeline:** Next phase (separate decision)

### Option 2: Verify & Fix Immediately
**Rationale:**
- Clear semantic errors identified
- Affects analysis accuracy
- Quick fixes (2-3 hours)

**Timeline:** This session

### Option 3: Document as "Known Issues"
**Rationale:**
- Pre-audit work is historical reference
- New work will use correct semantics
- Not worth fixing old analysis

**Timeline:** Never (just document)

---

## Current Recommendation: OPTION 1 (DEFER)

**Why:**
1. Audit complete ✅
2. Contracts locked ✅
3. Theory stable ✅
4. No immediate need (not running experiments)
5. Should be part of systematic P0 cleanup (Option A)

**Next steps:**
1. Close cleanup session
2. Decide on next phase (P0/gravity/cosmology/paper)
3. If Option A chosen → include P0 patches in scope
4. If other option → document as known issues

---

## Files Potentially Affected (If Fixed)

| File | Changes Needed | Verification |
|------|----------------|--------------|
| analysis/gravity_test/main.py | CLI args, graph building | Threshold independence test |
| analysis/gravity_test/clustering.py | assign_clusters signature | Index bounds test |
| analysis/gravity_test/metrics.py | count_bridges return | Reporting clarity test |
| analysis/gravity_test/distances.py | Background graph function | Range independence test |
| scripts/batch_*.py | Threshold semantics | Batch run test |

---

## Post-Audit Constraints

**Any P0 fixes MUST:**
- ✅ Conform to CANONICAL_METRICS.md (three-threshold separation)
- ✅ Pass validate_romion.py checks
- ✅ Maintain layer separation (L1/L2/L3)
- ✅ Not introduce magic constants
- ✅ Be theory-driven (not data-fitted)
- ✅ Pass test suite (test_canonical_metrics.py)

**Forbidden:**
- ❌ Changes to schema v2.0 (locked)
- ❌ Changes to canonical metrics (locked)
- ❌ Backreaction (L2 → L1)
- ❌ Layer mixing
- ❌ Silent parameter changes

---

## Decision Required

**Status:** DEFERRED  
**Decision point:** Next phase selection  
**Options:**
- A: Include in P0 Engine Cleanup (systematic)
- B: Fix now (quick patches)
- C: Document as known issues (historical)

**Recommendation:** OPTION A (defer to systematic cleanup)

---

## Session Notes (2026-01-11)

**Cleanup completed:**
- ✅ Obsolete files removed
- ✅ Documentation updated
- ✅ Audit status reflected

**P0 patches:**
- ⏸️ Deferred (not urgent post-audit)
- ⏸️ Will be addressed in next phase if Option A chosen
- ⏸️ No semantic drift risk (contracts locked)

**Safe to defer because:**
- Theory stable ✅
- Methodology locked ✅
- No experiments planned ✅
- Contracts prevent violations ✅

---

**Status:** REVIEW REQUIRED  
**Priority:** DEFERRED (not blocking post-audit)  
**Authority:** CANONICAL_*.md must be respected in any fixes

**For audit status:** docs/STATUS.md  
**For next phase:** docs/ROADMAP.md  
**For contracts:** CANONICAL_LOG_CONTRACT.md, CANONICAL_METRICS.md
