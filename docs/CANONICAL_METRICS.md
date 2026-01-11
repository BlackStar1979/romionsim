# ROMION Canonical Metrics Definitions

**Version:** 1.0  
**Status:** AUTHORITATIVE - SINGLE SOURCE OF TRUTH  
**Enforcement:** MANDATORY from 2026-01-11  
**Authority:** This document defines the ONLY valid metric definitions for ROMION

---

## ⚠️ FUNDAMENTAL PRINCIPLE

> **Every metric must have:**
> - Unique canonical definition
> - Explicit layer assignment (L1-CORE, L2-FRACTURE, L3-INTERPRETATION)
> - Mathematical formula
> - Valid range and bounds
> - Validation rules
> 
> **Metrics without canonical definition are FORBIDDEN.**
> 
> This contract is NON-NEGOTIABLE.

---

## 1. Metric Categories

ROMION metrics are organized by ontological layer:

### L1-CORE Metrics
**Ontological status:** PRIMARY (what exists)  
**Computed from:** Graph structure Δ(t)  
**Independence:** Do NOT depend on projection Πθ

Examples: κ, pressure, frustration, total_weight

### L2-FRACTURE Metrics  
**Ontological status:** DERIVED (what is observed)  
**Computed from:** Projection Πθ of CORE  
**Dependence:** MUST use metrics_post (after U)

Examples: visible_edges, hub_share, coverage

### L3-INTERPRETATION Metrics
**Ontological status:** INTERPRETIVE (what we infer)  
**Computed from:** Patterns in L2-FRACTURE  
**Purpose:** Scientific hypotheses (e.g., field strength proxy)

Examples: R0, R2, bridge_probability

---

## 2. L1-CORE Metrics (Primary)

### 2.1 mean_kappa

**Definition:** Average coupling strength across all edges

**Formula:**
```
mean_kappa = (1/|E|) × Σ_{e∈E} κ(e)

where κ(e) = sigmoid(w(e) / P(u) + w(e) / P(v))
```

**Layer:** L1-CORE  
**Type:** float  
**Range:** [0, 1] (approximately, sigmoid bounded)  
**Typical values:** 0.1 - 0.8

**Validation:**
- MUST be finite (no NaN, no Inf)
- SHOULD be in [0, 1] (warn if outside)
- IF edges = 0 THEN undefined (reject simulation)

**Implementation:** `core/engine.py::compute_metrics()`

**Used in:**
- Spawn decisions (metrics_pre)
- Projection threshold (compared to theta)
- Analysis (metrics_post)

**Notes:**
- κ is "decision info" - computed BEFORE and AFTER U
- Projection uses κ from metrics_post (CRITICAL)

---

### 2.2 mean_pressure

**Definition:** Average local pressure (weighted degree)

**Formula:**
```
mean_pressure = (1/|V|) × Σ_{v∈V} P(v)

where P(v) = Σ_{e incident to v} w(e)
```

**Layer:** L1-CORE  
**Type:** float  
**Range:** [0, ∞)  
**Typical values:** 0.5 - 5.0

**Validation:**
- MUST be finite
- MUST be >= 0
- IF nodes = 0 THEN undefined (reject simulation)

**Implementation:** `core/engine.py::compute_metrics()`

**Used in:**
- Frustration calculation
- S2-tail proxy (pressure-based)
- Normalize clamp decisions

**Notes:**
- Pressure is fundamental to S1 Closure
- Higher pressure → more likely to spawn

---

### 2.3 mean_frustration

**Definition:** Average edge frustration (deviation from equilibrium)

**Formula:**
```
mean_frustration = (1/|E|) × Σ_{e∈E} Frust(e)

where Frust(e) = |κ(e) - κ_eq|
      κ_eq = spawn_threshold (equilibrium target)
```

**Layer:** L1-CORE  
**Type:** float  
**Range:** [0, 1] (bounded by κ range)  
**Typical values:** 0.05 - 0.3

