# ROMION O'LOGIC Glossary
# Complete terminology reference

**Version:** 1.1
**Date:** 2026-01-11
**Status:** POST-AUDIT
**Format:** Term → Definition → Operationalization → Status

---

## POST-AUDIT ADDITIONS (2026-01-11)

### Schema v2.0
**Definition:** Mandatory log format separating metrics_pre (before evolution U) and metrics_post (after U), with explicit layer labels.
**Authority:** CANONICAL_LOG_CONTRACT.md
**Operationalization:** schema_version: "2.0" in METADATA event
**Status:** LOCKED (contractually enforced)

### L1-CORE (Layer 1)
**Definition:** Primary ontological layer - what exists. Graph structure Δ(t), evolution U, intrinsic properties independent of observation.
**Metrics:** mean_kappa, mean_pressure, mean_frustration, total_weight, n_edges, n_nodes
**Authority:** CANONICAL_METRICS.md
**Status:** LOCKED (layer separation enforced)

### L2-FRACTURE (Layer 2)  
**Definition:** Derived/epistemological layer - what is observed. Projection Πθ, threshold-dependent visibility.
**Metrics:** visible_edges, visible_ratio, mean_kappa_visible
**Critical:** MUST use metrics_post (after U)
**Authority:** CANONICAL_METRICS.md
**Status:** LOCKED (layer separation enforced)

### L3-INTERPRETATION (Layer 3)
**Definition:** Interpretive/linguistic layer - what we infer. Analysis patterns, physics analogies, NOT ontological claims.
**Metrics:** hub_share, coverage, R0, R2
**Rule:** Cannot be fed back to L1 (backreaction forbidden)
**Authority:** CANONICAL_METRICS.md
**Status:** LOCKED (layer separation enforced)

### mean_frustration
**Definition:** L1-CORE metric measuring deviation from equilibrium state. Required in schema v2.0.
**Formula:** Mean of frustration values across edges
**Range:** [0, 1]
**Authority:** CANONICAL_METRICS.md
**Status:** MANDATORY (v2.0 requirement)

### Canonical Metrics
**Definition:** Complete, authoritative specification of all 20 ROMION metrics (8 L1-CORE, 3 L2-FRACTURE, 4 L3-INTERPRETATION, 5 Evolution).
**Authority:** CANONICAL_METRICS.md (1000 lines)
**Enforcement:** validate_romion.py
**Status:** LOCKED (contracts enforce)

### Canonical Log Contract
**Definition:** Complete, authoritative specification of schema v2.0 log format.
**Authority:** CANONICAL_LOG_CONTRACT.md (700 lines)
**Enforcement:** validate_log_schema.py
**Status:** LOCKED (contracts enforce)

### Fail-Closed Validation
**Definition:** Methodology principle: invalid data → reject (no silent degradation).
**Applies to:** Schema validation, metric bounds, threshold relations
**Implementation:** validate_log_schema.py, validate_romion.py
**Status:** LOCKED (operationally enforced)

---

## Core Ontology

### Romion
**Definition:** Elementary unit of relational description. Not a "particle in space" but a node in relational configuration from which observable structures emerge.
**Operationalization:** In MVP corresponds to graph node.
**Status:** MVP

### Configuration Δ (Delta)
**Definition:** Total relational state of romionosphere (hypergraph of relations and weights) at given evolution step.
**Operationalization:** In MVP: G_t = (V, E, w) as simulation state at tick t.
**Status:** MVP

### delta_zero (Δ_∅)
**Definition:** Limiting state of minimal contradiction/topological tension. Treated as attractor of CORE evolution (local minimization tendency).
**Operationalization:** No direct implementation in MVP; pressure/tension as proxy for Φ functional.
**Status:** SPEC (formalism), PARTIAL (proxy)

### Functional Φ(Δ)
**Definition:** Abstract measure of "contradiction/topological energy" of configuration Δ. Used to define delta_zero and CORE evolution direction.
**Operationalization:** In MVP: no direct Φ; pressure/tension serve as proxy.
**Status:** SPEC/PARTIAL

---

## Two Phases

### CORE
**Definition:** Romionosphere phase with non-emergent dynamics, local tendency to reduce Φ(Δ) (approach delta_zero).
**Operationalization:** In MVP: no explicit phase separation; CORE behaviors approximated by tension-limiting rules.
**Status:** SPEC (phase), PARTIAL (proxy)

### FRACTURE
**Definition:** Emergent romionosphere phase where relational patterns (schemas) become stabilized and form observable structures.
**Operationalization:** In MVP: stabilization may correspond to "freeze" and repeatable graph patterns.
**Status:** SPEC/PARTIAL

### CORE/FRACTURE Boundary (Engine)
**Definition:** Thin, active layer where simultaneous generation of new relations and selection/stabilization of FRACTURE schemas occurs. The key engine of emergence.
**Operationalization:** In MVP: no explicit boundary layer; observed transitions (freeze/thaw, bridge changes) as proxy.
**Status:** SPEC (explicit mechanism), PARTIAL (proxy via metrics)

