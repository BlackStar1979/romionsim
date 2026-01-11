# ROMION O'LOGIC™ Methodology
# Standards for experimental testing and validation

**Version:** 2.1  
**Date:** 2026-01-11  
**Status:** POST-AUDIT - Operational Maturity  
**Authority:** CANONICAL_METRICS.md, CANONICAL_LOG_CONTRACT.md  
**Schema:** v2.0 (MANDATORY)

---

## 0. Fundamental Principle (from THEORY.md)

> **ROMION O'LOGIC™ treats CORE dynamics as ontologically primary.**  
> **All projections, clusters, fields and observables are epistemic and must never be fed back into CORE unless explicitly modeled as a separate physical mechanism.**

**This methodology enforces this principle through:**
- Explicit layer declarations for all metrics
- Fail-closed validation preventing layer violations
- Language standards prohibiting backreaction

---

## 1. Three-Layer Ontology in Practice

### 1.1 Layer Definitions (from THEORY.md)

**LAYER 1: CORE (Ontological)**
- Hypergraph H, evolution U
- Intrinsic properties: κ, P, Frust, Rec
- Independent of observation

**LAYER 2: FRACTURE/PROJECTION (Epistemological)**
- Projection Πθ
- Visible structures (κ ≥ θ)
- Observation-dependent

**LAYER 3: INTERPRETATION (Linguistic)**
- "Clusters", "field", "matter", "gravity"
- Useful comparisons to physics
- NOT imported back to CORE

### 1.2 Metric Layer Assignment

**ALL metrics must declare their ontological layer:**

| Metric | Layer | Ontological Status |
|--------|-------|-------------------|
| κ, P, Frust, Rec | CORE (L1) | Primary, observer-independent |
| visible_edges, clusters | FRACTURE (L2) | Derived via Πθ |
| range, hub_share | FRACTURE (L2) | Topology of projection |
| bridges (field interpretation) | INTERPRETATION (L3) | Language, not entity |

### 1.3 Forbidden Language

**DO NOT say:**
- ❌ "Objects exist" → ✅ "Clusters observed in projection"
- ❌ "Matter formed" → ✅ "Stable structures visible at θ=X"
- ❌ "Field detected" → ✅ "Field-consistent topology"
- ❌ "System has X bridges" → ✅ "X bridge-like edges at θ_bridge"

**Reason:** Layer 3 language can create false intuitions about Layer 1.

---

## 2. Core Principles

### 2.1 Fail-Closed

**Rule:** Invalid metric values invalidate entire run.

**Invalid conditions:**
- NaN or Infinity in any numeric field
- hub_share or coverage outside [0, 100]
- Negative values for unassigned_nodes, channel_capacity, anisotropy
- Missing required thresholds (wcluster, wdist, wbridge) in report
- **NEW:** Threshold relations violated (see 2.2)

**Implementation:** `analysis/gravity_test/validate.py`

**Ontological note:** Validation ensures measurement procedure is Layer-2 compliant, not CORE-corrupting.

### 2.2 Three-Threshold Separation

**CRITICAL:** These are THREE DISTINCT ONTOLOGICAL ENTITIES, not tuning parameters.

| Threshold | Symbol | Purpose | ROMION Layer | Meaning |
|-----------|--------|---------|--------------|---------|
| wcluster | θ_C | Cluster definition | L2 (Projection) | What relations project as "matter-like" |
| wdist | θ_D | Distance geometry | L2 (Projection) | Background for metric computation |
| wbridge | θ_B | Bridge detection | L2 (Projection) | What projects as "field-like" |

**Required relations (fail-closed):**
- `wcluster >= wdist` (typically `wcluster > wdist`)
- `wbridge <= wcluster` (field threshold below matter threshold)
- `wdist > 0` (positive geometry)

**Violation = INVALID run** (not just "unusual").

**Rule:** Every metric must declare which threshold(s) it uses AND its ontological layer.

