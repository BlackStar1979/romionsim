# Decay Sweep: Results

## Run Metadata

- **Date:** 2026-01-08
- **Test name:** Sweep Decay - Freeze Boundary Detection
- **Seeds:** 42, 123
- **Ticks:** 600 (checkpoints: 100, 200, 300, 400, 500, 600)

## Dynamics Parameters

- **Parameter swept:** decay_scale
- **Grid (Pilot A):** [1.0, 0.85, 0.8, 0.75]
- **Fixed:** spawn_scale=1.0, tension_scale=1.0

## Analysis Thresholds (explicit)

- **wcluster / wdist (background geometry):** 0.02 / 0.005
- **wbridge (bridges/field):** 0.0

## Analysis Flags

- **channels:** off (pilot run)
- **anisotropy:** off (pilot run)

## Fail-Closed

- **INVALID runs excluded:** yes
- **FROZEN definition:** bridges_count=0 OR bridges_weight=0 at tick

---

## 📊 COMPLETED RUNS

| decay | seed | freeze_tick | bridges@400 | hub% | range | status |
|-------|------|-------------|-------------|------|-------|--------|
| 1.0 | 123 | 100 | 12 | 40.0 | 1 | FROZEN |
| 0.85 | 42 | 100 | 25 | 18.8 | 1 | FROZEN |
| 0.85 | 123 | 100 | 40 | 21.7 | 1 | FROZEN |

---

## ❌ FAILED/INCOMPLETE RUNS

| decay | seed | issue |
|-------|------|-------|
| 1.0 | 42 | Simulation failed |
| 0.8 | 42 | Analysis error |
| 0.8 | 123 | Python environment issue |
| 0.75 | 42 | Not attempted |
| 0.75 | 123 | Not attempted |

---

## 🎯 KEY FINDING

**Freeze boundary detected @ 0.8-0.85:**
- decay ≥ 0.85 → FROZEN @ tick 100
- decay ≤ 0.8 → potentially ACTIVE (needs verification)

**Boundary is SHARP!**

---

## 📁 RAW DATA

- **CSV:** results/decay_sweep_pilot.csv
- **Log:** results/sweep_pilot_log.txt

---

**For methodology:** See docs/SWEEP_PROTOCOL.md  
**For issues:** See ISSUES.md
