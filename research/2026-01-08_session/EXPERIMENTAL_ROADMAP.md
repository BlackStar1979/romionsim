# ROMION Experimental Roadmap
# Detailed Protocol for Validation and Publication

**Version:** 1.0
**Date:** 2026-01-08
**Author:** Research collaboration (Michał + Claude)

---

## Executive Summary

This document outlines the experimental path to validate ROMION O'LOGIC theory
and prepare for academic publication. The roadmap is organized in phases with
clear milestones, success criteria, and fallback strategies.

---

## Phase 0: Foundation Solidification (Week 1-2)

### 0.1 Code Cleanup

**Objective:** Ensure all test code is production-ready and reproducible.

**Tasks:**
- [ ] Add docstrings to all analysis scripts
- [ ] Create `requirements.txt` for exact dependencies
- [ ] Add unit tests for core functions
- [ ] Verify all tests pass on fresh Python environment

**Files to audit:**
- `analysis/phase_propagation_test.py`
- `analysis/projection_ratio_test.py`
- `analysis/density_velocity_test.py`
- `analysis/gravity_test/` (entire module)

**Success criterion:** `pytest` passes with 100% on all platforms

### 0.2 Data Integrity

**Objective:** Document all simulation data and ensure reproducibility.

**Tasks:**
- [ ] Create manifest of all simulation files
- [ ] Record exact parameters for each run
- [ ] Verify simulation.jsonl files are complete
- [ ] Create checksums for data integrity

**Deliverable:** `data/MANIFEST.md` with complete provenance

### 0.3 Theory Documentation

**Objective:** Consolidate theory in single authoritative source.

**Tasks:**
- [ ] Copy Annexes M-V to `docs/theory/` in clean format
- [ ] Create `docs/theory/INDEX.md` with navigation
- [ ] Cross-reference code to theory sections
- [ ] Add derivation chains (where does each equation come from?)

**Deliverable:** Complete `docs/theory/` directory

---

## Phase 1: Projection Ratio Validation (Week 2-4)

### 1.1 Cross-Simulation Testing

**Objective:** Verify ~5% ratio is universal, not parameter-specific.

**Protocol:**
```
For each simulation in {R0, R1, R2, R3, R4, R5}:
    For each tick in {100, 200, 300, 400, 500}:
        Run projection_ratio_test.py
        Record: edge%, weight%, node% at θ = {0.3, 0.4, 0.5}
        
Compute:
    - Mean ratio across all runs
    - Standard deviation
    - Parameter sensitivity
```

**Success criterion:** Ratio consistently 3-10% at θ ≈ 0.5 across all runs

**Fallback:** If ratio varies wildly, identify which parameter controls it

### 1.2 Threshold Sensitivity Analysis

**Objective:** Determine if θ ≈ 0.5 is "natural" or arbitrary.

**Protocol:**
```
Vary θ from 0.0 to 1.0 in steps of 0.01
Plot: visible_fraction vs θ
Look for:
    - Inflection points
    - Phase transitions
    - Natural cutoffs
```

**Question to answer:** Is there a mathematical reason for θ ≈ 0.5?

### 1.3 Temporal Evolution

**Objective:** Track how projection ratio evolves over simulation time.

**Protocol:**
```
For tick in range(0, 1000, 10):
    Measure projection ratio at θ = 0.5
    
Plot: ratio vs tick
Look for:
    - Equilibrium value
    - Convergence time
    - Oscillations
```

**Success criterion:** Ratio converges to stable value (~5%)

---

## Phase 2: Phase Propagation Deep Dive (Week 4-6)

### 2.1 Pressure Cage Experiment

**Objective:** Verify photon can be "stopped" in dense regions.

**Protocol:**
```
1. Identify densest cluster in simulation
2. Inject phase signal at cluster center
3. Measure: does phase escape? How long until escape?
4. Compare with sparse region (should escape immediately)
```

**Prediction:** In sufficiently dense region, phase propagation → 0

**Success criterion:** Measurable difference in propagation time (>10x)

### 2.2 Interference Pattern Test

**Objective:** Verify "ways of possibility" - multiple simultaneous paths.

**Protocol:**
```
1. Create configuration with two paths A→B
2. Inject phase at A
3. Measure phase at B
4. Block one path, measure again
5. Compare: interference pattern should change
```

**Prediction:** Blocking path changes final amplitude (not just delays it)

### 2.3 CORE→FRACTURE Mapping

**Objective:** Derive projection function that maps 228% → ~5%.

**Hypothesis:** Multiple CORE paths average out in FRACTURE observation.

**Protocol:**
```
1. Measure propagation time across N paths
2. Compute: mean, std, distribution
3. Model: how does averaging reduce apparent effect?
4. Derive: projection function P(effect_CORE) → effect_FRACTURE
```

**Deliverable:** Mathematical model of projection

---

## Phase 3: Particle Physics Tests (Week 6-10)

### 3.1 Loop Detection Implementation

**Objective:** Implement Annex M (loop detection and classification).

**Tasks:**
- [ ] Implement `find_cycles(G, Lmax)` function
- [ ] Implement `canonical_signature(Cycle)` 
- [ ] Implement `cycle_metrics()` - L0, L1, μ, σ, Q_T
- [ ] Create `core/loops.py` module

**Test:** Verify detection on known graph with cycles

### 3.2 Fermion Classification

**Objective:** Classify loops as quark-like or lepton-like.

**Protocol based on Annex S-T:**
```
quark-like: 
    - L0 <= 5
    - μ >= μ0 (threshold)
    - Has color degeneracy (3 variants in same niche)
    
lepton-like:
    - No color degeneracy
    - Different Q_EM signature
```

**Test:** Count quark-like vs lepton-like in simulation

### 3.3 Pauli Exclusion Test

