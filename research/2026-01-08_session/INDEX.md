# Session Files Index
# 2026-01-08 ROMION Research Session

## Documentation

| File | Description |
|------|-------------|
| `SESSION_REPORT.md` | Comprehensive session report with all discoveries |
| `EXPERIMENTAL_ROADMAP.md` | Detailed plan for future experiments |
| `PROJECTION_RATIO_DATA.md` | Hard data from all projection tests |
| `THETA_5PCT_FINDING.md` | Critical finding: θ ≈ 0.46 gives 5% |
| `ADDITIONAL_CONCEPTS.md` | Extra concepts: elasticity, pressure cage details |

## Scripts

| File | Description |
|------|-------------|
| `run_batch_projection.py` | Batch runner for all simulations |
| `find_5pct_theta.py` | Fine-grained theta search |

## Raw Data (JSON)

| File | Description |
|------|-------------|
| `batch_results/all_projection_ratios.json` | Complete data from all 30 tests |
| `projection_ratio_tick300.json` | Single test detailed output |
| `projection_ratio_tick400.json` | Single test detailed output |
| `phase_propagation_tick200.json` | Phase propagation test output |

## Key Findings Summary

1. **Phase propagation slows in dense regions** (ρ = +0.83 at tick 200)
2. **Projection ratio is ~4-5%** across all simulations
3. **θ ≈ 0.46 gives exactly 5%** - matching baryonic fraction
4. **Results are robust** across different parameters
5. **Pressure cage** - photon can be stopped in dense regions (theory confirmed)
6. **Graph elasticity** - ~0.025 may be max stretch capacity (needs more testing)

## Theory Files Updated

| File | Location |
|------|----------|
| `PHOTON_ROMION.md` | `docs/theory/PHOTON_ROMION.md` |

## Analysis Scripts Created

| File | Location |
|------|----------|
| `phase_propagation_test.py` | `analysis/phase_propagation_test.py` |
| `projection_ratio_test.py` | `analysis/projection_ratio_test.py` |
| `density_velocity_test.py` | `analysis/density_velocity_test.py` |

---

## Quick Commands

```bash
# Run projection ratio test
python analysis/projection_ratio_test.py --log <path> --tick <N>

# Run phase propagation test  
python analysis/phase_propagation_test.py --log <path> --tick <N>

# Run batch tests
python research/2026-01-08_session/run_batch_projection.py
```

---

Session completed: 2026-01-08
Total files created: 10
Total tests run: 30+