**Validation:**
- MUST be finite
- MUST be >= 0
- MUST be <= 1
- **NEW in schema v2.0:** REQUIRED (not optional)

**Implementation:** `core/engine.py::compute_frustration()`

**Used in:**
- S2 Antipair theory (not implemented)
- Stability analysis
- System equilibrium detection

**Notes:**
- **CRITICAL:** Required in schema v2.0
- Missing in legacy v1.0 logs
- Fundamental to ROMION theory

---

### 2.4 total_weight

**Definition:** Sum of all edge weights

**Formula:**
```
total_weight = Σ_{e∈E} w(e)
```

**Layer:** L1-CORE  
**Type:** float  
**Range:** [0, ∞)  
**Typical values:** 1000 - 100000

**Validation:**
- MUST be finite
- MUST be >= 0
- IF edges > 0 THEN total_weight > 0

**Implementation:** `core/engine.py::compute_metrics()`

**Used in:**
- Normalization decisions
- System energy proxy
- Evolution tracking

**Notes:**
- Monotonic increase (spawn adds weight)
- Decay reduces weight
- Normalize clamps but doesn't reduce total

---

### 2.5 n_edges

**Definition:** Number of edges in graph

**Formula:**
```
n_edges = |E|
```

**Layer:** L1-CORE  
**Type:** integer  
**Range:** [0, ∞)  
**Typical values:** 5000 - 20000

**Validation:**
- MUST be integer
- MUST be >= 0
- SHOULD be <= theoretical_max (warn if excessive)

**Implementation:** `core/engine.py::compute_metrics()`

**Used in:**
- Averaging (mean_kappa, mean_pressure)
- Density calculations
- Freeze detection

**Notes:**
- Tracks topology evolution
- n_edges = 0 for window ticks → freeze detected

---

### 2.6 n_nodes

**Definition:** Number of nodes in graph

**Formula:**
```
n_nodes = |V|
```

**Layer:** L1-CORE  
**Type:** integer  
**Range:** [0, ∞)  
**Typical values:** 1000 (fixed in MVP)

**Validation:**
- MUST be integer
- MUST be >= 0
- SHOULD be constant (nodes not added/removed in MVP)

**Implementation:** `core/engine.py::compute_metrics()`

**Used in:**
- Averaging (mean_pressure)
- Density normalization
- Sanity checks

**Notes:**
- Fixed at initialization (MVP constraint)
- Future: Dynamic node sets

---

### 2.7 mean_tension

**Definition:** Average accumulated tension (emergent time proxy)

**Formula:**
```
mean_tension = (1/|V|) × Σ_{v∈V} T(v)

where T(v) accumulates based on pressure changes
```

**Layer:** L1-CORE (emergent observable)  
**Type:** float  
**Range:** [0, ∞)  
**Typical values:** 0.0 - 10.0

**Validation:**
- MUST be finite
- MUST be >= 0

**Implementation:** `core/engine.py::compute_emergent_time()`

**Used in:**
- Emergent time calculation
- Warp detection (future)
- Temporal structure analysis

**Notes:**
- Accumulated quantity (not instantaneous)
- Reset behavior: TBD (spec incomplete)

---

### 2.8 mean_emergent_time

**Definition:** System-wide emergent time (τ)

**Formula:**
```
mean_emergent_time = f(tension_history)

Exact formula: See THEORY.md (complex accumulation)
```

**Layer:** L1-CORE (emergent observable)  
**Type:** float  
**Range:** [0, ∞)  
**Typical values:** 0.0 - 100.0

**Validation:**
- MUST be finite
- MUST be >= 0
- SHOULD be monotonic (warn if decreases)

**Implementation:** `core/engine.py::compute_emergent_time()`

**Used in:**
- Temporal structure
- Warp analysis (future)
- Cosmological models (future)

