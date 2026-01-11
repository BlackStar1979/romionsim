# ROMION O'LOGIC™ Log Schema v2

**Canonical specification for simulation logs**

**Version:** 2.0  
**Date:** 2026-01-09  
**Status:** ONTOLOGICAL CONTRACT - Layer-Separated Logging

---

## Ontological Foundation

### From THEORY.md v2.0

> **ROMION O'LOGIC™ treats CORE dynamics as ontologically primary.**  
> **All projections are epistemic and must never be fed back into CORE.**

**This schema enforces:**
- Separation of CORE metrics (L1) from PROJECTION metrics (L2)
- Distinction between decision-time and observation-time states
- No backreaction from projection to dynamics

---

## Schema Version Evolution

| Version | Date | Key Change |
|---------|------|------------|
| v1 (implicit) | 2025 | Single metrics blob, no pre/post |
| **v2** | **2026-01-09** | **metrics_pre/post/projection split** |

**Migration:** v1 logs are incompatible with v2 analysis tools.

---

## Core Principles

### 1. Three-Phase Tick

Every tick has THREE distinct phases:

```
DECISION (metrics_pre):
  └─ CORE state BEFORE evolution
  └─ Used BY spawn/decay/normalize
  └─ Layer: L1-CORE

EVOLUTION (U operator):
  └─ spawn → s2/field → propagate → normalize
  └─ Layer: L1-CORE

OBSERVATION (metrics_post + projection):
  └─ CORE state AFTER evolution
  └─ Projection Πθ applied
  └─ Layers: L1-CORE (post) + L2-FRACTURE (projection)
```

**CRITICAL:** Decision metrics ≠ Observation metrics

### 2. No Backreaction

**Forbidden:**
- Using projection results in spawn/decay
- Feeding visible_edges back to CORE
- θ affecting evolution (only affects observation)

**Enforced by:** Temporal separation (pre → U → post/projection)

---

## Tick Event Schema (v2)

### Required Structure

```json
{
  "event": "TICK",
  "schema_version": "v2",
  "tick": <int>,
  
  "metadata": {
    "seed": <int>,
    "config_hash": "<sha256>",
    "timestamp_utc": "<ISO 8601>"
  },
  
  "metrics_pre": { ... },
  "metrics_post": { ... },
  "projection": { ... },
  
  "events": [ ... ]  // Optional: spawn/decay/field events
}
```

### Metadata (Required)

**Purpose:** Run identification and reproducibility

```json
"metadata": {
  "seed": 42,
  "config_hash": "a3f5e9...",  // SHA256 of full config
  "timestamp_utc": "2026-01-09T20:30:00Z",
  "schema_version": "v2"
}
```

**Validation:**
- seed ≥ 0
- config_hash length = 64 (SHA256)
- schema_version = "v2"

---

## metrics_pre (LAYER 1: CORE Decision State)

**Ontological status:** CORE properties BEFORE evolution U

**Purpose:** State used BY spawn/decay rules (decision-time)

### Required Fields

```json
"metrics_pre": {
  // CORE properties (L1)
  "n_nodes": <int>,           // Node count
  "n_edges": <int>,           // Edge count (all)
  "mean_kappa": <float>,      // Mean coherence κ
  "mean_pressure": <float>,   // Mean pressure P
  "mean_weight": <float>,     // Mean edge weight
  "max_pressure": <float>,    // Max pressure (horizon check)
  
  // Aggregates
  "total_tension": <float>,   // Σ tension (accumulated)
  "edges_at_horizon": <int>,  // Edges at W_max (clamped)
  
  // Optional: Frustration (if computed)
  "mean_frustration": <float>,  // Mean Frust
  "max_frustration": <float>    // Max Frust
}
```

**Bounds:**
- All counts ≥ 0
- All means finite
- mean_pressure ≤ max_pressure

**Layer:** L1-CORE (intrinsic, observer-independent)

---

## metrics_post (LAYER 1: CORE Observable State)

**Ontological status:** CORE properties AFTER evolution U

**Purpose:** State OBSERVED after dynamics (post-evolution)

### Required Fields

```json
"metrics_post": {
  // CORE properties (L1) - same structure as pre
  "n_nodes": <int>,
  "n_edges": <int>,
  "mean_kappa": <float>,
  "mean_pressure": <float>,
  "mean_weight": <float>,
  "max_pressure": <float>,
  
  "total_tension": <float>,
  "edges_at_horizon": <int>,
  
  // Horizon dynamics (NEW in v2)
  "horizon_hits": <int>,       // Edges clamped this tick
  "horizon_mass": <float>,     // Energy above W_max (lost)
  
  // Optional
  "mean_frustration": <float>,
  "max_frustration": <float>,
  
  // Emergent time (if enabled)
  "mean_emergent_time": <float>  // Mean dt
}
```

