# Experiment: MVP Smoke Test

Status: prerelease experiment  
Purpose: verify that the new engine API can produce a valid run log end-to-end.

---

## Goal

This experiment verifies the minimal pipeline:

- engine API can run for N ticks
- a schema-versioned JSONL log is created
- log contains METADATA, PARAMS, TICK events, and END event
- core and fracture fields are serializable and present in tick records

This experiment does not attempt scientific validation.
It is a technical integrity check.

---

## What This Experiment Is NOT

- not a hypothesis test
- not a physical interpretation
- not an optimization run
- not a performance benchmark

---

## Success Criteria

A run is considered successful if:

- a log file is written under the experiment output directory
- the first line is a METADATA event containing schema_version
- the second line is a PARAMS event containing explicit params
- TICK events exist for the full tick range
- an END event exists and reports ok true

---

## Fail Criteria

The experiment fails if:

- the engine crashes
- the log is missing required events
- parameters are not explicit in the log
- any tick record is not JSON-serializable

---

## Notes

This experiment exists to unlock the transition from documentation-only prerelease
to an implementation-backed prerelease.

End of spec