**Notes:**
- Not tick count (emergent != coordinate)
- Theory still under development

---

## 3. L2-FRACTURE Metrics (Derived from Projection)

### 3.1 visible_edges

**Definition:** Number of edges above projection threshold θ

**Formula:**
```
visible_edges = |{e ∈ E : κ(e) >= θ}|

CRITICAL: Uses κ from metrics_post (after U)
```

**Layer:** L2-FRACTURE  
**Type:** integer  
**Range:** [0, n_edges]  
**Typical values:** 1000 - 5000

**Validation:**
- MUST be integer
- MUST be >= 0
- MUST be <= n_edges
- **CRITICAL:** MUST use metrics_post (projection after evolution)

**Implementation:** `core/engine.py` (tick loop)

**Used in:**
- Projection ratio
- Visibility analysis
- Matter clustering proxy

**Dependencies:**
- theta (projection parameter)
- κ from metrics_post (NOT metrics_pre)

**Notes:**
- **Projection depends on post-evolution state**
- Using metrics_pre would violate methodology

---

### 3.2 visible_ratio

**Definition:** Fraction of edges visible under projection

**Formula:**
```
visible_ratio = visible_edges / n_edges
```

**Layer:** L2-FRACTURE  
**Type:** float  
**Range:** [0, 1]  
**Typical values:** 0.1 - 0.5

**Validation:**
- MUST be in [0, 1]
- IF n_edges = 0 THEN undefined

**Implementation:** Derived from visible_edges

**Used in:**
- Projection analysis
- theta calibration studies
- Visibility trends

**Notes:**
- Pure projection metric
- No CORE interpretation

---

### 3.3 mean_kappa_visible

**Definition:** Average κ among visible edges only

**Formula:**
```
mean_kappa_visible = (1/|E_vis|) × Σ_{e∈E_vis} κ(e)

where E_vis = {e ∈ E : κ(e) >= θ}
```

**Layer:** L2-FRACTURE  
**Type:** float  
**Range:** [θ, 1] (bounded by visibility threshold)  
**Typical values:** θ + 0.1 to 0.9

**Validation:**
- MUST be >= θ (by construction)
- MUST be <= 1
- IF visible_edges = 0 THEN undefined

**Implementation:** `core/engine.py` (optional metric)

**Used in:**
- Visible matter strength analysis
- Projection quality checks

**Notes:**
- Conditional mean (selection bias)
- Always >= global mean_kappa

---

## 4. L3-INTERPRETATION Metrics (Analysis)

### 4.1 hub_share

**Definition:** Degree dominance of largest hub in bridge graph

**Formula:**
```
hub_share = (degree_max / Σ_all_degrees) × 100

Computed on: Bridge graph (visible edges between clusters)
```

**Layer:** L3-INTERPRETATION  
**Type:** percentage  
**Range:** [0, 100]  
**Typical values:** 5 - 40

**Validation:**
- MUST be in [0, 100]
- IF total_degree = 0 THEN 0 (no bridges)

**Implementation:** `analysis/gravity_test/metrics.py::compute_hub_share()`

**Used in:**
- Central hub detection
- Hierarchical structure analysis
- Gravitational field hypothesis

**Notes:**
- Interpretation depends on cluster algorithm
- Not a CORE property (analysis artifact)

---

### 4.2 coverage

**Definition:** Fraction of clusters participating in bridges

**Formula:**
```
coverage = (clusters_with_bridge / n_clusters) × 100

where clusters_with_bridge = |{c : ∃ bridge incident to c}|
```

**Layer:** L3-INTERPRETATION  
**Type:** percentage  
**Range:** [0, 100]  
**Typical values:** 20 - 80

**Validation:**
- MUST be in [0, 100]
- IF n_clusters = 0 THEN undefined

**Implementation:** `analysis/gravity_test/metrics.py::compute_coverage()`

**Used in:**
- Network connectivity analysis
- Matter distribution studies
- Field reach hypothesis

