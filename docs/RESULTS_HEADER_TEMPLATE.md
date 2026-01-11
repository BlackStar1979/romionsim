# Results Header (Template)

Copy this block into each test's `RESULTS.md` (or the top of README results section).
Do not report numbers without this header.

---

## Run Metadata

- Date:
- Commit / version:
- Test name:
- Scenario / config:
- Seeds:
- Ticks:

## Dynamics Parameters (must be explicit)

- spawn_scale:
- decay_scale:
- tension_scale:
- any other modifiers:

## Analysis Thresholds (must be explicit)

- wcluster / wdist (background geometry):
- wbridge (bridges/field):

## Analysis Flags (must be explicit)

- channels: on/off
  - channels_mode:
- anisotropy: on/off
  - anisotropy_splits:

## Fail-Closed

- INVALID runs excluded: yes/no
- If invalid occurred: list reasons exactly as printed

## Notes

- Background geometry metrics computed on cluster meta-graph (wdist).
- Bridges/hub/coverage computed on bridges set (wbridge).
- Anisotropy is a proxy (split-axis variability) unless a directed/oriented model exists.

---
