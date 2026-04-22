# HYPOTHESIS — CWD Dipole (Loop-Repetition Cost Bias)

## Role

Testable hypothesis document.
Provides a ROMION-internal, falsifiable mechanism that can be compared to an external observational result.

This document:
- separates **External Observation** from **ROMION Hypothesis**,
- defines H1/H0, metrics, and falsification,
- does not modify canonical ontology (THEORY_V3.9.md).

---

## Epistemic Status

Category: HYPOTHESIS  
Authority level: Testable / falsifiable  
Not canonical. Not a domain-mapping document.

---

## 1) External Observation (Source Record Only)

### 1.1 Paper Identity

**Title:** Overdispersed Radio Source Counts and Excess Radio Dipole Detection  
**Journal:** Physical Review Letters 135, 201001 (2025)  
**DOI:** 10.1103/6z32-3zf4  
**Authors:** Lukas Böhme et al.  
**Received / revised / accepted / published:** included in PDF front matter  
Source: [6z32-3zf4.pdf](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563&EntityRepresentationId=709f1c97-ded6-45a6-b564-1f62298931c2).

[1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)

### 1.2 Key Result (Quantitative)

The paper reports that the **source count dipole** exceeds the expected kinematic dipole amplitude from standard cosmology by a factor:

**(3.67 ± 0.49) × d_exp**, described as a **5.4σ discrepancy**.

This result is obtained by combining:
- NVSS,
- RACS-low,
- LoTSS-DR2,

and using a Bayesian estimator accounting for **overdispersion** with a **negative binomial distribution**.

[1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)

### 1.3 Direction (Quantitative)

For the combined measurement (LoTSS-DR2 + RACS-low + NVSS), the reported direction is aligned with the CMB dipole within 1σ, with an example direction quoted as:

(α_RA, δ) = (165° ± 8°, −11° ± 11°), and angular separation Δθ ≈ (5° ± 10°) from the CMB dipole direction.

[1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)

### 1.4 Method Summary (As Stated)

- Counts-in-cells are evaluated using HEALPix N_side = 32 (12,288 cells). [1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)
- Overdispersion from multi-component radio sources is modeled with a negative binomial distribution, derived via a compound Poisson (Cox) process. [1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)
- The dipole is introduced as a modulation of expected counts per cell:
  λ_i = λ (1 + d cos θ_i), and analogously r_i for the negative binomial parameter. [1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)
- The estimator maximizes the log-likelihood for the negative binomial dipole model; parameters estimated include r, d, and direction. [1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)

The paper also notes survey-dependent robustness issues (e.g., declination bias/variance in LoTSS-DR2 due to limited sky coverage; systematic indications in VLASS; TGSS amplitude potentially affected by flux calibration systematics), and selects RACS-low and NVSS as robust under the unconstrained estimator, with LoTSS-DR2 added to strengthen combined constraints. [1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)

---

## 2) ROMION Hypothesis (Internal Mechanism)

### 2.1 Core Idea (ROMION-Internal)

H1 proposes that an apparent excess dipole in number counts can arise from a **purely structural bias** in emergence probability:
- regions with higher **loop repetition** (higher recurrence of compatible Δ-loop patterns) acquire lower effective transition cost,
- this induces a persistent anisotropy in emergent schema frequency and/or observability.

This mechanism:
- introduces no new substances,
- is non-teleological,
- operates as a bias in configuration-space accessibility.

(This is a ROMION-internal hypothesis; it is not asserted as the correct explanation of the PRL result.)

---

## 3) Formal Hypothesis Statements

### H1 (ROMION CWD Bias Hypothesis)

There exist ROMION regimes in which a persistent directional anisotropy in observable counts emerges because the effective stabilization / transition cost decreases with local loop repetition count N_Ω.

Operationally, the probability of generating or maintaining compatible schemas in region Ω is increased relative to baseline, producing an excess dipole-like anisotropy in projected observables.

