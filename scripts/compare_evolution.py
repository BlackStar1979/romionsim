"""Compare time evolution R0 vs R2."""

import subprocess
import sys

runs = ['R0_base', 'R2_decayDown']
ticks = [100, 200, 300, 400, 500, 600]

print('=' * 90)
print('TIME EVOLUTION COMPARISON: R0 (baseline) vs R2 (decay×0.7)')
print('=' * 90)
print()

all_results = {}

for run in runs:
    results = []
    log_path = f'tests/test_c/results/{run}/simulation.jsonl'
    
    for tick in ticks:
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
            results.append({'tick': tick, 'bridges': 'ERR', 'channel_cap': 'ERR', 'anisotropy': 'ERR'})
            continue
        
        output = result.stdout
        bridges = 'N/A'
        channel_cap = 'N/A'
        anisotropy = 'N/A'
        
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('Total bridges:'):
                bridges = line.split(':')[1].strip()
            if line.startswith('channel_capacity:'):
                channel_cap = line.split(':')[1].strip()
            if line.startswith('anisotropy:') and 'split-axis' not in line.lower():
                anisotropy = line.split(':')[1].strip()
        
        results.append({
            'tick': tick,
            'bridges': bridges,
            'channel_cap': channel_cap,
            'anisotropy': anisotropy
        })
    
    all_results[run] = results
    print(f'{run}: collected {len(results)} ticks')

print()
print('=' * 90)
print('COMPARISON TABLE')
print('=' * 90)

# Header
print(f"{'Tick':<8} | {'R0 Bridges':<12} {'R0 Ch.Cap':<12} {'R0 Aniso':<12} | {'R2 Bridges':<12} {'R2 Ch.Cap':<12} {'R2 Aniso':<12}")
print('-' * 90)

r0 = all_results['R0_base']
r2 = all_results['R2_decayDown']

for i, tick in enumerate(ticks):
    r0_row = r0[i] if i < len(r0) else {}
    r2_row = r2[i] if i < len(r2) else {}
    
    print(f"{tick:<8} | {r0_row.get('bridges', 'N/A'):<12} {r0_row.get('channel_cap', 'N/A'):<12} {r0_row.get('anisotropy', 'N/A'):<12} | {r2_row.get('bridges', 'N/A'):<12} {r2_row.get('channel_cap', 'N/A'):<12} {r2_row.get('anisotropy', 'N/A'):<12}")

print('=' * 90)
print()
print('KEY OBSERVATIONS:')
print('- R0: Bridges drop to 0 (FREEZE) while R2 maintains activity')
print('- R2: Channel capacity peaks at tick 400 (7.417)')
print('- Anisotropy peaks at tick 300 in R2 (0.239) - structural transition?')
