# ROMION O'LOGIC™ Theory Foundations

**Document:** Theoretical basis for romionsim implementation  
**Version:** 2.0  
**Date:** 2026-01-09  
**Status:** SEMANTIC REFACTOR - Ontological Clarity

---

## ⚠️ FUNDAMENTAL PRINCIPLE

> **ROMION O'LOGIC™ treats CORE dynamics as ontologically primary.**  
> **All projections, clusters, fields and observables are epistemic and must never be fed back into CORE unless explicitly modeled as a separate physical mechanism.**

This principle governs the entire theoretical framework and implementation.

---

## Three Ontological Layers

ROMION O'LOGIC™ operates on three distinct, non-interchangeable layers:

### 1. CORE (Ontological)
**What exists:**
- Hypergraph H = (V, E, w, σ)
- Relational dynamics U
- Intrinsic properties: κ, P, Frust, Rec

**Properties:**
- Primary reality
- Independent of observation
- Governed by evolution operator U
- **NO feedback from projection**

### 2. FRACTURE / PROJECTION (Epistemological)
**What we observe:**
- Projection operator Πθ
- Visible structures (κ ≥ θ)
- Emergent topology

**Properties:**
- Secondary (derived from CORE)
- Observation-dependent (threshold θ)
- **Does NOT affect CORE dynamics**
- Mapping, not mechanism

### 3. INTERPRETATION (Linguistic/Emergent)
**How we describe it:**
- "Clusters" = aggregated visible relations
- "Field" = long-range correlation pattern
- "Matter" = stable relational structures
- "Gravity" = pressure-induced correlations

**Properties:**
- Tertiary (language layer)
- Useful for comparison with physics
- **Never imported back into CORE or FRACTURE**
- Interpretative, not definitional

---

## Layer Separation Rules

**CRITICAL:** These rules are non-negotiable.

1. **CORE → FRACTURE is one-way**
   - Projection Πθ reads CORE, never writes
   - θ is observation parameter, NOT dynamics parameter

2. **No backreaction from observation**
   - Changing θ changes what you SEE
   - Changing θ does NOT change what EXISTS
   - spawn_threshold ≠ θ (different ontological roles)

3. **Interpretation language stays in Layer 3**
   - "Field detected" → "field-consistent topology observed"
   - "Matter exists" → "stable structures in projection"
   - "Objects formed" → "clusters in visible graph"

**Violation of these rules = methodological error**, even if code "works".

---

## Core Formalism (LAYER 1: CORE)

### Hypergraph Structure

```
H_n = (V_n, E_n, w_n, σ_n)
```

Where:
- **V_n:** Nodes (romions, relational entities)
- **E_n:** Edges (relations, mediating romions)
- **w_n:** Weights (relational strength)
- **σ_n:** Types (interaction modes)

**Ontological claim:** Relations are primary, not derived from "things".

---

## Evolution Operator (LAYER 1: CORE)

**Theoretical formulation:**
```
U = Normalize ∘ Fuse ∘ Propagate ∘ Spawn
```

**MVP implementation:**
```
U = Normalize ∘ Propagate ∘ Spawn ∘ Metrics
```

Note: "Fuse" integrated into Spawn (resonance mechanism).

**CRITICAL:** U operates ONLY on CORE. It has NO access to projection results.

---

## Spawn Rules (LAYER 1: CORE Dynamics)

### S1 - Closure (Topological Shortcuts) **[MVP - IMPLEMENTED]**

**Formula:**
```
w'(A→B) = α₁ · (∏_{e∈γ} κ(e)·w(e))^(1/|γ|)
```

**Relational meaning:** Creates shortcuts proportional to cycle strength in CORE topology.

**MVP Implementation:** Triangle closure with geometric mean (|γ|=2).

**In code (`rules.py::rule_spawn`):**
```python
signal = (e1.w * e2.w) ** 0.5  # |γ|=2
target_w = signal * spawn_damping  # α₁
```

**Parameter mapping:**
- `spawn_damping` = α₁
- **Status:** ❓ Needs derivation from first principles

**Expected range:** α₁ ∈ [0, 1] (damping, child weaker than parents)

**Ontological note:** This is CORE dynamics, NOT "object formation". Objects are LAYER 3 interpretation.

---

