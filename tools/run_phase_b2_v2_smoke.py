#!/usr/bin/env python3
"""
Phase B.2 v2.0 smoke test - ONE COMMAND.

Exit codes:
- 0: SUCCESS
- 1: FAILURE
"""

import sys
import json
import random
import hashlib
import platform
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from core.graph import Graph
from core.engine import CoreEngine
from core.metrics import compute_metrics, compute_frustration
from core.projection import compute_projection_metrics


def generate_log(output_path, n_nodes=200, n_ticks=20):
    params = {'theta': 0.25, 'spawn_threshold': 0.15, 'spawn_samples': 500, 'spawn_damping': 0.55,
        'spawn_cap': 500, 'reinforce_factor': 0.05, 'decay_kappa_discount': 0.9, 'min_weight': 0.005,
        'W_max': 2.5, 'w_cap': 2.5, 'beta_2hop': 0.25, 'twohop_sample': 15, 'time_alpha_scale': 1.0,
        'enable_field_tail': False, 'decay': 0.0056, 'frustration_mode': 'exact'}
    
    seed, n_edges_init = 42, 500
    random.seed(seed)
    G = Graph(n_nodes)
    for _ in range(n_edges_init):
        u, v = random.randint(0, n_nodes-1), random.randint(0, n_nodes-1)
        if u != v: G.add_edge(u, v, random.uniform(0.01, 0.5), params['w_cap'])
    
    engine = CoreEngine(G, params)
    cfg_hash = hashlib.sha256(json.dumps(params, sort_keys=True).encode()).hexdigest()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(json.dumps({'schema_version': '2.0', 'type': 'METADATA', 'run_id': 'b2_smoke',
            'seed': seed, 'config_hash': cfg_hash, 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
            'python_version': f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}',
            'platform': platform.system(), 'experiment_name': 'b2_smoke',
            'n_nodes': n_nodes, 'n_edges_init': n_edges_init, 'params': params, 'parameters': params}) + '\n')
        
        for i in range(n_ticks):
            m_pre = compute_metrics(G, params)
            f_pre = compute_frustration(G, m_pre['pressure_map'], params)
            stats = engine.tick()
            m_post = compute_metrics(G, params)
            f_post = compute_frustration(G, m_post['pressure_map'], params)
            proj = compute_projection_metrics(G, params['theta'])
            
            if i % 5 == 0 or i == n_ticks - 1:
                f.write(json.dumps({'type': 'STATE', 'tick': stats['tick'],
                    'metrics_pre': {'layer': 'L1-CORE', 'computed_before_U': True,
                        'mean_kappa': m_pre['mean_kappa'], 'mean_pressure': m_pre['mean_pressure'],
                        'mean_frustration': f_pre['mean_frust'], 'total_weight': sum(e.w for e in G.all_edges()),
                        'n_edges': len(G.edges), 'n_nodes': n_nodes},
                    'evolution': {'layer': 'L1-CORE', 'spawn_new': stats['spawn_new'],
                        'spawn_reinf': stats['spawn_reinf'], 'field_tail_added': stats['field_tail_added'],
                        'removed': stats['removed'], 'norm_ops': stats['norm_ops']},
                    'metrics_post': {'layer': 'L1-CORE', 'computed_after_U': True,
                        'mean_kappa': m_post['mean_kappa'], 'mean_pressure': m_post['mean_pressure'],
                        'mean_frustration': f_post['mean_frust'], 'total_weight': sum(e.w for e in G.all_edges()),
                        'n_edges': len(G.edges), 'n_nodes': n_nodes},
                    'projection': {'layer': 'L2-FRACTURE', 'uses_metrics_post': True,
                        'theta': params['theta'], 'visible_edges': proj['visible_edges'],
                        'visible_ratio': proj['visible_ratio'], 'mean_kappa_visible': proj['mean_kappa_visible']},
                    'observables': {'layer': 'L1-CORE', 'tension_step': stats['tension_step'],
                        'max_acc_tension': stats['max_acc_tension']}}) + '\n')
                # Emit GRAPH snapshot for analysis.gravity_test (expects GRAPH events)
                edges = [[int(e.u), int(e.v), float(e.w)] for e in G.all_edges()]
                f.write(json.dumps({
                    'type': 'GRAPH',
                    'tick': stats['tick'],
                    'n_nodes': n_nodes,
                    'n_edges': len(edges),
                    'edges': edges
                }) + '\n')
        
        f.write(json.dumps({'type': 'COMPLETION', 'final_tick': engine.n,
            'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'status': 'complete'}) + '\n')
    
    print(f"[OK] Generated: {output_path} (N={n_nodes}, T={n_ticks})")


def validate_log(log_path):
    validator = REPO_ROOT / 'scripts' / 'validate_log_schema.py'
    if not validator.exists():
        print(f"[ERROR] Validator missing: {validator}")
        return False
    
    import subprocess
    result = subprocess.run([sys.executable, str(validator), str(log_path)], capture_output=True, text=True)
    print("\n" + result.stdout)
    return 'VALID' in result.stdout and result.returncode == 0


def check_exp5(log_path):
    failures = []
    with open(log_path) as f:
        for line in f:
            evt = json.loads(line)
            if evt.get('type') != 'STATE': continue
            
            t, p, m = evt['tick'], evt['projection'], evt['metrics_post']
            theta, mkv, vr, mk = p['theta'], p['mean_kappa_visible'], p['visible_ratio'], m['mean_kappa']
            
            if not (0 <= vr <= 1): failures.append(f"T{t}: vr={vr} ∉ [0,1]")
            if not (theta <= mkv <= 1.0): failures.append(f"T{t}: mkv={mkv} ∉ [{theta},1]")
            if not (mkv >= mk): failures.append(f"T{t}: mkv={mkv} < mk={mk}")
    
    if failures:
        print("\n[FAIL] EXP 5 FAILURES:")
        for f in failures: print(f"   {f}")
        return False
    print("\n[PASS] EXP 5: PASS")
    return True


def main():
    print("="*70)
    print("PHASE B.2 V2.0 SMOKE TEST")
    print("="*70)
    
    output = REPO_ROOT / 'results' / 'phase_b2_smoke.jsonl'
    
    print("\n[1/3] Generate...")
    try: generate_log(output)
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1
    
    print("\n[2/3] Validate...")
    if not validate_log(output): return 1
    
    print("\n[3/3] Exp 5...")
    if not check_exp5(output): return 1
    
    print("\n" + "="*70)
    print("[PASS] SMOKE TEST PASSED")
    print("="*70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
