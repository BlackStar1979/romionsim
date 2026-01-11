# AUDIT LOG: main.py modifications for channels/anisotropy
# Date: 2026-01-08
# Status: COMPLETED AND TESTED

## Changes Made

### 1. Imports added (line ~12-26):
```python
from . import (
    # ... existing imports ...
    split_regions,
    path_capacity,
    anisotropy_index,
    validate_metrics,
    format_invalid_report
)
```

### 2. CLI arguments added (line ~280-290):
```python
parser.add_argument('--channels', action='store_true')
parser.add_argument('--channels-mode', choices=['cut_weight'], default='cut_weight')
parser.add_argument('--anisotropy', action='store_true')
parser.add_argument('--anisotropy-splits', type=int, default=5)
```

### 3. analyze_tick() extended (line ~220-270):
- Added channel_capacity computation using split_regions() + path_capacity()
- Added anisotropy_index computation
- Added validation layer using validate_metrics()
- All new metrics passed to print_report()

### 4. print_report() extended (line ~35-180):
- New parameters: channels_enabled, channel_capacity, channel_meta,
  anisotropy_enabled, anisotropy_val, anisotropy_meta, is_valid, validation_reasons
- New section: "CHANNELS (background geometry)"
- New section: "ANISOTROPY (split-axis variability)"
- New section: "VALIDATION" (only shown if invalid)

## Test Results

### Test 1: R2_decayDown @ tick 400 (active field)
```
CHANNELS (background geometry):
  channel_capacity: 7.417
  mode: cut_weight
  cut_edges: 539
  split: L=226 R=225 (seed=164)

ANISOTROPY (split-axis variability):
  anisotropy: 0.027690
  splits: 5
  degenerate: False
  capacities: ['7.42', '7.21', '7.28', '7.48', '7.04']
```
✓ PASS - metrics computed correctly

### Test 2: R0_base @ tick 400 (lower activity)
```
CHANNELS (background geometry):
  channel_capacity: 3.577
  mode: cut_weight
  cut_edges: 443
  split: L=348 R=347 (seed=271)

ANISOTROPY (split-axis variability):
  anisotropy: 0.020144
  splits: 5
  degenerate: False
  capacities: ['3.58', '3.54', '3.51', '3.43', '3.42']
```
✓ PASS - lower capacity/anisotropy for less active simulation

## Observations

1. **Channel capacity scales with activity:**
   - R2 (active): 7.417
   - R0 (less active): 3.577

2. **Anisotropy is low in both cases:**
   - R2: 0.028
   - R0: 0.020
   - This suggests relatively symmetric graph structure

3. **Split is balanced:**
   - L and R have nearly equal sizes (within 1)
   - Deterministic (seed cluster = hub cluster)

4. **Validation passed:**
   - No validation section shown = all metrics valid
   - hub_share and coverage within [0,100]

## Backward Compatibility

- Default: --channels and --anisotropy are OFF
- Existing command lines work unchanged
- New output sections only appear when flags enabled

## Files Modified

| File | Lines Changed | Description |
|------|---------------|-------------|
| main.py | +85 | Imports, CLI args, metrics, output |

## New Files Created (This Session)

| File | Lines | Description |
|------|-------|-------------|
| regions.py | 145 | Deterministic region split |
| channels.py | 162 | Channel capacity, anisotropy |
| validate.py | 104 | Fail-closed validation |
| distances.py | +81 | build_background_cluster_graph |

## Status

✅ COMPLETE - All changes tested and working
