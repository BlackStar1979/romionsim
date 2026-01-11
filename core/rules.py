# romionsim/core/rules.py
"""
Evolution rules for ROMION dynamics.

Implements:
- rule_spawn: S1 (Closure) + Resonance
- rule_propagate: Decay with κ-discount
- rule_normalize: Pressure clamping (event horizon)

Quantum Spark: Available but DISABLED by default.
Requires theoretical derivation from S2 (Antipair) before use.
"""

import random
from .graph import Graph


def rule_spawn(G: Graph, params: dict) -> tuple[int, int]:
    """
    SPAWN + RESONANCE rule.
    
    Implements S1 (Closure): w'(A→B) = α₁ · (∏ κ(e)·w(e))^(1/|γ|)
    
    Process:
    1. Triangle closure: If A→C→B exists, create/strengthen A→B
    2. Resonance: Existing shortcuts get boosted (free energy)
    3. [OPTIONAL] Quantum Spark: Random weak edges (S2-derived only)
    
    Args:
        G: Graph to evolve
        params: Configuration dict with:
            - spawn_threshold: Min κ for spawning parent
            - spawn_samples: Number of edges to sample
            - spawn_damping: α₁ factor for new edges
            - reinforce_factor: Boost for resonance
            - spawn_cap: Max new edges per tick
            - w_cap: Hard weight limit
            - epsilon_spark: Spark probability (if enabled)
            - spark_w: Spark strength (if enabled)
    
    Returns:
        (created_count, reinforced_count)
    """
    new_proposals = {}
    reinf_proposals = {}
    
    threshold = params.get('spawn_threshold', 0.5)
    
    # Sample edges (O(E²) is prohibitive, so we sample)
    all_edges_list = list(G.all_edges())
    sample_size = min(len(all_edges_list), params.get('spawn_samples', 100))
    sample_edges = random.sample(all_edges_list, sample_size)
    
    spawn_damping = params.get('spawn_damping', 0.5)     # α₁ from S1
    reinforce_factor = params.get('reinforce_factor', 0.1)
    w_cap = params.get('w_cap', 5.0)
    
    # --- TRIANGLE CLOSURE (S1) ---
    for e1 in sample_edges:
        # Only stable edges can spawn offspring
        if e1.kappa_cache < threshold:
            continue
        
        ends = [e1.u, e1.v]
        for i, center_node in enumerate(ends):
            other_node = ends[1 - i]
            
            # Look for neighbor k to close triangle: other → center → k
            for k, e2 in G.adj[center_node].items():
                if k == other_node:
                    continue
                if e2.kappa_cache < threshold:
                    continue
                
                # Signal strength = geometric mean of parents
                # This is S1 with |γ|=2: (w₁·w₂)^(1/2)
                signal = (e1.w * e2.w) ** 0.5
                
                # Unique key for potential shortcut
                low, high = (other_node, k) if other_node < k else (k, other_node)
                
                existing = G.get_edge(low, high)
                
                if existing:
                    # RESONANCE: Edge exists, signal strengthens it
                    # This is the only source of free energy (reward for coherence)
                    boost = signal * reinforce_factor
                    target_w = existing.w + boost
                    
                    if (low, high) in reinf_proposals:
                        reinf_proposals[(low, high)] = max(
                            reinf_proposals[(low, high)], target_w
                        )
                    else:
                        reinf_proposals[(low, high)] = target_w
                else:
                    # SPAWN: Edge doesn't exist, create weakened version
                    # Damping = cost of creation (child weaker than parents)
                    target_w = signal * spawn_damping
                    
                    if (low, high) in new_proposals:
                        new_proposals[(low, high)] = max(
                            new_proposals[(low, high)], target_w
                        )
                    else:
                        new_proposals[(low, high)] = target_w

    # Apply changes with limits
    
    # 1. New edges (quantity limit prevents memory explosion)
    spawn_cap = params.get('spawn_cap', 500)
    new_items = list(new_proposals.items())
    if len(new_items) > spawn_cap:
        random.shuffle(new_items)
        new_items = new_items[:spawn_cap]
        
    created_count = 0
    for (u, v), w in new_items:
        G.add_edge(u, v, w, limit=w_cap)
        created_count += 1
        
    # 2. Reinforcements (weight limit, no quantity limit - resonance is natural)
    reinf_count = 0
    for (u, v), w in reinf_proposals.items():
        G.add_edge(u, v, w, limit=w_cap)
        reinf_count += 1

    # --- QUANTUM SPARK (DEPRECATED - DO NOT USE) ---
    # 
    # ⚠️ WARNING: This feature is DISABLED by default (epsilon_spark=0.0)
    # 
    # **DEPRECATED as of 2026-01-09:** Quantum Spark has no theoretical derivation
    # from S2 (Antipair). It is a MAGIC FEATURE that was added speculatively.
    # 
    # Theoretical status: UNVERIFIED / DEPRECATED
    # - Cannot be derived from S2 formula: w'(e†) = α₂ · w(e) · exp(-μ·Frust(e))
    # - No falsifiable predictions
    # - Parameters (epsilon_spark, spark_w) are ad-hoc tuning
    # 
    # Original hypothesis: ε_spark = P(w'(e†) > w_min | Frust >> 1)
    #                       i.e., rare spontaneous antipairs in high-frustration regions
    # 
    # **Action required:** Remove this feature in future code cleanup.
    # **Until removed:** KEEP DISABLED (epsilon_spark=0.0)
    # 
    # If you enable this without theoretical justification, results are INVALID
    # per ROMION methodology (no magic constants, only theory-derived parameters).
    
    eps = params.get("epsilon_spark", 0.0)
    spark_w = params.get("spark_w", 0.0)
    
    sparks_created = 0
    if eps > 0.0 and spark_w > 0.0:
        # This code path should NEVER execute in valid ROMION experiments
        import warnings
        warnings.warn(
            "Quantum Spark is DEPRECATED and has no theoretical derivation. "
            "Results using epsilon_spark > 0 are methodologically invalid.",
            DeprecationWarning,
            stacklevel=2
        )
        
        num_sparks = int(max(0, round(G.num_nodes * eps)))
        num_sparks = min(num_sparks, 50)  # Safety cap

        for _ in range(num_sparks):
            u = random.randrange(G.num_nodes)
            v = random.randrange(G.num_nodes)
            if u == v:
                continue
            
            low, high = (u, v) if u < v else (v, u)
            
            # Only create if edge doesn't exist (don't disturb existing matter)
            if G.get_edge(low, high) is None:
                if G.add_edge(low, high, spark_w, limit=w_cap):
                    sparks_created += 1

    return created_count + sparks_created, reinf_count