**New fields:**
- `horizon_hits`: Count of edges clamped at W_max
- `horizon_mass`: Σ(w_before - W_max) for clamped edges

**Purpose:** Test "event horizon" interpretation

**Layer:** L1-CORE (intrinsic, post-evolution)

---

## projection (LAYER 2: FRACTURE Observation)

**Ontological status:** EPISTEMOLOGICAL (projection of CORE via Πθ)

**Purpose:** What we OBSERVE (threshold-dependent)

### Required Fields

```json
"projection": {
  // Projection operator parameters (L2)
  "theta": <float>,             // Visibility threshold θ
  
  // Observable counts (L2)
  "visible_edges": <int>,       // Edges with κ ≥ θ
  "invisible_edges": <int>,     // Edges with κ < θ
  "visibility_ratio": <float>,  // visible / total
  
  // Derived topology (L2)
  "visible_components": <int>,  // Connected components @ θ
  "largest_component_size": <int>
}
```

**Bounds:**
- 0 ≤ theta ≤ 1
- visible + invisible = n_edges (from metrics_post)
- 0 ≤ visibility_ratio ≤ 1

**Layer:** L2-FRACTURE (observation, θ-dependent)

**CRITICAL:** This is computed FROM metrics_post.kappa, NOT from metrics_pre

---

## events (Optional: Detailed Event Log)

**Purpose:** Granular tracking of spawn/decay/field events

```json
"events": [
  {
    "type": "SPAWN",
    "count": <int>,
    "total_weight": <float>
  },
  {
    "type": "DECAY",
    "count": <int>,
    "total_weight_lost": <float>
  },
  {
    "type": "FIELD_INJECTION",  // If field-tail active
    "count": <int>,
    "mean_distance": <float>
  },
  {
    "type": "HORIZON_CLAMP",
    "count": <int>,
    "mass_clamped": <float>
  }
]
```

**Layer:** L1-CORE (dynamics tracking)

---

## Run Metadata File (run_meta.json)

**Every simulation must produce:**

```json
{
  "schema_version": "v2",
  "config_hash": "<sha256>",
  "seed": <int>,
  
  "parameters": {
    // CORE parameters (L1)
    "W_max": <float>,
    "decay_scale": <float>,
    "spawn_damping": <float>,
    "spawn_threshold": <float>,
    
    // PROJECTION parameters (L2)
    "theta": <float>,
    
    // Other
    "ticks": <int>,
    "n_nodes_init": <int>
  },
  
  "execution": {
    "start_time": "<ISO 8601>",
    "end_time": "<ISO 8601>",
    "duration_seconds": <float>,
    "exit_status": 0,  // 0=success, 1=error, 2=terminated
    "error_message": null  // or string if failed
  },
  
  "validation": {
    "schema_valid": true,
    "tick_monotonic": true,
    "min_tick": 0,
    "max_tick": <int>,
    "ticks_logged": <int>
  }
}
```

**Purpose:** Complete run identification and validation

---

## Validation Rules

### Schema Compliance

```python
def validate_tick_event_v2(event: dict) -> tuple[bool, list[str]]:
    reasons = []
    
    # Schema version
    if event.get("schema_version") != "v2":
        reasons.append("schema_version must be 'v2'")
    
    # Required sections
    required = ["metadata", "metrics_pre", "metrics_post", "projection"]
    for section in required:
        if section not in event:
            reasons.append(f"Missing required section: {section}")
    
    # Metadata
    meta = event.get("metadata", {})
    if "seed" not in meta or not isinstance(meta["seed"], int):
        reasons.append("metadata.seed required (int)")
    if "config_hash" not in meta:
        reasons.append("metadata.config_hash required")
    
    # metrics_pre/post structure
    for phase in ["metrics_pre", "metrics_post"]:
        m = event.get(phase, {})
        if "mean_kappa" not in m:
            reasons.append(f"{phase}.mean_kappa required")
        if "n_edges" not in m:
            reasons.append(f"{phase}.n_edges required")
    
    # projection
    proj = event.get("projection", {})
    if "theta" not in proj:
        reasons.append("projection.theta required")
    if "visible_edges" not in proj:
        reasons.append("projection.visible_edges required")
    
    # Temporal consistency
    pre_edges = event.get("metrics_pre", {}).get("n_edges", 0)
    post_edges = event.get("metrics_post", {}).get("n_edges", 0)
    vis_edges = event.get("projection", {}).get("visible_edges", 0)
    invis_edges = event.get("projection", {}).get("invisible_edges", 0)
    
    if vis_edges + invis_edges != post_edges:
        reasons.append("projection edge counts don't sum to metrics_post.n_edges")
    
    return (len(reasons) == 0), reasons
```

### Fail-Closed

**Runs are INVALID if:**
- Schema version ≠ "v2"
- Missing required sections
- NaN/Inf in any metric
- Edge count inconsistencies
- Projection computed from metrics_pre (temporal violation)

