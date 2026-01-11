# Next Session TODO - Updated After Sweep Completion

**Status:** Sweep COMPLETE (18/18)  
**Date:** 2026-01-09  
**Context:** All immediate sweep tasks done, ready for next phase

---

## ✅ COMPLETED (This Session)

### Sweep Analysis
- ✅ All 18 runs analyzed
- ✅ Optimal η* identified (0.70)
- ✅ Freeze boundary documented (0.80-0.85)
- ✅ FINAL_RESULTS.md created
- ✅ Quick visualization done
- ✅ Statistical analysis complete

### Documentation
- ✅ ROADMAP.md updated (HIGH-1, HIGH-2 COMPLETE)
- ✅ STATUS.md updated
- ✅ README files updated (root + docs/)
- ✅ Session reports complete
- ✅ Audit performed

### Discoveries
- ✅ System size scaling understood
- ✅ R0 peak mechanism explained
- ✅ Anisotropy diagnostic validated

---

## 🔴 IMMEDIATE NEXT STEPS (Next Session)

### 1. Production Runs @ Optimal Parameters
**Priority:** HIGH  
**Time:** 2-3 hours

```bash
# Extended duration at optimal decay
python scripts/run_romion_extended.py \
  --ticks 1000 \
  --decay-scale 0.70 \
  --seed 42 \
  --dump-graph-every 50 \
  --out results/production_optimal_s42

# Multiple seeds for confidence
for seed in 123 7 99 202; do
  python scripts/run_romion_extended.py \
    --ticks 1000 \
    --decay-scale 0.70 \
    --seed $seed \
    --out results/production_optimal_s$seed
done
```

**Goals:**
- [ ] Verify 0.70 sustains activity to tick 1000
- [ ] Dense time series (every 50 ticks)
- [ ] 5 seeds for statistical confidence
- [ ] Document long-term behavior

---

### 2. System Size Sweep
**Priority:** HIGH  
**Time:** 4-6 hours

**Design:**
```
N ∈ [500, 1000, 2000, 4000]
decay ∈ [0.60, 0.70, 0.80, 1.00]
seeds: [42, 123]
Total: 4×4×2 = 32 runs
```

**Hypothesis:** Optimal decay scales with system size

**Goals:**
- [ ] Find decay*(N) relationship
- [ ] Verify freeze boundary scales
- [ ] Test universality of 0.70

**Expected findings:**
- Larger N tolerates higher decay
- Freeze boundary moves up with N
- May find scaling law: decay* ~ N^α

---

### 3. Anisotropy Continuous Tracking
**Priority:** MEDIUM  
**Time:** 2-3 hours

**Implementation:**
Add to core engine:
```python
# In core/engine.py main loop
if tick % 10 == 0:
    aniso = compute_anisotropy(graph, node2c)
    log_event("ANISO", tick, aniso)
```

**Goals:**
- [ ] Track anisotropy every 10 ticks
- [ ] Identify phase transition signatures
- [ ] Test as early warning system
- [ ] Validate @ optimal parameters

---

## 🟡 HIGH PRIORITY (This Week)

### 4. Dense Time Evolution Analysis
**Time:** 3-4 hours

Using production runs from #1:
- [ ] Plot bridges vs time (every 50 ticks)
- [ ] Capacity evolution curves
- [ ] Anisotropy timeline
- [ ] Spawn/decay balance
- [ ] Identify equilibrium state

### 5. Statistical Confidence Analysis
**Time:** 1-2 hours

- [ ] Bootstrap confidence intervals (optimal decay)
- [ ] Seed sensitivity (how much variation?)
- [ ] Outlier detection
- [ ] Power analysis (need more seeds?)

### 6. Publication-Ready Plots
**Time:** 2-3 hours

Create high-quality figures:
- [ ] Decay curve with error bars
- [ ] Freeze boundary visualization
- [ ] System size scaling plot
- [ ] Time evolution @ optimal

**Tools:** matplotlib, seaborn, or export to plotting software

---

## 🟢 MEDIUM PRIORITY (Next Week)

### 7. Theoretical Derivation
**Time:** 4-6 hours

**Goal:** Derive optimal decay from theory

Approach:
- [ ] Balance equation: spawn rate = decay rate
- [ ] Pressure dynamics at equilibrium
- [ ] Relate to graph size N
- [ ] Predict decay*(N)

### 8. Sensitivity Analysis
**Time:** 2-3 hours

