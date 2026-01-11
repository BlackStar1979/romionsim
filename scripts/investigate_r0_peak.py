"""
Dense time evolution analysis for R0 peak investigation.

Focus: tick 250-350 (peak window) with 10-tick intervals
Goal: Understand mechanism of 11.29 capacity spike @ tick 300
"""

import subprocess
import sys
import csv
from pathlib import Path

run = 'R0_base'
# Use available GRAPH dumps (every 100 ticks)
ticks = [100, 200, 300, 400, 500, 600]

print('=' * 80)
print(f'R0 PEAK INVESTIGATION: Time evolution @ available GRAPH dumps')
print(f'Ticks: {ticks}')
print('=' * 80)
print()

results = []

for i, tick in enumerate(ticks, 1):
    log_path = f'tests/test_c/results/{run}/simulation.jsonl'
    
    cmd = [
        sys.executable, 'analysis/gravity_test.py',
        '--log', log_path,
        '--tick', str(tick),
        '--wcluster', '0.02',
        '--wdist', '0.005', 
        '--wbridge', '0.0',
        '--disconnected-policy', 'maxdist',
        '--channels',
        '--channels-mode', 'cut_weight',
        '--anisotropy',
        '--anisotropy-splits', '5'
    ]
    
    print(f'[{i}/{len(ticks)}] Analyzing tick {tick}... ', end='', flush=True)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print('ERROR')
        continue
    
    output = result.stdout
    
    # Extract metrics
    bridges_count = None
    bridges_weight = None
    channel_cap = None
    anisotropy = None
    clusters = None
    hub_share = None
    coverage = None
    
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('Total bridges:'):
            bridges_count = int(line.split(':')[1].strip())
        if line.startswith('Total weight:'):
            bridges_weight = float(line.split(':')[1].strip())
        if line.startswith('channel_capacity:'):
            channel_cap = float(line.split(':')[1].strip())
        if line.startswith('anisotropy:') and 'split-axis' not in line.lower():
            anisotropy = float(line.split(':')[1].strip())
        if line.startswith('Clusters:'):
            clusters = int(line.split(':')[1].strip())
        if line.startswith('Hub share:'):
            hub_share = float(line.split(':')[1].strip().rstrip('%'))
        if line.startswith('Coverage:'):
            coverage = float(line.split(':')[1].strip().rstrip('%'))
    
    results.append({
        'tick': tick,
        'clusters': clusters,
        'bridges_count': bridges_count,
        'bridges_weight': bridges_weight,
        'channel_capacity': channel_cap,
        'anisotropy': anisotropy,
        'hub_share': hub_share,
        'coverage': coverage,
    })
    
    print(f'bridges={bridges_count}, cap={channel_cap:.3f}, aniso={anisotropy:.3f}')

# Write CSV
output_csv = Path('tests/test_c/results/R0_base/peak_analysis_dense.csv')
fieldnames = ['tick', 'clusters', 'bridges_count', 'bridges_weight', 
              'channel_capacity', 'anisotropy', 'hub_share', 'coverage']

with open(output_csv, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print()
print('=' * 80)
print(f'Results written to: {output_csv}')
print('=' * 80)
print()

# Summary statistics
print('PEAK ANALYSIS:')
print()

max_cap_entry = max(results, key=lambda x: x['channel_capacity'] or 0)
max_bridges_entry = max(results, key=lambda x: x['bridges_count'] or 0)
max_aniso_entry = max(results, key=lambda x: x['anisotropy'] or 0)

print(f'Maximum capacity:')
print(f'  tick {max_cap_entry["tick"]}: {max_cap_entry["channel_capacity"]:.3f}')
print(f'  bridges: {max_cap_entry["bridges_count"]}')
print(f'  anisotropy: {max_cap_entry["anisotropy"]:.3f}')
print()

print(f'Maximum bridges:')
print(f'  tick {max_bridges_entry["tick"]}: {max_bridges_entry["bridges_count"]}')
print(f'  capacity: {max_bridges_entry["channel_capacity"]:.3f}')
print(f'  anisotropy: {max_bridges_entry["anisotropy"]:.3f}')
print()

print(f'Maximum anisotropy:')
print(f'  tick {max_aniso_entry["tick"]}: {max_aniso_entry["anisotropy"]:.3f}')
print(f'  bridges: {max_aniso_entry["bridges_count"]}')
print(f'  capacity: {max_aniso_entry["channel_capacity"]:.3f}')
print()

# Find transitions
print('PHASE TRANSITIONS (anisotropy > 0.05):')
for r in results:
    if r['anisotropy'] and r['anisotropy'] > 0.05:
        print(f'  tick {r["tick"]}: aniso={r["anisotropy"]:.3f}, bridges={r["bridges_count"]}, cap={r["channel_capacity"]:.3f}')
print()

print('COLLAPSE PATTERN (bridge decay):')
prev_bridges = None
for r in results:
    if prev_bridges and r['bridges_count']:
        delta = r['bridges_count'] - prev_bridges
        if delta < -100:  # Large drop
            print(f'  tick {r["tick"]}: {delta} bridges (from {prev_bridges} to {r["bridges_count"]})')
    prev_bridges = r['bridges_count']