**Notes:**
- Depends on clustering parameters (wcluster)
- Not fundamental to CORE

---

### 4.3 R0 (hub dominance ratio)

**Definition:** Ratio of hub_share to coverage

**Formula:**
```
R0 = hub_share / coverage

Interpretation: How concentrated is connectivity?
```

**Layer:** L3-INTERPRETATION  
**Type:** ratio  
**Range:** (0, ∞) (typically 0.1 - 2.0)  
**Typical values:** 0.3 - 1.5

**Validation:**
- MUST be finite
- MUST be > 0
- IF coverage = 0 THEN undefined

**Implementation:** `analysis/gravity_test/metrics.py::compute_R0()`

**Used in:**
- Centralization analysis
- Gravity-like pattern detection
- Hierarchical structure quantification

**Notes:**
- R0 > 1: Hub dominates (concentrated)
- R0 < 1: Distributed connectivity
- Pure interpretation (not CORE)

---

### 4.4 Bridge Distance Metrics (R_d and D_d)

**ROMION SEMANTICS (2026-01-11 Correction):**

There are TWO distinct metrics for analyzing bridge-distance relationships:

#### 4.4.1 R_d — Conditional Bridge Probability (DIAGNOSTIC, "R2-family")

**Definition:** Probability that a cluster pair has a bridge GIVEN distance d

**Formula:**
```
R_d := P(bridge | dist = d)
     = bridged_pairs_at_dist[d] / background_pairs_at_dist[d]

where:
  - bridged_pairs_at_dist[d] = pairs with ≥1 bridge at distance d
  - background_pairs_at_dist[d] = ALL cluster pairs at distance d
```

**Layer:** L3-INTERPRETATION  
**Type:** probability  
**Range:** [0, 1]  
**Typical values:** 0.0 - 1.0 (depends on wbridge)

**Validation:**
- MUST be in [0, 1]
- Denominator requires background distance matrix

**Implementation:** `analysis/gravity_test/distances.py::distance_table()`  
**Field:** `p_bridge_given_dist` (DIAGNOSTIC)

**Used in:**
- Exp 2B: Canonical R2 = R_2 (distance-2 bridge probability)
- Field strength proxy
- Long-range coupling detection

**Notes:**
- R_2 > 0 suggests long-range effects
- R_1 ≈ 1.0 typical (nearest neighbors bridged)
- **DIAGNOSTIC METRIC** — not primary ROMION observable

---

#### 4.4.2 D_d — Bridge Distance Distribution (PRIMARY)

**Definition:** Probability distribution of distances FOR BRIDGED PAIRS

**Formula:**
```
D_d := P(dist = d | bridge)
     = bridged_pairs_at_dist[d] / total_bridged_pairs

where:
  - total_bridged_pairs = Σ_d bridged_pairs_at_dist[d]
```

**Layer:** L3-INTERPRETATION  
**Type:** probability distribution  
**Range:** [0, 1] per distance, Σ_d D_d = 1.0  
**Typical values:** D_1 ≈ 0.8-1.0, D_2 ≈ 0.0-0.2

**Validation:**
- MUST be in [0, 1] for each d
- MUST satisfy Σ_d D_d = 1.0 (normalization)
- IF no bridges THEN undefined

**Implementation:** `analysis/gravity_test/distances.py::distance_table()`  
**Field:** `p_dist_given_bridge` (PRIMARY)

**Used in:**
- Exp 2A: Bridge distance ordering/localization
- Field range analysis (finite vs extended)
- d_max computation (maximum distance with bridges)

**Notes:**
- **PRIMARY ROMION METRIC** for distance structure
- D_d measures field localization on actual bridges
- NOT hypothetical "candidate pairs"

---

#### 4.4.3 Experiment Assignment