Test robustness:
- [ ] Initial edge count variation
- [ ] Different spawn_scale values
- [ ] Tension_scale effects
- [ ] Random seed variation (10+ seeds)

### 9. Canonical Results Publication
**Time:** 3-4 hours

Location: `docs/SWEEP_RESULTS_CANONICAL.md`

**Sections:**
- Executive summary
- Complete methodology
- Full results table
- Statistical analysis
- Theoretical interpretation
- Implications for ROMION

---

## ⚪ LOW PRIORITY (Future)

### 10. Loop Detection [PHASE-2]
Requires new core modules (SPEC work)

### 11. Particle Classification [SPEC]
Requires loop detection first

### 12. Extended Parameter Space
- Different tension_scale
- Shock perturbations
- Combined parameters

---

## 🧹 CLEANUP & MAINTENANCE

### Code Cleanup
- [ ] Remove temp scripts from scripts/temp/
- [ ] Add docstrings to new functions
- [ ] Type hints for sweep tools
- [ ] Lint pass on all new code

### Documentation
- [ ] Verify all cross-references work
- [ ] Update file index
- [ ] Check for broken links
- [ ] Remove SUPERSEDED_ files (after verification)

### Git Hygiene
- [ ] Commit sweep results
- [ ] Tag version v2.4.0
- [ ] Update .gitignore
- [ ] Clean ignored files

---

## 📊 PRIORITY ORDER

### Week 1 (Next 2-3 sessions)
1. 🔴 Production runs @ optimal (0.70)
2. 🔴 System size sweep (N scaling)
3. 🟡 Dense time evolution analysis
4. 🟡 Statistical confidence

### Week 2
5. 🟡 Publication-ready plots
6. 🟢 Anisotropy continuous tracking
7. 🟢 Theoretical derivation
8. 🟢 Sensitivity analysis

### Week 3+
9. 🟢 Canonical results document
10. ⚪ Code cleanup & documentation
11. ⚪ Extended parameter space

---

## 🎯 SUCCESS CRITERIA

**Next session successful if:**
- [ ] At least 1 production run @ 0.70 complete (1000 ticks)
- [ ] System size sweep started (8+ runs)
- [ ] Time evolution data collected
- [ ] Path forward clear

**Bonus achievements:**
- [ ] Full system size sweep complete (32 runs)
- [ ] Scaling law identified
- [ ] Anisotropy tracking implemented
- [ ] Publication plots created

---

## 📝 NOTES FROM THIS SESSION

### Key Insights
- Optimal decay = 0.70 (universal for n=1000, 2000)
- Freeze boundary sharp: 0.80 < critical < 0.85
- System size matters: larger N tolerates higher decay
- Anisotropy is reliable phase marker

### Open Questions
- What is decay*(N) function?
- Does 0.70 work for n=500? n=4000?
- How long does optimal sustain? (need 1000+ ticks)
- Can we derive optimal from theory?

### Technical Notes
- In-process sweep works perfectly
- Analysis pipeline mature
- Channel metrics validated
- No remaining bugs

---

## 🔬 EXPERIMENTS QUEUE

**Ready to run:**
1. Production @ 0.70 (5 seeds, 1000 ticks) ← DO FIRST
2. System size sweep (32 runs) ← DO SECOND
3. Dense evolution (checkpoint every 10 ticks)

**Needs design:**
4. Anisotropy continuous (core engine mod)
5. Theoretical validation tests
6. Sensitivity parameter space

**Future work:**
7. Loop detection [PHASE-2]
8. Particle physics [SPEC]

---

## ⚠️ IMPORTANT REMINDERS

1. **Always use optimal parameters** (decay=0.70) as baseline
2. **System size scaling** is HIGH priority
3. **Document everything** as you go
4. **Don't skip statistical analysis**
5. **Production runs first** - need confidence in 0.70

---

## 📚 REFERENCES

**This Session:**
- session_reports/2026-01-09/SESSION_100_PERCENT_COMPLETE.md
- tests/sweep_decay_inprocess/FINAL_RESULTS.md
- tests/test_c/R0_PEAK_ANALYSIS.md

**Roadmap:**
- docs/ROADMAP.md (updated)

**Status:**
- docs/STATUS.md (current)

---

**Updated:** 2026-01-09 (after sweep completion)  
**Previous version:** Pre-sweep action plan  
**Next review:** After production runs complete

---

**Remember:** The goal is SCIENCE, not just code. Understand WHY 0.70 works!
