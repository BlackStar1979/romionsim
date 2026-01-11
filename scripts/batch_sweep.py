#!/usr/bin/env python3
"""
Batch sweep runner: Decay parameter sweep with channels/anisotropy diagnostics.

ROMION O'LOGIC three-threshold semantics:
- wcluster: objects/matter (clusters)
- wdist: background geometry (distances)  
- wbridge: field/interactions (bridges)
"""

import subprocess
import csv
import re
import json
import argparse
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Default grids
PILOT_COARSE = {
    "decay_scale": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
    "seeds": [42, 123],
}

# Pre-registered thresholds
ANALYSIS_PARAMS = {
    "wcluster": 0.02,
    "wdist": 0.005,
    "wbridge": 0.0,
    "wdist_mode": "threshold",
    "min_cluster_size": 2,
    "disconnected_policy": "maxdist",
}

SIM_PARAMS = {
    "ticks": 600,
    "dump_graph_every": 100,
}

CHECKPOINT_TICKS = [100, 200, 300, 400, 500, 600]


def get_repo_root() -> Path:
    """Get repository root directory."""
    script_path = Path(__file__).resolve()
    return script_path.parent.parent


def setup_env():
    """Setup environment for subprocess calls."""
    repo_root = get_repo_root()
    env = os.environ.copy()
    
    # Add repo root to PYTHONPATH
    pythonpath = env.get('PYTHONPATH', '')
    if pythonpath:
        env['PYTHONPATH'] = f"{repo_root}{os.pathsep}{pythonpath}"
    else:
        env['PYTHONPATH'] = str(repo_root)
    
    return env


def run_simulation_direct(decay: float, seed: int, output_dir: str) -> bool:
    """Run simulation directly with proper PYTHONPATH."""
    repo_root = get_repo_root()
    env = setup_env()
    
    cmd = [
        "python",
        str(repo_root / "scripts" / "run_romion_extended.py"),
        "--ticks", str(SIM_PARAMS["ticks"]),
        "--decay-scale", str(decay),
        "--seed", str(seed),
        "--dump-graph-every", str(SIM_PARAMS["dump_graph_every"]),
        "--out", output_dir,
    ]
    
    print(f"  Running simulation: decay={decay}, seed={seed}")
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
            env=env,
            cwd=str(repo_root)
        )
        if proc.returncode != 0:
            print(f"    [FAIL] Simulation failed")
            print(f"    stderr: {proc.stderr[:300]}")
            return False
        print(f"    [OK] Simulation complete")
        return True
    except subprocess.TimeoutExpired:
        print(f"    [FAIL] Simulation timeout")
        return False
    except Exception as e:
        print(f"    [FAIL] Error: {e}")
        return False


