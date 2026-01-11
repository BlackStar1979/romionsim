# Migration Guide: Log Schema v1 → v2

**Date:** 2026-01-09  
**Status:** PLANNING - Not yet implemented in code  
**Breaking Change:** YES - v1 logs incompatible with v2 tools

---

## Overview

**Schema v2** introduces temporal separation (metrics_pre/post/projection) to enforce the fundamental ROMION principle: **no backreaction from observation to dynamics**.

**This is a BREAKING CHANGE.** All existing logs, analysis tools, and sweep results must be migrated or deprecated.

---

## What Changes

### Current (v1 - Implicit Schema)

```json
{
  "tick": 100,
  "spawn_new": 87,
  "removed": 32,
  "visible_edges": 3421,
  "mean_kappa_pre": 0.42,
  "mean_kappa_post": 0.44,
  ...
}
```

**Problems:**
- No schema_version (ambiguous)
- No metadata (seed, config_hash)
- Flat structure (mixes L1 and L2)
- No distinction between decision and observation states

### Target (v2 - Explicit Schema)

```json
{
  "event": "TICK",
  "schema_version": "v2",
  "tick": 100,
  
  "metadata": {
    "seed": 42,
    "config_hash": "a3f5e9...",
    "timestamp_utc": "2026-01-09T..."
  },
  
  "metrics_pre": {
    "n_nodes": 1000,
    "n_edges": 5234,
    "mean_kappa": 0.42,
    "mean_pressure": 1.85,
    ...
  },
  
  "metrics_post": {
    "n_nodes": 1000,
    "n_edges": 5289,
    "mean_kappa": 0.44,
    "mean_pressure": 1.92,
    "horizon_hits": 2,
    "horizon_mass": 0.45,
    ...
  },
  
  "projection": {
    "theta": 0.25,
    "visible_edges": 3421,
    "invisible_edges": 1868,
    "visibility_ratio": 0.647
  },
  
  "events": [
    {"type": "SPAWN", "count": 87, ...},
    {"type": "DECAY", "count": 32, ...}
  ]
}
```

**Benefits:**
- Explicit schema version
- Full reproducibility (metadata)
- Layer separation (L1 vs L2)
- Temporal clarity (pre vs post)

---

## Migration Strategy

### Phase 1: Mark All v1 Data as LEGACY

**Action:** DO NOT try to "upgrade" v1 → v2

**Reason:** Temporal information is LOST in v1 logs. We cannot reconstruct:
- Whether κ was computed before or after evolution
- What projection used (decision or observation state)
- Metadata (seed, config_hash)

**Mark files:**
```
sweep_decay_inprocess/ → sweep_decay_v1_LEGACY/
session_reports/2026-01-09/*.md mentioning 18/18 → add [v1-LEGACY] tag
```

### Phase 2: Implement v2 in Code

**Files to modify:**

1. **core/engine.py** (CRITICAL)
   - Add schema_version to return
   - Restructure return dict per LOG_SCHEMA_V2.md
   - Add metadata section
   - Split metrics_pre/post
   - Add projection section

2. **scripts/run_romion_*.py**
   - Pass seed to engine
   - Compute config_hash
   - Add timestamp
   - Write run_meta.json

3. **analysis/ tools**
   - Reject logs without schema_version
   - Parse v2 structure
   - Use metrics_post (NOT pre) for analysis

### Phase 3: Re-run Critical Experiments

**Which sweeps:**
- decay_sweep (18 runs, ~3 hours)
- Boundary tests (if any)
- Critical falsification tests

**Label:** All new runs get `[v2]` tag

### Phase 4: Deprecate v1 Tools

**Mark as deprecated:**
- Old analysis scripts expecting v1 format
- Session reports referencing v1 data without [LEGACY] tag

---

## Implementation Checklist

### Code Changes (Phase 2)

**core/engine.py:**
- [ ] Add schema_version: "v2"
- [ ] Add metadata dict (seed, config_hash, timestamp)
- [ ] Restructure return: metrics_pre/post/projection
- [ ] Add horizon_hits, horizon_mass tracking
- [ ] Split events into separate array

