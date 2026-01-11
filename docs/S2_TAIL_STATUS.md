# S2-tail Implementation Status

**Date:** 2026-01-07 20:30
**Status:** IMPLEMENTED but needs tuning

**[HISTORICAL - PRE-AUDIT]**  
**Note:** This documents S2-tail implementation work prior to audit.  
**Post-audit clarification:** field_tail ≠ S2 Antipair (proxy only, KROK 5)  
**For current status:** IMPLEMENTATION_STATUS.md (S2 marked SPEC)

---

## ✅ What Was Done:

### 1. Implementation Complete:
- ✅ `rule_s2_tail()` in core/rules.py (line 260)
- ✅ Integrated into core/engine.py tick() sequence
- ✅ CLI flags in run_romion_extended.py
- ✅ Helper functions (_cluster_distance_bg, etc.)

### 2. Bug Fixes:
- ✅ Fixed `G.has_edge()` → use `v in G.adj[u]` 
- ✅ Tested and runs without crashes

### 3. Initial Tests:
- ✅ test_s2_quick: 100 ticks, S2=0 (too short)
- ✅ test_s2_final: 500 ticks, S2=1 @ tick 200 (ONE bridge!)

---

## ❌ Problem: Bridges NOT Visible in gravity_test

### Test: test_s2_final @ tick 200
```
S2 column shows: 1 bridge added
gravity_test shows: P(bridge|dist>=2) = 0.000
```

### Possible Causes:

1. **Weight Issue:**
   - tail_w = 0.008
   - wbridge = 0.0
   - Bridge should be counted... unless removed by decay

2. **Same-Cluster Issue:**
   - S2-tail samples from "different clusters"
   - But maybe clusters are computed differently?
   - Need to verify cluster membership

3. **Too Few Samples:**
   - tail_samples = 200
   - tail_base_rate = 0.05
   - Expected bridges per tick: ~200 * 0.05 * g(frust) * exp(-λ*d)
   - For dist=2: 200 * 0.05 * 0.5 * exp(-0.5*2) ≈ 1.8
   - But only 1 bridge in 200 ticks!

---

## 🔧 Required Tuning:

### Phase 1: Diagnostic Run
```bash
python run_romion_extended.py \
  --ticks 500 \
  --enable-s2-tail \
  --tail-samples 500 \
  --tail-base-rate 0.10 \
  --lambda-dist 0.3 \
  --tail-w 0.008 \
  --decay-scale 0.7 \
  --dump-graph-every 50 \
  --out test_s2_diagnostic
```

**Expected:** S2 column shows 5-10+ bridges by tick 400

### Phase 2: Verify Distance
Check if added bridges are actually at dist>=2:
- Add logging in rule_s2_tail()
- Print: (u, v, dist, frust, p_accept) when accepted
- Verify clusters are truly different

### Phase 3: Increase Aggressiveness
If diagnostic shows dist>=2 but still 0 in gravity:
```python
tail_samples = 1000        # More candidates
tail_base_rate = 0.20      # Higher acceptance
lambda_dist = 0.2          # Less distance penalty
frust_x0 = 0.3             # Lower frustration threshold
```

---

## 📋 Next Steps:

### Immediate:
1. Add debug logging to rule_s2_tail()
2. Run diagnostic with verbose output
3. Check if bridges survive decay

### If Still Failing:
1. Verify cluster computation matches gravity_test
2. Check if tail_w bridges counted in bridge stats
3. Consider increasing tail_w slightly (0.010-0.012)

### Once Working:
1. Document optimal parameters
2. Test with R2 (decay×0.7) combo
3. Run full 1200 tick test
4. Verify P(bridge|dist>=2) > 0 in gravity_test

---

## ⚠️ Thaw Shock: NOT IMPLEMENTED YET

Shock fracture mode is specified but not coded. This is lower priority until S2-tail is proven working.

---

**Status:** Implementation complete, tuning required
**Blocker:** Parameters too conservative
**Action:** Diagnostic run with increased aggressiveness
