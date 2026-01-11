# Test C: Before/After Bug Fix Comparison

**Bug:** node2c=-1 leak  
**Fixed:** 2026-01-08  
**Impact:** All metrics were inflated

---

## 🐛 THE BUG

### What Happened:
```python
# After min_cluster_size filtering
# Unassigned nodes had node2c = -1
# Python -1 = last index!

cu, cv = node2c[u], node2c[v]
# cu=-1 accessed deg[-1] (WRONG cluster!)
# Counted cluster↔(-1) as bridges
```

### Symptoms:
- Hub share >100% (impossible!)
- Coverage >100% (impossible!)
- Bridge counts inflated
- Metrics nonsensical

---

## 📊 R2@400 COMPARISON

### Before Fix (WRONG):
```
Bridges: 976
Pairs: 213
Hub: 31%
Coverage: 101% ❌
```

### After Fix (CORRECT):
```
Bridges: 246 ✅
Pairs: 150 ✅
Hub: 10.7% ✅
Coverage: 100.0% ✅
```

**Changes:**
- Bridges: -75% (976→246)
- Hub: Normalized (<100%)
- Coverage: Fixed (exactly 100%)

**Matches ChatGPT calculation:** 246 bridges ✅

---

## 📊 R0@400 COMPARISON

### Before Fix (WRONG):
```
Bridges: 150
Pairs: 17
Hub: 106% ❌
Coverage: 101% ❌
```

### After Fix (CORRECT):
```
Bridges: 0 ✅
Pairs: 0 ✅
Hub: 0% ✅
Coverage: 100% ✅
```

**Critical Discovery:**
- Baseline is FROZEN (not weak!)
- Previous "150 bridges" was artifact
- System reaches frozen attractor

---

## 📋 ALL RUNS IMPACT

### Before (All WRONG):
| Run | Bridges | Hub % |
|-----|---------|-------|
| R0 | 150 | 106% ❌ |
| R1 | 41 | 113% ❌ |
| R2 | 976 | 31% |
| R3 | 233 | 90% |
| R4 | 323 | 69% |
| R5 | 150 | 106% ❌ |

### After (CORRECT):
| Run | Bridges | Hub % |
|-----|---------|-------|
| R0 | 0 ✅ | 0% ✅ |
| R1 | 0 ✅ | 0% ✅ |
| R2 | 246 ✅ | 10.7% ✅ |
| R3 | 12 ✅ | 25.0% ✅ |
| R4 | 38 ✅ | 16.0% ✅ |
| R5 | 0 ✅ | 0% ✅ |

---

## 🔍 WHAT CHANGED

### Ranking:
```
Before: R2 > R4 > R3 > R0=R5 > R1
After:  R2 > R4 > R3 > R0=R1=R5 (frozen)
```

### Interpretation:
```
Before: "R2 is best, others weaker"
After:  "R2 prevents freeze, others frozen"

Qualitative change in understanding!
```

---

## ✅ VERIFICATION

### Bug Fix Checks:
1. ✅ Hub share <100% everywhere
2. ✅ Coverage = 100% everywhere
3. ✅ Matches independent calculation (ChatGPT)
4. ✅ Frozen runs show 0 bridges
5. ✅ No impossible values

### Sanity Asserts Added:
```python
# In compute_hub():
assert 0 <= a < n_clusters
assert 0 <= b < n_clusters

# In count_bridges():
if cu < 0 or cv < 0:
    continue  # Skip unassigned
```

---

## 📝 LESSONS

### Methodological:
1. Impossible values (>100%) are RED FLAGS
2. Always verify against independent calculations
3. Peer review catches bugs (ChatGPT spotted it!)
4. Python -1 indexing dangerous with filters

### Scientific:
1. Bug changed INTERPRETATION not just numbers
2. "Baseline weak" → "Baseline FROZEN"
3. Critical to fix before conclusions
4. Retest everything after bug fix

---

## 🚀 IMPACT ON PROJECT

### Immediate:
- ✅ All Test C metrics corrected
- ✅ Baseline correctly identified as frozen
- ✅ decay effect properly quantified

### Next Steps:
- ✅ Informed sweep design (freeze boundary)
- ✅ Correct understanding of dynamics
- ✅ Valid basis for theory

---

**Bug documentation:** ../../docs/CRITICAL_BUG_FIX_20260108.md  
**Fix summary:** ../../docs/BUG_FIX_COMPLETE_SUMMARY.md
