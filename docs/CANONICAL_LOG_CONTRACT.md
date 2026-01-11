# ROMION Canonical Log Contract

**Version:** 2.0  
**Status:** AUTHORITATIVE - SINGLE SOURCE OF TRUTH  
**Enforcement:** MANDATORY from 2026-01-11  
**Authority:** This document defines the ONLY valid log format for ROMION simulations

---

## ⚠️ FUNDAMENTAL PRINCIPLE

> **Every log must be self-validating, complete, and reproducible.**
> 
> Logs without `schema_version` are LEGACY and REJECTED by analysis tools.
> 
> This contract is NON-NEGOTIABLE.

---

## 1. Schema Version (REQUIRED)

### 1.1 Version Field

**EVERY** log file MUST contain `schema_version` in the FIRST event.

```json
{
  "schema_version": "2.0",
  "type": "METADATA",
  ...
}
```

**Validation:**
- Missing `schema_version` → **REJECT** (mark as LEGACY-V1)
- Wrong version (≠ "2.0") → **REJECT**
- schema_version not in first event → **REJECT**

### 1.2 Supported Versions

| Version | Status | Support |
|---------|--------|---------|
| 2.0 | CURRENT | Full support ✅ |
| 1.0 | LEGACY | Read-only with warnings ⚠️ |
| none | INVALID | REJECTED ❌ |

**Legacy handling:**
- v1 logs: Analysis emits warning, marks results [LEGACY-V1]
- v1+v2 mixed: **FORBIDDEN** - analysis REJECTS aggregation
- Unknown version: **REJECT**

---

## 2. Required Event Types

Every log MUST contain these event types in order:

### 2.1 METADATA (First event)

**Purpose:** Run identification and reproducibility

**Required fields:**
```json
{
  "schema_version": "2.0",
  "type": "METADATA",
  "run_id": "2026-01-11T00:00:00Z_abc123",
  "seed": 42,
  "config_hash": "sha256_of_sorted_params",
  "timestamp_utc": "2026-01-11T00:00:00Z",
  "git_commit": "abc123..." | null,
  "git_dirty": false | true | null,
  "python_version": "3.11.5",
  "platform": "Windows-10-...",
  "experiment_name": "decay_sweep",
  "parameters": {
    "spawn_threshold": 0.15,
    "decay": 0.008,
    "W_max": 2.5,
    "theta": 0.25,
    "wcluster": 0.02,
    "wdist": 0.005,
    "wbridge": 0.0,
    ...
  }
}
```

**Validation:**
- All fields REQUIRED except git_* (can be null)
- seed MUST be integer >= 0
- config_hash MUST be SHA256 hex string
- parameters MUST contain ALL ROMION parameters

### 2.2 STATE (Periodic - every 50 ticks)

**Purpose:** System state snapshots with CORE/FRACTURE separation

**Schema v2.0 structure:**
```json
{
  "schema_version": "2.0",
  "type": "STATE",
  "tick": 100,
  "timestamp_utc": "2026-01-11T00:01:23Z",
  
  "metrics_pre": {
    "layer": "L1-CORE",
    "computed_before_U": true,
    "mean_kappa": 0.456,
    "mean_pressure": 1.234,
    "mean_frustration": 0.123,
    "total_weight": 8543.21,
    "n_edges": 8543,
    "n_nodes": 1000
  },
  
  "evolution": {
    "layer": "L1-CORE",
    "spawn_new": 45,
    "spawn_reinf": 23,
    "field_tail_added": 0,
    "removed": 12,
    "norm_ops": 5
  },
  
  "metrics_post": {
    "layer": "L1-CORE",
    "computed_after_U": true,
    "mean_kappa": 0.461,
    "mean_pressure": 1.245,
    "mean_frustration": 0.119,
    "total_weight": 8576.43,
    "n_edges": 8576,
    "n_nodes": 1000
  },
  
  "projection": {
    "layer": "L2-FRACTURE",
    "theta": 0.25,
    "visible_edges": 2341,
    "mean_kappa_visible": 0.678,
    "uses_metrics_post": true
  },
  
  "observables": {
    "layer": "L1-CORE",
    "mean_tension": 0.045,
    "mean_emergent_time": 0.987
  }
}
```

