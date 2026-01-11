# Measurement Thresholds in ROMION O'LOGIC™

**Canonical specification for the three ontological thresholds**

**Version:** 2.0  
**Date:** 2026-01-09  
**Status:** SEMANTIC REFACTOR - Layer-Aware Thresholds

---

## Ontological Foundation

### From THEORY.md v2.0

**CRITICAL PRINCIPLE:**
> ROMION O'LOGIC™ treats CORE dynamics as ontologically primary.  
> All projections, clusters, fields and observables are epistemic.

**This document specifies:**
- How LAYER 2 (FRACTURE/Projection) parameters work
- Why they are THREE DISTINCT ONTOLOGICAL ENTITIES
- How to prevent backreaction into LAYER 1 (CORE)

---

## The Three Ontological Layers (Quick Reference)

**LAYER 1: CORE** (What exists)
- Hypergraph H, evolution U
- Intrinsic properties: κ, P, Frust
- Independent of observation

**LAYER 2: FRACTURE** (What we observe)
- Projection Πθ
- Thresholds: wcluster, wdist, wbridge
- Observation-dependent

**LAYER 3: INTERPRETATION** (How we describe)
- "Clusters" = matter-like
- "Bridges" = field-like
- Language only, NOT entities

---

## The Three Projection Thresholds (LAYER 2)

These are **observation parameters**, NOT dynamics parameters.

### 1. Matter-Like Threshold — `wcluster` (θ_C)

**Ontological role:** Determines which CORE relations project as "matter-like" structures.

**Layer:** L2 (FRACTURE - projection parameter)

**Definition:** Edges with weight ≥ `wcluster` define intra-cluster connectivity in projection.

**Physical interpretation (L3):** "Matter" — regions where relations project as dense and stable.

**Typical value:** Higher than `wdist` (matter-like structures are "harder" than background).

**CRITICAL:** Changing wcluster changes WHAT YOU SEE, NOT what EXISTS in CORE.

**Correct language:**
- ✅ "Clusters observed at wcluster=0.02"
- ❌ "Objects exist with threshold 0.02"
- ✅ "Matter-like structures visible"
- ❌ "Matter has formed"

---

### 2. Background Geometry Threshold — `wdist` (θ_D)

**Ontological role:** Determines which CORE relations project as "background metric fabric".

**Layer:** L2 (FRACTURE - projection parameter)

**Definition:** Edges with weight ≥ `wdist` define the background meta-graph for distance calculation.

**Physical interpretation (L3):** "Spacetime geometry" — the projected relational structure for metric computation.

**Typical value:** Lower than `wcluster`, ensures connected projection with meaningful distances.

**CRITICAL:** This defines the OBSERVATION SPACE for distances, NOT the CORE geometry.

**Correct language:**
- ✅ "Background graph constructed at wdist=0.005"
- ❌ "Spacetime has metric with threshold 0.005"
- ✅ "Projected metric structure"
- ❌ "The geometry is defined by wdist"

---

### 3. Field-Like Threshold — `wbridge` (θ_B)

**Ontological role:** Determines which CORE relations project as "field-like" connections.

**Layer:** L2 (FRACTURE - projection parameter)

**Definition:** Edges with weight ≥ `wbridge` crossing cluster boundaries are counted as bridges in projection.

**Physical interpretation (L3):** "Field" — anomalous connections detected against background.

**Typical value:** Often > `wdist` for selective detection; `wbridge=0.0` is debug mode (all edges visible).

**CRITICAL:** This is DETECTION threshold in projection, NOT a CORE mechanism.

**Correct language:**
- ✅ "Bridge-like edges detected at wbridge=0.0"
- ❌ "Field exists with threshold 0.0"
- ✅ "Field-consistent topology observed"
- ❌ "The system has a field"

---

## Threshold Relations (Fail-Closed)

These relations are REQUIRED for valid projection:

```
wcluster >= wdist > 0
wbridge <= wcluster
```

**Violations = INVALID run** (not "unusual").

**Reason:** 
- If wcluster < wdist: matter threshold below background (ontologically inconsistent)
- If wbridge > wcluster: field threshold above matter (field "harder" than matter - invalid)
- If wdist <= 0: negative/zero geometry (meaningless projection)

**Ontological note:** These are projection-space consistency rules (L2), NOT CORE constraints (L1).

---

## The Two Meta-Graphs (LAYER 2 Constructs)

Both are **projection-space artifacts**, NOT CORE entities.

### `meta_bg` (Background Graph) [L2]

- **Built from:** CORE edges with weight ≥ `wdist`, projected to cluster space
- **Nodes:** Clusters (from `wcluster` clustering)
- **Edges:** Exist if any CORE edge connects cluster A to cluster B above wdist
- **Purpose:** Compute distances D_bg(A,B) = shortest_path(meta_bg, A, B) IN PROJECTION

**Ontological status:** Derived structure in FRACTURE, NOT primary geometry.

### `meta_bridge` (Bridge Graph) [L2]

- **Built from:** CORE edges with weight ≥ `wbridge`, projected to cluster space
- **Nodes:** Same clusters (from wcluster)
- **Edges:** Aggregated bridge statistics (count, weight_sum)
- **Purpose:** Detect field-like anomalies in projection

**Ontological status:** Detection artifact in FRACTURE, NOT field entity in CORE.

---

## Critical Rule: Distance Computation

> **Distances are ALWAYS computed on `meta_bg` (wdist), NEVER on `meta_bridge` (wbridge).**

**Why:**
- Bridges by definition give distance=1 (tautology)
- Pairs without bridges often have distance=∞ (artifact)
- Detection becomes circular

