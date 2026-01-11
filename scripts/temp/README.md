# Temporary Helper Scripts

**Purpose:** Quick debugging, fix scripts, and experimental tests from session 2026-01-09

These scripts were used for ad-hoc verification, repairs, and testing during the decay sweep analysis. They are NOT part of the main codebase and can be deleted after the session.

## Files

### Debugging Scripts
- **check_incomplete.py** - Verified which sweep runs had complete logs
- **check_r0.py** - Checked Test C R0 data for system size comparison  
- **check_sweep.py** - Quick verification of sweep run completion

### One-Time Fix
- **fix_d05_s123.py** - Repaired incomplete d0.5_s123 run (now complete)

### Test Scripts
- **quick_test_sweep.py** - Quick 2-run test to verify batch_sweep works
- **test_sweep_simple.py** - Minimal sweep runner for testing

## Main Scripts (Still in scripts/)

The production scripts that should be kept:
- `sweep_inprocess.py` - Working sweep runner (PRODUCTION)
- `analyze_sweep.py` - Analysis pipeline (PRODUCTION)
- `final_report.py` - Report generator (PRODUCTION)
- `quick_viz.py` - Visualization tool (PRODUCTION)
- `investigate_r0_peak.py` - R0 peak analysis (PRODUCTION)

## Usage

These temp scripts were run with:
```bash
python C:\Work\romionsim\scripts\temp\<script>.py
```

All issues have been resolved. These scripts are kept for reference but are no longer needed.

## Status

✅ All issues resolved  
✅ 18/18 runs complete  
✅ Scripts no longer needed  
🗑️ **Can be deleted anytime** (entire temp/ directory)

---

*Created: 2026-01-09*  
*Purpose: Session cleanup & historical reference*  
*Recommendation: Delete this entire directory after session review*