**Critical separations:**

1. **metrics_pre (BEFORE U):**
   - Computed BEFORE spawn/propagate/normalize
   - Used for DECISION (spawn rules)
   - Layer: L1-CORE
   - MUST have: `computed_before_U: true`

2. **evolution (U operations):**
   - Counts of topology changes
   - Layer: L1-CORE
   - All counts >= 0

3. **metrics_post (AFTER U):**
   - Computed AFTER all physics
   - Used for OBSERVATION
   - Layer: L1-CORE
   - MUST have: `computed_after_U: true`

4. **projection (Πθ):**
   - Derived from metrics_post
   - Layer: L2-FRACTURE
   - MUST have: `uses_metrics_post: true`
   - MUST include theta value

5. **observables (emergent):**
   - Accumulated quantities
   - Layer: L1-CORE

**Validation:**
- All 5 sections REQUIRED
- layer fields MUST be present and correct
- Boolean flags (computed_before_U, etc) REQUIRED
- Frustration MUST be present (new in v2.0)
- projection MUST reference metrics_post not metrics_pre

### 2.3 GRAPH (Periodic - configurable)

**Purpose:** Complete graph snapshots

**Required fields:**
```json
{
  "schema_version": "2.0",
  "type": "GRAPH",
  "tick": 100,
  "timestamp_utc": "2026-01-11T00:01:23Z",
  "n_nodes": 1000,
  "n_edges": 8576,
  "edges": [
    [0, 5, 0.234],
    [0, 7, 0.567],
    ...
  ]
}
```

**Validation:**
- edges array length MUST equal n_edges
- Each edge: [u, v, w] with 0 <= u,v < n_nodes, w > 0
- No self-loops: u ≠ v

### 2.4 COMPLETION (Final event)

**Purpose:** Run finalization and status

**Required fields:**
```json
{
  "schema_version": "2.0",
  "type": "COMPLETION",
  "tick": 600,
  "timestamp_utc": "2026-01-11T00:10:00Z",
  "status": "SUCCESS" | "FAILED" | "INTERRUPTED",
  "error": null | "error message",
  "final_n_edges": 7854,
  "final_n_nodes": 1000,
  "duration_seconds": 300.5,
  "freeze_detected": false,
  "freeze_tick": null
}
```

**Validation:**
- status MUST be one of three values
- If status="FAILED", error MUST be non-null
- duration_seconds MUST be positive

---

## 3. Event Ordering Requirements

**Mandatory sequence:**

```
1. METADATA (first event, once)
2. STATE (periodic, every 50 ticks)
3. GRAPH (periodic, configurable)
4. COMPLETION (last event, once)
```

**Validation rules:**
- First event MUST be METADATA
- Last event MUST be COMPLETION
- STATE events MUST have monotonically increasing ticks
- GRAPH events MUST have monotonically increasing ticks
- No events after COMPLETION

---

## 4. Validation Rules (Fail-Closed)

### 4.1 Technical Validation

**File level:**
- MUST be valid JSONL (one JSON object per line)
- MUST be UTF-8 encoded
- MUST have .jsonl extension
- MUST be non-empty

**Schema level:**
- MUST have schema_version in first event
- MUST have METADATA as first event
- MUST have COMPLETION as last event
- MAY have STATE and GRAPH events between

**Field level:**
- All numeric fields MUST be finite (no NaN, no Inf)
- All required fields MUST be present
- All type constraints MUST be satisfied

### 4.2 Semantic Validation (ROMION Methodology)

**Layer separation:**
- metrics_pre MUST have layer="L1-CORE"
- metrics_post MUST have layer="L1-CORE"
- projection MUST have layer="L2-FRACTURE"
- projection MUST NOT affect metrics_pre or metrics_post

**Temporal consistency:**
- metrics_pre computed BEFORE evolution
- metrics_post computed AFTER evolution
- projection uses metrics_post (MUST have flag)

**Physical constraints:**
- All counts (spawn_new, etc) >= 0
- All weights > 0
- All pressures >= 0
- Kappa ∈ [0,1] approximately (sigmoid)