### S2 - Antipair (Quasi-Unitarity) **[SPEC - NOT IMPLEMENTED]**

**Theoretical formula:**
```
w'(e†) = α₂ · w(e) · exp(-μ·Frust(e))
```

**Relational meaning:** Generates conjugate/inverse relations (basis for interference).

**Implementation status:** 🔴 **UNIMPLEMENTED - SPEC ONLY**

**Status:** THEORETICAL MECHANISM (future work)

---

#### ⚠️ CRITICAL: What IS vs What IS NOT S2

**S2 (Antipair) = SPEC (not in code):**
- Theoretical mechanism from ROMION theory
- Formula: w'(e†) = α₂ · w(e) · exp(-μ·Frust(e))
- Generates conjugate relations (antipairs)
- Status: Requires full derivation before implementation

**Field-tail = MVP PROXY (in code, disabled by default):**
- Experimental proxy for long-range effects
- Function: `rule_field_tail()` (renamed from `rule_s2_tail` 2026-01-09)
- Status: Phenomenological (NOT theory-derived)
- Enable via: `--enable-field-tail` flag
- **NOT S2**: Different mechanism, different purpose

**Quantum Spark = DEPRECATED (in code, removal pending):**
- Was: Speculative feature claimed to relate to S2
- Status: 🔴 DEPRECATED (no theoretical basis)
- In code: DeprecationWarning if enabled
- Action: Will be REMOVED in cleanup

---

#### Field-Tail Proxy Details **[MVP - OPTIONAL]**

**What it does:**
- Adds rare weak bridges at dist>=2
- Modulated by frustration and distance
- Experimental mechanism for testing long-range field hypothesis

**What it is NOT:**
- ❌ NOT S2 (Antipair)
- ❌ NOT theory-derived
- ❌ Parameters are phenomenological

**Parameters (ad-hoc):**
- `tail_base_rate` = 0.01
- `lambda_dist` = 0.5
- `tail_w` = 0.008

**Status:** Experimental proxy, useful for testing field-like topologies

**See:** `SPEC_S2_TAIL.md` for full specification

---

### S3 - Triadic (Type Composition) **[SPEC - NOT IMPLEMENTED]**

**Formula:**
```
w'(A→C) = w(A→C) + α₃ · ΔCompat(A,B,C)
```

**Relational meaning:** Composite relational channels through type compatibility.

**Implementation:** NOT YET IMPLEMENTED

**Future work:** Type-dependent interactions (σ field).

---

## Metrics (LAYER 1: CORE Properties)

These are intrinsic properties of CORE, NOT observations.

### Coherence (κ)

**Theoretical formula:**
```
κ(e) = exp(-λ·Frust(e)) · Rec(e)/(Rec(e)+c)
```

**Current MVP approximation (`metrics.py`):**
```python
rec_factor = 1.0 + triangle_strength + beta * two_hop_strength
k = (edge.w * rec_factor) / (1.0 + 0.1 * avg_pressure)
kappa = k / (1.0 + k)  # Sigmoid
```

**Mapping hypothesis:**
- Rec(e) ≈ 1 + triangles + β·2hop
- Frust(e) ≈ avg_pressure (inverse)
- exp(-λ·Frust) ≈ 1/(1 + factor·pressure)
- Final sigmoid normalization

**Status:** ⚠️ APPROXIMATION - needs proper derivation

**Parameters:**
- `beta_2hop` = β (weight for longer loops)
- **Status:** ❓ Needs justification

**Ontological note:** κ exists in CORE independent of whether we observe it.

---

### Pressure (LAYER 1: CORE Property)

**Definition:**
```
P(u) = Σ_{e incident to u} w(e)
```

**Relational meaning:** Local relational load (analogous to energy density).

**Normalization:** W_max caps pressure (event horizon).

**Parameter:**
- `W_max` = 2.5 (THEORY VALUE)
- **Status:** ❓ Needs derivation from horizon physics

**IMPORTANT:** MVP code default = 5.0 (INCONSISTENT - requires fix)

---

### Tension (LAYER 1: CORE Property)

**Definition:**
```
T(u) = Σ_t (P(u) - W_max)_+
```

**Relational meaning:** Accumulated constraint (candidate for gravitational mass analog).

**In code:**
```python
if pressure > W_max:
    tension[u] += pressure - W_max
```

