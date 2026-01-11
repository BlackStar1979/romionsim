"""
⚠️⚠️⚠️ DEPRECATED - DO NOT USE ⚠️⚠️⚠️

THIS IS A MONOLITHIC ARCHIVE FROM BEFORE PACKAGE SPLIT.

**USE INSTEAD:** analysis/gravity_test.py → gravity_test/ package

**ARCHIVE STATUS:** Historical reference only
**DO NOT RUN:** Use modular gravity_test/ package

---

gravity_test.py (ARCHIVED - Pre-split monolithic version)

ROMION "Gravity Test" (Test B / Test C support)

What it does
------------
Given a simulation JSONL log produced by run_romion_extended.py (with graph dumps),
this tool measures whether *inter-cluster bridges* behave like a distance-dependent
field.

Key methodology choices (post-audit)
-----------------------------------
1) Separation of concerns (three thresholds):
   - --wcluster : edges that *define objects/matter* (clusters)
   - --wbridge  : edges that *count as interactions/field* (bridges)
   - --wdist    : edges that define the *independent background graph* for distance

2) Coverage:
   - With --disconnected-policy maxdist, ALL cluster-pairs are assigned a distance
     (disconnected pairs get max_known_dist + 1). Coverage becomes 100%.

3) Correlation hygiene:
   - By default, correlations are computed on distances <= --corr-dist-max (default 6)
     and with the maxdist bucket excluded, because disconnected pairs can dominate.

4) Anti-tautology:
   - Distances are computed on an independent background graph (wdist-mode), not on
     the bridge graph.

Outputs
-------
- Pair coverage, hub topology, Spearman rho (count/weight and log versions)
- Hub-excluded robustness rho (optional)
- Distance-conditional table:
    N_pairs, pairs_with_bridge, total_cnt, total_wgt, P(bridge>0|d), E(wgt|d)
- "range" = max distance with any bridges (excluding maxdist bucket)

Notes
-----
If *all* bridges are at dist==1 (common in current baseline), then any negative rho
is typically a connectivity effect, not a long-range field. This tool flags that.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


# -----------------------------
# Basic stats helpers
# -----------------------------


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def _rankdata(values: Sequence[float]) -> List[float]:
    """Average ranks for ties (1..n)."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        # average rank for ties
        avg_rank = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def _pearson(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        return float("nan")
    mx, my = _mean(x), _mean(y)
    vx = sum((xi - mx) ** 2 for xi in x)
    vy = sum((yi - my) ** 2 for yi in y)
    if vx == 0.0 or vy == 0.0:
        return float("nan")
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    return cov / math.sqrt(vx * vy)


def spearmanr(x: Sequence[float], y: Sequence[float]) -> float:
    """Spearman rho via Pearson of ranks; returns nan if degenerate."""
    if len(x) != len(y) or len(x) < 2:
        return float("nan")
    rx = _rankdata(x)
    ry = _rankdata(y)
    return _pearson(rx, ry)


# -----------------------------
# Snapshot parsing
# -----------------------------


def load_graph_snapshot(log_path: str, tick: int) -> Dict:
    """Return the GRAPH entry for a given tick."""
    if not os.path.exists(log_path):
        raise FileNotFoundError(log_path)

    snapshot = None
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Support both formats: {"type":"GRAPH"} and {"event":"GRAPH_DUMP"}
            if obj.get("type") == "GRAPH" and obj.get("tick") == tick:
                snapshot = obj
                break
            if obj.get("event") == "GRAPH_DUMP" and obj.get("tick") == tick:
                snapshot = obj
                break
    if snapshot is None:
        raise ValueError(
            f"No GRAPH entry found for tick={tick}. "
            "Make sure you ran with --dump-graph-every that hits this tick."
        )
    # Return data if nested, otherwise return whole object
    if "data" in snapshot:
        return snapshot["data"]
    return snapshot


def infer_n(edges: Sequence[Sequence]) -> int:
    mx = -1
    for u, v, *_ in edges:
        mx = max(mx, int(u), int(v))
    return mx + 1


# -----------------------------
# Graph building
# -----------------------------


def build_node_adj_threshold(edges: Sequence[Sequence], wmin: float) -> Dict[int, List[int]]:
    adj: Dict[int, List[int]] = defaultdict(list)
    for u, v, w in edges:
        u = int(u)
        v = int(v)
        w = float(w)
        if w >= wmin:
            adj[u].append(v)
            adj[v].append(u)
    return adj


def build_node_adj_topk(
    edges: Sequence[Sequence],
    k: int,
    min_w: float,
) -> Dict[int, List[int]]:
    """Background adjacency by keeping top-k weighted neighbors per node."""
    per_node: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
    for u, v, w in edges:
        u = int(u)
        v = int(v)
        w = float(w)
        if w < min_w:
            continue
        per_node[u].append((v, w))
        per_node[v].append((u, w))

    chosen: Dict[int, set] = defaultdict(set)
    for u, lst in per_node.items():
        lst.sort(key=lambda t: t[1], reverse=True)
        for v, _w in lst[:k]:
            chosen[u].add(v)

    # make undirected adjacency
    adj: Dict[int, List[int]] = defaultdict(list)
    for u, nbrs in chosen.items():
        for v in nbrs:
            adj[u].append(v)
            adj[v].append(u)
    return adj


def find_components(n: int, adj: Dict[int, List[int]]) -> List[List[int]]:
    visited = [False] * n
    comps: List[List[int]] = []

    for start in range(n):
        if visited[start]:
            continue
        # BFS even for isolated nodes
        stack = [start]
        visited[start] = True
        comp = [start]
        while stack:
            u = stack.pop()
            for v in adj.get(u, []):
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
                    comp.append(v)
        comps.append(comp)
    return comps


def assign_clusters(comps: List[List[int]]) -> List[int]:
    node2c = [-1] * sum(len(c) for c in comps)
    for cid, comp in enumerate(comps):
        for u in comp:
            node2c[u] = cid
    return node2c


@dataclass
class BridgeAgg:
    cnt: int = 0
    wgt: float = 0.0


def count_bridges(
    edges: Sequence[Sequence],
    node2c: Sequence[int],
    wbridge: float,
) -> Dict[Tuple[int, int], BridgeAgg]:
    bridges: Dict[Tuple[int, int], BridgeAgg] = defaultdict(BridgeAgg)
    for u, v, w in edges:
        u = int(u)
        v = int(v)
        w = float(w)
        if w < wbridge:
            continue
        cu, cv = node2c[u], node2c[v]
        # CRITICAL: Skip unassigned nodes (-1)
        if cu < 0 or cv < 0:
            continue
        if cu == cv:
            continue
        a, b = (cu, cv) if cu < cv else (cv, cu)
        bridges[(a, b)].cnt += 1
        bridges[(a, b)].wgt += w
    return bridges


def build_cluster_graph_from_edges(
    edges: Iterable[Tuple[int, int]],
    n_clusters: int,
) -> Dict[int, List[int]]:
    adj: Dict[int, List[int]] = defaultdict(list)
    for a, b in edges:
        if a == b:
            continue
        adj[a].append(b)
        adj[b].append(a)
    # ensure keys exist for isolated clusters
    for i in range(n_clusters):
        adj.setdefault(i, [])
    return adj


def all_pairs_cluster_distances(
    cluster_adj: Dict[int, List[int]],
    disconnected_policy: str,
) -> Tuple[Dict[Tuple[int, int], int], int]:
    """Return distances for ALL pairs and the maxdist bucket value.

    disconnected_policy:
      - 'drop'    : disconnected pairs are omitted (coverage < 100%)
      - 'maxdist' : disconnected pairs are assigned (max_known+1)
    """
    clusters = sorted(cluster_adj.keys())
    c = len(clusters)
    index = {cid: i for i, cid in enumerate(clusters)}

    # BFS from each cluster
    dist_mat: List[List[Optional[int]]] = [[None] * c for _ in range(c)]
    max_known = 0
    for src_cid in clusters:
        src = index[src_cid]
        q = [src_cid]
        dist_mat[src][src] = 0
        head = 0
        while head < len(q):
            cur_cid = q[head]
            head += 1
            cur = index[cur_cid]
            dcur = dist_mat[src][cur]
            assert dcur is not None
            for nb_cid in cluster_adj.get(cur_cid, []):
                nb = index[nb_cid]
                if dist_mat[src][nb] is None:
                    dist_mat[src][nb] = dcur + 1
                    max_known = max(max_known, dcur + 1)
                    q.append(nb_cid)

    maxdist_bucket = max_known + 1
    out: Dict[Tuple[int, int], int] = {}
    for i in range(c):
        for j in range(i + 1, c):
            d = dist_mat[i][j]
            if d is None:
                if disconnected_policy == "drop":
                    continue
                d = maxdist_bucket
            out[(clusters[i], clusters[j])] = int(d)
    return out, maxdist_bucket


# -----------------------------
# Analysis & reporting
# -----------------------------


def compute_hub(bridges: Dict[Tuple[int, int], BridgeAgg], n_clusters: int) -> Tuple[int, int, float, float]:
    """Return (hub_id, hub_degree, hub_share, max_over_mean_degree)."""
    deg = [0] * n_clusters
    for (a, b), agg in bridges.items():
        # SANITY: Ensure no invalid cluster indices (fail-closed against -1 leak)
        assert 0 <= a < n_clusters, f"Invalid cluster index a={a} (n_clusters={n_clusters})"
        assert 0 <= b < n_clusters, f"Invalid cluster index b={b} (n_clusters={n_clusters})"
        if agg.cnt <= 0:
            continue
        deg[a] += 1
        deg[b] += 1
    hub_id = max(range(n_clusters), key=lambda i: deg[i]) if n_clusters > 0 else -1
    hub_degree = deg[hub_id] if hub_id >= 0 else 0
    total_edges = sum(deg) / 2.0
    hub_share = (hub_degree / total_edges) if total_edges > 0 else 0.0
    mean_deg = (sum(deg) / n_clusters) if n_clusters > 0 else 0.0
    max_over_mean = (hub_degree / mean_deg) if mean_deg > 0 else 0.0
    return hub_id, hub_degree, hub_share, max_over_mean


def correlations(
    pair_dists: Dict[Tuple[int, int], int],
    bridges: Dict[Tuple[int, int], BridgeAgg],
    maxdist_bucket: int,
    corr_dist_max: int,
    exclude_maxdist: bool,
    exclude_hub: Optional[int],
) -> Dict[str, float]:
    xs: List[float] = []
    yc: List[float] = []
    yw: List[float] = []
    ylc: List[float] = []
    ylw: List[float] = []

    for (a, b), d in pair_dists.items():
        if exclude_hub is not None and (a == exclude_hub or b == exclude_hub):
            continue
        if exclude_maxdist and d == maxdist_bucket:
            continue
        if corr_dist_max is not None and d > corr_dist_max:
            continue
        agg = bridges.get((a, b), BridgeAgg())
        c = float(agg.cnt)
        w = float(agg.wgt)
        xs.append(float(d))
        yc.append(c)
        yw.append(w)
        ylc.append(math.log1p(c))
        ylw.append(math.log1p(w))

    out = {
        "count": spearmanr(xs, yc),
        "weight": spearmanr(xs, yw),
        "log_count": spearmanr(xs, ylc),
        "log_weight": spearmanr(xs, ylw),
        "n": float(len(xs)),
    }
    return out


def distance_table(
    pair_dists: Dict[Tuple[int, int], int],
    bridges: Dict[Tuple[int, int], BridgeAgg],
) -> Tuple[List[Dict], int]:
    by_d = defaultdict(lambda: {"n_pairs": 0, "pairs_with_bridge": 0, "total_cnt": 0, "total_wgt": 0.0})
    for (a, b), d in pair_dists.items():
        row = by_d[int(d)]
        row["n_pairs"] += 1
        agg = bridges.get((a, b))
        if agg is not None and agg.cnt > 0:
            row["pairs_with_bridge"] += 1
            row["total_cnt"] += int(agg.cnt)
            row["total_wgt"] += float(agg.wgt)

    dists = sorted(by_d.keys())
    rows: List[Dict] = []
    range_max = 0
    for d in dists:
        r = by_d[d]
        n = r["n_pairs"]
        pwb = r["pairs_with_bridge"]
        tc = r["total_cnt"]
        tw = r["total_wgt"]
        p = (pwb / n) if n else 0.0
        e = (tw / n) if n else 0.0
        rows.append(
            {
                "dist": d,
                "n_pairs": n,
                "pairs_with_bridge": pwb,
                "total_cnt": tc,
                "total_wgt": tw,
                "p_gt0": p,
                "e_wgt": e,
            }
        )
        if pwb > 0:
            range_max = max(range_max, d)
    return rows, range_max


def is_connectivity_only(distance_rows: List[Dict], maxdist_bucket: int) -> bool:
    """True if all bridges occur at dist==1 and none at dist>=2 (excluding maxdist)."""
    any_ge2 = any(r["dist"] >= 2 and r["dist"] != maxdist_bucket and r["pairs_with_bridge"] > 0 for r in distance_rows)
    any_d1 = any(r["dist"] == 1 and r["pairs_with_bridge"] > 0 for r in distance_rows)
    return any_d1 and (not any_ge2)


def print_report(
    *,
    tick: int,
    n_clusters_total: int,
    n_clusters: int,
    singletons: int,
    filtered_out: int,
    cluster_sizes: List[int],
    total_pairs: int,
    used_pairs: int,
    maxdist_bucket: int,
    bridges: Dict[Tuple[int, int], BridgeAgg],
    corr_main: Dict[str, float],
    corr_nohub: Optional[Dict[str, float]],
    hub_info: Tuple[int, int, float, float],
    distance_rows: List[Dict],
    range_max: int,
    corr_dist_max: int,
    exclude_maxdist: bool,
):
    hub_id, hub_deg, hub_share, hub_ratio = hub_info
    pairs_with_bridge = sum(1 for agg in bridges.values() if agg.cnt > 0)
    total_bridge_count = sum(agg.cnt for agg in bridges.values())
    total_bridge_weight = sum(agg.wgt for agg in bridges.values())
    avg_bridges_per_pair = (total_bridge_count / pairs_with_bridge) if pairs_with_bridge else 0.0

    print("=" * 70)
    print(f"ROMION Gravity Test @ tick={tick}")
    print("=" * 70)
    cov = (used_pairs / total_pairs) * 100.0 if total_pairs else 0.0
    
    # Cluster statistics with filtering info
    singleton_pct = (singletons / n_clusters_total * 100) if n_clusters_total > 0 else 0
    unassigned = sum(1 for c in cluster_sizes if c == 0) if hasattr(cluster_sizes, '__iter__') else 0
    
    print(f"Clusters: {n_clusters} active (total: {n_clusters_total}, filtered: {filtered_out})")
    print(f"  Singletons: {singletons} ({singleton_pct:.1f}% of total)")
    print(f"  Unassigned nodes: {filtered_out} (excluded from analysis)")
    if cluster_sizes:
        print(f"  Active cluster sizes: min={min(cluster_sizes)}, max={max(cluster_sizes)}, mean={sum(cluster_sizes)/len(cluster_sizes):.1f}")
    print(f"Pairs: total={total_pairs}, used={used_pairs}, coverage={cov:.1f}%")
    print(
        f"Pairs with bridges: {pairs_with_bridge} | "
        f"Total bridge count: {total_bridge_count} | "
        f"Total bridge weight: {total_bridge_weight:.3f} | "
        f"Avg bridges/pair: {avg_bridges_per_pair:.2f}"
    )
    print("")

    print(f"Hub topology: cluster {hub_id} (degree={hub_deg}, share={hub_share*100:.1f}%, max/mean={hub_ratio:.1f})")
    if hub_share > 0.30 and hub_ratio > 3.0:
        print("  WARNING: Strong hub detected - may dominate correlation")
    print("")

    tag = f"dist<={corr_dist_max}" + (" (maxdist excluded)" if exclude_maxdist else "")
    print(f"Spearman correlations (dist vs bridges) [{tag}]:")
    print(f"  count:         {corr_main['count']:.3f}")
    print(f"  weight:        {corr_main['weight']:.3f}")
    print(f"  log(1+count):  {corr_main['log_count']:.3f}")
    print(f"  log(1+weight): {corr_main['log_weight']:.3f}")

    if corr_nohub is not None:
        print("")
        print("Hub-excluded correlations (robustness check):")
        print(f"  count (no hub):  {corr_nohub['count']:.3f}")
        print(f"  weight (no hub): {corr_nohub['weight']:.3f}")
        print(f"  (pairs without hub: {int(corr_nohub['n'])})")

    print("")
    connectivity_only = is_connectivity_only(distance_rows, maxdist_bucket)
    if pairs_with_bridge == 0:
        print("NOTE: No bridges detected at this tick.")
    elif range_max <= 1 and connectivity_only:
        print("NOTE: Bridges occur only at dist=1. This is connectivity-only (no long-range field).")
    else:
        print("PASS: Negative correlation suggests 'closer' -> 'more bridges'.")
        if range_max <= 1:
            print("  WARNING: Range<=1, treat rho as local-only.")

    print("")
    print("Distance-conditional bridge statistics:")
    print("  Dist  N_pairs  PairsBr  TotalCnt  TotalWgt   P(>0)       E(wgt)")
    print("  " + "-" * 70)
    for r in distance_rows:
        print(
            f"  {r['dist']:<5} {r['n_pairs']:<7} {r['pairs_with_bridge']:<7} "
            f"{r['total_cnt']:<8} {r['total_wgt']:<9.3f} {r['p_gt0']:<11.3e} {r['e_wgt']:<11.3e}"
        )

    print("")
    # simple histogram of N_pairs
    print("Histogram N_pairs by dist (sanity):")
    for r in distance_rows:
        d = r["dist"]
        n = r["n_pairs"]
        label = "maxdist" if d == maxdist_bucket else str(d)
        print(f"  dist={label:<7}  N_pairs={n}")

    print("")
    # Top bridges
    top = sorted(((agg.cnt, agg.wgt, pair) for pair, agg in bridges.items() if agg.cnt > 0), reverse=True)[:10]
    if top:
        print("Top 10 bridges (count, weight, pair):")
        for cnt, wgt, pair in top:
            print(f"  {cnt:>5}  {wgt:>7.2f}  {pair}")


def analyze_tick(args, tick: int) -> None:
    snapshot = load_graph_snapshot(args.log, tick)
    edges = snapshot.get("edges", [])
    if not edges:
        raise ValueError("Snapshot has no 'edges' list.")
    n = int(snapshot.get("n", infer_n(edges)))

    # clusters
    adj_cluster = build_node_adj_threshold(edges, args.wcluster)
    comps = find_components(n, adj_cluster)
    
    # Filter by min cluster size
    min_size = getattr(args, 'min_cluster_size', 1)
    all_comps = comps
    active_comps = [c for c in comps if len(c) >= min_size]
    
    # Build node2cluster mapping ONLY for active clusters
    node2c = [-1] * n
    for cid, comp in enumerate(active_comps):
        for u in comp:
            node2c[u] = cid
    
    n_clusters_total = len(all_comps)
    n_clusters = len(active_comps)
    cluster_sizes = [len(c) for c in active_comps]
    singletons = sum(1 for c in all_comps if len(c) == 1)
    filtered_out = n_clusters_total - n_clusters

    # bridges (interaction edges)
    bridges = count_bridges(edges, node2c, args.wbridge)

    # background graph for distance
    if args.wdist_mode == "threshold":
        adj_bg = build_node_adj_threshold(edges, args.wdist)
    elif args.wdist_mode == "topk":
        adj_bg = build_node_adj_topk(edges, args.topk, args.wdist_minw)
    else:
        raise ValueError(f"Unknown --wdist-mode {args.wdist_mode}")

    # meta graph on clusters from background edges
    meta_edges = set()
    for u, nbrs in adj_bg.items():
        cu = node2c[u]
        if cu < 0:  # Skip unassigned nodes
            continue
        for v in nbrs:
            cv = node2c[v]
            if cv < 0 or cu == cv:  # Skip unassigned or same cluster
                continue
            a, b = (cu, cv) if cu < cv else (cv, cu)
            meta_edges.add((a, b))
    meta_adj = build_cluster_graph_from_edges(meta_edges, n_clusters)

    pair_dists, maxdist_bucket = all_pairs_cluster_distances(meta_adj, args.disconnected_policy)

    # coverage
    total_pairs = n_clusters * (n_clusters - 1) // 2
    used_pairs = len(pair_dists)

    # hub
    hub_id, hub_deg, hub_share, hub_ratio = compute_hub(bridges, n_clusters)

    # correlation (main)
    corr_main = correlations(
        pair_dists,
        bridges,
        maxdist_bucket,
        args.corr_dist_max,
        args.exclude_maxdist,
        exclude_hub=None,
    )

    corr_nohub = None
    if args.exclude_hub:
        corr_nohub = correlations(
            pair_dists,
            bridges,
            maxdist_bucket,
            args.corr_dist_max,
            args.exclude_maxdist,
            exclude_hub=hub_id,
        )

    # distance table
    distance_rows, range_max = distance_table(pair_dists, bridges)
    # range should ignore maxdist bucket for interpretation
    range_real = max((r["dist"] for r in distance_rows if r["dist"] != maxdist_bucket and r["pairs_with_bridge"] > 0), default=0)

    print_report(
        tick=tick,
        n_clusters_total=n_clusters_total,
        n_clusters=n_clusters,
        singletons=singletons,
        filtered_out=filtered_out,
        cluster_sizes=cluster_sizes,
        total_pairs=total_pairs,
        used_pairs=used_pairs,
        maxdist_bucket=maxdist_bucket,
        bridges=bridges,
        corr_main=corr_main,
        corr_nohub=corr_nohub,
        hub_info=(hub_id, hub_deg, hub_share, hub_ratio),
        distance_rows=distance_rows,
        range_max=range_real,
        corr_dist_max=args.corr_dist_max,
        exclude_maxdist=args.exclude_maxdist,
    )


def parse_tick_range(s: str) -> Tuple[int, int, int]:
    parts = s.split(":")
    if len(parts) != 3:
        raise ValueError("tick-range must be start:end:step")
    return int(parts[0]), int(parts[1]), int(parts[2])


def main() -> None:
    ap = argparse.ArgumentParser(description="ROMION Gravity Test")
    ap.add_argument("--log", required=True, help="Path to simulation.jsonl")
    ap.add_argument("--tick", type=int, help="Tick to analyze")
    ap.add_argument("--tick-range", type=str, help="start:end:step (analyze multiple ticks)")

    ap.add_argument("--wcluster", type=float, default=0.02, help="Cluster threshold")
    ap.add_argument("--wbridge", type=float, default=0.0, help="Bridge threshold")

    ap.add_argument("--wdist", type=float, default=0.005, help="Background distance threshold (threshold mode)")
    ap.add_argument(
        "--wdist-mode",
        choices=["threshold", "topk"],
        default="threshold",
        help="How to build independent background graph for distances",
    )
    ap.add_argument("--topk", type=int, default=10, help="top-k per node (wdist-mode=topk)")
    ap.add_argument("--wdist-minw", type=float, default=0.0, help="min weight filter for topk background")
    
    ap.add_argument("--min-cluster-size", type=int, default=2, help="Minimum cluster size to include (default: 2, filters singletons)")

    ap.add_argument(
        "--disconnected-policy",
        choices=["drop", "maxdist"],
        default="maxdist",
        help="How to handle disconnected cluster pairs",
    )

    ap.add_argument("--exclude-hub", action="store_true", help="Report hub-excluded correlations")
    ap.add_argument(
        "--include-maxdist",
        action="store_true",
        help="Include maxdist bucket in correlations (default: excluded)",
    )
    ap.add_argument(
        "--corr-dist-max",
        type=int,
        default=6,
        help="Compute correlations only for dist <= this value (recommended)",
    )

    args = ap.parse_args()
    
    # Convert include-maxdist to exclude-maxdist
    args.exclude_maxdist = not args.include_maxdist
    if args.tick is None and args.tick_range is None:
        raise SystemExit("Provide --tick or --tick-range")

    if args.tick is not None:
        analyze_tick(args, args.tick)
        return

    start, end, step = parse_tick_range(args.tick_range)
    for t in range(start, end + 1, step):
        try:
            analyze_tick(args, t)
        except Exception as e:
            print("=" * 70)
            print(f"tick={t} ERROR: {e}")


if __name__ == "__main__":
    main()
