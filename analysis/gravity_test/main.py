"""
Main CLI and reporting for gravity_test.

Command-line interface and result formatting.
"""

import argparse
import sys
from typing import Dict, List

from . import (
    load_graph_snapshot,
    parse_tick_range,
    infer_n,
    build_node_adj_threshold,
    build_node_adj_topk,
    find_components,
    assign_clusters,
    count_bridges,
    build_cluster_graph_from_edges,
    compute_hub,
    correlations,
    all_pairs_cluster_distances,
    distance_table,
    is_connectivity_only,
    # New modules for channels/anisotropy
    split_regions,
    path_capacity,
    anisotropy_index,
    validate_metrics,
    format_invalid_report
)

# ROMION fail-closed validation (KROK 4)
from .validate_romion import (
    validate_thresholds,
    validate_experiment,
    ValidationStatus,
    format_validation_report
)


def print_report(
    tick: int,
    n_nodes: int,
    comps: List[List[int]],
    node2c: List[int],
    bridges: Dict,
    hub_id: int,
    hub_deg: int,
    hub_share: float,
    coverage: float,
    dists: Dict,
    distance_rows: List[Dict],
    maxdist_bucket: int,
    w_d_p: float,
    w_d_s: float,
    n_d_p: float,
    n_d_s: float,
    unassigned_nodes: int,
    skipped_edges: int,
    wcluster: float,
    wdist: float,
    wbridge: float,
    meta_bg_density: float,
    # New channel/anisotropy params
    channels_enabled: bool = False,
    channel_capacity: float = None,
    channel_meta: Dict = None,
    anisotropy_enabled: bool = False,
    anisotropy_val: float = None,
    anisotropy_meta: Dict = None,
    is_valid: bool = True,
    validation_reasons: List[str] = None
):
    """Print comprehensive analysis report."""
    
    # Header
    print("=" * 70)
    print(f"GRAVITY TEST REPORT - Tick {tick}")
    print("=" * 70)
    print()
    
    # Thresholds (ROMION semantic)
    print("THRESHOLDS (ROMION O'LOGIC):")
    print(f"  wcluster (objects):    {wcluster}")
    print(f"  wdist (background):    {wdist}")
    print(f"  wbridge (field):       {wbridge}")
    if wbridge == 0.0:
        print("  NOTE: wbridge=0.0 => bridges include all positive edges (debug mode)")
    if meta_bg_density > 0.5:
        print(f"  WARNING: meta_bg density={meta_bg_density:.1%} => consider raising wdist")
    print()
    
    # Clustering
    print("CLUSTERING:")
    print(f"  Total nodes: {n_nodes}")
    print(f"  Clusters: {len(comps)}")
    
    # Count active clusters (with bridges)
    active = set()
    for (a, b) in bridges.keys():
        active.add(a)
        active.add(b)
    print(f"  Active clusters (with bridges): {len(active)}")
    
    # Singletons
    singletons = sum(1 for c in comps if len(c) == 1)
    singleton_pct = (singletons / len(comps) * 100) if comps else 0.0
    print(f"  Singletons: {singletons} ({singleton_pct:.1f}%)")
    
    if unassigned_nodes > 0:
        print(f"  Unassigned nodes: {unassigned_nodes} (excluded from analysis)")
    if skipped_edges > 0:
        print(f"  Skipped edges (unassigned endpoints): {skipped_edges}")
    print()
    
    # Bridges
    print("BRIDGES:")
    total_bridges = sum(agg.count for agg in bridges.values())
    pairs_with_bridge = len(bridges)
    print(f"  Pairs with bridges: {pairs_with_bridge}")
    print(f"  Total bridges: {total_bridges}")
    
    if pairs_with_bridge > 0:
        avg = total_bridges / pairs_with_bridge
        print(f"  Avg bridges/pair: {avg:.2f}")
    
    total_weight = sum(agg.w_sum for agg in bridges.values())
    print(f"  Total weight: {total_weight:.3f}")
    print()
    
    # Hub
    print("HUB ANALYSIS:")
    if hub_id >= 0:
        print(f"  Hub cluster: {hub_id}")
        print(f"  Hub degree: {hub_deg}")
        print(f"  Hub share: {hub_share:.1f}%")
        print(f"  Coverage: {coverage:.1f}%")
    else:
        print("  No hub (no bridges)")
    print()
    
    # Range
    print("RANGE:")
    if distance_rows:
        max_dist = max(row['dist'] for row in distance_rows)
        print(f"  Max distance with bridges: {max_dist}")
        
        if is_connectivity_only(distance_rows, maxdist_bucket):
            print(f"  Pattern: Connectivity-only (all @ dist={maxdist_bucket})")
        else:
            print(f"  Pattern: Distance-dependent")
    else:
        print("  No bridges (range=0)")
    print()
    
    # Distance table
    if distance_rows:
        print("BRIDGE DISTANCE DISTRIBUTION:")
        print(f"  {'Dist':<6} {'Bridged':<10} {'P(d|br)':<10} {'BkgPairs':<10} {'P(br|d)':<10} {'Bridges':<10} {'Weight':<10} {'Avg/pair':<10}")
        print("  " + "-" * 100)
        for row in distance_rows:
            print(f"  {row['dist']:<6} {row['bridged_pairs']:<10} {row['p_dist_given_bridge']:<10.4f} "
                  f"{row['background_pairs']:<10} {row['p_bridge_given_dist']:<10.4f} "
                  f"{row['bridges']:<10} {row['weight']:<10.3f} {row['avg_bridges_per_pair']:<10.2f}")
        
        # Validate P(dist|bridge) sums to 1.0
        total_p = sum(row['p_dist_given_bridge'] for row in distance_rows)
        if abs(total_p - 1.0) > 1e-6:
            print(f"  WARNING: ΣP(dist|bridge) = {total_p:.6f} (expected 1.000000)")
        print()
    
    # Correlations
    if len(dists) > 1:
        print("CORRELATIONS (weight/count vs distance):")
        print(f"  w~d Pearson:  {w_d_p:+.3f}")
        print(f"  w~d Spearman: {w_d_s:+.3f}")
        print(f"  n~d Pearson:  {n_d_p:+.3f}")
        print(f"  n~d Spearman: {n_d_s:+.3f}")
        print()
    
    # Channels (on background geometry)
    if channels_enabled:
        print("CHANNELS (background geometry):")
        if channel_meta and 'error' in channel_meta:
            print(f"  ERROR: {channel_meta['error']}")
        elif channel_capacity is not None:
            print(f"  channel_capacity: {channel_capacity:.3f}")
            if channel_meta:
                print(f"  mode: {channel_meta.get('mode', 'unknown')}")
                print(f"  cut_edges: {channel_meta.get('cut_edges', 'N/A')}")
                if 'split' in channel_meta:
                    split = channel_meta['split']
                    print(f"  split: L={split.get('L_size', '?')} R={split.get('R_size', '?')} "
                          f"(seed={split.get('seed_cluster', '?')})")
        else:
            print("  channel_capacity: N/A (requires >=2 clusters)")
        print()
    
    # Anisotropy
    if anisotropy_enabled:
        print("ANISOTROPY (split-axis variability):")
        if anisotropy_meta and 'error' in anisotropy_meta:
            print(f"  ERROR: {anisotropy_meta['error']}")
        elif anisotropy_val is not None:
            print(f"  anisotropy: {anisotropy_val:.6f}")
            if anisotropy_meta:
                print(f"  splits: {anisotropy_meta.get('n_splits', 'N/A')}")
                print(f"  degenerate: {anisotropy_meta.get('degenerate', False)}")
                caps = anisotropy_meta.get('caps', [])
                if caps:
                    print(f"  capacities: {[f'{c:.2f}' for c in caps]}")
        else:
            print("  anisotropy: N/A (requires >=2 clusters)")
        print()
    
    # Validation status
    if not is_valid:
        print("VALIDATION:")
        print(format_invalid_report(validation_reasons or []))
        print()
    
    print("=" * 70)


