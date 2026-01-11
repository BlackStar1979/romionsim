# ⚠️ RETRACTED: RANGE=2 "Discovery" (2026-01-07)

**Date of Claim:** 2026-01-07  
**Retraction Date:** 2026-01-09  
**Status:** **INVALID - Methodological artifacts**

---

## ⚠️ SUMMARY OF RETRACTION

**Original Claim:** "First long-range evidence @ R2 tick 400: Range=2 (4 bridges at dist=2)"

**Retraction Reason:** The "discovery" was an **artifact of multiple methodological errors**, NOT evidence of long-range field.

**Correct Result:** NO long-range field detected when methodology is correct.

---

## 🔴 METHODOLOGICAL ERRORS IDENTIFIED

### Error #1: topk-mode Fragmentation Artifact

**What was done wrong:**
- Used `wdist-mode=topk` with k=10 for background graph
- Created 451 clusters (vs 195 with threshold mode)
- Fragmentation inflated cluster count artificially

**Why this created false positives:**
- More clusters = more candidate pairs (quadratic growth)
- Fragmented clusters appear "far apart" in background graph
- Weak bridges between fragments counted as "long-range"
- **Reality:** Fragments are part of same physical structure

**Correct procedure:**
- Use `wdist-mode=threshold` with consistent wdist value
- Fragmentation indicates **wrong choice of clustering parameter**, not physical effect

### Error #2: Singletons Counted as Clusters

**What was done wrong:**
- Singletons (1-node clusters) included in analysis
- Each singleton contributes O(N) pairs to pair count

**Why this inflated results:**
- 451 "clusters" included many singletons
- Singleton pairs have undefined/maximal distance
- Artificially inflated "pairs total" metric

**Correct procedure:**
- Filter clusters by min_size >= 2
- Singletons are unassigned nodes (excluded from analysis)

### Error #3: Correlation Window Artifacts

**What was done wrong:**
- Used `dist<=6` window without understanding data distribution
- 4 bridges at dist=2 out of 8577 pairs (0.05%)

**Why this is not significant:**
- P=0.0005 is below noise threshold
- No statistical test for significance
- Cherry-picked window size post-hoc

**Correct procedure:**
- Pre-register correlation window
- Compute p-values for significance
- Check robustness across window sizes

### Error #4: Maxdist Bucket Misinterpretation

**What was done wrong:**
- Excluded maxdist bucket (disconnected pairs)
- Claimed this "revealed signal"

**Why this is wrong:**
- Disconnected pairs ARE part of topology
- Exclusion changes what you're measuring
- "Signal" appeared only after exclusion (cherry-picking)

**Correct procedure:**
- Use `disconnected_policy=maxdist` for coverage
- Report results WITH and WITHOUT maxdist
- No post-hoc exclusions

### Error #5: Decay Parameter Conflation

**What was done wrong:**
- Claimed "decay×0.7 creates range=2"
- Confused parameter tuning with physical mechanism

**Why this is wrong:**
- decay is EXPERIMENTAL parameter (not theory-derived)
- Different decay changes topology (lifetime), not range per se
- Range increase could be:
  - Artifact of fragmentation (more likely)
  - Longer lifetime allowing bridges to form
  - Statistical fluctuation

**Correct procedure:**
- Separate lifetime effects from range effects
- Derive decay from theory (not tune for results)
- Pre-register predictions before parameter sweeps

---

## ✅ CORRECT INTERPRETATION (Post-Retraction)

### What R2@400 Actually Shows

**With correct methodology:**
- Clustering at wcluster=0.02 (threshold mode)
- Background at wdist=0.005 (threshold mode)
- Bridges at wbridge=0.0 (all edges)
- min_cluster_size >= 2 (no singletons)

**Result:**
- ~200-300 clusters (physical aggregates)
- Range = 1 (connectivity-only)
- NO bridges at dist>=2 (or statistically insignificant)

