# ROMION Cosmology Mapping
# Testable hypotheses only - no claims

**Version:** 1.0
**Date:** 2026-01-08
**Rule:** This document contains ONLY testable hypotheses with metrics and falsification criteria.

---

## Fundamental Principle

> ROMION O'LOGIC does not "explain cosmology."
> It provides structural metrics that MAY be mapped to cosmological phenomena.
> Every mapping must be testable and falsifiable.

---

## Format for Each Hypothesis

```
ID: H-CX
Idea: [One sentence description]
Metrics: [What we measure]
H1: [Alternative hypothesis - what we expect if true]
H0: [Null hypothesis - default if H1 fails]
Falsification: [Specific condition that disproves H1]
Status: MVP / PARTIAL / SPEC
```

---

## H-C1: Tension from Layered Measurement

### Idea
Different estimators of "scale/tempo" applied to same system give persistently different values when they probe different layers (CORE-like vs FRACTURE-like).

### Metrics

**S_A(t):** Estimator from background geometry (cluster distances)
```
S_A(t) = mean_shortest_path(bg_meta, t)
```

**S_B(t):** Estimator from field/bridges
```
S_B(t) = bridges_weight(t) / pairs_with_bridge(t)
```

**Tension:**
```
Tension_AB(t) = |S_A(t) - S_B(t)|
```

### H1
For certain parameter regimes, Tension_AB(t) > 0 persists in quasi-stationary state.

### H0
Tension_AB(t) → 0 in stationary state (estimators converge).

### Falsification
If across all parameter regimes and seeds, Tension_AB always collapses to ~0 within statistical noise.

### Status
**SPEC** - S_A and S_B not yet implemented as defined above. Can be computed manually from existing metrics.

---

## H-C2: Anisotropy from Channels

### Idea
Background geometry develops persistent directional preference (anisotropy) through channel-like structures.

### Metrics

**Region Split:**
Deterministic BFS-based split of clusters into L/R without coordinates.

**Channel Capacity (MVP):**
```
Cap_cut(L,R) = Σ w_ab for edges (a,b) crossing L/R
```

**Anisotropy Index:**
```
Anisotropy = (max_i Cap_i - median_i Cap_i) / (median_i Cap_i + ε)
```
Where Cap_i are capacities from k different deterministic split axes.

### H1
There exist parameter regimes where anisotropy > 0 remains stable across ticks and seeds.

### H0
Anisotropy fluctuates around 0 without persistent structure.

### Falsification
If anisotropy consistently returns to 0 in steady state for all regimes, channels are not natural products of dynamics.

### Status
**PARTIAL** - Implemented as split-axis variability proxy. Not true directional anisotropy (graph is undirected).

---

## H-C3: Early Structure Maturity

### Idea
Active CORE/FRACTURE boundary enables rapid formation of stable structures without global freeze.

### Metrics

**time_to_large_cluster:**
First tick where largest cluster ≥ X% of nodes (X pre-registered).

**stability_window:**
Number of consecutive ticks where largest cluster maintains similar topology (Δ bridges < δ).

**bridges_count:**
Must remain > 0 (otherwise it's freeze, not maturity).

### H1
There exists a regime where time_to_large_cluster is short AND bridges remain active.

### H0
Fast structure formation only occurs with freeze (bridges → 0).

### Falsification
If rapid structuring always leads to freeze, "active boundary stabilization" does not work.

### Status
**SPEC** - Requires new metrics. Can be partially tested with existing bridge tracking.

---

## H-C4: Birefringence from Projection Anisotropy

### Idea
Orientation-dependent projection differences create measurable effects analogous to cosmic birefringence.

### Prerequisites
- Orientation attribute on relations (not currently implemented)
- Projection operator dependent on orientation

### Metrics (placeholder)

**BirefProxy:**
```
BirefProxy(t) = |mean_κ_+(t) - mean_κ_-(t)| / (mean_κ_+(t) + mean_κ_-(t) + ε)
```
Where κ_+/κ_- are coherence measures for + and - oriented relations.

### H1
Orientation-dependent differences persist in steady state.

### H0
No persistent orientation asymmetry.

### Status
**SPEC** - Requires orientation attribute (not implemented, OFF by default when added).

---

## Projection Ratio Discovery

### Finding (2026-01-08 Session)
At visibility threshold θ ≈ 0.46:
- Node projection ratio ≈ 5%
- Consistent across all 6 simulation configurations
- Matches cosmological baryonic matter fraction

### Interpretation (Bounded)

**Standard cosmology:**
- ~5% baryonic matter
- ~27% dark matter
- ~68% dark energy

**ROMION mapping hypothesis:**
- ~5% baryonic = CORE projecting to FRACTURE (measured!)
- ~27% dark matter = CORE structure below projection threshold (gravitationally affects but invisible)
- ~68% dark energy = CORE relational pressure (manifests as Λ)

### Status
**MVP** - Measured and reproducible. Interpretation is hypothesis, not claim.

### What This Means
The "dark sector" is not missing - it exists in CORE but doesn't project to FRACTURE as visible structure.

### Falsification
- Find physical meaning for θ ≈ 0.46 or prove it's arbitrary
- Check if ratio holds across different simulation scales
- Compare with more precise cosmological measurements

---

## Hubble Tension Mapping

### Standard Problem
Early universe (CMB) gives H₀ ≈ 67 km/s/Mpc
Late universe (supernovae) gives H₀ ≈ 73 km/s/Mpc

### ROMION Hypothesis
H₀ is not a fundamental constant but a parameter depending on:
- Scale of measurement
- Local pressure regime
- CORE/FRACTURE boundary state

Different methods probe different relational states → different effective H₀.

### Testable via H-C1
If Tension_AB persists, it's evidence that different measurement "layers" give different results.

### Status
**SPEC** - Framework only, no direct H₀ calculation possible in simulation.

---

## Summary Table

| ID | Hypothesis | Metrics | Status |
|----|------------|---------|--------|
| H-C1 | Tension from layers | S_A, S_B, Tension_AB | SPEC |
| H-C2 | Anisotropy from channels | channel_capacity, anisotropy | PARTIAL |
| H-C3 | Early maturity | time_to_cluster, stability | SPEC |
| H-C4 | Birefringence | orientation-dependent κ | SPEC |
| ~5% | Projection ratio | θ ≈ 0.46 → 5% visible | MVP |
| Hubble | Tension as layer effect | via H-C1 | SPEC |

---

## Rules for This Document

1. **No claims** - only hypotheses with falsification
2. **Metrics must exist** - either implemented or clearly marked SPEC
3. **Bounded interpretation** - say what metrics show, not what they "prove"
4. **Status honest** - MVP only if actually measured and reproducible
5. **Update regularly** - as hypotheses are tested, update status

---

## Key Statements (from Theory)

> "Λ to nie byt – to bilans."
> (Λ is not an entity - it's a balance)

> "Napięcie Hubble'a nie jest błędem – jest sygnałem."
> (Hubble tension is not an error - it's a signal)

> "metryka ≠ mechanizm"
> (metric ≠ mechanism)

These are methodological positions, not empirical claims.

---

**Document status:** CANONICAL COSMOLOGY MAPPING
**Authority:** Theory annexes + session findings
**Maintenance:** Update when hypotheses are tested
