#!/usr/bin/env python3
"""
Exp 5: Mean Kappa Visible Consistency Checker.

Automated bounds checking for schema v2.0 logs.

Exit codes:
- 0: PASS (all bounds hold)
- 1: FAIL (bounds violated)
- 2: INVALID (missing required fields)
"""

import sys
import json
from pathlib import Path


def check_exp5(log_path):
    """
    Check Exp 5 bounds on schema v2.0 log.
    
    Checks:
    1. 0 <= visible_ratio <= 1
    2. theta <= mean_kappa_visible <= 1.0
    3. mean_kappa_visible >= mean_kappa (post)
    
    Returns:
        (status, failures) where status in ['PASS', 'FAIL', 'INVALID']
    """
    
    failures = []
    ticks_checked = 0
    missing_fields = set()
    
    with open(log_path) as f:
        for line in f:
            evt = json.loads(line)
            
            if evt.get('type') != 'STATE':
                continue
            
            tick = evt.get('tick', '?')
            
            # Check required fields
            try:
                proj = evt['projection']
                post = evt['metrics_post']
                
                theta = proj['theta']
                mkv = proj['mean_kappa_visible']
                vr = proj['visible_ratio']
                mk = post['mean_kappa']
            except KeyError as e:
                missing_fields.add(str(e))
                continue
            
            ticks_checked += 1
            
            # Check 1: visible_ratio bounds
            if not (0 <= vr <= 1):
                failures.append({
                    'tick': tick,
                    'check': 'visible_ratio ∈ [0,1]',
                    'value': vr,
                    'expected': '[0, 1]'
                })
            
            # Check 2: mean_kappa_visible bounds
            if not (theta <= mkv <= 1.0):
                failures.append({
                    'tick': tick,
                    'check': 'theta ≤ mean_kappa_visible ≤ 1.0',
                    'value': mkv,
                    'expected': f'[{theta}, 1.0]'
                })
            
            # Check 3: selection effect
            if not (mkv >= mk):
                failures.append({
                    'tick': tick,
                    'check': 'mean_kappa_visible ≥ mean_kappa',
                    'values': f'{mkv} >= {mk}',
                    'delta': mkv - mk
                })
    
    if missing_fields:
        return ('INVALID', list(missing_fields))
    
    if failures:
        return ('FAIL', failures)
    
    if ticks_checked == 0:
        return ('INVALID', ['No STATE events found'])
    
    return ('PASS', ticks_checked)


def main():
    if len(sys.argv) < 2:
        print("Usage: exp5_check.py <log.jsonl>")
        return 2
    
    log_path = Path(sys.argv[1])
    
    if not log_path.exists():
        print(f"❌ File not found: {log_path}")
        return 2
    
    print("=" * 70)
    print(f"EXP 5 CONSISTENCY CHECK: {log_path.name}")
    print("=" * 70)
    
    status, result = check_exp5(log_path)
    
    if status == 'INVALID':
        print(f"\n❌ INVALID: Missing required fields")
        for field in result:
            print(f"   - {field}")
        return 2
    
    elif status == 'FAIL':
        print(f"\n❌ FAIL: {len(result)} bounds violations\n")
        for f in result:
            print(f"Tick {f['tick']}:")
            print(f"  Check: {f['check']}")
            if 'value' in f:
                print(f"  Value: {f['value']}")
                print(f"  Expected: {f['expected']}")
            if 'values' in f:
                print(f"  Values: {f['values']}")
                print(f"  Delta: {f.get('delta', 'N/A')}")
            print()
        return 1
    
    elif status == 'PASS':
        print(f"\n✅ PASS: All bounds hold")
        print(f"   Ticks checked: {result}")
        print(f"   Checks per tick: 3 (visible_ratio, kappa bounds, selection)")
        print(f"   Total checks: {result * 3}")
        return 0


if __name__ == '__main__':
    sys.exit(main())
