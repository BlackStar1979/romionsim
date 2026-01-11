"""Time evolution of channel metrics for R2_decayDown."""

import subprocess
import sys

run = 'R2_decayDown'
ticks = [100, 200, 300, 400, 500, 600]

print('=' * 80)
print(f'TIME EVOLUTION: {run} - channel metrics across ticks')
print('=' * 80)
print()

results = []

for tick in ticks:
    log_path = f'tests/test_c/results/{run}/simulation.jsonl'
    
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
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f'Tick {tick}: ERROR')
        continue
    
    output = result.stdout
    
    # Extract metrics
    bridges = 'N/A'
    channel_cap = 'N/A'
    anisotropy = 'N/A'
    clusters = 'N/A'
    hub_share = 'N/A'
    
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('Total bridges:'):
            bridges = line.split(':')[1].strip()
        if line.startswith('channel_capacity:'):
            channel_cap = line.split(':')[1].strip()
        if line.startswith('anisotropy:') and 'split-axis' not in line.lower():
            anisotropy = line.split(':')[1].strip()
        if line.startswith('Clusters:'):
            clusters = line.split(':')[1].strip()
        if line.startswith('Hub share:'):
            hub_share = line.split(':')[1].strip()
    
    results.append({
        'tick': tick,
        'clusters': clusters,
        'bridges': bridges,
        'hub_share': hub_share,
        'channel_cap': channel_cap,
        'anisotropy': anisotropy
    })
    print(f'Tick {tick}: bridges={bridges}, ch_cap={channel_cap}, aniso={anisotropy}')

print()
print('=' * 80)
print('EVOLUTION TABLE')
print('=' * 80)
header = f"{'Tick':<8} {'Clusters':<10} {'Bridges':<10} {'Hub%':<10} {'Ch.Cap':<12} {'Aniso':<12}"
print(header)
print('-' * 70)

for r in results:
    row = f"{r['tick']:<8} {r['clusters']:<10} {r['bridges']:<10} {r['hub_share']:<10} {r['channel_cap']:<12} {r['anisotropy']:<12}"
    print(row)

print('=' * 80)