def rule_propagate(G: Graph, params: dict) -> int:
    """
    PROPAGATE / DECAY rule.
    
    Implements entropy and noise cleaning.
    Smart decay: stable loops (high κ) decay slower.
    
    Args:
        G: Graph to evolve
        params: Configuration dict with:
            - decay: Base decay rate
            - min_weight: Minimum weight threshold (vacuum cleaner)
            - decay_kappa_discount: κ protection factor
    
    Returns:
        Number of edges removed
    """
    base_decay = params.get('decay', 0.01)
    min_w = params.get('min_weight', 0.001)
    kappa_discount = params.get('decay_kappa_discount', 0.9)
    
    to_remove = []
    
    for key, edge in list(G.edges.items()):
        k = edge.kappa_cache
        
        # SMART DECAY: Cost of existence decreases with stability
        # More needed (part of loop) → less energy lost
        current_decay = base_decay * (1.0 - kappa_discount * k)
        
        # Always keep minimum decay (5% of base) - nothing lives forever without resonance
        current_decay = max(current_decay, base_decay * 0.05)
        
        edge.w *= (1.0 - current_decay)
        
        # Remove dead relations ("vacuum cleaner")
        if edge.w < min_w:
            to_remove.append(key)
            
    # Cleanup
    for key in to_remove:
        u, v = key
        del G.edges[key]
        del G.adj[u][v]
        del G.adj[v][u]
        
    return len(to_remove)