### Romionosphere
**Definition:** Operationally: area/layer of active romion relations encompassing CORE, FRACTURE and their boundary; the "place" where we define emergence metrics and test theory.
**Operationalization:** In MVP: entire simulation graph at given tick plus metrics (κ, θ, P, T, bridges, range).
**Status:** MVP (operational concept), PARTIAL (phases)

---

## Metrics and Parameters

### Coherence κ (kappa)
**Definition:** Measure of relational coherence (local or global), determining pattern's ability to stabilize and project to observability.
**Operationalization:** In MVP: kappa/cache κ, used as gate (threshold) and/or spawn rule component.
**Status:** PARTIAL

### Visibility Threshold θ (theta)
**Definition:** Projection operator determining which relational patterns are "visible" as observable structures.
**Operationalization:** visible(x) ⟺ κ(x) ≥ θ; in MVP usually as filter/report "VIS%".
**Status:** PARTIAL

### Pressure P
**Definition:** Measure of local "relational stress/load" in configuration; treated as proxy contribution to Φ.
**Operationalization:** pressure in logs; used for weight change decisions, clamp, emergence.
**Status:** MVP/PARTIAL (theoretical proxy)

### Tension T
**Definition:** Measure of global accumulated contradiction/topological energy in configuration; global Φ proxy.
**Operationalization:** tension in logs; sanity/stability monitoring.
**Status:** MVP/PARTIAL

---

## Structural Elements

### Loop (Δ-loop)
**Definition:** Cycle in projection graph - sequence of nodes returning to start. Fundamental building block of "matter" in ROMION.
**Types:**
- Simple loop (no vertex repetitions)
- Complex loop (allows repetitions)
- Hyperloop (on hyperedge level)
- Channel loop (contains channel-like edges)
- Oriented loop (with σ ∈ {+1, -1})
**Status:** SPEC (detection), partial proxy via cluster analysis

### Loop Invariants
**Definition:** Properties that classify loops as "particle-like":
- L₀: topological length
- L₁: metric length  
- μ: mass/stability score
- Q_T: topological charge
- σ: orientation
**Status:** SPEC

### Bridges
**Definition:** Relations connecting distinct objects (clusters) and determining flow/coherence between them.
**Operationalization:** bridges counted as edges between clusters at wbridge threshold.
**Status:** MVP

### Background Geometry
**Definition:** Relation structure used to define distances between objects; not identified with bridges.
**Operationalization:** Cluster graph built at wdist threshold, used for range calculation.
**Status:** MVP (analytical tool)

---

## Threshold Parameters

### wcluster
**Definition:** Minimum weight for edges within clusters (object definition).
**Usage:** Defines what constitutes a "thing" - internal coherence threshold.
**Status:** MVP

### wdist  
**Definition:** Minimum weight for background geometry edges (distance measurement).
**Usage:** Defines how we measure distances - geometric structure threshold.
**Status:** MVP

### wbridge
**Definition:** Minimum weight for bridge edges (field/interaction).
**Usage:** Defines what constitutes interaction - connection strength threshold.
**Status:** MVP

### Critical Rule
> wcluster, wdist, and wbridge MUST be measured separately. Mixing them invalidates results.

---

## Dynamic Rules

### S1 (Closure)
**Definition:** Closing cycles/paths and strengthening relations leading to topological compression.
**Operationalization:** Spawn through short path/triad detection (MVP).
**Status:** PARTIAL (heuristic vs target formula)

### S2 (Antipair / quasi-unitarity)
**Definition:** Mechanism balancing transitions and limiting dynamics "spread".
**Operationalization:** None; S2-tail is field heuristic, not full S2.
**Status:** SPEC

### S3 (Triadic)
**Definition:** Three-way/higher-order interactions as generator of new schemas.
**Operationalization:** None.
**Status:** SPEC

---

## Particle Ontology

### Quark-like
**Definition:** Elementary loop with small L₀, high μ - local, "stiff" resonator with color degeneracy.
**Color:** c(C) ∈ {R, G, B} - three stable orbits under niche automorphisms.
**Flavor:** f(C) ∈ {u, d, c, s, t, b} - determined by (L₀, μ, Q_T, motif).
**Status:** SPEC

### Lepton-like
**Definition:** Colorless loop (no SU(3)_C degeneracy) with EM charge from phase mode.
**Types:** electron/muon/tau (Q_EM = -1, generations 1-3), neutrinos (Q_EM = 0).
**Status:** SPEC

### Baryon-like
**Definition:** Triad of loops {C₁, C₂, C₃} bound to common core with color completeness and stability S(B) ≥ S₀.
**Examples:** proton = B(u,u,d), neutron = B(u,d,d)
**Status:** SPEC

### Meson-like
**Definition:** Pair of loops with high overlap and opposite orientation, balanced by CANCEL/FUSE.
**Status:** SPEC

---

## Boson Modes

### Photon (γ)
**Definition:** U(1) phase mode on loops and bridges.
**Formula:** γ ≡ δθ
**Coupling:** To loops with Q_EM ≠ 0
**Status:** SPEC (implemented as phase propagation test)

