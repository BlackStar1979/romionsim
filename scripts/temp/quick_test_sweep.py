#!/usr/bin/env python3
"""Quick test - just 2 runs to verify batch_sweep works."""

import subprocess
import sys

# Just test decay=1.0 and decay=0.7 with seed=42
TEST_RUNS = [
    (1.0, 42),
    (0.7, 42),
]

def test_single_run(decay, seed):
    """Test single sweep point."""
    cmd = [
        "python", "scripts/run_romion_extended.py",
        "--ticks", "600",
        "--decay-scale", str(decay),
        "--seed", str(seed),
        "--dump-graph-every", "100",
        "--out", f"tests/sweep_decay/test/d{decay}_s{seed}",
    ]
    
    print(f"\n{'='*70}")
    print(f"Testing: decay={decay}, seed={seed}")
    print(f"{'='*70}")
    
    proc = subprocess.run(cmd, timeout=300)
    return proc.returncode == 0

def main():
    print("QUICK TEST: 2 simulation runs")
    print(f"This will take ~5-10 minutes")
    
    for decay, seed in TEST_RUNS:
        success = test_single_run(decay, seed)
        if not success:
            print(f"\n[FAIL] Run failed: decay={decay}, seed={seed}")
            return 1
        print(f"\n[OK] Run complete: decay={decay}, seed={seed}")
    
    print("\n" + "="*70)
    print("[SUCCESS] All test runs complete!")
    print("batch_sweep.py should now work.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
