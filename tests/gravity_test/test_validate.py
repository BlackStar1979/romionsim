"""Tests for validation layer (fail-closed)."""

from __future__ import annotations

import math
import pytest


def test_validate_metrics_ok():
    from analysis.gravity_test.validate import validate_metrics

    ok, reasons = validate_metrics({
        "hub_share": 80.0,
        "coverage": 100.0,
        "unassigned_nodes": 0,
        "channel_capacity": 12.0,
        "anisotropy": 0.5,
    })
    assert ok is True
    assert reasons == []


def test_validate_metrics_bounds_fail():
    from analysis.gravity_test.validate import validate_metrics

    ok, reasons = validate_metrics({
        "hub_share": 120.0,
        "coverage": -1.0,
        "unassigned_nodes": -5,
    })
    assert ok is False
    assert any("hub_share out of [0,100]" in r for r in reasons)
    assert any("coverage out of [0,100]" in r for r in reasons)
    assert any("unassigned_nodes negative" in r for r in reasons)


def test_validate_metrics_nan_inf_fail():
    from analysis.gravity_test.validate import validate_metrics

    ok, reasons = validate_metrics({
        "hub_share": float("nan"),
        "coverage": float("inf"),
        "anisotropy": -0.1,
    })
    assert ok is False
    assert any("hub_share is not finite" in r for r in reasons)
    assert any("coverage is not finite" in r for r in reasons)
    assert any("anisotropy negative" in r for r in reasons)


def test_validate_metrics_negative_channel_capacity_fail():
    from analysis.gravity_test.validate import validate_metrics

    ok, reasons = validate_metrics({
        "hub_share": 50.0,
        "coverage": 50.0,
        "channel_capacity": -1.0,
    })
    assert ok is False
    assert any("channel_capacity negative" in r for r in reasons)


def test_format_invalid_report():
    from analysis.gravity_test.validate import format_invalid_report

    report = format_invalid_report(["hub_share out of [0,100]: 120", "coverage negative"])
    assert "INVALID RUN" in report
    assert "hub_share" in report
    assert "coverage" in report
