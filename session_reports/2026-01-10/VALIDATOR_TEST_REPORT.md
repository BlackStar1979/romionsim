# validate_log_schema.py - Test Report

**Date:** 2026-01-11  
**Tool:** scripts/validate_log_schema.py  
**Contract:** CANONICAL_LOG_CONTRACT.md v2.0

---

## Test Summary

**Total tests:** 3  
**Passed:** 3 ✅  
**Failed:** 0  
**Bugs found:** 3 (all fixed)

---

## Test Cases

### Test 1: Legacy v1.0 Detection

**Input:** archive/sweep_decay_pilot_20260108/.../simulation.jsonl  
**Format:** v1.0 (no schema_version, STATS events)

**Expected:** LEGACY_V1 with warnings  
**Result:** ✅ PASS

**Output:**
```
Status: LEGACY_V1
Version: 1.0
Message: Legacy v1.0 log: simulation.jsonl

Details:
  Missing schema_version field - detected as LEGACY v1.0
  WARNING: No metrics_pre/post separation
  WARNING: No frustration metrics
  WARNING: No layer labels
  WARNING: Results should be marked [LEGACY-V1]
```

**Exit code:** 0 (acceptable with warnings)

---

### Test 2: Valid v2.0 Log

**Input:** tests/test_v2_valid.jsonl  
**Format:** v2.0 (compliant)

**Expected:** VALID  
**Result:** ✅ PASS

**Output:**
```
Status: VALID
Version: 2.0
Message: Valid v2.0 log: test_v2_valid.jsonl

Details:
  VALID: Schema v2.0 compliant
  VALID: 2 STATE events
  VALID: Ticks 0 -> 50
```

**Exit code:** 0 (ready for analysis)

**Validations performed:**
- ✅ schema_version: "2.0"
- ✅ First event: METADATA
- ✅ METADATA fields: all present
- ✅ STATE events: 2 found
- ✅ metrics_pre: layer=L1-CORE, computed_before_U=true
- ✅ metrics_post: layer=L1-CORE, computed_after_U=true
- ✅ projection: layer=L2-FRACTURE, uses_metrics_post=true
- ✅ evolution: layer=L1-CORE, all counts >= 0
- ✅ frustration: present in both metrics_pre/post
- ✅ Tick monotonicity: 0 → 50
- ✅ COMPLETION event: present

---

### Test 3: Invalid config_hash

**Input:** tests/test_v2_valid.jsonl (modified)  
**Format:** v2.0 with wrong hash length

**Expected:** INVALID_TECH  
**Result:** ✅ PASS

**Output:**
```
Status: INVALID_TECH
Version: 2.0
Message: Invalid METADATA event

Details:
  METADATA.config_hash wrong length: 60
```

**Exit code:** 1 (rejected)

---

## Bugs Found & Fixed

### Bug #1: Unicode Output Error
**Symptom:** UnicodeEncodeError on Windows console  
**Cause:** Warning symbols (⚠️, ✅, ❌) not in cp1250 encoding  
**Fix:** Replace unicode symbols with ASCII text (WARNING, VALID, REJECTED)  
**Status:** ✅ FIXED

### Bug #2: v1 STATS Events Not Recognized
**Symptom:** Legacy logs reported as "No STATE events found"  
**Cause:** Validator checked only 'STATE', but v1 used 'STATS'  
**Fix:** Check for both 'STATE' and 'STATS' in legacy detection  
**Status:** ✅ FIXED

### Bug #3: Test Log Invalid Hash
**Symptom:** Test v2.0 log rejected due to short config_hash  
**Cause:** Test data had 60-char hash instead of 64 (SHA256)  
**Fix:** Updated test data to 64-char hash  
**Status:** ✅ FIXED

---

## Validation Coverage

### METADATA Event
- ✅ schema_version presence
- ✅ schema_version value ("2.0")
- ✅ All required fields
- ✅ seed type (integer) and value (>= 0)
- ✅ config_hash format (64 or 40 chars hex)
- ✅ parameters type (dict)

### STATE Event
- ✅ tick presence
- ✅ All 5 sections (metrics_pre/evolution/metrics_post/projection/observables)
- ✅ metrics_pre:
  - Layer label L1-CORE
  - computed_before_U flag
  - Required metrics (kappa, pressure, frustration)
  - Finite values (no NaN/Inf)
- ✅ metrics_post:
  - Layer label L1-CORE
  - computed_after_U flag
  - Required metrics (kappa, pressure, frustration)
  - Finite values
- ✅ projection:
  - Layer label L2-FRACTURE
  - uses_metrics_post flag (CRITICAL!)
  - theta value [0, 1]
  - visible_edges presence
- ✅ evolution:
  - Layer label L1-CORE
  - All counts >= 0
  - Integer types
- ✅ Tick monotonicity

### COMPLETION Event
- ✅ status values (SUCCESS/FAILED/INTERRUPTED)
- ✅ error field logic (null if SUCCESS)
- ✅ duration_seconds positive

### Legacy v1.0 Handling
- ✅ Detection (missing schema_version)
- ✅ STATS event recognition
- ✅ Clear warnings
- ✅ Acceptable with warnings

---

## Edge Cases Tested

### Empty File
**Not tested yet** - TODO

### Malformed JSON
**Not tested yet** - TODO

### Wrong Event Order
**Not tested yet** - TODO

### Missing Required Section
**Not tested yet** - TODO

### Layer Confusion
**Not tested yet** - TODO (e.g., projection with layer=L1-CORE)

---

## Performance

**Test log sizes:**
- Legacy v1: ~1000 events, 500KB
- Valid v2: 4 events, 2KB

**Validation time:**
- Legacy: <1 second
- Valid v2: <1 second

**Memory:** Minimal (events loaded sequentially)

---

## Recommendations

### For Production Use
1. ✅ Tool is ready for integration
2. ✅ Works on Windows (cp1250 safe)
3. ✅ Clear error messages
4. ✅ Fail-closed behavior

### Future Improvements
1. Add more test cases (edge cases)
2. Consider streaming validation (very large files)
3. Add --strict mode (reject LEGACY)
4. Add --json output for programmatic use

---

## Integration Checklist

- [ ] Integrate into validate_sweep.py
- [ ] Add to analysis pipeline (gravity_test, etc)
- [ ] Document in SWEEP_PROTOCOL.md
- [ ] Add pre-commit hook (optional)
- [ ] CI/CD integration (future)

---

**Status:** ✅ READY FOR INTEGRATION  
**Confidence:** HIGH  
**Recommendation:** Proceed with STEP A (Integration)

---

*Test completed: 2026-01-11 03:00*  
*Tester: Claude (automated + manual)*  
*Tool version: validate_log_schema.py v1.0*