---

## Layer Separation Enforcement

### Rule 1: Projection Uses Post, Not Pre

**CORRECT:**
```python
# After evolution U
metrics_post = compute_metrics(G)
visible = sum(1 for e in G.edges if e.kappa_cache >= theta)
```

**WRONG:**
```python
# Before evolution U
metrics_pre = compute_metrics(G)
# ... evolution ...
visible = sum(1 for e in G.edges if e.kappa_cache >= theta)  # WRONG! Uses pre-kappa
```

### Rule 2: Decision Uses Pre Only

**CORRECT:**
```python
metrics_pre = compute_metrics(G)
# spawn/decay use metrics_pre.mean_kappa, etc.
spawn(G, metrics_pre)
```

**WRONG:**
```python
proj = compute_projection(G, theta)
spawn(G, proj.visible_edges)  # WRONG! Backreaction
```

### Rule 3: No Threshold Mixing

**CORRECT:**
```python
params_L1 = {"W_max": 2.5, "spawn_threshold": 0.15}  # CORE
params_L2 = {"theta": 0.25, "wcluster": 0.02}  # FRACTURE
```

**WRONG:**
```python
params = {"theta": 0.25, "spawn_threshold": 0.25}  # Conflated!
```

---

## Migration from v1

**v1 logs have:**
- Single `metrics` blob (no pre/post)
- No `projection` section
- No `schema_version`

**Migration strategy:**
- v1 logs are incompatible with v2 tools
- Mark all v1 runs as `[LEGACY]`
- Rerun critical experiments with v2 schema

**DO NOT:**
- Try to "upgrade" v1 → v2 (temporal info lost)
- Mix v1 and v2 in same analysis

---

## Example: Complete Tick Event

```json
{
  "event": "TICK",
  "schema_version": "v2",
  "tick": 100,
  
  "metadata": {
    "seed": 42,
    "config_hash": "a3f5e9d2c1b4a8...",
    "timestamp_utc": "2026-01-09T20:30:00.123Z"
  },
  
  "metrics_pre": {
    "n_nodes": 1000,
    "n_edges": 5234,
    "mean_kappa": 0.42,
    "mean_pressure": 1.85,
    "mean_weight": 0.38,
    "max_pressure": 3.21,
    "total_tension": 124.5,
    "edges_at_horizon": 12
  },
  
  "metrics_post": {
    "n_nodes": 1000,
    "n_edges": 5289,
    "mean_kappa": 0.44,
    "mean_pressure": 1.92,
    "mean_weight": 0.39,
    "max_pressure": 3.15,
    "total_tension": 128.3,
    "edges_at_horizon": 10,
    "horizon_hits": 2,
    "horizon_mass": 0.45
  },
  
  "projection": {
    "theta": 0.25,
    "visible_edges": 3421,
    "invisible_edges": 1868,
    "visibility_ratio": 0.647,
    "visible_components": 23,
    "largest_component_size": 856
  },
  
  "events": [
    {"type": "SPAWN", "count": 87, "total_weight": 12.4},
    {"type": "DECAY", "count": 32, "total_weight_lost": 3.2},
    {"type": "HORIZON_CLAMP", "count": 2, "mass_clamped": 0.45}
  ]
}
```

---

## Implementation Checklist

### core/engine.py Changes

- [ ] Compute metrics_pre before evolution
- [ ] Store in tick_data
- [ ] Compute metrics_post after evolution
- [ ] Compute projection from metrics_post (NOT pre)
- [ ] Add horizon_hits, horizon_mass tracking
- [ ] Write schema_version: "v2" to logs

### analysis/ Tool Updates

- [ ] Reject logs without schema_version
- [ ] Validate v2 structure
- [ ] Use metrics_post for all analysis
- [ ] Never mix pre/post in same metric

### Documentation

- [ ] Update COMMANDS.md with schema info
- [ ] Add migration guide for v1 users
- [ ] Example notebooks with v2 logs

---

## Ontological Guarantees

**This schema guarantees:**

1. **No backreaction:** Projection computed AFTER evolution
2. **Layer separation:** L1 (CORE) ≠ L2 (FRACTURE) explicit
3. **Temporal clarity:** Decision state ≠ Observable state
4. **Reproducibility:** Full metadata + config_hash
5. **Fail-closed:** Invalid logs rejected, not analyzed

**Violations of this schema = methodological error**, not data anomaly.

---

**Status:** CANONICAL SCHEMA v2  
**Authority:** THEORY.md v2.0 + METHODOLOGY.md v2.0  
**Effective:** 2026-01-09  
**Previous:** v1 (implicit, deprecated)

---

**See also:**
- `docs/THEORY.md` — Ontological foundations
- `docs/METHODOLOGY.md` — Layer-aware metrics
- `core/engine.py` — Implementation