**Interpretation:**
- Current baseline has NO long-range field
- Bridges occur ONLY between adjacent clusters (dist=1)
- This is **connectivity effect**, not field

### What Would Constitute Real Long-Range Evidence?

**Required:**
1. **Systematic effect:** Bridges at dist>=2 for MULTIPLE runs
2. **Statistical significance:** p < 0.01 (corrected for multiple tests)
3. **Pre-registered prediction:** Before running experiment
4. **Robustness:** Survives methodology variations (topk/threshold, window size)
5. **Mechanism:** Derived from S2 or field-tail theory

**Current status:** NONE of these requirements met

---

## 📊 COMPARISON: False Positive vs Reality

| Metric | "Discovery" (WRONG) | Correct Methodology |
|--------|---------------------|---------------------|
| wdist-mode | topk (fragmentation) | threshold (stable) |
| Clusters | 451 (inflated) | ~200-300 (physical) |
| Singletons | Included (error) | Excluded (correct) |
| Range | 2 (artifact) | 1 (connectivity) |
| Bridges @ dist=2 | 4 (0.05%, noise) | 0-2 (insignificant) |
| Interpretation | "Long-range exists" ❌ | "No long-range" ✅ |

---

## 🎓 LESSONS LEARNED

### 1. Fragmentation is Not Discovery
More clusters ≠ more structure. It often means **wrong parameter choice**.

### 2. Post-hoc Exclusions are Cherry-Picking
Excluding maxdist AFTER seeing results invalidates findings.

### 3. Significance Requires Statistics
0.05% effect without p-value is noise, not signal.

### 4. Methodology Must Be Pre-Registered
Changing analysis procedure to "reveal signal" is p-hacking.

### 5. Parameter Tuning ≠ Physics
Adjusting decay to get range=2 is tuning, not theory confirmation.

---

## 🚫 INVALIDATED CLAIMS

**All claims from 2026-01-07 document are INVALID:**

❌ "First long-range evidence"  
❌ "Range=2 is REAL (not artifact)"  
❌ "decay×0.7 creates TWO effects"  
❌ "Weak long-range mechanism exists"  
❌ "Methodology improvements reveal signal"

**Correct statement:**
✅ "No long-range field detected. Apparent range=2 was fragmentation artifact."

---

## 📋 CORRECTIVE ACTIONS TAKEN

1. ✅ Methodology refactored (METHODOLOGY.md v2.0)
2. ✅ Three-threshold separation enforced
3. ✅ Fail-closed validation (no fragmentation)
4. ✅ Singletons excluded by default
5. ✅ This retraction document created

---

## 🔍 WHAT TO DO IF YOU CITED THIS

**If you referenced the "RANGE=2 discovery":**
1. Mark citation as **[RETRACTED]**
2. Update with: "No long-range field detected in baseline"
3. Reference: This retraction document

**If you used similar methodology:**
1. Check for fragmentation (cluster count vs threshold)
2. Exclude singletons (min_cluster_size >= 2)
3. Pre-register analysis plan
4. Compute p-values

---

## 📖 HISTORICAL NOTE

**Why was this document named "RETRACTED" from the start?**

The original document (2026-01-07) was written celebratory ("🎉 DISCOVERY"), suggesting valid findings. However, methodological review (2026-01-09 audit) revealed multiple errors.

The filename `DISCOVERY_RANGE_2_RETRACTED.md` was meant to indicate retraction, but the **content** remained celebratory, creating dangerous mixed messaging.

**This version (v2.0)** completely rewrites the document to:
- Lead with retraction (first 10 lines)
- Explain errors clearly
- Provide correct interpretation
- Invalidate all original claims

---

**Document Status:** AUTHORITATIVE RETRACTION  
**Version:** 2.0 (2026-01-09)  
**Replaces:** Original celebratory version (2026-01-07)  
**Reference:** ROMION METHODOLOGY v2.0 (fail-closed, three-threshold)