### 4.3 Validation Results

**Validator MUST return one of:**

| Status | Meaning | Action |
|--------|---------|--------|
| VALID | Fully compliant v2.0 | Accept for analysis ✅ |
| LEGACY_V1 | Old format, readable | Accept with warning ⚠️ |
| INVALID_TECH | Technical error | REJECT - fix log ❌ |
| INVALID_SEMANTIC | Methodology violation | REJECT - fix methodology ❌ |
| INCOMPLETE | Missing events | REJECT - rerun ❌ |

---

## 5. Legacy Handling

### 5.1 Version 1.0 Logs (Legacy)

**Characteristics:**
- No schema_version field
- Single metrics section (no pre/post split)
- No frustration metrics
- No layer labels

**Handling:**
```python
def handle_legacy_v1(log_path):
    warnings.warn(
        f"LEGACY LOG: {log_path} uses schema v1.0\n"
        f"- No metrics_pre/post separation\n"
        f"- No frustration data\n"
        f"- Results marked [LEGACY-V1]"
    )
    
    # Read with compatibility mode
    data = read_v1_format(log_path)
    
    # Mark all results
    data['legacy_version'] = '1.0'
    data['analysis_warnings'] = ['LEGACY_V1']
    
    return data
```

**Restrictions:**
- Cannot mix v1 + v2 in aggregation
- v1 results MUST be marked [LEGACY-V1]
- v1 logs acceptable for historical comparison ONLY

### 5.2 Migration from v1 to v2

**NOT automatic** - requires rerun with v2 writer.

**If rerun not possible:**
- Keep v1 logs separate
- Mark analysis [LEGACY-V1]
- Document limitations

**Migration tool** (optional helper):
```bash
python scripts/migrate_log_v1_to_v2.py <v1_log> --output <v2_log>
```

Adds:
- schema_version: "2.0-MIGRATED"
- Synthetic metrics_pre (copy of metrics)
- Synthetic metrics_post (copy of metrics)
- Note: "MIGRATION - metrics_pre/post identical"

**Migrated logs:**
- Still marked as approximate
- Cannot be used for precise pre/post analysis
- Better than nothing, worse than native v2

---

## 6. Enforcement (Tools)

### 6.1 Writer Enforcement (Production)

**sweep_krok6.py (COMPLIANT v2.0):**
- Writes schema_version in METADATA ✅
- Separates metrics_pre/post ✅
- Includes frustration ✅
- Layer labels ✅

**Old runners (NON-COMPLIANT):**
- run_romion_clean.py → produces v1 format ⚠️
- sweep_inprocess.py → produces v1 format ⚠️

**Action:**
- Use sweep_krok6.py for NEW experiments
- Mark old runners as [LEGACY-GENERATOR]
- Update or deprecate old runners

### 6.2 Validator Enforcement

**validate_log_schema.py (NEW):**
```python
from scripts.validate_log_schema import validate_log_schema

result = validate_log_schema("experiments/run1/simulation.jsonl")

if result.status == "VALID":
    # Proceed with analysis
    pass
elif result.status == "LEGACY_V1":
    # Warn and proceed
    warnings.warn(result.message)
else:
    # REJECT
    raise ValueError(f"Invalid log: {result.reason}")
```

**Integration points:**
1. validate_sweep.py → call validate_log_schema()
2. Analysis tools → check schema before processing
3. Aggregation → reject mixed versions

### 6.3 Analysis Enforcement

**All analysis tools MUST:**
1. Check schema_version FIRST
2. Reject unknown versions
3. Warn on legacy
4. Verify layer separation (if v2.0)

**Example:**
```python
def load_simulation_log(path):
    # Validate schema
    result = validate_log_schema(path)
    
    if result.status == "INVALID_TECH":
        raise ValueError(f"Invalid log: {result.reason}")
    
    if result.status == "LEGACY_V1":
        warnings.warn("Using legacy v1.0 log - limited features")
    
    # Load based on version
    if result.version == "2.0":
        return load_v2(path)
    elif result.version == "1.0":
        return load_v1_compat(path)
    else:
        raise ValueError(f"Unsupported version: {result.version}")
```

---

## 7. Contract Guarantees