**Prediction:** T correlates with LAYER 3 "gravitational" effects (cluster attraction).

---

### Emergent Time (LAYER 1: CORE Property)

**Formula:**
```
dt(u) = 1 / (1 + α·P(u))
```

**Relational meaning:** Time dilation from relational density.

**In code:**
```python
dt = 1.0 / (1.0 + time_alpha * pressure)
emergent_time[u] += dt
```

**Parameter:**
- `time_alpha_scale` = 1.0
- **Status:** ✅ Phenomenological (reasonable choice)

---

## Projection (LAYER 1 → LAYER 2 Mapping)

### CORE → FRACTURE Operator

**Operator:**
```
Π_θ: H_CORE → M_FRACTURE
```

**Mechanism:** Only edges with κ(e) ≥ θ project to observable space.

**MVP implementation:**
```python
visible_edges = sum(1 for e in G.all_edges() if e.kappa_cache >= theta)
```

**Parameter:**
- `theta` = θ = 0.25 (THEORY VALUE)
- **Status:** ✅ THEORETICAL (projection threshold)

**IMPORTANT:** MVP code default = 0.5 (INCONSISTENT - requires fix)

**Critical distinction:**
- θ is OBSERVATION parameter (LAYER 2)
- NOT dynamics parameter (LAYER 1)
- Changing θ changes visibility, NOT existence

**Physical interpretation (LAYER 3 language):**
- High κ → stable, geometric shortcut (ER bridge)
- Low κ → unstable, correlations only (EPR without ER)

---

## Observables (LAYER 2: What We Measure)

All observables are DERIVED from CORE via projection Πθ.

### Visible Edges

**Definition:** Count of edges with κ ≥ θ

**Formula:**
```
N_vis(θ) = |{e ∈ E | κ(e) ≥ θ}|
```

**Ontological status:** Epistemological (depends on θ choice)

**NOT a CORE property:** Different θ gives different count, but CORE unchanged.

---

### Clusters (LAYER 2/3: Projected Structures)

**Definition:** Connected components in visible graph

**Ontological status:** 
- LAYER 2: Topological feature of projection
- LAYER 3: Interpreted as "objects" or "matter"

**CRITICAL:** Clusters are projection artifacts, NOT CORE entities.

**Correct language:**
- ✅ "Clusters observed in projection at θ=0.25"
- ❌ "Objects exist in the system"
- ✅ "Stable structures visible at this threshold"  
- ❌ "Matter has formed"

---

## Interpretations (LAYER 3: Emergent Language)

These are useful analogies for connecting to physics, NOT definitions.

### Locality

**CORE (LAYER 1):** Local interactions (triangle closure, neighbors).  
**FRACTURE (LAYER 2):** May appear nonlocal (projection artifact).

**Key insight:** Entanglement = single Δ-channel in CORE, not two correlated states.

---

### Entanglement

```
Ψ_AB := Δ_AB
```

**NOT:** ψ_A ⊗ ψ_B (product states)  
**INSTEAD:** Single relational channel (CORE entity)

**Bell correlations:** Emerge from projection statistics, not "spooky action".

---

### ER=EPR

**High κ (LAYER 2):** Geometric shortcut visible (ER bridge interpretation)  
**Low κ (LAYER 2):** Correlations only visible (EPR without ER interpretation)

**Prediction:** κ determines transition from geometric to statistical correlation.

**Ontological note:** This is LAYER 3 interpretation. CORE just has relations with different κ values.

---

### Gravity (LAYER 3 Interpretation)

**Hypothesis:**
```
G_μν ∼ F(ρ_Δ, ∇κ, P_CORE, warp_pressure)
```

**Tension as mass analog:** Accumulated constraint → gravitational source candidate

**Emergent time:** Pressure → time dilation analog

**CRITICAL:** This is interpretation. Testing "does gravity emerge" means testing "do correlation patterns match GR predictions", NOT "does gravity exist in CORE".

---

### Dark Matter (LAYER 3 Speculation)

**Hypothesis:** Stable Δ-channels without baryonic projection.

**Prediction:** High κ but σ ≠ 0 (non-standard interaction type).

**Status:** Speculative, requires S3 implementation.

---

## Experimental Predictions (Testing LAYER 2 Patterns)

### SQUID Topology Hypothesis

