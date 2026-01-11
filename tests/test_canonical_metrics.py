#!/usr/bin/env python3
"""
Test canonical metrics validation (KROK 3).

Tests validate_canonical_metrics() against CANONICAL_METRICS.md v1.0.
"""

import sys
from pathlib import Path

# Add project root
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

# Now import works
from analysis.gravity_test.validate_romion import (
    validate_canonical_metrics,
    validate_L1_metrics,
    validate_L2_metrics,
    validate_L3_metrics,
    ValidationStatus
)


def test_L1_valid():
    """Test valid L1-CORE metrics."""
    metrics = {
        'mean_kappa': 0.5,
        'mean_pressure': 1.2,
        'mean_frustration': 0.1,
        'total_weight': 1000.0,
        'n_edges': 100,
        'n_nodes': 50
    }
    
    status, reasons = validate_L1_metrics(metrics, schema_version="2.0")
    assert status == ValidationStatus.VALID, f"Expected VALID, got {status}: {reasons}"
    print("[PASS] test_L1_valid PASSED")


def test_L1_missing_frustration():
    """Test L1 missing frustration (v2.0 requirement)."""
    metrics = {
        'mean_kappa': 0.5,
        'mean_pressure': 1.2,
        # missing mean_frustration
        'total_weight': 1000.0,
        'n_edges': 100,
        'n_nodes': 50
    }
    
    status, reasons = validate_L1_metrics(metrics, schema_version="2.0")
    assert status == ValidationStatus.INVALID_THEORY, f"Expected INVALID_THEORY, got {status}"
    assert any("mean_frustration" in r for r in reasons), f"Expected frustration error, got: {reasons}"
    print("[PASS] test_L1_missing_frustration PASSED")


def test_L1_invalid_bounds():
    """Test L1 metrics out of bounds."""
    metrics = {
        'mean_kappa': 2.0,  # Way too high (beyond tolerance)
        'mean_pressure': -0.1,  # Negative
        'mean_frustration': 0.1,
        'total_weight': 1000.0,
        'n_edges': 100,
        'n_nodes': 50
    }
    
    status, reasons = validate_L1_metrics(metrics, schema_version="2.0")
    assert status == ValidationStatus.INVALID_TECH, f"Expected INVALID_TECH, got {status}"
    # At least one error expected (either kappa or pressure or both)
    assert len(reasons) > 0, "Expected errors for out-of-bounds metrics"
    print("[PASS] test_L1_invalid_bounds PASSED")


def test_L2_valid():
    """Test valid L2-FRACTURE projection."""
    projection = {
        'visible_edges': 50,
        'visible_ratio': 0.5,
        'uses_metrics_post': True
    }
    
    metrics_post = {
        'n_edges': 100
    }
    
    theta = 0.25
    
    status, reasons = validate_L2_metrics(projection, metrics_post, theta)
    assert status == ValidationStatus.VALID, f"Expected VALID, got {status}: {reasons}"
    print("[PASS] test_L2_valid PASSED")


def test_L2_uses_metrics_pre():
    """Test L2 projection using metrics_pre (CRITICAL ERROR)."""
    projection = {
        'visible_edges': 50,
        'uses_metrics_post': False  # WRONG!
    }
    
    metrics_post = {
        'n_edges': 100
    }
    
    theta = 0.25
    
    status, reasons = validate_L2_metrics(projection, metrics_post, theta)
    assert status == ValidationStatus.INVALID_THEORY, f"Expected INVALID_THEORY, got {status}"
    assert any("CRITICAL" in r for r in reasons), f"Expected CRITICAL error, got: {reasons}"
    print("[PASS] test_L2_uses_metrics_pre PASSED")


def test_L2_visible_exceeds_total():
    """Test L2 visible_edges > n_edges (impossible)."""
    projection = {
        'visible_edges': 150,  # More than total!
        'uses_metrics_post': True
    }
    
    metrics_post = {
        'n_edges': 100
    }
    
    theta = 0.25
    
    status, reasons = validate_L2_metrics(projection, metrics_post, theta)
    assert status == ValidationStatus.INVALID_TECH, f"Expected INVALID_TECH, got {status}"
    assert any("visible_edges" in r and "n_edges" in r for r in reasons), f"Expected visible>total error"
    print("[PASS] test_L2_visible_exceeds_total PASSED")


def test_L3_valid():
    """Test valid L3-INTERPRETATION metrics."""
    metrics = {
        'hub_share': 30.0,
        'coverage': 60.0,
        'R0': 0.5,  # 30/60
        'R2': 0.1
    }
    
    status, reasons = validate_L3_metrics(metrics)
    assert status == ValidationStatus.VALID, f"Expected VALID, got {status}: {reasons}"
    print("[PASS] test_L3_valid PASSED")


def test_L3_invalid_bounds():
    """Test L3 metrics out of bounds."""
    metrics = {
        'hub_share': 150.0,  # > 100!
        'coverage': -10.0,   # Negative!
        'R0': 0.5,
        'R2': 1.5  # > 1!
    }
    
    status, reasons = validate_L3_metrics(metrics)
    assert status == ValidationStatus.INVALID_TECH, f"Expected INVALID_TECH, got {status}"
    assert any("hub_share" in r for r in reasons), "Expected hub_share error"
    assert any("coverage" in r for r in reasons), "Expected coverage error"
    assert any("R2" in r for r in reasons), "Expected R2 error"
    print("[PASS] test_L3_invalid_bounds PASSED")


def test_complete_validation():
    """Test complete canonical metrics validation."""
    metrics_pre = {
        'mean_kappa': 0.45,
        'mean_pressure': 1.0,
        'mean_frustration': 0.12,
        'total_weight': 900.0,
        'n_edges': 90,
        'n_nodes': 50
    }
    
    metrics_post = {
        'mean_kappa': 0.50,
        'mean_pressure': 1.1,
        'mean_frustration': 0.10,
        'total_weight': 1000.0,
        'n_edges': 100,
        'n_nodes': 50
    }
    
    projection = {
        'visible_edges': 50,
        'visible_ratio': 0.5,
        'uses_metrics_post': True
    }
    
    analysis = {
        'hub_share': 30.0,
        'coverage': 60.0,
        'R0': 0.5,
        'R2': 0.0
    }
    
    theta = 0.25
    
    status, reasons = validate_canonical_metrics(
        metrics_pre=metrics_pre,
        metrics_post=metrics_post,
        projection=projection,
        analysis_metrics=analysis,
        theta=theta,
        schema_version="2.0"
    )
    
    assert status == ValidationStatus.VALID, f"Expected VALID, got {status}: {reasons}"
    print("[PASS] test_complete_validation PASSED")


def main():
    """Run all tests."""
    print("=" * 70)
    print("CANONICAL METRICS VALIDATION - TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        test_L1_valid,
        test_L1_missing_frustration,
        test_L1_invalid_bounds,
        test_L2_valid,
        test_L2_uses_metrics_pre,
        test_L2_visible_exceeds_total,
        test_L3_valid,
        test_L3_invalid_bounds,
        test_complete_validation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"RESULTS: {passed}/{len(tests)} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("[SUCCESS] All tests passed")
        return 0
    else:
        print(f"[FAILED] {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