### 7.1 What This Contract Guarantees

**For compliant v2.0 logs:**
1. ✅ **Reproducibility:**
   - seed + config_hash → exact reproduction
   - git_commit → code state
   
2. ✅ **Layer separation:**
   - metrics_pre ≠ metrics_post (temporal)
   - CORE (L1) ≠ FRACTURE (L2) (ontological)
   
3. ✅ **Completeness:**
   - All required metrics present
   - Frustration included
   - Evolution events tracked
   
4. ✅ **Validity:**
   - Technical constraints enforced
   - Semantic constraints enforced
   - No silent corruption

### 7.2 What This Contract Does NOT Guarantee

**Even with valid v2.0 logs:**
- ❌ Scientific correctness (hypothesis may be wrong)
- ❌ Parameter optimality (may be suboptimal)
- ❌ Numerical accuracy (finite precision)
- ❌ Theory validity (ROMION may be incomplete)

**Contract covers:**
- Format ✅
- Completeness ✅
- Reproducibility ✅

**Contract does NOT cover:**
- Interpretation ❌
- Validity of results ❌
- Physical meaning ❌

---

## 8. Violation Handling

### 8.1 Technical Violations

**Missing schema_version:**
```
ERROR: Missing schema_version in log
File: experiments/run1/simulation.jsonl
Action: Mark as LEGACY_V1 or REJECT
Reason: Cannot determine format version
```

**Wrong version:**
```
ERROR: Unsupported schema_version: "1.5"
File: experiments/run2/simulation.jsonl
Action: REJECT
Reason: Unknown schema version
```

**Missing required field:**
```
ERROR: Missing required field 'metrics_post'
File: experiments/run3/simulation.jsonl
Event: STATE at tick 100
Action: REJECT as INVALID_TECH
Reason: Incomplete STATE event
```

### 8.2 Semantic Violations

**Layer confusion:**
```
ERROR: Projection uses metrics_pre instead of metrics_post
File: experiments/run4/simulation.jsonl
Event: STATE at tick 100
Action: REJECT as INVALID_SEMANTIC
Reason: Layer separation violated
```

**Missing frustration:**
```
ERROR: metrics_post missing 'mean_frustration'
File: experiments/run5/simulation.jsonl
Event: STATE at tick 100
Action: REJECT as INVALID_SEMANTIC
Reason: Required metric missing (v2.0)
```

### 8.3 Recovery Procedures

**If log is INVALID:**
1. Check if rerun possible
2. If yes → rerun with compliant writer
3. If no → mark as [LEGACY/INVALID], exclude from publication

**If log is LEGACY_V1:**
1. Check if rerun possible
2. If yes → rerun recommended
3. If no → use with warnings, mark results [LEGACY-V1]

**If log is INCOMPLETE:**
1. Always rerun
2. No partial analysis on incomplete logs
3. REJECT all incomplete runs

---

## 9. Extension Mechanism

### 9.1 Adding New Fields

**Permitted:**
- Additional fields in METADATA (experiment-specific)
- Additional metrics in metrics_pre/post (derived quantities)
- Additional observables

**Requirements:**
- Do NOT remove required fields
- Do NOT change required field semantics
- Do NOT break existing validators

**Example (permitted extension):**
```json
{
  "schema_version": "2.0",
  "type": "STATE",
  ...
  "metrics_post": {
    "mean_kappa": 0.461,
    "mean_pressure": 1.245,
    "mean_frustration": 0.119,
    "custom_metric_xyz": 0.789  // OK - additional metric
  },
  "custom_section": {  // OK - additional section
    "experiment_specific_data": ...
  }
}
```

### 9.2 Future Schema Versions

**When to create v3.0:**
- Breaking changes to required fields
- Incompatible semantic changes
- Major structural reorganization

**How to introduce v3.0:**
1. Create CANONICAL_LOG_CONTRACT_V3.md
2. Implement validators for v3.0
3. Support v2.0 as LEGACY
4. Migrate logs or keep separate

**Versioning rules:**
- Major version (2.0 → 3.0): Breaking changes
- Minor version (2.0 → 2.1): Backward-compatible additions
- Patch version (2.0.0 → 2.0.1): Clarifications only