**Exp 2A: Distance Ordering (uses D_d)**
- Metric: P(dist | bridge) = D_d
- Question: "Where do bridges localize in background geometry?"
- Pass condition: Clear ordering (e.g., D_1 > D_2 > D_3)

**Exp 2B: Canonical R2 (uses R_d)**
- Metric: P(bridge | dist=2) = R_2
- Question: "Do distant cluster pairs show field coupling?"
- Pass condition: R_2 > baseline (e.g., R_2 > 0.01)

---

#### 4.4.4 Relationship Between Metrics

**Bayes theorem:**
```
R_d = P(bridge | dist=d)
D_d = P(dist=d | bridge)

Related by:
R_d × P(dist=d) = D_d × P(bridge)

where:
  P(dist=d) = background_pairs_at_dist[d] / total_background_pairs
  P(bridge) = total_bridged_pairs / total_background_pairs
```

**Key distinction:**
- R_d: "Given distance, what's bridge probability?" (conditional on geometry)
- D_d: "Given bridge, what's distance distribution?" (conditional on field)

---

#### 4.4.5 Implementation Notes

**In distance_table() output:**
```python
{
    'dist': d,
    'bridged_pairs': int,              # Pairs with bridges
    'p_dist_given_bridge': float,      # D_d (PRIMARY)
    'background_pairs': int,            # All pairs at d
    'p_bridge_given_dist': float,      # R_d (DIAGNOSTIC)
    ...
}
```

**Validation:**
```python
# Check D_d normalization
assert abs(sum(row['p_dist_given_bridge'] for row in rows) - 1.0) < 1e-6

# Check R_d bounds
for row in rows:
    assert 0 <= row['p_bridge_given_dist'] <= 1.0
```

**Reporting:**
- PRIMARY: Report D_d distribution and d_max
- DIAGNOSTIC: Report R_d values if testing field hypothesis
- NEVER: Mix interpretations or claim R_d is "the" metric

---

## 5. Evolution Metrics (Topology Changes)

### 5.1 spawn_new

**Definition:** Number of new edges added by S1 Closure

**Formula:**
```
spawn_new = |{e : e added by spawn, e was not in graph}|
```

**Layer:** L1-CORE (evolution counter)  
**Type:** integer  
**Range:** [0, ∞)  
**Typical values:** 0 - 1500

**Validation:**
- MUST be integer
- MUST be >= 0

**Implementation:** `core/rules.py::rule_spawn()`

**Used in:**
- Topology growth tracking
- Spawn activity monitoring
- Freeze detection

**Notes:**
- Per-tick count (not cumulative)
- spawn_new = 0 for window → possible freeze

---

### 5.2 spawn_reinf

**Definition:** Number of existing edges reinforced by S1 Closure

**Formula:**
```
spawn_reinf = |{e : e reinforced by spawn, e already in graph}|
```

**Layer:** L1-CORE (evolution counter)  
**Type:** integer  
**Range:** [0, ∞)  
**Typical values:** 0 - 800

**Validation:**
- MUST be integer
- MUST be >= 0

**Implementation:** `core/rules.py::rule_spawn()`

**Used in:**
- Reinforcement tracking
- Recurrence detection
- Edge persistence analysis

**Notes:**
- Reinforcement strengthens existing edges
- Part of S1 Closure mechanism

---

### 5.3 field_tail_added

**Definition:** Number of edges added by field-tail proxy (NOT S2!)

**Formula:**
```
field_tail_added = |{e : e added by field_tail rule}|
```

**Layer:** L1-CORE (evolution counter)  
**Type:** integer  
**Range:** [0, ∞)  
**Typical values:** 0 (usually disabled)

**Validation:**
- MUST be integer
- MUST be >= 0

**Implementation:** `core/rules.py::rule_field_tail()`

**Used in:**
- Experimental field proxy tracking
- S2 hypothesis testing (indirect)

**Notes:**
- **CRITICAL:** field_tail ≠ S2 Antipair
- field_tail is MVP proxy, not theory-derived
- Usually disabled (enable_field_tail=false)

