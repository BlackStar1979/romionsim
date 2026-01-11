#!/usr/bin/env python3
"""
Gravity Test - Bridge Analysis for ROMION

Entry point wrapper for backward compatibility.
The actual implementation is in the gravity_test/ package.

Usage:
    python analysis/gravity_test.py --log simulation.jsonl --tick 400 --wcluster 0.02
"""

from gravity_test.main import main

if __name__ == '__main__':
    main()
