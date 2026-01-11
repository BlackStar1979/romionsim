# Decay Sweep: Issues & Debugging

**Date:** 2026-01-08

---

## 🐛 TECHNICAL ISSUES

### 1. Simulation Failures
```
Run: decay=1.0, seed=42
Error: Simulation failed (no stderr)
Status: Unknown cause

Directory exists: sweep_pilot_d1.0_s42/
But: No simulation.jsonl or empty file

Action: Check if simulation actually ran
```

### 2. Python Crashes
```
Run: decay=0.8, seed=123
Error: Fatal Python error: Failed to import encodings module
       ModuleNotFoundError: No module named 'encodings'

Likely: Memory corruption or Python environment issue
Action: Retry with fresh Python process
```

### 3. Analysis Failures
```
Run: decay=0.8, seed=42
Simulation: SUCCESS (freeze=never!)
Analysis: FAILED

Error: No GRAPH entry found for tick=400

Cause: Simulation ran but no graph dumps?
Check: Is dump_graph_every working?
```

---

## ⚠️ METHODOLOGICAL ISSUES

### 1. Freeze Detection Too Simple
```
Current: freeze_tick = first tick with 0 bridges

Problem:
- Single tick might be transient
- Doesn't check if freeze is sustained
- May give false positives

Better:
- Require N consecutive ticks with 0 bridges
- Check if bridges never return
- Define "sustained freeze"
```

### 2. Bridges After Freeze Puzzle
```
Observation:
- decay=1.0, 0.85 freeze @ tick 100
- Yet show bridges @ tick 400

Questions:
- Are these real bridges?
- Residual from before freeze?
- Detection bug?

Resolution needed!
```

### 3. Batch Runner Error Recovery
```
Current: If one run fails, continues to next

Problem:
- No retry mechanism
- No error logging
- Hard to debug

Better:
- Log full stderr
- Attempt retry once
- Save partial results
```

---

## 🔍 MISSING DATA

### Critical Missing Runs:
```
1. decay=1.0, seed=42 (baseline replication)
2. decay=0.8, seed=42 (boundary - exists but not analyzed!)
3. decay=0.8, seed=123 (boundary - crashed)
4. decay=0.75, seed=42 (below boundary)
5. decay=0.75, seed=123 (below boundary)
```

### Impact:
- 63% failure rate (5/8)
- Boundary (0.8) not fully tested
- Below boundary (0.75) not tested at all

---

## 🚧 ACTION ITEMS

### Priority 1 (Critical):
1. **Manually analyze decay=0.8, seed=42**
   - File exists: results/sweep_pilot_d0.8_s42/
   - Has simulation.jsonl
   - Run gravity_test.py manually

2. **Retry decay=0.8, seed=123**
   - Fresh Python process
   - Check memory
   - Save full logs

3. **Run decay=0.75 × 2 seeds**
   - Below boundary
   - Should stay active
   - Critical for verification

### Priority 2 (Important):
4. **Debug simulation failures**
   - Check why d1.0_s42 failed
   - Reproduce error
   - Fix runner

5. **Improve freeze detection**
   - Require sustained freeze
   - Document criteria
   - Update batch_sweep.py

### Priority 3 (Nice to Have):
6. **Batch runner improvements**
   - Better error logging
   - Retry mechanism
   - Progress saving

---

## 🔧 DEBUGGING COMMANDS

### Manual Analysis of decay=0.8, seed=42:
```bash
cd tests/sweep_decay/results

# Check file exists
ls sweep_pilot_d0.8_s42/simulation.jsonl

# Count lines
wc -l sweep_pilot_d0.8_s42/simulation.jsonl

# Check for GRAPH dumps
grep "GRAPH" sweep_pilot_d0.8_s42/simulation.jsonl | wc -l

# Run analysis manually
python ../../analysis/gravity_test.py \
  --log sweep_pilot_d0.8_s42/simulation.jsonl \
  --tick 400 \
  --wcluster 0.02 --wbridge 0.0 --wdist 0.005 \
  --wdist-mode threshold --min-cluster-size 2
```

### Check Simulation Success:
```bash
# Check all directories
ls -la sweep_pilot_*/

# Check simulation.jsonl sizes
du -h sweep_pilot_*/simulation.jsonl
```

---

## 📊 FAILURE ANALYSIS

### By Type:
```
Simulation failures: 1/8 (12.5%)
Python crashes: 1/8 (12.5%)
Analysis failures: 1/8 (12.5%)
Not attempted: 2/8 (25%)

Total failure rate: 5/8 (62.5%)
```

### By decay Value:
```
decay=1.0: 1/2 failed (50%)
decay=0.85: 0/2 failed (0%) ✅
decay=0.8: 2/2 failed (100%) ⚠️
decay=0.75: 2/2 not attempted
```

**Critical:** decay=0.8 (boundary) both failed!

---

## 🎯 LESSONS

### What Worked:
1. decay=0.85 × 2 seeds: Success
2. Freeze detection: Worked for those that ran
3. CSV output: Clean format

### What Failed:
1. Error recovery: None
2. Logging: Insufficient
3. Robustness: 62.5% failure rate

### Improvements Needed:
1. Better error handling
2. Retry mechanism
3. Full stderr capture
4. Progress checkpointing

---

**Next:** Priority 1 actions (manual analysis of d0.8_s42)
