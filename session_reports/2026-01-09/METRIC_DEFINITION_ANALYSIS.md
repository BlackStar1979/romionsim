# Metric Definition Inconsistency Analysis

**Date:** 2026-01-09  
**Issue:** hub_share and coverage definitions in code ≠ docs  
**Source:** GPT audit point #19

---

## Problem Statement

**METHODOLOGY.md v2.0 says:**
```
hub_share@T: % of cluster-pairs in largest connected component of bridge graph
coverage@T: % of cluster-pairs touched by bridge analysis
```

**Code (metrics.py) computes:**
```python
# hub_share = degree-based metric
hub_share = (hub_deg / total_connections * 100)

# coverage = cluster participation metric  
coverage = (clusters_with_bridges / n_clusters * 100)
```

These are **fundamentally different metrics**.

---

## Analysis

### hub_share Discrepancy

**Doc definition:** "% pairs in largest connected component"
- This would require: graph connectivity analysis
- Finding largest component (BFS/DFS)
- Counting pairs IN that component
- Computing ratio to total pairs

**Code implementation:** "Hub degree as % of total degree"
- Finds cluster with most bridge connections (degree)
- Computes: hub_degree / sum_of_all_degrees × 100

**These measure different things:**
- Doc: Component-based topology (graph structure)
- Code: Degree centrality (hub dominance)

### coverage Discrepancy

**Doc definition:** "% pairs touched by analysis"
- Would count: how many (cluster_i, cluster_j) pairs have ANY bridge
- Denominator: all possible pairs C(n_clusters, 2)

**Code implementation:** "% clusters with ≥1 bridge"
- Counts: how many clusters participate in bridges
- Denominator: total clusters

**These measure different things:**
- Doc: Pair coverage (quadratic in clusters)
- Code: Cluster participation (linear in clusters)

---

## Which is Correct?

### From GPT Audit

> **Wariant A (zalecany): poprawić dokumentację do tego, co realnie mierzy kod.**

Reasoning:
- Code metrics are simpler and more interpretable
- Pair-based metrics grow ~N² and become unreadable
- Degree-based hub_share is meaningful
- Cluster participation (coverage) is useful diagnostic

**Recommendation:** Update METHODOLOGY.md to match code.

### Alternative: Change Code

**Wariant B:** Change code to compute doc definitions
- Requires new metrics: lcc_share (largest component)
- Requires pair-based coverage computation
- More complex, less interpretable

**NOT recommended** for ROMION (simpler is better).

---

## Correct Definitions (Code-Based)

### hub_share (degree dominance)

**Definition:** Percentage of total bridge-graph degree held by the most-connected cluster.

**Formula:**
```
hub_id = argmax_c degree(c)
hub_share = degree(hub_id) / Σ_c degree(c) × 100
```

**Interpretation (L3):**
- High hub_share → topology dominated by single cluster
- Low hub_share → connections distributed evenly

**Ontological layer:** L2-FRACTURE (projection metric)

**Bounds:** [0, 100]

### coverage (cluster participation)

**Definition:** Percentage of clusters that have at least one bridge connection.

**Formula:**
```
coverage = |{c | degree(c) > 0}| / n_clusters × 100
```

**Interpretation (L3):**
- High coverage → most clusters participate in field-like connections
- Low coverage → isolated clusters, sparse field

**Ontological layer:** L2-FRACTURE (projection metric)

**Bounds:** [0, 100]

---

## Action Required

### Phase A (Documentation - NOW)

1. ✅ Create this analysis document
2. [ ] Update METHODOLOGY.md v2.0 with correct definitions
3. [ ] Add note: "Previous docs incorrectly described these"

### Phase B (Code - LATER)

1. [ ] Add docstring clarifications to compute_hub()
2. [ ] Consider: add lcc_share as separate metric (optional)
3. [ ] Ensure validate.py checks bounds [0,100]

---

## Updated Definitions for METHODOLOGY.md

```markdown
### 4.1 Primary Metrics (for ranking)

| Metric | Definition | Formula | Layer | Bounds |
|--------|------------|---------|-------|--------|
| hub_share@T | Degree dominance: % of total bridge-graph degree held by most-connected cluster | hub_deg/Σdeg × 100 | L2 | [0,100] |
| coverage@T | Cluster participation: % of clusters with ≥1 bridge | clusters_with_bridge/n_clusters × 100 | L2 | [0,100] |

**Ontological notes:**
- **hub_share:** Measures degree centrality (NOT largest component size)
- **coverage:** Measures cluster participation (NOT pair coverage)
- These are PROJECTION METRICS computed in bridge graph (θ_bridge)
```

---

## Historical Note

**Why the discrepancy existed:**

Original intuition may have been "component-based" but implementation chose simpler "degree-based" approach. Over time, docs drifted from code.

**GPT audit found this** because it read both code AND docs carefully.

**Fix:** Documentation alignment (Wariant A).

---

**Status:** Analysis complete, awaiting METHODOLOGY.md update  
**Priority:** HIGH (affects all result interpretations)  
**Phase:** A (documentation only)
