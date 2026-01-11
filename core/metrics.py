# romionsim/core/metrics.py
"""
Metrics computation for ROMION observables.

Computes:
- Pressure: Local sum of weights
- Kappa (κ): Coherence/stability metric
  Formula: κ(e) ≈ (w·Rec) / (1 + pressure_factor)
  
Note: Current κ formula is APPROXIMATION.
Theoretical form: κ(e) = exp(-λ·Frust(e)) · Rec(e)/(Rec(e)+c)
Requires derivation from S1/S2/S3.
"""

import random
from .graph import Graph


def compute_metrics(G: Graph, params: dict) -> dict:
    """
    Compute global statistics and update κ cache in edges.
    
    Complexity optimized via 2-hop sampling.
    
    Args:
        G: Graph to analyze
        params: Configuration dict with:
            - beta_2hop: Weight for 2-hop paths in κ
            - twohop_sample: Sample limit for 2-hop neighbors
            - theta: Visibility threshold (for FRACTURE projection)
    
    Returns:
        Dict with:
            - pressure_map: Dict[node_id -> pressure]
            - mean_pressure: Average pressure
            - max_pressure: Maximum pressure
            - mean_kappa: Average κ across all edges
    """
    # 1. Pressure Map (local sum of weights)
    pressure_map = {i: 0.0 for i in range(G.num_nodes)}
    total_pressure = 0.0
    max_pressure = 0.0
    
    for u in range(G.num_nodes):
        p = sum(e.w for e in G.adj[u].values())
        pressure_map[u] = p
        total_pressure += p
        if p > max_pressure:
            max_pressure = p

    # 2. Kappa (Relational Coherence)
    # κ determines how much an edge is "part of a loop"
    
    beta = params.get('beta_2hop', 0.2)
    sample_limit = params.get('twohop_sample', 10)
    
    total_kappa = 0.0
    
    for edge in G.all_edges():
        u, v = edge.u, edge.v
        
        u_neigh = list(G.adj[u].keys())
        v_neigh = list(G.adj[v].keys())
        
        u_set = set(u_neigh)
        v_set = set(v_neigh)
        shared = u_set.intersection(v_set)

        # A. Triangles (shared neighbors - direct closure)
        triangle_strength = 0.0
        for k in shared:
            # Path weight = geometric mean
            w_path = (G.adj[u][k].w * G.adj[k][v].w) ** 0.5
            triangle_strength += w_path

        # B. 2-Hop (longer loops - sampled for performance)
        two_hop_strength = 0.0
        if beta > 0:
            candidates_u = [n for n in u_neigh if n != v and n not in shared]
            candidates_v = [n for n in v_neigh if n != u and n not in shared]
            
            if len(candidates_u) > sample_limit:
                candidates_u = random.sample(candidates_u, sample_limit)
            if len(candidates_v) > sample_limit:
                candidates_v = random.sample(candidates_v, sample_limit)

            for nu in candidates_u:
                for nv in candidates_v:
                    edge_bridge = G.get_edge(nu, nv)
                    if edge_bridge:
                        # 3-edge path: geometric mean with exponent 1/3
                        path_w = (
                            G.adj[u][nu].w * edge_bridge.w * G.adj[nv][v].w
                        ) ** 0.33
                        two_hop_strength += path_w

        # κ Formula: (Own strength × Recurrence) / Ambient pressure
        # 
        # WARNING: This is APPROXIMATION of theoretical formula:
        # κ(e) = exp(-λ·Frust(e)) · Rec(e)/(Rec(e)+c)
        # 
        # Current mapping:
        # - Rec(e) ≈ 1 + triangle_strength + β·two_hop_strength
        # - Frust(e) ≈ avg_pressure (inverse relation)
        # - Sigmoid instead of exp
        # 
        # TODO: Derive proper mapping from S1/S2/S3
        
        avg_pressure = (pressure_map[u] + pressure_map[v]) / 2.0 + 1e-6
        rec_factor = 1.0 + triangle_strength + beta * two_hop_strength
        
        k = (edge.w * rec_factor) / (1.0 + 0.1 * avg_pressure)
        
        # Sigmoid normalization [0, 1]
        final_k = k / (1.0 + k)
        edge.kappa_cache = final_k
        total_kappa += final_k

    num_nodes = G.num_nodes if G.num_nodes > 0 else 1
    num_edges = len(G.edges) if len(G.edges) > 0 else 1

    return {
        "pressure_map": pressure_map,
        "mean_pressure": total_pressure / num_nodes,
        "max_pressure": max_pressure,
        "mean_kappa": total_kappa / num_edges
    }


def compute_frustration(G: Graph, pressure_map: dict, params: dict) -> dict:
    """
    Compute frustration Frust(e) for all edges.
    
    Frustration measures incompatibility with surrounding relations.
    Higher frustration = edge conflicts with neighbors.
    
    Approximation: Frust(e) ≈ f(pressure_imbalance, weak_triangles)
    
    Theory: Frust appears in S2 (Antipair) and κ formulas
    
    Returns:
        Dict with:
            - frustration_map: Dict[(u,v) -> Frust(e)]
            - mean_frust: Average frustration
            - max_frust: Maximum frustration
    """
    frustration_map = {}
    total_frust = 0.0
    max_frust = 0.0
    
    for edge in G.all_edges():
        u, v = edge.u, edge.v
        
        # Component 1: Pressure imbalance
        # Edges connecting high-pressure to low-pressure nodes are frustrated
        p_u = pressure_map.get(u, 0.0)
        p_v = pressure_map.get(v, 0.0)
        pressure_imbalance = abs(p_u - p_v) / (p_u + p_v + 1e-6)
        
        # Component 2: Weak triangle participation
        # Edges not in strong triangles are frustrated
        u_neigh = set(G.adj[u].keys())
        v_neigh = set(G.adj[v].keys())
        shared = u_neigh.intersection(v_neigh)
        
        triangle_strength = 0.0
        for k in shared:
            w_path = (G.adj[u][k].w * G.adj[k][v].w) ** 0.5
            triangle_strength += w_path
        
        # Normalize by edge weight
        triangle_deficit = max(0, edge.w - triangle_strength) / (edge.w + 1e-6)
        
        # Combined frustration
        # Higher values = more frustrated
        frust = pressure_imbalance + triangle_deficit
        
        key = (edge.u, edge.v)
        frustration_map[key] = frust
        total_frust += frust
        
        if frust > max_frust:
            max_frust = frust
    
    num_edges = len(G.edges) if len(G.edges) > 0 else 1
    
    return {
        "frustration_map": frustration_map,
        "mean_frust": total_frust / num_edges,
        "max_frust": max_frust
    }
