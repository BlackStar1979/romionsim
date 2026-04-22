# OLDIES EVOLUTION REVIEW — ROMION

Purpose:
Capture what the historical materials in `workflow/oldies/` actually teach us
for the current rebuild of `romionsim`,
without importing old chaos, inflated process, or invalid claims.

Date:
2026-04-20

Status:
Active historical synthesis.
This is not canonical theory.
It is an operational reading note for the current rebuild.

---

## 1. Scope of review

Reviewed sources included:
- `workflow/oldies/GPT_ROMION_EVOLUTION.md`
- `workflow/oldies/GPT_memory_extract.txt`
- `workflow/oldies/20260109/dla_claude.txt`
- `workflow/oldies/20260108/theory_update_description.txt`
- `workflow/oldies/20260111/elements.txt`
- `workflow/oldies/CLAUDE_WORKFLOW_V2.md`
- `workflow/oldies/20260115/ROMION_AUDIT_REPORT.md`
- `workflow/oldies/20260115/ROMION_FINAL_AUDIT_REPORT.md`
- selected files from `workflow/oldies/romionsim_old_repos/romionsim1/`
  including `README.md`, `docs/THEORY.md`, `docs/METHODOLOGY.md`,
  `docs/theory/MEASUREMENT_THRESHOLDS.md`, `docs/IMPLEMENTATION_STATUS.md`,
  and `research/2026-01-08_session/SESSION_REPORT.md`

Also observed:
- large historical data holdings under `workflow/oldies/oldromion/`
- telescope / detector data traces and analysis artifacts in old research trees

---

## 2. High-confidence lessons from theory evolution

### 2.1 The durable core of the theory is narrower than many old materials suggest

Across the old materials, the most stable conceptual spine is:
- relations are primary
- CORE is ontologically primary
- FRACTURE is emergent / observed
- the CORE/FRACTURE boundary matters
- projection/observables are epistemic, not ontological

This spine survives many generations of wording.

The old materials also show repeated expansion far beyond that spine:
- warp engineering
- detector blueprints
- large families of derived constants
- particle taxonomies
- cosmology-wide reinterpretations

These expansions are historically interesting,
but they are not equally grounded.

Operational lesson:
- preserve the narrow ontological spine as trustworthy
- treat the larger speculative envelope as historical exploration, not present implementation target

---

### 2.2 The "annual" version of ROMION is richer than the old code repos

One repeated historical diagnosis is correct and important:
the older repos often preserved the method,
but not the full maturity of the theory as you later framed it.

Repeatedly missing or flattened in old repos:
- `delta_zero` as an explicit attractor / pole of CORE behavior
- boundary as an active emergent interface, not merely thresholding
- Romionosphere as a named operational object
- explicit RI/SI discipline
- clear distinction between target formalism and current MVP implementation

Operational lesson:
- older repos are useful memory and warning systems
- they are not a complete substitute for the current conceptual canon in `docs/`

---

### 2.3 The strongest mature methodological insight from old repos was layer discipline

The old audited repo converged on a very strong rule set:
- L1-CORE
- L2-FRACTURE / projection
- L3-INTERPRETATION

and on the key sentence:
- projection and interpretation must never silently feed back into CORE

This is one of the most valuable recoveries from `oldies`.

Operational lesson:
- keep using this as a design guardrail
- current rebuild should continue preferring validator-first and contract-first work
- any future extension must clearly belong to one layer

---

## 3. High-confidence lessons from old process failures

### 3.1 Workflow bloat became a system of its own

Old materials show a pattern:
- many milestone files
- many audit files
- many status layers
- many "final" and "absolutely final" artifacts

This matches the failure mode already observed in practice:
the process started consuming more cognition than the code.

Operational lesson:
- current `workflow/` must stay smaller than the experiment itself
- prefer one living summary over many ceremonial reports
- archive historical complexity, do not recreate it

---

### 3.2 Packaging / audit completion was repeatedly mistaken for scientific completion

The 2026-01-15 audit reports are mainly packaging and engineering audits:
- PEP8
- CI/CD
- pre-commit
- structure cleanup
- tests