---

### 5.4 removed

**Definition:** Number of edges removed by decay

**Formula:**
```
removed = |{e : e removed because w(e) < min_weight}|
```

**Layer:** L1-CORE (evolution counter)  
**Type:** integer  
**Range:** [0, ∞)  
**Typical values:** 0 - 100

**Validation:**
- MUST be integer
- MUST be >= 0

**Implementation:** `core/rules.py::rule_propagate()`

**Used in:**
- Decay activity tracking
- Edge lifetime analysis
- Stability monitoring

**Notes:**
- Decay removes weak edges
- Part of S3 Propagate

---

### 5.5 norm_ops

**Definition:** Number of edges clamped by normalize

**Formula:**
```
norm_ops = |{e : w(e) was clamped to W_max}|
```

**Layer:** L1-CORE (evolution counter)  
**Type:** integer  
**Range:** [0, ∞)  
**Typical values:** 0 - 500

**Validation:**
- MUST be integer
- MUST be >= 0

**Implementation:** `core/rules.py::rule_normalize()`

**Used in:**
- Clamp frequency tracking
- Horizon detection
- Weight distribution analysis

**Notes:**
- High norm_ops → many edges at W_max
- W_max is "event horizon"
- Normalize prevents runaway growth

---

## 6. Validation Rules (Cross-Metric)

### 6.1 Consistency Checks

**Pre/Post Metrics:**
```
IF metrics_post exists THEN:
  - n_nodes_post = n_nodes_pre (nodes don't change in MVP)
  - n_edges_post >= n_edges_pre - removed (edges can grow or shrink)
  - total_weight_post >= 0
```

**Evolution Counts:**
```
Δn_edges = spawn_new - removed
n_edges_post = n_edges_pre + Δn_edges (approximately, ignore reinforcement)
```

**Projection:**
```
visible_edges <= n_edges_post (by construction)
mean_kappa_visible >= theta (by definition)
visible_ratio = visible_edges / n_edges_post
```

### 6.2 Physical Constraints

**Pressure:**
```
mean_pressure >= 0 (always)
IF mean_pressure = 0 THEN n_edges = 0 (no edges → no pressure)
```

**Kappa:**
```
mean_kappa approximately in [0, 1] (sigmoid range)
WARN IF mean_kappa > 1.0 (unusual, check implementation)
```

**Frustration:**
```
mean_frustration >= 0 (by definition |κ - κ_eq|)
mean_frustration <= 1 (bounded by κ range)
```

### 6.3 Bounds Validation

**Percentages:**
```
hub_share in [0, 100]
coverage in [0, 100]
visible_ratio in [0, 1]
```

**Probabilities:**
```
R2 in [0, 1]
All probability metrics in [0, 1]
```

**Counts:**
```
All evolution counts >= 0
spawn_new, spawn_reinf, removed, norm_ops >= 0
```

---

## 7. Layer Separation Rules

### 7.1 L1-CORE Independence

**FORBIDDEN:**
```
L1 metrics MUST NOT depend on:
- theta (projection parameter)
- Clustering parameters (wcluster, wdist, wbridge)
- Analysis parameters
```

**REQUIRED:**
```
L1 metrics depend ONLY on:
- Graph structure Δ(t)
- Evolution operator U
- CORE parameters (spawn_threshold, decay, W_max, etc)
```

### 7.2 L2-FRACTURE Dependence

**REQUIRED:**
```
L2 metrics MUST use:
- theta (projection threshold)
- metrics_post (after U, not metrics_pre)
```

**EXAMPLE:**
```
visible_edges = count(κ >= theta)
where κ from metrics_post (CRITICAL!)
```

### 7.3 L3-INTERPRETATION Constraints

**REQUIRED:**
```
L3 metrics labeled as:
- INTERPRETATION (not CORE truth)
- Dependent on analysis choices
- Hypothesis-testing tools (not ontological)
```