---

## 10. Checklist for Compliance

### 10.1 For Writers (Production Code)

- [ ] Writes schema_version: "2.0" in METADATA
- [ ] Computes metrics_pre BEFORE U
- [ ] Computes metrics_post AFTER U
- [ ] Includes frustration in both
- [ ] Projection uses metrics_post
- [ ] Layer labels present and correct
- [ ] All required fields present
- [ ] COMPLETION event at end

### 10.2 For Validators

- [ ] Checks schema_version first
- [ ] Rejects unknown versions
- [ ] Warns on LEGACY_V1
- [ ] Validates all required fields
- [ ] Checks layer separation
- [ ] Validates temporal consistency
- [ ] Returns clear status (VALID/LEGACY/INVALID)

### 10.3 For Analysis Tools

- [ ] Validates log before processing
- [ ] Rejects invalid logs
- [ ] Warns on legacy logs
- [ ] Does NOT mix versions
- [ ] Marks results with schema version
- [ ] Documents limitations if legacy

---

## 11. Authority and Updates

### 11.1 Authority

**This document is the SINGLE SOURCE OF TRUTH for ROMION log format.**

**Hierarchy:**
1. This document (CANONICAL_LOG_CONTRACT.md)
2. Implementation (validate_log_schema.py)
3. Examples (docs/examples/)

**In case of conflict:**
- This document wins
- Implementation MUST be updated to match
- Examples are illustrative only

### 11.2 Update Process

**This document can be updated ONLY for:**
1. Clarifications (no semantic change)
2. Bug fixes in validation rules
3. Addition of optional fields
4. Creation of new major version

**Approval required:**
- Principal investigator
- Lead developer
- Documentation review

**History:**
- v2.0 (2026-01-11): Initial authoritative contract
  - Replaces ad-hoc LOG_SCHEMA_V2.md
  - Adds enforcement rules
  - Locks KROK 2

---

## 12. Migration Timeline

### 12.1 Immediate (2026-01-11)

- [ ] This document becomes authoritative
- [ ] validate_log_schema.py implemented
- [ ] sweep_krok6.py verified compliant

### 12.2 Week 1 (2026-01-18)

- [ ] All new experiments use v2.0
- [ ] Analysis tools enforce validation
- [ ] Legacy v1 marked clearly

### 12.3 Month 1 (2026-02-11)

- [ ] Old runners deprecated or updated
- [ ] All active work uses v2.0
- [ ] v1 logs archived with [LEGACY] tags

### 12.4 Month 3 (2026-04-11)

- [ ] v1 support deprecated (read-only warnings)
- [ ] All publication-quality work is v2.0
- [ ] Migration guide for historical data

---

## 13. FAQ

### Q1: Can I still use old logs?
**A:** Yes, with warnings. Mark results [LEGACY-V1].

### Q2: Must I rerun all experiments?
**A:** For new work, yes. For historical comparison, no (but mark legacy).

### Q3: What if my log is missing one field?
**A:** REJECT as INVALID. Fix the writer and rerun.

### Q4: Can I add custom fields?
**A:** Yes, as extensions. Do not remove/change required fields.

### Q5: How do I migrate v1 to v2?
**A:** Prefer rerun. If impossible, use migration tool (lossy).

### Q6: What if validator fails on valid log?
**A:** Bug in validator. Fix validator to match this contract.

### Q7: Can I create v2.1 with optional additions?
**A:** Yes. Do not break v2.0 validators.

### Q8: When to create v3.0?
**A:** Only for breaking changes. Avoid if possible.

---

## 14. Summary

**This contract ensures:**
- ✅ Every log is self-validating
- ✅ Every log is reproducible
- ✅ Every log separates CORE/FRACTURE
- ✅ Every log includes all required metrics
- ✅ Invalid logs are REJECTED not analyzed

**This closes KROK 2: Kontrakt logów**

**Next:** CANONICAL_METRICS.md (closes KROK 3)

---

**Status:** AUTHORITATIVE  
**Version:** 2.0  
**Date:** 2026-01-11  
**Enforcement:** MANDATORY

**This document is the LAW for ROMION log format.**