**Critical distinction from CORE:**
- These thresholds affect WHAT WE SEE (Layer 2)
- They do NOT affect WHAT EXISTS (Layer 1)
- spawn_threshold (CORE, Layer 1) ≠ theta (FRACTURE, Layer 2)

### 2.3 MVP vs SPEC Separation

- **MVP/IMPLEMENTED:** Currently in code with tests
- **PARTIAL:** Implemented as proxy or approximation  
- **SPEC/ROADMAP:** Theoretical only, not implemented

**NEW: Layer labeling:**
- MVP/SPEC items must ALSO declare their ontological layer
- Example: "S2 Antipair [SPEC, L1-CORE]"

---

## 3. Pre-Registration Template

Every test must document before running:

```markdown
## Pre-registration

### Hypotheses (Layer-Explicit)
- H1 [L2]: [What projection pattern you expect]
  - Example: "Bridge count > 0 at tick 400 (L2 observation)"
- H0 [L2]: [Null hypothesis - default pattern]
  - Example: "System freezes (bridges=0) by tick 400"

### Manipulated Variables (declare layer)
- decay_scale [L1-CORE]: [range]
- theta [L2-FRACTURE]: [value]
- wbridge [L2-FRACTURE]: [value]

### Fixed Parameters (declare layer)
- wcluster [L2]: [value]
- wdist [L2]: [value]  
- wbridge [L2]: [value]
- W_max [L1]: [value]
- spawn_threshold [L1]: [value]

### Primary Metrics (layer-explicit)
- bridges_count@400 [L2-FRACTURE, θ_bridge] - tests H1
- hub_share@400 [L2-FRACTURE, θ_bridge] - diagnostic

### Secondary Metrics
- [List supporting/diagnostic metrics with layers]

### Exclusion Criteria (fail-closed)
- [ ] Invalid runs (NaN, bounds, threshold violations)
- [ ] Freeze runs (bridges = 0) - if testing active field
- [ ] [Other criteria]

### Falsification Rule
- H1 is falsified if: [specific, measurable L2 condition]
- Ontological note: This tests projection patterns, not CORE directly
```

---

## 4. Canonical Metrics

### 4.1 Primary Metrics (for ranking)

**All primary metrics are Layer 2 (FRACTURE/Projection).**

| Metric | Definition | Threshold | Layer | Bounds |
|--------|------------|-----------|-------|--------|
| freeze_tick | First tick where bridges=0 for W ticks | wbridge | L2 | ≥0 or null |
| bridges_count@T | Count of projected bridge edges at tick T | wbridge | L2 | ≥0 |
| bridges_weight@T | Sum of projected bridge weights at tick T | wbridge | L2 | ≥0 |
| pairs_with_bridge@T | Cluster pairs with ≥1 visible bridge | wbridge | L2 | ≥0 |
| hub_share@T | Degree dominance: % of total bridge-graph degree held by most-connected cluster | wbridge | L2 | [0,100] |
| coverage@T | Cluster participation: % of clusters with ≥1 bridge connection | wbridge | L2 | [0,100] |

**Ontological notes:**
- **hub_share:** Measures degree centrality (hub_degree / Σ_all_degrees × 100), NOT largest component size
- **coverage:** Measures cluster participation (clusters_with_bridge / n_clusters × 100), NOT pair coverage
- **IMPORTANT:** Previous documentation incorrectly described these as component/pair-based. Corrected 2026-01-09.
- These are PROJECTION METRICS. Changing θ_bridge changes values WITHOUT changing CORE.

### 4.2 Secondary Metrics (for diagnostics)

| Metric | Definition | Threshold | Layer | Bounds |
|--------|------------|-----------|-------|--------|
| range@T | Mean/max shortest path in background graph | wdist | L2 | ≥0 |
| unassigned_nodes@T | Nodes not in any cluster (at θ_C) | wcluster | L2 | ≥0 |
| skipped_edges@T | Edges skipped (unassigned endpoints) | - | L2 | ≥0 |
| channel_capacity@T | Cut-weight between regions | wdist | L2 | ≥0 |
| anisotropy@T | Split-axis capacity variance | wdist | L2 | ≥0 |