**FORBIDDEN:**
```
Interpreting L3 as L1:
- hub_share is NOT a CORE property
- R0 is NOT fundamental
- R2 is NOT proof of field
```

---

## 8. Metric Usage Guidelines

### 8.1 When to Use metrics_pre

**Use cases:**
- Spawn decisions (S1 Closure input)
- Rule conditionals (before evolution)
- Logging "decision info"

**Example:**
```python
# In spawn rule
metrics = compute_metrics(G)  # metrics_pre
if metrics['mean_kappa'] < spawn_threshold:
    # Spawn logic
```

### 8.2 When to Use metrics_post

**Use cases:**
- Projection (Πθ computation)
- Observation (what we see)
- Analysis (post-evolution state)
- Logging "observable state"

**Example:**
```python
# After U (spawn, propagate, normalize)
metrics_post = compute_metrics(G)  # After all physics
visible = count(e for e in G.edges if e.kappa >= theta)
```

### 8.3 When to Use L3 Metrics

**Use cases:**
- Pattern detection
- Hypothesis testing
- Scientific analysis
- NOT for CORE decisions

**Example:**
```python
# In analysis (not in simulation)
R0 = hub_share / coverage
if R0 > 1.0:
    print("Centralized structure (interpretation)")
```

---

## 9. Deprecated / Forbidden Metrics

### 9.1 Deprecated (Legacy v1.0)

**s2_tail_added:**
- **Replaced by:** field_tail_added
- **Reason:** Naming confusion (s2_tail ≠ S2)
- **Migration:** Rename in analysis

**single metrics section:**
- **Replaced by:** metrics_pre + metrics_post
- **Reason:** No temporal separation
- **Migration:** Use schema v2.0

### 9.2 Forbidden (Never Use)

**Backreaction metrics:**
- Any metric that feeds projection back into CORE
- Example: "visible_edges" as spawn input (FORBIDDEN!)

**Ontologically confused:**
- "Matter density" without layer specification
- "Field strength" without interpretation label
- "Gravity" without L3-INTERPRETATION tag

---

## 10. Canonical Definitions Summary

### L1-CORE (Primary)
| Metric | Formula | Range | Required |
|--------|---------|-------|----------|
| mean_kappa | avg(κ(e)) | [0,1] | YES |
| mean_pressure | avg(P(v)) | [0,∞) | YES |
| mean_frustration | avg(\|κ-κ_eq\|) | [0,1] | YES (v2.0) |
| total_weight | Σw(e) | [0,∞) | YES |
| n_edges | \|E\| | ℕ | YES |
| n_nodes | \|V\| | ℕ | YES |
| mean_tension | avg(T(v)) | [0,∞) | Optional |
| mean_emergent_time | f(tension) | [0,∞) | Optional |

### L2-FRACTURE (Projection)
| Metric | Formula | Range | Dependencies |
|--------|---------|-------|--------------|
| visible_edges | count(κ≥θ) | [0,n_edges] | theta, metrics_post |
| visible_ratio | visible/total | [0,1] | theta, metrics_post |
| mean_kappa_visible | avg(κ\|κ≥θ) | [θ,1] | theta, metrics_post |

### L3-INTERPRETATION (Analysis)
| Metric | Formula | Range | Purpose |
|--------|---------|-------|---------|
| hub_share | max_deg/Σdeg × 100 | [0,100] | Centralization |
| coverage | bridges/clusters × 100 | [0,100] | Connectivity |
| R0 | hub_share/coverage | (0,∞) | Hierarchy |
| R2 | P(bridge\|d=2) | [0,1] | Long-range |

### Evolution (Counters)
| Metric | Meaning | Range |
|--------|---------|-------|
| spawn_new | New edges | ℕ |
| spawn_reinf | Reinforced edges | ℕ |
| field_tail_added | Proxy field edges | ℕ |
| removed | Decayed edges | ℕ |
| norm_ops | Clamped edges | ℕ |

