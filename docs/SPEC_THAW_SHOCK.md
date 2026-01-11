# Thaw Shock Implementation Spec

**Status:** [SPEC] - Theoretical specification  
**Implementation:** None (remains future work)  
**Post-audit note:** Valid specification for future Option A (P0 Engine Cleanup)

**Goal:** Make shock work by creating structural changes (fracture) to escape frozen attractor

---

## Problem:

Current shock (R5) fails because:
- Frozen state has NEW=0, RMV=0
- Increasing spawn/decay multipliers has no edges to act on
- System is trapped in attractor

---

## Solution: Fracture Mode

### Mechanism:

During shock window:

1. **Identify Target Clusters:**
   - Find largest clusters (by node count)
   - Target top 1-3 clusters

2. **Controlled Fracture:**
   - Remove `fracture_rate` of **highest-weight edges** in target clusters
   - This creates structural instability
   - Forces system out of frozen basin

3. **Halo Rebuild (Optional):**
   - Lower decay for weak edges during shock
   - Allows new connections to form
   - Rebuilds field around fractured clusters

---

## Parameters:

```python
shock_mode: str = "default"     # "default" or "fracture"
fracture_rate: float = 0.15     # Fraction of heavy edges to remove
fracture_targets: int = 3       # Number of largest clusters to fracture
fracture_threshold: float = 0.5 # Only remove edges w > threshold * max_weight
decay_weak_mult: float = 0.5    # Decay multiplier for weak edges during shock
```

---

## CLI Flags:

```bash
--shock-mode fracture         # Use fracture mode
--shock-fracture-rate 0.15    # Remove 15% of heavy edges
--shock-fracture-targets 3    # Target 3 largest clusters
--shock-fracture-threshold 0.5  # Only edges > 50% of max weight
--shock-decay-weak-mult 0.5   # Reduce decay for weak edges
```

---

## Example Usage:

### Baseline Shock (fails):
```bash
python run_romion_extended.py --ticks 1200 \
  --shock-tick 650 --shock-len 120 \
  --shock-spawn 1.5 --shock-decay 0.7
```

### Fracture Shock (should work):
```bash
python run_romion_extended.py --ticks 1200 \
  --shock-mode fracture \
  --shock-tick 650 --shock-len 120 \
  --shock-fracture-rate 0.15 \
  --shock-fracture-targets 3 \
  --shock-decay-weak-mult 0.5
```

---

## Acceptance Test:

### Expected Results:

**Pre-shock (tick 600):**
```
Bridges: 0 (frozen)
Clusters: ~131
NEW: 0, RMV: 0
```

**During shock (tick 650-770):**
```
NEW: > 0 (new edges spawning!)
RMV: > 0 (fractured edges removed)
Bridges: starts increasing
```

**Post-shock (tick 800+):**
```
Bridges: > 0 (some persistence)
If S2-tail enabled: P(bridge>0|dist>=2) > 0
```

---

## Implementation Location:

Modify shock handling in `core/engine.py`:

```python
def _apply_shock(self):
    """Apply shock parameters during shock window."""
    if not self.in_shock_window():
        return
    
    if self.shock_mode == "fracture":
        # NEW: Fracture mode
        self._fracture_largest_clusters()
        self._adjust_decay_for_shock()
    else:
        # Existing: parameter multipliers
        self._apply_spawn_multiplier()
        self._apply_decay_multiplier()
```

---

## Fracture Logic:

```python
def _fracture_largest_clusters(self):
    """Remove heavy edges from largest clusters."""
    
    # 1. Identify largest clusters
    clusters = self._find_components(threshold=self.wcluster)
    largest = sorted(clusters, key=len, reverse=True)[:self.fracture_targets]
    
    # 2. Find heavy edges in these clusters
    heavy_edges = []
    max_weight = max(e[2] for e in self.graph.edges if e[2] > 0)
    threshold = max_weight * self.fracture_threshold
    
    for cluster in largest:
        for u, v, w in self.graph.edges:
            if u in cluster and v in cluster and w > threshold:
                heavy_edges.append((u, v))
    
    # 3. Remove fraction of heavy edges
    n_remove = int(len(heavy_edges) * self.fracture_rate)
    to_remove = random.sample(heavy_edges, n_remove)
    
    for u, v in to_remove:
        self.graph.remove_edge(u, v)
```

---

## Why This Should Work:

1. **Creates Instability:**
   - Removing heavy edges breaks frozen structure
   - Forces system to reorganize

2. **Allows New Spawn:**
   - Fractured clusters have higher frustration
   - spawn mechanism can act again

3. **Escapes Attractor:**
   - Structural change moves system out of basin
   - Not just parameter tweaking

4. **Theory-Consistent:**
   - Mimics "stress fracture" in material
   - Frustration-driven reorganization

---

## Comparison to Current Shock:

| Aspect | Current (R5) | Fracture |
|--------|--------------|----------|
| Mechanism | Multiply spawn/decay | Remove heavy edges |
| In frozen state | No effect (NEW=0) | Creates instability |
| Exit attractor | ❌ No | ✅ Yes |
| Theory basis | Parameter tweak | Structural fracture |

---

**Status:** Ready for implementation
**Priority:** #2 (Important for second wave testing)
**Depends on:** S2-tail (for dist>=2 bridges after shock)
