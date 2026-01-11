
def compute_projection_metrics(G, theta: float) -> dict:
    """
    Compute L2-FRACTURE projection metrics.
    
    Args:
        G: Graph instance
        theta: Visibility threshold
        
    Returns:
        Dict with:
            - visible_edges: Count of edges with κ >= θ
            - visible_ratio: visible_edges / total_edges
            - mean_kappa_visible: Average κ among visible edges
    """
    visible_kappas = []
    total_edges = 0
    
    for e in G.all_edges():
        total_edges += 1
        if e.kappa_cache >= theta:
            visible_kappas.append(e.kappa_cache)
    
    visible_edges = len(visible_kappas)
    visible_ratio = visible_edges / max(1, total_edges)
    mean_kappa_visible = (
        sum(visible_kappas) / visible_edges
        if visible_edges > 0 else 0.0
    )
    
    return {
        'visible_edges': visible_edges,
        'visible_ratio': visible_ratio,
        'mean_kappa_visible': mean_kappa_visible
    }
