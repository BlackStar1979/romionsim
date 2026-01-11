"""Full comparison test R0-R5 with channels/anisotropy metrics."""

import subprocess
import sys
from pathlib import Path

runs = ['R0_base', 'R1_spawnUp', 'R2_decayDown', 'R3_tensionUp', 'R4_combo', 'R5_shock']
tick = 400

print('=' * 80)
print('FULL COMPARISON TEST: R0-R5 @ tick 400 with channels/anisotropy')
print('=' * 80)
print()

results = []

for run in runs:
    log_path = f'tests/test_c/results/{run}/simulation.jsonl'
    
    if not Path(log_path).exists():
        print(f'{run}: MISSING FILE')
        continue
    
    cmd = [
        sys.executable, 'analysis/gravity_test.py',
        '--log', log_path,
        '--tick', str(tick),
        '--wcluster', '0.02',
        '--wdist', '0.005', 
        '--wbridge', '0.0',
        '--channels',
        '--anisotropy',
        '--anisotropy-splits', '5'
    ]
    
    print(f'Running {run}...')
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f'  ERROR: {result.stderr}')
        continue
    
    output = result.stdout
    
    # Extract key metrics
    bridges = 'N/A'
    hub_share = 'N/A'
    coverage = 'N/A'
    channel_cap = 'N/A'
    anisotropy = 'N/A'
    clusters = 'N/A'
    
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('Total bridges:'):
            bridges = line.split(':')[1].strip()
        if line.startswith('Hub share:'):
            hub_share = line.split(':')[1].strip()
        if line.startswith('Coverage:'):
            coverage = line.split(':')[1].strip()
        if line.startswith('channel_capacity:'):
            channel_cap = line.split(':')[1].strip()
        if line.startswith('anisotropy:') and 'split-axis' not in line.lower():
            anisotropy = line.split(':')[1].strip()
        if line.startswith('Clusters:'):
            clusters = line.split(':')[1].strip()
    
    results.append({
        'run': run,
        'clusters': clusters,
        'bridges': bridges,
        'hub_share': hub_share,
        'coverage': coverage,
        'channel_cap': channel_cap,
        'anisotropy': anisotropy
    })
    print(f'  clusters={clusters}, bridges={bridges}, ch_cap={channel_cap}, aniso={anisotropy}')

print()
print('=' * 80)
print('SUMMARY TABLE')
print('=' * 80)
header = f"{'Run':<15} {'Clusters':<10} {'Bridges':<10} {'Hub%':<10} {'Cover%':<10} {'Ch.Cap':<10} {'Aniso':<12}"
print(header)
print('-' * 80)

for r in results:
    row = f"{r['run']:<15} {r['clusters']:<10} {r['bridges']:<10} {r['hub_share']:<10} {r['coverage']:<10} {r['channel_cap']:<10} {r['anisotropy']:<12}"
    print(row)

print('=' * 80)

# Save to CSV
csv_path = 'tests/test_c/CHANNELS_COMPARISON.csv'
with open(csv_path, 'w') as f:
    f.write('run,clusters,bridges,hub_share,coverage,channel_capacity,anisotropy\n')
    for r in results:
        f.write(f"{r['run']},{r['clusters']},{r['bridges']},{r['hub_share']},{r['coverage']},{r['channel_cap']},{r['anisotropy']}\n")

print(f'\nResults saved to: {csv_path}')
