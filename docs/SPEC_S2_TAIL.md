# S2-tail Implementation Spec

**Status:** [SPEC] - Theoretical specification  
**Implementation:** Partial (field_tail as proxy, not true S2 Antipair)  
**Post-audit note:** S2 Antipair remains SPEC (KROK 5 clarification)  
**See also:** IMPLEMENTATION_STATUS.md (S2 marked SPEC)

**Goal:** Implement long-range weak bridges (S2-tail) to create P(bridge>0|dist>=2) > 0

---

## Mechanism (per tick):

### 1. Build Structures (existing):
- Clusters using `wcluster` (unchanged)
- Background graph using `wdist` for distance computation

### 2. Sample Candidate Pairs:
- Sample `tail_samples` pairs of nodes from **different clusters**
- Compute distance `d` in background graph (cluster-to-cluster)
- Only consider pairs with `d >= 2`

### 3. Acceptance Probability:
```python
p = tail_base_rate * g(local_frust_or_pressure) * exp(-lambda_dist * d)

where:
  g(x) = min(1.0, x / frust_x0)  # Simple frustratio scaling
  or
  g(x) = 1 / (1 + exp(-(x - frust_x0) / frust_scale))  # Sigmoid
```

### 4. Add Bridge Edge:
- If accepted: add edge with weight `tail_w` (near min_weight)
- **Must NOT merge clusters** (weight < wcluster)
- This is "field", not "matter"

---

## Parameters:

```python
tail_samples: int = 200       # Candidate pairs per tick
tail_base_rate: float = 0.01  # Base acceptance probability
lambda_dist: float = 0.5      # Distance decay factor
tail_w: float = 0.008         # Bridge weight (< wcluster, > min_weight)
frust_x0: float = 0.5         # Frustration threshold
frust_scale: float = 0.2      # Sigmoid width (if sigmoid used)
enable_s2_tail: bool = False  # Default OFF
```

---

## CLI Flags:

```bash
--enable-s2-tail              # Enable mechanism
--tail-samples 200            # Number of candidates per tick
--tail-base-rate 0.01         # Base probability
--lambda-dist 0.5             # Distance decay
--tail-w 0.008                # Bridge weight
--frust-x0 0.5                # Frustration threshold
```

---

## Acceptance Test:

### With S2-tail enabled @ tick 400+:
```python
# In gravity_test output:
P(bridge>0|dist=2) > 0   # Even if small (0.01-0.10)
P(bridge>0|dist=3) > 0   # Should decay with distance
P(bridge>0|dist=4) > 0   # Smaller than dist=3

# Distance decay pattern:
P(dist=2) > P(dist=3) > P(dist=4) > ...
```

### Critical Constraint:
- Bridges must stay below `wcluster` (no cluster merging)
- Keep clusters unchanged from baseline
- Only bridges at dist>=2 should appear

---

## Implementation Location:

Add to `core/engine.py` after spawn step, before decay:

```python
def update_tick(self):
    self.tick += 1
    
    # Existing: spawn, reinforce
    self._spawn_new_edges()
    self._reinforce_active()
    
    # NEW: S2-tail (if enabled)
    if self.enable_s2_tail:
        self._add_s2_tail_bridges()
    
    # Existing: decay, remove
    self._decay_edges()
    self._remove_weak()
```

---

## Minimal Footprint:

- No changes to cluster definition
- No changes to existing spawn/decay/tension
- Self-contained in one function `_add_s2_tail_bridges()`
- Can be disabled via flag (default OFF)

---

**Status:** Ready for implementation
**Priority:** #1 (Critical for long-range field)