**Ontological note:** All are Layer 2 (derived from projection), NOT Layer 1 (CORE properties).

### 4.3 CORE Metrics (Layer 1 - Intrinsic)

These exist independent of observation threshold:

| Metric | Definition | Layer | Computed |
|--------|------------|-------|----------|
| κ(e) | Coherence of edge e | L1 | Yes (cached) |
| P(u) | Pressure at node u | L1 | Yes |
| Frust(e) | Frustration of edge e | L1 | Yes |
| Rec(e) | Recurrence of edge e | L1 | Partial |

**CRITICAL:** CORE metrics are NOT affected by projection thresholds (θ, wcluster, wdist, wbridge).

### 4.4 Metric Suffixes

- `@T` = measured at tick T
- `_count` = integer count
- `_weight` = sum of weights
- `_share` = percentage [0,100]

---

## 5. Ranking Protocol

### 5.1 Gates (Filters Before Ranking)

```
GATE-0: Valid (Layer 2 compliance)
  └─ Run is not INVALID (fail-closed passed)
  └─ Threshold relations satisfied

GATE-1: Active (if testing field interpretation)
  └─ bridges_count > 0 at target tick

GATE-2: Non-degenerate (projection quality)
  └─ coverage > 0
  └─ hub_share < 100 (not single-hub collapse)
```

Runs failing any gate are **excluded**, not ranked low.

**Ontological note:** Gates test projection quality (L2), not CORE validity (L1 always exists).

### 5.2 Core Ranking (lexicographic)

1. **max** bridges_weight
2. **min** hub_share  
3. **max** coverage
4. **max** bridges_count

**Ontological note:** This ranks L2 patterns (projection features), NOT L1 systems (CORE configurations).

### 5.3 Diagnostic Tier (non-ranking)

- channel_capacity - for regime identification
- anisotropy - for structure detection

**Rule:** Do not use diagnostic metrics to select "winner" until validated.

---

## 6. Report Format

### 6.1 Required Header

```
GRAVITY TEST REPORT - Tick T
============================================================
ONTOLOGICAL LAYER: L2 (FRACTURE/Projection Analysis)

Projection Parameters (L2):
  wcluster: X.XXX (cluster threshold)
  wdist: X.XXX (background geometry threshold)  
  wbridge: X.XXX (bridge/field threshold)
  
CORE Parameters (L1):
  W_max: X.XX (event horizon)
  decay: X.XXX (relational decay rate)
  seed: XXXX
  
Units: [SI/normalized/dimensionless]
Schema: tick_v2 (pre/post separation)
```

### 6.2 Required Sections

1. **CLUSTERING [L2]** - cluster count, sizes, unassigned (at θ_C)
2. **BRIDGES [L2]** - pairs, count, weight, hub_share, coverage (at θ_B)
3. **DISTANCES [L2]** - range metrics (from bg graph at θ_D, NOT bridges)
4. **CHANNELS [L2]** (if enabled) - capacity, anisotropy
5. **VALIDITY [L2]** - pass/fail with reasons (threshold relations, bounds)

**Language rules:**
- Use "observed", "projected", "visible" for L2 features
- NEVER say "exists", "is", "has" for L2 features as if they were L1

### 6.3 Result Table Standard

| run_id | seed | tick | layer | wcluster | wdist | wbridge | metric | value | notes |
|--------|------|------|-------|----------|-------|---------|--------|-------|-------|

**NEW:** `layer` column declares metric ontological layer (L1/L2/L3).

---

## 7. Cosmology Mapping Hypotheses

**Ontological framing:** These test WHETHER projection patterns MATCH physical expectations, NOT whether ROMION "is" cosmology.

### H-C1: Tension from Layered Measurement

**Idea:** "Hubble tension" analogs from measuring different projection layers.