def analyze_tick(args, tick: int) -> None:
    """Analyze a single tick.
    
    Uses three semantic thresholds (ROMION O'LOGIC):
    - wcluster: for building objects/clusters (matter)
    - wdist: for background geometry/distances
    - wbridge: for field/bridge detection
    """
    
    # === PRE-FLIGHT VALIDATION (ROMION fail-closed - KROK 4) ===
    # Validate threshold relations BEFORE analysis
    thresh_status, thresh_reasons = validate_thresholds(
        args.wcluster, args.wdist, args.wbridge
    )
    
    if thresh_status == ValidationStatus.INVALID_TECH or thresh_status == ValidationStatus.INVALID_THEORY:
        print("=" * 70)
        print(f"GRAVITY TEST @ tick {tick} - ABORTED")
        print("=" * 70)
        print()
        print(format_validation_report(thresh_status, thresh_reasons))
        print()
        print("Experiment cannot proceed with invalid threshold configuration.")
        print("Fix thresholds according to ROMION methodology (see METHODOLOGY.md)")
        print("=" * 70)
        return  # FAIL-CLOSED: Do not proceed
    
    # Show warnings if present but allow to proceed
    if thresh_status == ValidationStatus.PARTIAL:
        print("=" * 70)
        print(f"PRE-FLIGHT VALIDATION - Tick {tick}")
        print("=" * 70)
        print()
        print(format_validation_report(thresh_status, thresh_reasons))
        print()
        print("Proceeding with analysis (warnings present)...")
        print("=" * 70)
        print()
    
    # Load snapshot
    snapshot = load_graph_snapshot(args.log, tick)
    edges = snapshot.get('edges', [])
    n = infer_n(edges)
    
    # === (I) BUILD CLUSTERS using wcluster ===
    if args.cluster_mode == 'threshold':
        adj = build_node_adj_threshold(edges, args.wcluster)
    elif args.cluster_mode == 'topk':
        adj = build_node_adj_topk(edges, args.cluster_k, args.disconnected_policy)
    else:
        raise ValueError(f"Unknown cluster_mode: {args.cluster_mode}")
    
    comps = find_components(n, adj)
    
    # Filter small clusters
    if args.min_cluster_size > 1:
        comps = [c for c in comps if len(c) >= args.min_cluster_size]
    
    node2c = assign_clusters(comps, n)
    
    # Count unassigned nodes (those with node2c == -1)
    unassigned_nodes = sum(1 for c in node2c if c < 0)
    
    # === (II) BUILD BACKGROUND META-GRAPH using wdist ===
    # This is for distances - independent from bridges
    meta_bg = build_cluster_graph_from_edges(edges, node2c, args.wdist)
    
    # Sanity check: warn if meta_bg is too dense (range will always be 1)
    n_clusters = len(comps)
    n_meta_edges = len(meta_bg)
    max_possible_edges = n_clusters * (n_clusters - 1) // 2 if n_clusters > 1 else 0
    meta_bg_density = n_meta_edges / max_possible_edges if max_possible_edges > 0 else 0.0
    
    # === (III) COUNT BRIDGES using wbridge ===
    bridges, skipped_edges = count_bridges(edges, node2c, args.wbridge)
    
    # Hub analysis (on bridges)
    hub_id, hub_deg, hub_share, coverage = compute_hub(bridges, len(comps))
    
    # === DISTANCES on background graph (not bridge graph!) ===
    dists = all_pairs_cluster_distances(meta_bg, len(comps))
    distance_rows = distance_table(bridges, dists)
    
    # Correlations
    w_d_p, w_d_s, n_d_p, n_d_s = correlations(bridges, dists)
    
    # === (IV) CHANNEL / ANISOTROPY METRICS (on background geometry) ===
    channel_capacity = None
    channel_meta = None
    anisotropy_val = None
    anisotropy_meta = None
    
    if args.channels and n_clusters >= 2:
        try:
            L, R, split_meta = split_regions(meta_bg, n_clusters, method="bfs_seed")
            channel_capacity, channel_meta = path_capacity(
                meta_bg, L, R, mode=args.channels_mode
            )
            channel_meta['split'] = split_meta
        except ValueError as e:
            channel_meta = {'error': str(e)}
    
    if args.anisotropy and n_clusters >= 2:
        try:
            anisotropy_val, anisotropy_meta = anisotropy_index(
                meta_bg, n_clusters, 
                n_splits=args.anisotropy_splits,
                split_method="bfs_seed",
                capacity_mode=args.channels_mode
            )
        except ValueError as e:
            anisotropy_meta = {'error': str(e)}
    
    # === (V) VALIDATION (fail-closed) ===
    metrics_to_validate = {
        'hub_share': hub_share,
        'coverage': coverage,
        'unassigned_nodes': unassigned_nodes,
    }
    if channel_capacity is not None:
        metrics_to_validate['channel_capacity'] = channel_capacity
    if anisotropy_val is not None:
        metrics_to_validate['anisotropy'] = anisotropy_val
    
    is_valid, validation_reasons = validate_metrics(metrics_to_validate)
    
    # Report
    maxdist_bucket = max(dists.values()) if dists else 0
    print_report(
        tick, n, comps, node2c, bridges,
        hub_id, hub_deg, hub_share, coverage,
        dists, distance_rows, maxdist_bucket,
        w_d_p, w_d_s, n_d_p, n_d_s,
        unassigned_nodes, skipped_edges,
        args.wcluster, args.wdist, args.wbridge,
        meta_bg_density,
        # New channel/anisotropy params
        channels_enabled=args.channels,
        channel_capacity=channel_capacity,
        channel_meta=channel_meta,
        anisotropy_enabled=args.anisotropy,
        anisotropy_val=anisotropy_val,
        anisotropy_meta=anisotropy_meta,
        is_valid=is_valid,
        validation_reasons=validation_reasons
    )


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Gravity Test: Analyze inter-cluster bridges',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required
    parser.add_argument('--log', required=True, help='Path to simulation.jsonl')
    
    # Tick selection
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--tick', type=int, help='Single tick to analyze')
    group.add_argument('--tick-range', type=str, help='Range: "start end step"')
    
    # === THREE SEMANTIC THRESHOLDS (ROMION O'LOGIC) ===
    # wcluster: defines OBJECTS (matter) - stable local structures
    # wdist:    defines GEOMETRY (background) - metric/distances between objects
    # wbridge:  defines FIELD (interactions) - sparse selective channels
    
    # Clustering params (OBJECTS)
    parser.add_argument('--wcluster', type=float, default=0.02,
                       help='Weight threshold for clustering/objects (default: 0.02)')
    parser.add_argument('--cluster-mode', choices=['threshold', 'topk'], 
                       default='threshold', help='Clustering mode')
    parser.add_argument('--cluster-k', type=int, default=5,
                       help='Top-k edges per node (topk mode)')
    parser.add_argument('--min-cluster-size', type=int, default=1,
                       help='Minimum cluster size (default: 1)')
    
    # Background geometry params (GEOMETRY)
    parser.add_argument('--wdist', type=float, default=0.005,
                       help='Weight threshold for background/distance graph (default: 0.005)')
    parser.add_argument('--disconnected-policy', 
                       choices=['threshold', 'maxdist'], default='maxdist',
                       help='How to handle disconnected clusters in distance calc')
    
    # Bridge params (FIELD)
    parser.add_argument('--wbridge', type=float, default=0.0,
                       help='Min weight for bridge/field edges (default: 0.0)')
    
    # === CHANNEL / ANISOTROPY METRICS (on background geometry) ===
    parser.add_argument('--channels', action='store_true',
                       help='Enable channel capacity metrics (on background geometry)')
    parser.add_argument('--channels-mode', choices=['cut_weight'], default='cut_weight',
                       help='Channel capacity mode (default: cut_weight)')
    parser.add_argument('--anisotropy', action='store_true',
                       help='Enable anisotropy metrics (implies --channels)')
    parser.add_argument('--anisotropy-splits', type=int, default=5,
                       help='Number of split axes for anisotropy (default: 5)')
    
    args = parser.parse_args()
    
    # --anisotropy implies --channels
    if args.anisotropy:
        args.channels = True
    
    # Analyze
    try:
        if args.tick is not None:
            analyze_tick(args, args.tick)
        else:
            start, end, step = parse_tick_range(args.tick_range)
            for tick in range(start, end + 1, step):
                analyze_tick(args, tick)
                if tick < end:
                    print("\n" * 2)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