**Formula:**
```
S_I(f) = S_I^std(f) + β·C_cycles·f^(-α)
```

**Key prediction:**
```
A_n / A_1 = n (amplitude ratio = cycle count)
```

**Status:** ✅ DERIVED, needs experimental test

**Falsification:** If ratio ≠ C_cycles → topology interpretation wrong

**Ontological note:** This tests projection signatures, not CORE directly.

---

### CHSH Violation

**Standard:** <CHSH> ≤ 2 (classical), ≈ 2.82 (QM)

**ROMION prediction:** Same violation magnitude, but:
- Topology-dependent
- Boundary condition variations testable
- Mechanism: Projection statistics, not "nonlocality"

**Status:** Needs full formalization

---

## Parameter Derivation Status

| Parameter | Current | Theory | Status | Layer |
|-----------|---------|--------|--------|-------|
| spawn_damping | 0.55 | α₁ from S1 | ❓ | CORE |
| spawn_threshold | 0.15 | Min κ for spawn | ❓ | CORE |
| reinforce_factor | 0.05 | Resonance | ❓ | CORE |
| decay | 0.008 | Base entropy | ❓ | CORE |
| decay_kappa_discount | 0.9 | κ protection | ❓ | CORE |
| W_max | 2.5 (theory) | Event horizon | ❓ | CORE |
| w_cap | 2.5 | Hard limit | ✅ | CORE |
| **theta** | **0.25 (theory)** | **Projection** | **✅** | **FRACTURE** |
| beta_2hop | 0.25 | 2-hop weight | ❓ | CORE |
| epsilon_spark | 0.0 | S2 tail? | 🔴 | DEPRECATED |
| spark_w | 0.0 | Spark strength | 🔴 | DEPRECATED |

**CRITICAL INCONSISTENCIES (require code fix in Phase B):**
- W_max: theory=2.5, code default=5.0
- theta: theory=0.25, code default=0.5

---

## Falsification Criteria

### What Would Disprove ROMION?

1. **SQUID C_cycles test fails:**
   - If A_n/A_1 ≠ n → topology mechanism wrong

2. **SOC disappears with theory-constrained parameters:**
   - If derived parameters kill SOC → approximations were load-bearing

3. **κ formula cannot be derived:**
   - If no consistent mapping exists → ad-hoc metric

4. **Quantum Spark cannot be derived from S2:**
   - If ε is truly magic → implementation cheated

5. **CHSH test shows no boundary dependence:**
   - If topology doesn't matter → projection mechanism wrong

**Ontological note:** All tests are LAYER 2 (projection patterns). We cannot directly test LAYER 1 (CORE).

---

## Theory Development Roadmap

### Phase 1: Semantic Cleanup (CURRENT)
- [x] Clarify CORE/FRACTURE/INTERPRETATION layers
- [ ] Verify code consistency with theory defaults
- [ ] Remove/deprecate Quantum Spark
- [ ] Separate S2 (SPEC) from Field-tail (MVP proxy)

### Phase 2: Parameter Validation
- [ ] Derive spawn_damping from α₁
- [ ] Justify W_max theoretically
- [ ] Map κ approximation to theory
- [ ] Verify Field-tail as valid S2 proxy

### Phase 3: New Predictions
- [ ] SQUID C_cycles experiment
- [ ] CHSH boundary variations
- [ ] Cluster gravity test (tension correlation)

### Phase 4: Full Formalism
- [ ] Implement S3 (type composition)
- [ ] Multi-σ interactions
- [ ] Dark matter analog (non-projecting channels)

---

## References

**Internal:**
- `docs/METHODOLOGY.md` - Metrics and fail-closed validation
- `docs/theory/MEASUREMENT_THRESHOLDS.md` - Three-threshold system
- `SPEC_S2_TAIL.md` - Field-tail proxy specification

**Physics:**
- Bell (1964) - Bell inequalities
- EPR (1935) - Entanglement paradox
- Maldacena-Susskind (2013) - ER=EPR conjecture
- CHSH (1969) - Testable inequality
- Aspect (1982) - Experimental violation
- Hensen (2015) - Loophole-free test

---

**Status:** SEMANTIC REFACTOR COMPLETE  
**Version:** 2.0 - Ontological layers clarified  
**Next:** Phase B code alignment (after METHODOLOGY.md refactor)