**scripts/run_romion_clean.py:**
- [ ] Import hashlib, datetime
- [ ] Compute config_hash = hashlib.sha256(json.dumps(params).encode()).hexdigest()
- [ ] Pass seed to CoreEngine
- [ ] Write run_meta.json with execution info

**analysis/gravity_test/:**
- [ ] Add schema validation (reject v1)
- [ ] Update parsers for v2 structure
- [ ] Use metrics_post for all metrics

**scripts/validate_simulation.py:**
- [ ] Add schema_version check
- [ ] Validate v2 structure
- [ ] Check metrics_pre/post consistency

### Data Management (Phase 1 & 3)

- [ ] Rename sweep_decay_inprocess → sweep_decay_v1_LEGACY
- [ ] Tag all session reports mentioning 18/18 with [v1-LEGACY]
- [ ] Create sweep_decay_v2/ for new runs
- [ ] Update ROADMAP.md with migration status

### Documentation (Phase 4)

- [ ] Update COMMANDS.md (v2 format examples)
- [ ] Update QUICK_REFERENCE.md (v2 schema)
- [ ] Add [DEPRECATED-v1] tags to old docs
- [ ] Create MIGRATION_STATUS.md tracking progress

---

## Testing Strategy

### Validation Tests

**Before deploying v2:**
1. Run single tick with v2 code
2. Verify schema_version present
3. Verify metrics_pre ≠ metrics_post
4. Verify projection uses metrics_post
5. Validate with validate_simulation.py

**Regression tests:**
1. Compare metrics_post.mean_kappa (v2) with mean_kappa_post (v1)
2. Should be identical (same computation)
3. Validates backward compatibility of CORE

---

## Breaking Changes Summary

**What BREAKS:**
- ❌ All v1 analysis tools (expect flat dict)
- ❌ All sweep automation scripts (parse old format)
- ❌ All v1 logs (no schema_version)
- ❌ Result comparisons v1 vs v2 (different structure)

**What STAYS COMPATIBLE:**
- ✅ CORE simulation logic (same physics)
- ✅ gravity_test methodology (three thresholds)
- ✅ Metric definitions (hub_share, coverage, etc)
- ✅ Theory documents (already v2.0)

---

## Timeline Estimate

**Phase 1 (Marking):** 1 hour
- Rename directories
- Tag documents

**Phase 2 (Code):** 4-6 hours
- engine.py restructure
- Runner updates
- Analysis tool updates
- Validation

**Phase 3 (Re-run):** 3-4 hours
- decay_sweep (18 runs)
- Validation tests
- Comparison checks

**Phase 4 (Docs):** 1-2 hours
- Update commands
- Tag deprecated
- Migration status

**TOTAL:** 9-13 hours of work

---

## Risk Mitigation

### Risk 1: Data Loss

**Mitigation:**
- Keep ALL v1 data as LEGACY
- Never overwrite v1 with v2
- Clear directory naming (v1_LEGACY vs v2)

### Risk 2: Tool Breakage

**Mitigation:**
- Schema validation at tool entry
- Fail-closed on v1 logs
- Clear error messages

### Risk 3: Result Non-Comparability

**Mitigation:**
- Document that v1/v2 PHYSICS is identical
- Compare regression tests
- Accept that STRUCTURE differs

---

## Decision Point

**PROCEED WITH MIGRATION?**

**YES if:**
- You want reproducible, fail-closed methodology
- You need temporal separation guarantee
- You plan long-term experiments

**NO if:**
- Current v1 data is critical short-term
- 9-13 hours is too expensive now
- You prefer gradual migration

---

## Current Recommendation

**DO NOT IMPLEMENT v2 YET** in this session.

**Reason:**
- 9-13 hours of work
- Breaks all existing data
- Requires systematic re-runs

**Instead:**
1. ✅ Complete remaining P0 patches (epsilon_spark, S2-tail rename)
2. ✅ Finalize Phase A/B documentation
3. ⏳ Plan v2 migration for dedicated session

---

**Status:** Migration planned, not executed  
**Next:** Complete lightweight P0 patches (P0.5, P0.6)  
**Future:** Dedicated v2 migration session