def _safe_float(x: str, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def _is_invalid(text: str) -> Tuple[bool, str]:
    """Detect INVALID RUN (fail-closed)"""
    if "INVALID RUN" not in text and "INVALID" not in text:
        return False, ""
    if "INVALID RUN" in text:
        lines = text.splitlines()
        idx = next((i for i, ln in enumerate(lines) if "INVALID RUN" in ln), None)
        if idx is None:
            return True, "INVALID"
        snippet = "\n".join(lines[idx : idx + 12]).strip()
        return True, snippet
    return True, "INVALID"


def parse_gravity_output(text: str) -> Dict:
    """Extract metrics from gravity_test output."""
    invalid, invalid_blob = _is_invalid(text)
    
    result = {
        "invalid": invalid,
        "invalid_reasons": invalid_blob,
        "clusters_active": 0,
        "clusters_total": 0,
        "singletons": 0,
        "unassigned": 0,
        "pairs_with_bridge": 0,
        "total_bridge_count": 0,
        "total_bridge_weight": 0.0,
        "hub_share": 0.0,
        "coverage": 0.0,
        "range": 0,
        "channel_capacity": None,
        "anisotropy": None,
    }
    
    # Parse metrics
    m = re.search(r"Clusters:\s+(\d+)", text)
    if m:
        result["clusters_total"] = int(m.group(1))
    
    m = re.search(r"Active clusters \(with bridges\):\s+(\d+)", text)
    if m:
        result["clusters_active"] = int(m.group(1))
    
    m = re.search(r"Unassigned nodes:\s+(\d+)", text)
    if m:
        result["unassigned"] = int(m.group(1))
    
    m = re.search(r"Singletons:\s+(\d+)", text)
    if m:
        result["singletons"] = int(m.group(1))
    
    m = re.search(r"Pairs with bridges:\s+(\d+)", text)
    if m:
        result["pairs_with_bridge"] = int(m.group(1))
    
    m = re.search(r"Total bridges:\s+(\d+)", text)
    if m:
        result["total_bridge_count"] = int(m.group(1))
    
    m = re.search(r"Total weight:\s+([\d.]+)", text)
    if m:
        result["total_bridge_weight"] = _safe_float(m.group(1))
    
    m = re.search(r"Hub share:\s+([\d.]+)%", text)
    if m:
        result["hub_share"] = _safe_float(m.group(1))
    
    m = re.search(r"Coverage:\s+([\d.]+)%", text)
    if m:
        result["coverage"] = _safe_float(m.group(1))
    
    m = re.search(r"Max distance with bridges:\s+(\d+)", text)
    if m:
        result["range"] = int(m.group(1))
    
    m = re.search(r"(?:Channel capacity|channel_capacity):\s+([\d.]+)", text)
    if m:
        result["channel_capacity"] = _safe_float(m.group(1))
    
    m = re.search(r"\banisotropy:\s+([\d.]+)", text)
    if m:
        result["anisotropy"] = _safe_float(m.group(1))
    
    return result


def analyze_tick(
    log_path: str,
    tick: int,
    with_diagnostics: bool = False,
    anisotropy_splits: int = 5,
) -> Dict:
    """Run gravity_test for specific tick."""
    repo_root = get_repo_root()
    env = setup_env()
    
    cmd = [
        "python",
        str(repo_root / "analysis" / "gravity_test.py"),
        "--log", log_path,
        "--tick", str(tick),
        "--wcluster", str(ANALYSIS_PARAMS["wcluster"]),
        "--wbridge", str(ANALYSIS_PARAMS["wbridge"]),
        "--wdist", str(ANALYSIS_PARAMS["wdist"]),
        "--wdist-mode", ANALYSIS_PARAMS["wdist_mode"],
        "--min-cluster-size", str(ANALYSIS_PARAMS["min_cluster_size"]),
        "--disconnected-policy", ANALYSIS_PARAMS["disconnected_policy"],
    ]
    
    if with_diagnostics:
        cmd += [
            "--channels",
            "--channels-mode", "cut_weight",
            "--anisotropy",
            "--anisotropy-splits", str(anisotropy_splits),
        ]
    
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
            env=env,
            cwd=str(repo_root)
        )
        if proc.returncode != 0:
            return {
                "invalid": True,
                "invalid_reasons": (proc.stderr or proc.stdout or "")[:400],
            }
        return parse_gravity_output(proc.stdout)
    except Exception as e:
        return {"invalid": True, "invalid_reasons": f"exception: {e}"}


def _is_frozen(metrics: Dict) -> bool:
    """FROZEN if bridges_count==0 OR bridges_weight==0"""
    if metrics.get("invalid"):
        return False
    return (metrics.get("total_bridge_count", 0) == 0) or \
           (metrics.get("total_bridge_weight", 0.0) == 0.0)


def detect_freeze_tick(
    log_path: str,
    ticks: List[int],
    with_diagnostics: bool = False,
    anisotropy_splits: int = 5,
) -> Optional[int]:
    """Find first tick where FROZEN."""
    for tick in sorted(ticks):
        metrics = analyze_tick(log_path, tick, with_diagnostics, anisotropy_splits)
        if metrics.get("invalid"):
            return None
        if _is_frozen(metrics):
            return tick
    return None