### H0 (Null Hypothesis)

Under the same experimental protocol, loop repetition does not generate sustained anisotropy beyond statistical fluctuations and projection artifacts; any dipole-like signal averages to ~0 across seeds and runs.

---

## 4) Operationalization in ROMION Terms

### 4.1 Required Internal Quantities (ROMION)

- N_Ω: loop repetition count (or proxy) in region Ω
- η(N): amplification factor of schema persistence/emergence probability as a function of N
- A(t): anisotropy index of observable counts (defined below)

NOTE: The definition of “region Ω” must be graph-based and coordinate-free (consistent with THEORY rules).

### 4.2 Minimal Metrics (MVP-Compatible)

#### Metric M1 — Loop repetition proxy
- loops_found@t: number of detected Δ-loops at tick t (or within a window)
- repeat_rate@t: fraction of loops whose canonical signature repeats vs previous ticks

(If loop detection is not implemented yet, this metric is SPEC and blocks empirical evaluation.)

#### Metric M2 — Structural anisotropy proxy (counts)
Define a deterministic partition of the observable domain into two regions (L/R) by a structural rule, then compute:
- counts_L@t, counts_R@t
- dipole_proxy@t = |counts_L@t - counts_R@t| / (counts_L@t + counts_R@t + ε)

This is a ROMION-internal anisotropy proxy and does not assume physical coordinates.

#### Metric M3 — Coupling between repetition and anisotropy
Compute correlation across runs or time windows:
- corr( repeat_rate , dipole_proxy )

---

## 5) Falsification Criteria (Fail-Closed)

This hypothesis is **falsified (in the ROMION simulation context)** if, under pre-registered conditions:

1) repeat_rate increases (or N_Ω differs across regions), but
2) dipole_proxy remains statistically indistinguishable from baseline across seeds,
3) and no stable positive correlation corr(repeat_rate, dipole_proxy) is observed.

Additionally, invalid runs are excluded per fail-closed policy.

---

## 6) Relationship to External Observation (How to Compare)

This document does not claim equivalence between:
- dipole_proxy in ROMION, and
- the PRL radio source count dipole amplitude.

Instead, it defines a comparison strategy:

- External: PRL reports a dipole amplitude ratio (3.67 ± 0.49) × d_exp and 5.4σ discrepancy using a negative-binomial estimator. [1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)
- Internal: ROMION tests whether a loop-repetition cost bias can produce a sustained dipole-like anisotropy proxy and whether its magnitude can be tuned to a stable regime.

A “match” would mean only:
- consistency of mechanism producing a stable anisotropy signal,
not confirmation of the external claim’s causal origin.

---

## 7) Notes on External Systematics (Source Record)

The PRL paper explicitly considers multiple explanations for the excess dipole amplitude, including:
- greater-than-expected contamination from local sources producing a clustering dipole,
- local bulk flow beyond ΛCDM expectations,
- systematics such as calibration and survey geometry effects,
- and notes that sparse sky sampling in another survey can yield a dipole consistent with CMB expectation. [1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)

These are external considerations and do not affect ROMION hypothesis logic, except as guidance for what confounds a simulation should be robust against.

---

## 8) Implementation Dependencies (Non-Canonical Checklist)

To test this hypothesis in ROMION simulation, the following capabilities must exist:

- Δ-loop detection and canonical signature (needed for repeat_rate)
- deterministic region split for anisotropy proxy
- standard fail-closed validity gating

These are implementation requirements and belong outside canonical theory.

---

## 9) Status

- External observation: established in PRL paper (source record only). [1](https://onedrive.live.com?cid=F9DADBED595BF469&id=F9DADBED595BF469!s49bbf388d4bd487cbbb5390482168563)
- ROMION mechanism: HYPOTHESIS (requires simulation tests; not yet confirmed).

---

_End of HYPOTHESIS_CWD_DIPOLE_