**Test [L2]:**
- S_A(t) = estimator from background geometry (θ_D)
- S_B(t) = estimator from bridges (θ_B)
- Tension_AB = |S_A - S_B|

**H1:** Tension_AB > 0 persists (different projection layers)
**H0:** Tension_AB → 0 (estimators converge)

**Ontological note:** This is L2 pattern test, NOT L1 cosmology claim.

**Status:** MVP testable

### H-C2: Anisotropy from Channels

**Idea:** Directional preference emerges in projection.

**Test [L2]:**
- Split visible graph into L/R regions
- Measure capacity asymmetry

**H1:** Anisotropy > 0 stable across seeds
**H0:** Anisotropy fluctuates around 0

**Status:** SPEC (needs path-based capacity)

### H-C3: Early Structure Maturity

**Idea:** Active boundary enables fast stable projection structures.

**Test [L2]:**
- time_to_large_cluster = first tick with cluster ≥ X%
- stability_window = ticks largest cluster is stable

**H1:** Short time_to_large_cluster with active bridges
**H0:** Fast clustering only with freeze

**Status:** MVP testable

### H-C4: Birefringence from Projection

**Idea:** Orientation-dependent projection differences.

**Status:** SPEC only (needs orientation attribute)

---

## 8. Channel Metrics (SPEC, Layer 2)

### 8.1 Region Split

**Method:** BFS from seed cluster
- Seed = cluster with highest degree
- Alternate assignment L/R during BFS
- Deterministic (same input → same split)

**Ontological note:** This is projection-space partitioning (L2), not CORE partitioning (L1).

### 8.2 Path Capacity

**MVP (cut_weight) [L2]:**
```
Cap_cut(L,R) = Σ w_ab for visible edges (a,b) crossing L/R
```

**SPEC (path_count) [L2]:**
```
Cap_paths(L,R;d) = count of projected paths ≤ d between regions
```

### 8.3 Anisotropy Index [L2]

```
Anisotropy = (max_i Cap_i - median_i Cap_i) / (median_i Cap_i + ε)
```

Where Cap_i are capacities from k different split axes IN PROJECTION.

---

## 9. Validation Layer

### 9.1 Bounds Checks (L2 Compliance)

```python
def validate_metrics(metrics: dict, thresholds: dict) -> tuple[bool, list[str]]:
    reasons = []
    
    # Finite check
    for key in numeric_keys:
        if not isfinite(metrics[key]):
            reasons.append(f"{key} is not finite")
    
    # Bounds check
    if not (0 <= metrics["hub_share"] <= 100):
        reasons.append("hub_share out of bounds")
    if not (0 <= metrics["coverage"] <= 100):
        reasons.append("coverage out of bounds")
    
    # Non-negative check
    for key in ["unassigned_nodes", "channel_capacity", "anisotropy"]:
        if metrics.get(key, 0) < 0:
            reasons.append(f"{key} is negative")
    
    # Threshold relations (NEW)
    if thresholds["wcluster"] < thresholds["wdist"]:
        reasons.append("wcluster < wdist (invalid relation)")
    if thresholds["wbridge"] > thresholds["wcluster"]:
        reasons.append("wbridge > wcluster (field above matter)")
    if thresholds["wdist"] <= 0:
        reasons.append("wdist <= 0 (invalid geometry)")
    
    return (len(reasons) == 0), reasons
```

### 9.2 Degenerate vs Invalid

- **Degenerate [L2]:** Metric is 0 or undefined but projection is valid
  - Example: no cross-region edges (capacity=0)
  - Mark with `degenerate=True` in metadata
  - NOT invalid

- **Invalid [L2]:** Metric violates bounds OR threshold relations
  - Entire run is excluded
  - Cannot be used for comparison

**Ontological note:** "Invalid" means "projection procedure failed", NOT "CORE is bad".

---

## 10. Documentation Standards

### 10.1 Status Labels

Every concept must be labeled with:
- **Implementation:** `[IMPLEMENTED/MVP]` / `[PARTIAL]` / `[SPEC]`
- **Ontological layer:** `[L1-CORE]` / `[L2-FRACTURE]` / `[L3-INTERPRETATION]`

