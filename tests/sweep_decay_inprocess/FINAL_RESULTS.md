# Decay Sweep: Final Results

**Date:** 2026-01-09
**System:** n=1000 nodes, e=10000 initial edges
**Runs:** 18 total

---

## Results Summary @ Tick 400

| Decay | Seed 42 | Seed 123 | Avg Bridges | Avg Capacity | Status |
|-------|---------|----------|-------------|--------------|--------|
| 1.00 | 0 | 0 | 0.0 | 0.000 | FROZEN |
| 0.90 | 0 | 0 | 0.0 | 0.000 | FROZEN |
| 0.85 | 0 | 0 | 0.0 | 0.000 | FROZEN |
| 0.80 | 0 | 3 | 1.5 | 0.009 | CRITICAL |
| 0.75 | 26 | 27 | 26.5 | 0.143 | CRITICAL |
| 0.70 | 744 | 589 | 666.5 | 3.919 | MEDIUM |
| 0.65 | 468 | 422 | 445.0 | 2.606 | LOW |
| 0.60 | 223 | 75 | 149.0 | 0.660 | LOW |
| 0.50 | 185 | 219 | 202.0 | 0.730 | LOW |

---

## Visual Chart: Bridges vs Decay

```
decay=1.00  0
decay=0.90  0
decay=0.85  0
decay=0.80  2
decay=0.75 # 26
decay=0.70 ################################################## 666
decay=0.65 ################################# 445
decay=0.60 ########### 149
decay=0.50 ############### 202
```

---

## Pattern Analysis

### Freeze Boundary

- **Lowest FROZEN:** decay = 0.85
- **Highest ACTIVE:** decay = 0.80
- **Boundary interval:** (0.80, 0.85)
- **Width:** Δ = 0.05

### Optimal Decay

- **Peak capacity:** 3.919 @ decay = 0.70
- **Bridges at peak:** 666

### Anisotropy Patterns

| Decay | Avg Anisotropy | Interpretation |
|-------|----------------|----------------|
| 1.00 | 0.000 | Stable |
| 0.90 | 0.000 | Stable |
| 0.85 | 0.000 | Stable |
| 0.80 | 0.000 | Stable |
| 0.75 | 0.217 | Collapsing |
| 0.70 | 0.036 | Normal |
| 0.65 | 0.173 | Collapsing |
| 0.60 | 0.491 | Collapsing |
| 0.50 | 0.106 | Collapsing |

---

## Key Findings

1. **Decay Paradox Confirmed:** Higher decay does NOT produce higher activity
2. **Sharp Freeze Boundary:** Transition occurs in narrow range (Δ ≈ 0.05)
3. **Optimal Point Exists:** Peak activity at intermediate decay rate
4. **Anisotropy Diagnostic:** Low values indicate stable systems

---

## Comparison with Test C

**Important:** Test C used n=2000 nodes, this sweep uses n=1000

| Run | System Size | Decay | Bridges @400 | Notes |
|-----|-------------|-------|--------------|-------|
| Test C R0 | n=2000 | 1.0 | 879 | Survives |
| Sweep d1.0 | n=1000 | 1.0 | 0 | FROZEN |
| Test C R2 | n=2000 | 0.7 | 1389 | Winner |
| Sweep d0.7 | n=1000 | 0.7 | 666 | Compare |

**Conclusion:** Larger systems tolerate higher decay rates

---

## Technical Details

**Simulation parameters:**
- Nodes: 1000
- Initial edges: 10,000
- Ticks: 600
- Analysis tick: 400
- Seeds: [42, 123]

**Analysis parameters:**
- wcluster: 0.02
- wdist: 0.005
- wbridge: 0.0

**Files:**
- Raw data: tests/sweep_decay_inprocess/results/analysis_results.csv
- This report: tests/sweep_decay_inprocess/FINAL_RESULTS.md

---

*Generated: 2026-01-09*