**Objective:** Verify identical fermion states are forbidden.

**Protocol from Annex P:**
```
1. Identify fermion state: (sig, core, Q_T, s, n)
2. Attempt to create second identical state in same niche
3. Verify: rejection or instability
```

**Success criterion:** pauli_rejects counter > 0

### 3.4 Baryon Formation

**Objective:** Detect proton/neutron-like structures.

**Protocol from Annex O:**
```
Baryon = triad of loops with:
    - Same core cluster
    - Color completeness (R, G, B)
    - Stability S(B) >= S0
    
proton = (u, u, d) configuration
neutron = (u, d, d) configuration
```

**Test:** Do stable triads form? Do they have expected properties?

---

## Phase 4: Astronomical Data Connection (Week 10-14)

### 4.1 Clean Data Analysis

**Objective:** Analyze raw telescope data WITHOUT ChatGPT constants.

**Available data:**
- Chandra X-ray (6 observations)
- Fermi-LAT (4FGL catalogs)
- LIGO/Virgo (AUXR_HDF_v2)

**Approach:**
```
1. Extract basic statistics (energy distribution, timing)
2. Do NOT apply any "ROMION corrections"
3. Compare with ROMION predictions:
   - Phase dispersion in different density regions?
   - Correlation with galactic structure?
```

### 4.2 Specific ROMION Predictions for Astronomy

**Prediction 1: Void vs Cluster photons**
- Photons through cosmic voids: less dispersion
- Photons through galaxy clusters: more dispersion
- Effect size: ~0.1-7% (author estimate)

**Prediction 2: Energy-dependent effects**
- Higher energy = stronger coupling to graph structure
- Expect slight energy-time correlation in transients

**Prediction 3: Gravitational lensing anomalies**
- "Dark matter" halos = dense CORE regions that don't project
- Lensing should occur where visible matter is absent

### 4.3 Falsification Criteria

**ROMION would be falsified if:**
1. Projection ratio is wildly different from ~5%
2. Phase propagation is FASTER in dense regions
3. No correlation between graph density and astronomical observables
4. Particle-like structures don't emerge from loops

---

## Phase 5: Publication Preparation (Week 14-20)

### 5.1 Technical Paper 1: Projection Ratios

**Target journal:** Journal of Complex Networks / Physical Review E

**Outline:**
```
1. Abstract: We study projection properties of hypergraph dynamics
2. Introduction: Relational approaches to emergence
3. Methods: Hypergraph simulation, projection thresholds
4. Results: Consistent ~5% projection ratio
5. Discussion: Potential implications (carefully stated)
6. Conclusion: Stable emergent property
```

**Key figure:** Projection ratio vs θ across all simulations

**Supplementary:** All code, data, reproduction instructions

### 5.2 Technical Paper 2: Phase Dynamics

**Target journal:** Physical Review E / Entropy

**Outline:**
```
1. Abstract: Phase propagation in discrete networks
2. Introduction: Information flow in complex systems
3. Methods: Phase field definition, propagation rules
4. Results: Density-dependent propagation speed
5. Discussion: Analogy to wave mechanics
6. Conclusion: Discrete phase dynamics framework
```

**Key figure:** Propagation time vs density

### 5.3 Theory Paper: ROMION Framework

**Target journal:** Foundations of Physics / Studies in History and Philosophy of Science

**Outline:**
```
1. Abstract: Relational ontology for emergent spacetime
2. Introduction: Problems with substantivalist spacetime
3. Formalism: CORE, FRACTURE, projection
4. Predictions: Particle emergence, "dark sector"
5. Connection to existing physics
6. Falsifiability and tests
7. Conclusion
```

**This paper references Papers 1-2 for empirical support.**

---

## Risk Analysis

### Risk 1: ~5% ratio is coincidence

**Mitigation:** 
- Test across many parameter values
- Derive theoretical reason for ratio
- Find additional correlating predictions

### Risk 2: Academic rejection

**Mitigation:**
- Start with technical papers (no extraordinary claims)
- Build credibility through reproducibility
- Engage with criticism constructively

### Risk 3: Priority/scooping

**Mitigation:**
- Prepint on arXiv immediately
- Document development history (this file)
- Timestamp all discoveries

### Risk 4: Implementation errors

**Mitigation:**
- Independent code review
- Unit tests for all functions
- Multiple team members reproduce results

---

## Success Metrics

### Minimum Success (Publishable)
- [ ] Consistent projection ratio across simulations
- [ ] Phase propagation density effect confirmed
- [ ] One technical paper accepted

### Target Success (Theory Viable)
- [ ] All Phase 1-3 tests pass
- [ ] Two technical papers accepted
- [ ] Theory paper submitted

### Maximum Success (Paradigm Shift)
- [ ] Astronomical predictions confirmed
- [ ] Independent replication by other groups
- [ ] Major journal publication on dark matter interpretation

---

## Timeline Summary

| Week | Phase | Key Milestone |
|------|-------|---------------|
| 1-2 | 0 | Code and docs ready |
| 2-4 | 1 | Projection ratio validated |
| 4-6 | 2 | Phase propagation understood |
| 6-10 | 3 | Particle physics tests |
| 10-14 | 4 | Astronomical connection |
| 14-20 | 5 | Papers written and submitted |

---

## Appendix: Quick Reference Commands

```bash
# Run projection ratio test
python analysis/projection_ratio_test.py --log <path> --tick <N>

# Run phase propagation test
python analysis/phase_propagation_test.py --log <path> --tick <N> --n-sources 15

# Run full test suite
pytest

# Generate all results for a simulation
./scripts/run_all_tests.sh <simulation_dir>
```

---

**Document status:** ACTIVE ROADMAP
**Next review:** After Phase 1 completion
**Owner:** Research collaboration
