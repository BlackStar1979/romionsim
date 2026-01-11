#!/usr/bin/env python3
"""Find exact theta for 5% node visibility."""

import sys
sys.path.insert(0, ".")

from analysis.projection_ratio_test import measure_projection_ratio

thresholds = [0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58, 0.60]

result = measure_projection_ratio(
    'tests/test_c/results/R2_decayDown/simulation.jsonl',
    400,
    thresholds
)

print('theta -> node%')
print('-' * 20)
for p in result['projections']:
    marker = ' <-- ~5%' if 4.5 < p['node_ratio_percent'] < 5.5 else ''
    print(f"{p['theta']:.2f} -> {p['node_ratio_percent']:.2f}%{marker}")
