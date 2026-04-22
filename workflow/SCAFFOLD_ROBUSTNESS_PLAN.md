# SCAFFOLD ROBUSTNESS PLAN — Current MVP Stability Scaffold

Purpose:
Define the smallest useful test grid for checking whether
current stability findings survive beyond the present fixed scaffold.

This plan is methodological.
It does not replace the current next engine step (`KROK 40`).
It creates the next honest lane for checking
how much of Stage 1 stability is real mechanics
and how much may still depend on scaffold choice.

---

## 1. CURRENT SCAFFOLD UNDER REVIEW

The present stability conclusions are conditional on:
- `seed = 42`
- `n_nodes = 50`
- `ticks = 100` in the historical runs
- `spawn_scale = 1.0`
- `decay_scale = 1.0`
- `w_init_min = 0.01`
- `w_init_max = 0.05`
- `p_add = 0.05`
- `w_prune = 0.0`

The currently swept variables in preserved Stage 1 work were:
- `p_decay`
- `w_visible`

---

## 2. MAIN QUESTION

Which fixed scaffold members are most likely to change
the Stage 1 mechanical reading if moved away from their current values?

The goal is not full parameter-space coverage.
The goal is to find the smallest set of robustness checks
that can separate:
- stable mechanics,
- from scaffold accidents.

---

## 3. PRIORITY ORDER

### Priority A — Seed robustness

Why first:
- old local materials show `seed = 42` was historically only a baseline seed,
  not the full protocol
- this is the cheapest meaningful robustness check
- if multi-seed behavior already breaks the ordering,
  deeper scaffold work should pause

What to test:
- replicate the current refine slice for a small seed set:
  - `42`
  - `123`
  - one additional seed not historically privileged

Minimal target:
- check whether monotonic degradation with increasing `w_visible`
  still holds at `p_decay = 0.995`

Success criterion:
- ordering remains directionally stable across seeds

Failure meaning:
- current Stage 1 conclusions are single-seed only

---

### Priority B — Node-count robustness

Why second:
- `n_nodes = 50` is one of the least historically grounded current choices
- it can strongly affect graph density, bridge opportunities, and decay behavior
- it is structurally more important than small weight-band tweaks

What to test:
- compare one short grid at:
  - `n_nodes = 50`
  - `n_nodes = 100`
  - `n_nodes = 200`

Keep other scaffold values fixed at first.

Minimal target:
- test whether the broad ordering by `p_decay` and `w_visible`
  survives size increase

Success criterion:
- direction of the ordering survives,
  even if absolute thresholds shift

Failure meaning:
- current Stage 1 reading is strongly size-specific

---

### Priority C — Injection-rate robustness (`p_add`)

Why third:
- `p_add = 0.05` is likely to matter directly for late-time persistence
- unlike neutral scales, it changes how much new structure is continually fed into CORE
- it has no strong old-baseline justification in the current MVP form

What to test:
- compare:
  - `p_add = 0.02`
  - `p_add = 0.05`
  - `p_add = 0.10`

Minimal target:
- test one representative refine subset near the old boundary

Success criterion:
- boundary ordering remains qualitatively similar,
  even if shifted

Failure meaning:
- current boundary picture is strongly feed-rate dependent

---

### Priority D — Initial weight band robustness

Why fourth:
- `w_init_min` / `w_init_max` shape the initial condition directly
- but they are slightly less urgent than seed, size, and injection
  because they mostly affect startup geometry

What to test:
- narrow band:
  - `0.005 .. 0.03`
- current band:
  - `0.01 .. 0.05`
- wider band:
  - `0.02 .. 0.08`

Minimal target:
- test whether broad Stage 1 ordering survives

Success criterion:
- startup changes move absolute values,
  but do not invert the broad stability ordering

Failure meaning:
- current conclusions are highly initializer-dependent

---

### Priority E — Prune policy robustness

Why fifth:
- `w_prune = 0.0` is explicit and important,
  but changing it changes the semantics of edge death more directly
- this is worth testing, but after simpler structural checks

What to test:
- `w_prune = 0.0`
- small positive prune threshold

Minimal target:
- determine whether persistence claims collapse immediately
  under mild pruning

Success criterion:
- broad ordering survives mild prune variation

Failure meaning:
- current persistence is strongly dependent on a no-prune convention

---

## 4. WHAT NOT TO TEST FIRST

Do not start robustness with:
- `spawn_scale`
- `decay_scale`

Reason:
- these are historically grounded neutral multipliers
- and in the current MVP runs they are not the highest-risk unknowns

Do not start with:
- full Cartesian sweeps across all scaffold members

Reason:
- too expensive
- too easy to recreate the old workflow bloat

---

## 5. MINIMAL EXECUTION STRATEGY

Keep robustness work narrow and layered:

1. one parameter family at a time
2. one small registered subset, not full Cartesian coverage
3. preserve the same metrics:
   - `FRACTURE_SURVIVAL_TIME(theta = 0.1)`
   - `TAIL_MEAN_VISIBLE_RATIO_N20`
4. use the new tick policy:
   - `300` default
   - `500` only if saturation persists

This gives comparability without recreating the entire Stage 1 campaign.

---

## 6. RECOMMENDED MICRO-ROADMAP

### Robustness R1 — Seed
- smallest cost
- highest immediate credibility gain

### Robustness R2 — Node count
- biggest structural unknown in the current scaffold

### Robustness R3 — Injection rate
- biggest dynamic unknown in the current scaffold

### Robustness R4 — Initial weight band
- startup robustness

### Robustness R5 — Mild prune policy
- semantic stress test

---

## 7. WHAT COUNTS AS A GOOD RESULT

A good robustness result does NOT require
all absolute numbers to stay the same.

The main thing to preserve is:
- broad ordering,
- monotonic direction,
- and qualitative regime separation.

If absolute thresholds move but ordering survives,
the mechanics look more real than accidental.

If ordering itself breaks,
the current Stage 1 picture must be narrowed again.

---

## 8. PRACTICAL RECOMMENDATION

When Stage 3A/3B/3C work reaches a natural pause,
the first robustness pass should be:

`R1 — seed robustness on the p_decay = 0.995 refine slice at 300 ticks`

Reason:
- cheapest meaningful test
- directly repairs the biggest known missing half
  of the old reproducibility protocol

End of plan