**Ontological reason:** 
- `meta_bg` is MEASUREMENT SPACE (how we compute metric)
- `meta_bridge` is DETECTION SPACE (what we look for)
- Mixing them conflates observation with observed

**Violation = methodological error**, even if code "works".

---

## Implementation Pipeline (Layer-Aware)

```
CORE (L1):
  H = hypergraph with κ, P, Frust

PROJECTION (L2):
  1. clusters = build_clusters(H, wcluster)  [L2: visibility filter]
  2. meta_bg = build_meta_bg(H, clusters, wdist)  [L2: metric space]
  3. dists = all_pairs_shortest(meta_bg)  [L2: distances in projection]
  4. bridges = build_bridges(H, clusters, wbridge)  [L2: field detection]

REPORT (L2):
  5. report(clusters, meta_bg_stats, dist_stats, bridges, thresholds)

INTERPRETATION (L3):
  6. "X clusters observed" (matter-like)
  7. "Y bridges detected" (field-like)
  8. "Range = Z" (metric structure)
```

**Each step operates in LAYER 2 (projection space).** 

**NO feedback to LAYER 1 (CORE).**

---

## Fail-Closed Policy (L2 Validation)

### Invalid Runs (Excluded)
- Threshold relations violated
- NaN/Inf in metrics
- Bounds violations

### Frozen Runs (Excluded from field tests)
- bridges=0 at target tick
- System inactive in projection

### Degenerate Runs (Flagged, not excluded)
- meta_bg disconnected (range=∞ valid)
- No bridges (valid if testing freeze)

**Ontological note:** "Invalid" means projection procedure failed (L2), NOT that CORE is invalid (L1 always exists).

---

## Diagnostic Warnings

### `wbridge=0.0` (Debug Mode)
```
NOTE: wbridge=0.0 => bridges include all positive edges (debug mode)
Field detection disabled - all inter-cluster edges count as bridges
```

**Ontological note:** Debug mode makes ALL CORE edges visible as bridges (L2 artifact).

### Background Too Dense
```
WARNING: meta_bg density > X => consider raising wdist
Range=1 for all bridges suggests wdist too low
```

**Ontological note:** This is projection quality issue (L2), not CORE problem (L1).

### Threshold Order Violation
```
ERROR: wcluster < wdist (invalid projection)
Matter threshold cannot be below background threshold
```

**Ontological note:** L2 consistency violated, projection unreliable.

---

## Common Errors to Avoid

### Error 1: Treating Thresholds as CORE Parameters

**WRONG:**
- "Changing wcluster affects system evolution"
- "wbridge controls field strength"

**CORRECT:**
- "Changing wcluster affects what we observe as clusters"
- "wbridge controls field detection sensitivity"

**Reason:** Thresholds are L2 (observation), NOT L1 (dynamics).

---

### Error 2: Computing Distances on Bridge Graph

**WRONG:**
```python
dists = shortest_path(meta_bridge)  # NEVER DO THIS
```

**CORRECT:**
```python
dists = shortest_path(meta_bg)
```

**Reason:** meta_bridge is detection space, NOT metric space.

---

### Error 3: Conflating Detection with Existence

**WRONG:**
- "No bridges means no field"
- "More clusters means more matter"

**CORRECT:**
- "No bridges detected at wbridge=X"
- "More clusters observed at wcluster=Y"

**Reason:** Detection is L2 (projection-dependent), existence is L1 (threshold-independent).

---

### Error 4: Mixing θ (projection) with spawn_threshold (dynamics)

**WRONG:**
- "theta affects spawning"
- "spawn_threshold affects visibility"

**CORRECT:**
- "theta affects what edges are visible" [L2]
- "spawn_threshold affects what edges are created" [L1]

**Reason:** theta is FRACTURE (L2), spawn_threshold is CORE (L1). They are different ontological layers.

---

## Summary Table

| Threshold | Entity Interpretation (L3) | Meta-graph (L2) | Layer | Used for |
|-----------|---------------------------|-----------------|-------|----------|
| `wcluster` (θ_C) | Matter-like structures | - | L2-FRACTURE | Clustering in projection |
| `wdist` (θ_D) | Background geometry | `meta_bg` | L2-FRACTURE | Distance computation |
| `wbridge` (θ_B) | Field-like connections | `meta_bridge` | L2-FRACTURE | Bridge detection |
| `theta` (θ) | Visibility cutoff | - | L2-FRACTURE | Projection operator Πθ |
| `spawn_threshold` | Spawn filter | - | L1-CORE | Dynamics rule |

**CRITICAL:** First four are L2 (projection), last one is L1 (CORE). Never mix.

---

## Ontological Checklist

When using thresholds, verify:

- [ ] All thresholds labeled as L2-FRACTURE parameters
- [ ] No language suggesting thresholds affect CORE
- [ ] Distances computed on meta_bg (wdist), NOT meta_bridge
- [ ] Threshold relations satisfied (wcluster >= wdist, wbridge <= wcluster)
- [ ] spawn_threshold vs theta distinction maintained
- [ ] "Observed/detected/visible" language used (not "exists/has/is")
- [ ] Fail-closed validation includes threshold checks

---

**See also:**
- `docs/THEORY.md` v2.0 — Ontological foundations
- `docs/METHODOLOGY.md` v2.0 — Layer-aware metrics
- `docs/COMMANDS.md` — CLI reference
- `analysis/gravity_test/` — Implementation

---

**Status:** SEMANTIC REFACTOR COMPLETE  
**Version:** 2.0 - Layer-aware thresholds  
**Authority:** THEORY.md v2.0 ontological framework