def rule_normalize(G: Graph, pressure_map: dict, params: dict) -> tuple[int, dict]:
    """
    NORMALIZE rule (Event Horizon).
    
    If sum of weights in node exceeds W_max, throttling occurs.
    Excess energy converts to Tension (gravity/mass).
    
    2-phase for determinism:
    1. Decision: compute scale per node
    2. Execution: apply interference on edges
    
    Args:
        G: Graph to normalize
        pressure_map: Dict[node_id -> pressure]
        params: Configuration dict with:
            - W_max: Maximum pressure per node
    
    Returns:
        (num_operations, tension_map)
    """
    W_max = params.get('W_max', 5.0)
    ops = 0
    overload_tension = {}
    
    # Phase 1: Decision (compute scale per node)
    node_scales = {u: 1.0 for u in range(G.num_nodes)}
    
    for u, pressure in pressure_map.items():
        if pressure > W_max:
            ops += 1
            scale = W_max / pressure
            node_scales[u] = scale
            overload_tension[u] = pressure - W_max

    # Phase 2: Execution (apply restriction interference on edges)
    if ops > 0:
        for edge in G.all_edges():
            scale_u = node_scales[edge.u]
            scale_v = node_scales[edge.v]
            # Restriction determined by "bottleneck" (min)
            if scale_u < 1.0 or scale_v < 1.0:
                edge.w *= min(scale_u, scale_v)

    return ops, overload_tension



def rule_field_tail(G: Graph, params: dict) -> int:
    """
    FIELD-TAIL: Long-range weak bridges (MVP proxy for field).
    
    **CRITICAL:** This is NOT S2 (Antipair). This is an EXPERIMENTAL PROXY.
    
    NAME CHANGE (2026-01-09): Renamed from "rule_s2_tail" to "rule_field_tail"
    to avoid confusion with true S2 (Antipair) mechanism which is UNIMPLEMENTED.
    
    **What this IS:**
    - MVP: Experimental proxy for long-range gravitational field
    - Mechanism: Random weak bridges at dist>=2, modulated by frustration
    - Status: Phenomenological (parameters not theory-derived)
    
    **What this is NOT:**
    - NOT S2 (Antipair): S2 = e† with w'(e†) = α₂ · w(e) · exp(-μ·Frust(e))
    - NOT theory-derived: Parameters are ad-hoc (tail_base_rate, lambda_dist)
    - NOT validated: No falsifiable predictions from ROMION theory
    
    **Terminology:**
    - OLD (incorrect): "S2-tail" - implied connection to S2 Antipair
    - NEW (correct): "field-tail" - explicit that this is field proxy only
    
    **DEFAULT: DISABLED** (enable_field_tail=False)
    Must be explicitly enabled via CLI flag.
    
    **Future Work:**
    When true S2 (Antipair) is implemented from theory, this becomes:
    - `rule_field_proxy()` - for phenomenological field tests (this function)
    - `rule_s2_antipair()` - for theoretical S2 mechanism (NEW, unimplemented)
    
    Mechanism (per tick):
    1. Sample candidate pairs from different clusters
    2. Compute distance in background graph
    3. Accept with P ~ frustration * exp(-lambda * dist)
    4. Add weak bridge (w ~ min_weight, field not matter)
    
    Args:
        G: Graph to evolve
        params: Configuration dict with:
            - enable_field_tail: Enable mechanism (default: False)
            - tail_samples: Candidate pairs per tick (default: 200)
            - tail_base_rate: Base acceptance probability (default: 0.01)
            - lambda_dist: Distance decay factor (default: 0.5)
            - tail_w: Bridge weight (default: 0.008)
            - frust_x0: Frustration threshold (default: 0.5)
            - wcluster: Cluster threshold (for finding different clusters)
            - wdist: Background graph threshold (for distance)
            - min_weight: Minimum edge weight (constraint)
    
    Returns:
        Number of bridges added
    """
    if not params.get('enable_field_tail', False):
        return 0  # Disabled by default
    
    # Parameters
    tail_samples = params.get('tail_samples', 200)
    tail_base_rate = params.get('tail_base_rate', 0.01)
    lambda_dist = params.get('lambda_dist', 0.5)
    tail_w = params.get('tail_w', 0.008)
    frust_x0 = params.get('frust_x0', 0.5)
    wcluster = params.get('wcluster', 0.02)
    wdist = params.get('wdist', 0.005)
    min_weight = params.get('min_weight', 0.005)
    
    # Safety: tail_w must be < wcluster (no cluster merging)
    if tail_w >= wcluster:
        tail_w = wcluster * 0.8  # Force below threshold
    
    # Safety: tail_w must be >= min_weight
    if tail_w < min_weight:
        tail_w = min_weight * 1.2
    
    # 1. Find clusters (components at wcluster threshold)
    clusters = _find_components(G, wcluster)
    
    if len(clusters) < 2:
        return 0  # Need at least 2 clusters
    
    # 2. Build background graph for distance (edges with w >= wdist)
    bg_graph = _build_background_graph(G, wdist)
    
    # 3. Sample candidate pairs from different clusters
    added = 0
    
    for _ in range(tail_samples):
        # Random pair of clusters
        c1, c2 = random.sample(clusters, 2)
        
        # Random nodes from each cluster
        u = random.choice(c1)
        v = random.choice(c2)
        
        # Skip if edge exists (check adj dict)
        if v in G.adj[u] or u in G.adj[v]:
            continue
        
        # Compute distance in background graph
        dist = _cluster_distance_bg(c1, c2, bg_graph)
        
        if dist is None or dist < 2:
            continue  # Only dist>=2
        
        # Compute frustration proxy (simple: pressure - W_max / 2)
        # Better: use actual Frust from metrics, but this is minimal
        pressure_u = sum(e.w for e in G.adj[u].values())
        pressure_v = sum(e.w for e in G.adj[v].values())
        frust = max(0, (pressure_u + pressure_v) / 2 - params.get('W_max', 2.5) / 2)
        
        # Frustration scaling g(x) = min(1, x / x0)
        g_frust = min(1.0, frust / frust_x0) if frust_x0 > 0 else 1.0
        
        # Acceptance probability
        import math
        p_accept = tail_base_rate * g_frust * math.exp(-lambda_dist * dist)
        
        if random.random() < p_accept:
            # Add weak bridge
            G.add_edge(u, v, tail_w)
            added += 1
    
    return added