Those are useful,
but they do not establish theoretical correctness.

Operational lesson:
- treat engineering polish and scientific closure as separate axes
- do not let "audited / structured / packaged" masquerade as "validated theory"

---

### 3.3 Earlier models repeatedly over-claimed from exploratory or proxy results

Strong examples found in old materials:
- projection ratio near baryonic fraction
- phase propagation claims
- field-like interpretations
- S2-tail / proxy language drifting toward full-theory claims

The old repo also contains explicit self-corrections warning against this drift.

Operational lesson:
- keep using narrow wording:
  - "consistent with"
  - "support"
  - "proxy"
  - "diagnostic"
- avoid upgrading proxies into ontology
- avoid turning interesting numerical echoes into cosmological proof

---

### 3.4 Data-fitting and invented constants were a real historical contamination path

The old session report identifies a concrete bad pattern:
- constants introduced without derivation
- equations invented to fit external data
- outputs then described as ROMION verification

This is one of the clearest anti-patterns in the archive.

Operational lesson:
- external data may constrain or challenge theory
- external data must not be used to backfill arbitrary engine constants
- no telescope / detector dataset may define a current engine parameter without explicit theory-side derivation and pre-registered test logic

---

## 4. Historical data assets present in oldies

The archive now contains substantial historical empirical material, including traces of:
- Chandra / X-ray holdings
- Fermi-LAT catalogs
- LIGO / Virgo / GWOSC-related HDF5 and AUXR workflows
- IceCube material
- MAGIC material
- additional astronomy / lensing related files

These holdings are valuable as:
- future empirical comparison sources
- provenance for old claims
- historical evidence of what was attempted

They are not, by themselves, current evidence for the rebuilt engine.

Operational rule:
- treat them as external-data assets waiting for a clean future protocol
- do not let them shape MVP engine semantics ad hoc

---

## 5. What oldies implies for the current rebuild

### 5.1 Good directions already recovered in the current rebuild

The current rebuild is aligned with the best part of the old mature method:
- layer separation
- fail-closed validation
- explicit prerelease language
- keeping theory and implementation status separate
- warning against over-reading short-horizon or scaffold-bound results

This is good and should continue.

---

### 5.2 KROK 40 should remain narrow

Nothing in oldies justifies jumping from the current Stage 3 work
into particle ontologies, cosmology, or telescope-backed claims.

The archive reinforces the opposite lesson:
- finish minimal engine semantics first
- validate each capability stage narrowly
- only then move outward

Therefore:
- KROK 40 should remain an interval-based validator step
- no thaw, no cosmology, no particle layer import, no empirical grand claims yet

---

### 5.3 Future theory-document gap worth tracking, but not forcing now

Old materials do suggest a real long-term documentation gap to revisit later:
- active boundary language
- `delta_zero`
- Romionosphere
- explicit theory-vs-MVP separation

But this should not be solved by speculative code changes.

Operational lesson:
- revisit those as documentation architecture work after the current engine stages are stronger

---

## 6. Things explicitly NOT to import from oldies into the current repo

Do not import as current truth:
- old "final" packaging claims
- old projection-ratio-to-baryons claim as if established
- arbitrary historical constants
- technology / detector / warp blueprints
- full particle taxonomy as if already supported by current engine
- any workflow shape that explodes file count and process load

Do not silently inherit:
- stale parameter defaults from old repos
- old labels that blurred proxy versus ontology
- external-data-derived heuristics

---

## 7. Things worth preserving as living guardrails

Preserve these lessons actively:
- CORE is primary
- projection is epistemic
- no backreaction without explicit modeling
- proxy is not ontology
- packaging is not validation
- historical datasets are not license for tuning constants
- workflow must remain smaller than the experiment

---

## 8. Current operational conclusion

The old archive is valuable mainly in three ways:
- as theory-memory
- as anti-pattern memory
- as a source of future empirical comparison assets

It does not change the immediate build order.

Current best next move remains:
- keep `KROK 40` narrow and validator-first
- keep scaffold robustness as a parallel methodological lane, not a derailment
- revisit broader theory-history imports only when the current engine stage reaches a natural pause

End of review