def run_sweep(
    config: Dict,
    output_prefix: str,
    main_tick: int = 400,
    with_diagnostics: bool = False,
    anisotropy_splits: int = 5,
) -> List[Dict]:
    """Run sweep with simulations and analysis."""
    results = []
    decay_values = config["decay_scale"]
    seeds = config["seeds"]
    total = len(decay_values) * len(seeds)
    
    print("=" * 70)
    print(f"DECAY SWEEP: {total} runs")
    print(f"Main tick: {main_tick}")
    print(f"Diagnostics: {'ON' if with_diagnostics else 'OFF'}")
    print("=" * 70)
    
    for i, decay in enumerate(decay_values, 1):
        for j, seed in enumerate(seeds, 1):
            run_num = (i-1) * len(seeds) + j
            print(f"\n[{run_num}/{total}] decay={decay}, seed={seed}")
            
            output_dir = f"tests/sweep_decay/results/{output_prefix}_d{decay}_s{seed}"
            
            if not run_simulation_direct(decay, seed, output_dir):
                print(f"  [SKIP] Simulation failed")
                continue
            
            log_path = Path(output_dir) / "simulation.jsonl"
            if not log_path.exists():
                print(f"  [SKIP] Log not found")
                continue
            
            # Detect freeze_tick
            print(f"  Detecting freeze_tick...")
            freeze_tick = detect_freeze_tick(
                str(log_path),
                CHECKPOINT_TICKS,
                with_diagnostics,
                anisotropy_splits,
            )
            print(f"    freeze_tick = {freeze_tick if freeze_tick is not None else 'never'}")
            
            # Analyze @ main tick
            print(f"  Analyzing @ tick {main_tick}...")
            metrics = analyze_tick(str(log_path), main_tick, with_diagnostics, anisotropy_splits)
            
            invalid = bool(metrics.get("invalid"))
            frozen = (not invalid) and _is_frozen(metrics)
            
            result = {
                "decay_scale": decay,
                "seed": seed,
                "tick": main_tick,
                "freeze_tick": freeze_tick if freeze_tick is not None else 0,
                "invalid": invalid,
                "frozen": frozen,
                **metrics
            }
            results.append(result)
            
            status = "INVALID" if invalid else ("FROZEN" if frozen else "OK")
            cap = metrics.get("channel_capacity")
            an = metrics.get("anisotropy")
            cap_s = f"{cap:.3f}" if isinstance(cap, (int, float)) else "-"
            an_s = f"{an:.3f}" if isinstance(an, (int, float)) else "-"
            
            print(
                f"  [{status}] bridges={metrics.get('total_bridge_count', 0)} "
                f"(w={metrics.get('total_bridge_weight', 0.0):.3f}), "
                f"hub={metrics.get('hub_share', 0.0):.1f}%, "
                f"cov={metrics.get('coverage', 0.0):.1f}%, "
                f"cap={cap_s}, aniso={an_s}"
            )
    
    return results


def write_results(results: List[Dict], filename: str):
    """Write results to CSV."""
    if not results:
        print("\n[FAIL] No results to write")
        return
    
    fieldnames = [
        "decay_scale", "seed", "tick", "freeze_tick",
        "invalid", "frozen",
        "clusters_active", "clusters_total", "singletons", "unassigned",
        "pairs_with_bridge", "total_bridge_count", "total_bridge_weight",
        "hub_share", "coverage", "range",
        "channel_capacity", "anisotropy",
    ]
    
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print("\n" + "=" * 70)
    print(f"[OK] Results written to: {filename}")
    print(f"   {len(results)} runs completed")


def main():
    ap = argparse.ArgumentParser(description="Decay sweep with channels/anisotropy")
    ap.add_argument("mode", nargs="?", choices=["pilot"], default="pilot")
    ap.add_argument("--tick", type=int, default=400)
    ap.add_argument("--with-diagnostics", action="store_true")
    ap.add_argument("--anisotropy-splits", type=int, default=5)
    args = ap.parse_args()
    
    config = PILOT_COARSE
    prefix = "sweep_pilot_ch"
    csv_name = "tests/sweep_decay/results/decay_sweep_pilot_channels.csv"
    
    results = run_sweep(
        config,
        prefix,
        main_tick=args.tick,
        with_diagnostics=args.with_diagnostics,
        anisotropy_splits=args.anisotropy_splits,
    )
    
    write_results(results, csv_name)
    
    print("\n" + "=" * 70)
    print(f"DECAY SWEEP COMPLETE: {len(results)}/{len(config['decay_scale']) * len(config['seeds'])} runs")


if __name__ == "__main__":
    main()