**Examples:**
- "S2 Antipair [SPEC, L1-CORE]"
- "hub_share metric [MVP, L2-FRACTURE]"
- "Gravity analog [INTERPRETATION, L3]"

### 10.2 Threshold Declarations

Every analysis output must include:
```
Projection Thresholds (L2):
  wcluster: X.XX [cluster definition - what projects as matter-like]
  wdist: X.XX [background geometry - metric space]
  wbridge: X.XX [field threshold - what projects as field-like]

CORE Parameters (L1):
  W_max: X.XX [event horizon]
  theta: X.XX [projection threshold - visibility cutoff]
```

### 10.3 No Backreaction Language

**Forbidden:**
- ❌ "Changing θ affects system evolution"
- ❌ "Projection influences dynamics"
- ❌ "Observation creates structure"

**Correct:**
- ✅ "Changing θ affects what we observe"
- ✅ "Projection reveals different features"
- ✅ "Observable structures depend on threshold"

### 10.4 No Cosmology Narrative

In test results:
- ❌ "This proves ROMION explains dark matter"
- ✅ "H-C1 not falsified: Tension_AB = 0.15 at tick 400 [L2]"
- ✅ "Pattern consistent with dark matter interpretation [L3]"

---

## 11. Canonical Contracts (POST-AUDIT)

**Authority for all metrics:** `docs/CANONICAL_METRICS.md`

**20 metrics fully specified:**
- **L1-CORE (8):** mean_kappa, mean_pressure, **mean_frustration** (v2.0), total_weight, n_edges, n_nodes, mean_tension, mean_emergent_time
- **L2-FRACTURE (3):** visible_edges, visible_ratio, mean_kappa_visible
- **L3-INTERPRETATION (4):** hub_share, coverage, R0, R2
- **Evolution (5):** spawn_new, spawn_reinf, field_tail_added, removed, norm_ops

**Schema v2.0 requirements:** `docs/CANONICAL_LOG_CONTRACT.md`
- metrics_pre (before U) and metrics_post (after U) separation
- mean_frustration MANDATORY in both
- projection.uses_metrics_post = true (CRITICAL)
- Layer labels enforced

**Validation enforcement:**
- `scripts/validate_log_schema.py` - Schema v2.0 entry gate
- `analysis/gravity_test/validate_romion.py` - Metrics bounds/consistency
- `tests/test_canonical_metrics.py` - Test suite (9/9 passed)

**Cross-reference:** All metrics in Section 4 must conform to CANONICAL_METRICS.md

---

## 12. Checklist for PRs

Every PR touching metrics/analysis must confirm:

- [ ] Layer separation maintained (L1/L2/L3 explicit)
- [ ] No backreaction language (projection → CORE)
- [ ] Fail-closed validation present with threshold checks
- [ ] Proxy metrics labeled as proxy + layer
- [ ] All thresholds explicit in output
- [ ] Layer declared for all metrics
- [ ] IMPLEMENTATION_STATUS.md updated with layer info
- [ ] No cosmology claims in test results (use L3 interpretation language)
- [ ] Pre-registration template followed for new tests
- [ ] spawn_threshold vs theta distinction maintained
- [ ] **NEW:** Conforms to CANONICAL_METRICS.md (authority)
- [ ] **NEW:** Schema v2.0 compliant (if producing logs)
- [ ] **NEW:** Passes validate_log_schema.py (if applicable)

---

**Document status:** CANONICAL METHODOLOGY  
**Version:** 2.1 - POST-AUDIT  
**Authority:** CANONICAL_METRICS.md, CANONICAL_LOG_CONTRACT.md  
**Maintenance:** Update when adding metrics (must conform to canonical contracts)

**For metric definitions:** CANONICAL_METRICS.md  
**For schema details:** CANONICAL_LOG_CONTRACT.md  
**For audit status:** STATUS.md