---

## 11. Implementation Reference

**Primary implementation:**
- `core/engine.py::compute_metrics()` - L1-CORE metrics
- `core/engine.py::tick()` - L2-FRACTURE projection
- `analysis/gravity_test/metrics.py` - L3-INTERPRETATION

**Validation:**
- `scripts/validate_log_schema.py` - Schema v2.0 enforcement
- `analysis/gravity_test/validate_romion.py` - Threshold validation
- Future: `scripts/validate_metrics.py` - Canonical enforcement

---

## 12. Authority and Updates

### 12.1 Authority

**This document is the SINGLE SOURCE OF TRUTH for ROMION metric definitions.**

**Hierarchy:**
1. This document (CANONICAL_METRICS.md)
2. Implementation (must conform to this)
3. Legacy docs (historical only)

**In case of conflict:**
- This document wins
- Implementation MUST be updated
- Analysis MUST use these definitions

### 12.2 Update Process

**Allowed updates:**
1. Clarifications (no semantic change)
2. New metrics (with full specification)
3. Deprecation notices (with migration path)
4. Formula corrections (with version bump)

**Approval required:**
- Principal investigator
- Lead developer
- Methodology review

**History:**
- v1.0 (2026-01-11): Initial canonical definitions
  - Consolidates scattered definitions
  - Adds layer labels
  - Locks KROK 3

---

## 13. Validation Checklist

### For Implementations
- [ ] All metrics have canonical definition
- [ ] Layer labels correct (L1/L2/L3)
- [ ] Formulas match this document
- [ ] Bounds validated
- [ ] metrics_pre vs metrics_post correct

### For Analysis
- [ ] Uses canonical definitions
- [ ] Cites this document
- [ ] Layer interpretation correct
- [ ] No backreaction (L2 → L1)
- [ ] L3 metrics labeled as interpretation

### For Logs (Schema v2.0)
- [ ] metrics_pre has all required L1 metrics
- [ ] metrics_post has all required L1 metrics
- [ ] projection uses metrics_post
- [ ] Frustration present (required v2.0)
- [ ] Layer labels present

---

## 14. FAQ

### Q1: What if my analysis needs a new metric?
**A:** Add it to this document first with full specification. Then implement.

### Q2: Can I use metrics_pre for projection?
**A:** NO. Projection MUST use metrics_post. This is CRITICAL for layer separation.

### Q3: Is hub_share a CORE property?
**A:** NO. hub_share is L3-INTERPRETATION. It depends on clustering algorithm.

### Q4: What's the difference between mean_kappa and mean_kappa_visible?
**A:** mean_kappa is L1-CORE (all edges). mean_kappa_visible is L2-FRACTURE (only visible edges).

### Q5: Why is frustration required in v2.0 but not v1.0?
**A:** v2.0 enforces theoretical completeness. Frustration is fundamental to ROMION theory.

### Q6: Can I interpret R2 > 0 as proof of field?
**A:** NO. R2 is L3-INTERPRETATION. It's consistent with field hypothesis, not proof.

### Q7: What if implementation formula differs from this document?
**A:** This document wins. File a bug report and fix implementation.

### Q8: Can I add a metric without updating this document?
**A:** NO. All metrics MUST have canonical definition here first.

---

## 15. Summary

**This contract ensures:**
- ✅ Every metric has unique canonical definition
- ✅ Layer separation enforced
- ✅ No backreaction (L2 → L1 forbidden)
- ✅ Validation rules explicit
- ✅ Single source of truth

**This closes KROK 3: Spójność metryk**

**Next:** Integration with validate_romion.py

---

**Status:** AUTHORITATIVE  
**Version:** 1.0  
**Date:** 2026-01-11  
**Enforcement:** MANDATORY

**This document is the LAW for ROMION metric definitions.**
