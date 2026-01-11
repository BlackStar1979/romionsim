# Test C: Results Summary

## Run Metadata

- **Date:** 2026-01-08 (updated with channels/anisotropy)
- **Commit/version:** romionsim main
- **Test name:** Test C - Parameter Exploration
- **Seeds:** 42
- **Ticks:** 600 (analyzed @ 400)

## Dynamics Parameters

| Run | spawn_scale | decay_scale | tension_scale | shock |
|-----|-------------|-------------|---------------|-------|
| R0 | 1.0 | 1.0 | 1.0 | - |
| R1 | 1.2 | 1.0 | 1.0 | - |
| R2 | 1.0 | 0.7 | 1.0 | - |
| R3 | 1.0 | 1.0 | 1.2 | - |
| R4 | 1.2 | 0.7 | 1.2 | - |
| R5 | 1.0 | 1.0 | 1.0 | tick 200-250, spawn×1.5, decay×1.5 |

## Analysis Thresholds (explicit)

- **wcluster / wdist (background geometry):** 0.02 / 0.005
- **wbridge (bridges/field):** 0.0 (all positive edges)
- **min-cluster-size:** 2
- **disconnected-policy:** maxdist

## Analysis Flags

- **channels:** on
  - channels_mode: cut_weight
- **anisotropy:** on
  - anisotropy_splits: 5

## Fail-Closed

- **INVALID runs excluded:** yes
- **FROZEN runs (bridges=0):** tracked but included in comparison

---

## 📊 FULL METRICS TABLE @ TICK 400

| Run | Parameter | Clusters | Bridges | Weight | Hub% | Coverage | Ch.Cap | Anisotropy | Status |
|-----|-----------|----------|---------|--------|------|----------|--------|------------|--------|
| R0 | Baseline | 695 | 879 | 3.58 | 0.7% | 73.5% | 3.577 | 0.020 | FROZEN@600 |
| R1 | spawn×1.2 | 580 | 440 | 1.68 | 1.1% | 59.3% | 1.680 | 0.061 | FROZEN@600 |
| **R2** | **decay×0.7** | **451** | **1389** | **7.42** | **2.6%** | **66.7%** | **7.417** | **0.028** | **ACTIVE** |
| R3 | tension×1.2 | 691 | 1045 | 4.54 | 0.6% | 75.7% | 4.538 | 0.045 | FROZEN@600 |
| R4 | Combo | 465 | 797 | 4.31 | 1.2% | 66.7% | 4.306 | 0.039 | FROZEN@600 |
| R5 | Shock | 709 | 579 | 2.37 | 0.7% | 62.9% | 2.370 | 0.026 | FROZEN@600 |

---

## 🏆 CORE WINNER (ranked)

**Ranking rule (lexicographic):**
1. max bridges_weight
2. min hub_share  
3. max coverage
4. max bridges_count

**Winner: R2 (decay×0.7)**
- bridges_weight: 7.42 (highest)
- hub_share: 2.6% (acceptable)
- coverage: 66.7%
- channel_capacity: 7.417 (highest)

---

## ❌ REJECTED RUNS

### FROZEN (bridges collapse by tick 600)
- R0: baseline → frozen after tick 300 peak
- R1: spawn×1.2 → frozen
- R3: tension×1.2 → frozen
- R4: combo → frozen
- R5: shock → frozen (shock had NEGATIVE effect)

---

## 📈 TIME EVOLUTION DISCOVERY

| Tick | R0 Bridges | R0 Ch.Cap | R2 Bridges | R2 Ch.Cap |
|------|------------|-----------|------------|-----------|
| 200 | 1242 | 4.50 | 1574 | 5.88 |
| **300** | **2204** | **11.29** | 326 | 2.27 |
| 400 | 879 | 3.58 | 1389 | 7.42 |
| 500 | 114 | 0.47 | 988 | 4.41 |
| 600 | 15 | 0.04 | 387 | 1.44 |

**Key finding:** R0 has HIDDEN PEAK at tick 300 (11.29 capacity!) but collapses rapidly.
R2 is more sustainable despite lower peak.

---

## 🔬 DIAGNOSTICS (non-ranking)

**Best channel_capacity:** R2 (7.417)
**Highest anisotropy:** R1 (0.061) - indicates structural asymmetry

**Anisotropy as phase transition marker:**
- R2@tick 300: anisotropy=0.239 (10x normal!) → structural reorganization
- High anisotropy (>0.1) signals phase transitions

---

## 📋 FINDINGS

1. **Decay paradox:** slower decay (R2) prevents extremes → more sustainable
2. **Single-tick analysis insufficient:** R0 hidden peak missed at tick 400
3. **Shock negative effect:** R5 shock REDUCED activity (579 vs 879 baseline)
4. **Anisotropy diagnostic:** spikes indicate structural transitions

---

## 📁 RAW DATA

- **CSV:** results/test_c_corrected_results.csv
- **Channels comparison:** CHANNELS_COMPARISON.csv
- **Evolution analysis:** EVOLUTION_ANALYSIS.md

---

**For methodology:** See docs/METHODOLOGY.md  
**For theory:** See docs/theory/
