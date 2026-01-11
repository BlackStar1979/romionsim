# Decay Sweep: IN-PROCESS Solution

## Problem Resolved

**Issue:** batch_sweep.py failed with `ModuleNotFoundError: No module named 'core'`

**Root cause:** subprocess calls don't inherit parent's sys.path modifications

**Solution:** Created `sweep_inprocess.py` - runs simulations directly in Python process without subprocess

## Implementation

### sweep_inprocess.py
- **No subprocess:** Imports core modules directly
- **18 runs:** decay ∈ [1.0, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.5], seeds=[42, 123]
- **600 ticks** per run with DUMP_EVERY=100
- **Output:** tests/sweep_decay_inprocess/results/d{decay}_s{seed}/

### analyze_sweep.py
- Runs gravity_test.py on all completed runs
- Extracts channels + anisotropy @ tick 400
- Generates CSV with full metrics
- Prints summary by decay value

## Execution Status

**Started:** 2026-01-09  
**Process PID:** 26528  
**Progress:** Run 1/18 complete (decay=1.0, seed=42)  
**ETA:** ~30-60 minutes for all 18 runs

**First result:** 275 edges @ tick 600 for decay=1.0, seed=42

## Coverage

### Decay points
| Decay | Status | Notes |
|-------|--------|-------|
| 1.0 | Running | R0 baseline |
| 0.9 | Queued | Between R0-R2 |
| 0.85 | Queued | NEW point |
| 0.8 | Queued | Between R0-R2 |
| 0.75 | Queued | NEW point |
| 0.7 | Queued | R2 winner |
| 0.65 | Queued | NEW point |
| 0.6 | Queued | Below R2 |
| 0.5 | Queued | Low decay |

### Comparison with Test C
- R0 (decay=1.0): 879 bridges @ tick 400 (Test C)
- R2 (decay=0.7): 1389 bridges @ tick 400 (Test C)
- **New data:** 7 additional decay points to map curve

## Analysis Pipeline

Once sweep completes:

```bash
# 1. Analyze all runs
python scripts/analyze_sweep.py

# 2. Output: tests/sweep_decay_inprocess/results/analysis_results.csv
# Columns: decay, seed, tick, bridges, weight, hub, coverage, capacity, anisotropy

# 3. Plot decay curve (external tool or manual)
# X-axis: decay
# Y-axis: channel_capacity, bridges_weight
# Expected: Non-monotonic curve with peak ~0.7
```

## Expected Outcomes

### H1: Decay Paradox Confirmation
- **Test:** Is channel_capacity non-monotonic in decay?
- **Prediction:** Peak exists between 0.6-0.8
- **Evidence so far:** R2 (0.7) > R0 (1.0) from Test C

### H2: Optimal Decay Rate
- **Test:** Find η* that maximizes sustained activity
- **Method:** Compare avg(channel_capacity) across decay values
- **Use:** Production runs at optimal η*

### H3: Anisotropy Correlation
- **Test:** Does anisotropy predict system state?
- **Method:** Correlate anisotropy with freeze events
- **Insight:** Early warning signals for collapse

## Files Created

### Scripts
- `scripts/sweep_inprocess.py` (130 lines) - Direct simulation runner
- `scripts/analyze_sweep.py` (200 lines) - Analysis pipeline

### Documentation
- `tests/sweep_decay_inprocess/STATUS.md` - This file
- Output dir: `tests/sweep_decay_inprocess/results/`

## Lessons Learned

### What Worked
✅ Direct in-process execution (no subprocess issues)  
✅ Using CoreEngine API directly  
✅ Clear separation: simulate → analyze  

### What Didn't Work
❌ batch_sweep.py with subprocess calls  
❌ Relying on PYTHONPATH inheritance  
❌ Complex subprocess wrappers  

### Key Insight
**Simplicity wins:** Direct Python execution is more reliable than complex subprocess orchestration for batch tasks.

## Next Steps

1. ⏳ **Wait for sweep completion** (~30-60 min)
2. ⏳ **Run analysis:** `python scripts/analyze_sweep.py`
3. ⏳ **Examine decay curve** - Find η* optimum
4. ⏳ **Update ROADMAP.md** - Mark HIGH-1 complete
5. ⏳ **Write RESULTS.md** - Document findings

---

**Status:** 🟡 IN PROGRESS (1/18 runs complete)  
**ETA:** 2026-01-09 late afternoon  
**Check progress:** `python scripts/analyze_sweep.py` (safe to run anytime)