### Gluons (g)
**Definition:** SU(3)_C generators - operators changing color label.
**Formula:** gₐ: c(C) → c'(C), a = 1,...,8
**Status:** SPEC

### W±, Z⁰
**Definition:** Weak modes as family/chirality transformation operators.
**Status:** SPEC

### Higgs (H)
**Definition:** Background functional modifier affecting cost/stability.
**Status:** SPEC

### Graviton
**Definition:** Three equivalent views:
- G1: Metric quantum (δd)
- G2: Cluster coherence mode (δK)
- G3: Bridge bundle with spin-2 symmetry
**Status:** SPEC

---

## Phenomena

### Freeze / Thaw
**Definition:** Freeze = transition to vanishing connectivity (bridges→0) and schema stabilization; Thaw = exit from this state.
**Operationalization:** freeze_tick, bridges@T, tick dynamics.
**Status:** MVP (phenomenon), PARTIAL (phase interpretation)

### Pressure Cage
**Definition:** Extremely dense region where phase propagation stops completely (δθ = 0), maintaining stable oscillation.
**Analogy:** Slow light in BEC, light stopped in cold atoms, event horizon.
**Status:** SPEC (hypothesis from session)

### Warp Channel (CWD)
**Definition:** Persistent preferential relational permeability between romionosphere regions (flow anisotropy).
**Operationalization:** Channel capacity via cut_weight (MVP), anisotropy via split-axis variance (MVP)
**Status:** MVP (implemented in analysis/gravity_test/channels.py)

### Event Horizon / W_max (Clamp)
**Definition:** Mechanism limiting relation weight growth, stabilizing configuration and preventing degeneracy.
**Operationalization:** Weight clamp in code; observable via weight saturation and tension behavior.
**Status:** MVP (mechanism), PARTIAL (interpretation)

---

## Cosmological Mappings

### "Dark Matter"
**ROMION interpretation:** CORE structure below projection threshold - exists, affects gravity, but doesn't project to FRACTURE as visible structure.
**Status:** Hypothesis supported by ~5% projection ratio finding

### "Dark Energy" / Λ
**ROMION interpretation:** CORE relational pressure balance, not substance. Λ is effective parameter of regime, not ontological entity.
**Key statement:** "Λ to nie byt – to bilans."
**Status:** Methodological framework

### Hubble Tension
**ROMION interpretation:** Not error but signal - different methods measure different relational states. H₀ is parameter dependent on scale, pressure, regime.
**Status:** Hypothesis for testing

### Projection Ratio (~5%)
**Definition:** Fraction of CORE structure that projects to FRACTURE at natural threshold.
**Finding:** θ ≈ 0.46 gives ~5% visible structure (matches baryonic fraction!)
**Status:** MVP (measured), under validation

---

## Methodological Terms

### Pre-registration
**Definition:** Documenting hypothesis, metrics, and falsification criteria BEFORE running test.
**Status:** Required for all tests

### Fail-closed
**Definition:** Invalid metric values (NaN, out-of-bounds, semantic mismatch) invalidate entire run.
**Status:** Enforced in analysis tools

### MVP vs SPEC
**Definition:** 
- MVP (Implemented): Currently in code and tested
- SPEC (Specification): Theoretical framework, not yet implemented
**Status:** All documents must clearly mark status

### SI/RI Units
**Definition:** System International vs Romion Internal units.
**Rule:** Every numerical result must be labeled [SI] or [RI] or [RI?].
**Status:** SPEC/PARTIAL (labeling rule, not unit definitions)

---

## Quick Reference: Key Formulas

### Loop Mass/Stability
```
μ(C) = (∏ κ(e)·w(e))^{1/|C|}
```

### Topological Charge
```
Q_T(C) = σ(C) · (L₀(C) mod 2)
```

### Visibility
```
visible(x) ⟺ κ(x) ≥ θ
```

### Bundle Stability
```
S(B) = Σᵢ μ(Cᵢ) - λ Σᵢ<ⱼ O_E(Cᵢ, Cⱼ)
```

### Pauli Exclusion
```
(core₁, n₁) = (core₂, n₂) AND (Q₁, s₁, sig₁) = (Q₂, s₂, sig₂) ⟹ FORBIDDEN
```

---

## Cross-References (POST-AUDIT)

**For canonical definitions:**
- Metrics: CANONICAL_METRICS.md
- Schema: CANONICAL_LOG_CONTRACT.md
- Methodology: METHODOLOGY.md
- Layer separation: THEORY.md

**For implementation:**
- Status: IMPLEMENTATION_STATUS.md
- Validation: validate_log_schema.py, validate_romion.py
- Tests: test_canonical_metrics.py

---

**Document status:** CANONICAL GLOSSARY  
**Version:** 1.1 - POST-AUDIT  
**Maintenance:** Update when adding new terms to theory  
**Authority:** Cross-reference CANONICAL_*.md for L1/L2/L3 metrics