def _find_components(G: Graph, threshold: float) -> list:
    """Find connected components using edges with w >= threshold."""
    visited = set()
    components = []
    
    for start in range(G.num_nodes):
        if start in visited:
            continue
        
        # BFS from start
        component = []
        queue = [start]
        visited.add(start)
        
        while queue:
            u = queue.pop(0)
            component.append(u)
            
            for v, edge in G.adj[u].items():
                if edge.w >= threshold and v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        components.append(component)
    
    return components


def _build_background_graph(G: Graph, threshold: float) -> dict:
    """Build adjacency dict for background graph (edges w >= threshold)."""
    bg = {u: set() for u in range(G.num_nodes)}
    
    for edge in G.all_edges():
        if edge.w >= threshold:
            bg[edge.u].add(edge.v)
            bg[edge.v].add(edge.u)
    
    return bg


def _cluster_distance_bg(c1: list, c2: list, bg_graph: dict) -> int:
    """
    Compute minimum distance between two clusters in background graph.
    
    Uses multi-source BFS from all nodes in c1 to find closest node in c2.
    """
    if not c1 or not c2:
        return None
    
    # BFS from all nodes in c1
    queue = [(u, 0) for u in c1]
    visited = set(c1)
    
    while queue:
        u, dist = queue.pop(0)
        
        # Check if we reached c2
        if u in c2:
            return dist
        
        # Expand neighbors in background graph
        for v in bg_graph.get(u, []):
            if v not in visited:
                visited.add(v)
                queue.append((v, dist + 1))
    
    return None  # No path found
