# 🚨 CRITICAL BUG FIXED - node2c=-1 Leak

**Time:** 2026-01-08 09:30 (just before leaving)
**Discovered by:** ChatGPT peer review
**Impact:** ALL previous Test C numbers WRONG!

---

## 🐛 THE BUG:

### What Happened:
```python
# After min_cluster_size filter:
node2c[unassigned_nodes] = -1

# Python: -1 = LAST INDEX!
# Hub calculation used deg[-1] (wrong cluster!)
# Bridge counts included cluster↔(-1) (not inter-cluster!)
# Coverage >100% (impossible pairs counted!)
```

### Symptoms:
- Hub share >100% (impossible!)
- Coverage >100% (impossible!)
- Bridge counts inflated (included -1 pairs)

---

## ✅ THE FIX:

### count_bridges():
```python
cu, cv = node2c[u], node2c[v]
if cu < 0 or cv < 0:  # Skip unassigned!
    continue
```

### meta_edges:
```python
cu = node2c[u]
if cu < 0:
    continue
cv = node2c[v]  
if cv < 0 or cu == cv:
    continue
```

---

## 📊 CORRECTED NUMBERS (R2@400):

### BEFORE Fix (WRONG):
```
Bridges: 976
Pairs: 213
Hub: 31%
Coverage: 101%
```

### AFTER Fix (CORRECT):
```
Bridges: 246 ✅
Pairs: 150 ✅
Hub: 10.7% ✅
Coverage: 100.0% ✅
```

**Matches ChatGPT calculation!** ✅

---

## ⚠️ IMPACT:

### ALL Test C Rankings INVALID:
- Numbers in TEST_C_FINAL_RANKING.md: WRONG
- Numbers in TEST_C_CLEAN_RESULTS.md: WRONG
- Numbers in STATUS.md: WRONG
- Only R2@400 retested so far

### Need to Rerun:
- [ ] R0@400
- [ ] R1@400
- [ ] R3@400
- [ ] R4@400
- [ ] R5@400
- [ ] Update all ranking docs

---

## 🚀 TODO (After Returning):

1. Retest ALL runs (R0-R5) @ 400
2. Update rankings
3. Update STATUS.md, README.md
4. Then: ChatGPT approval for sweep

---

**Status:** Critical bug fixed. One run verified. Full retest needed.

**Leaving for doctor - will complete when back!**
