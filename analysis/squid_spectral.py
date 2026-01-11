"""
SQUID-B Spectral Analysis

Analyzes power spectral density (PSD) of ROMION observables.
Tests for Self-Organized Criticality (SOC) via 1/f noise detection.

Uses Δ-signals (first differences) to remove global trends.
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

JSONL_PATH = "simulation.jsonl"
START_TICK = 300  # Skip transient phase

# Field name candidates (auto-detection)
CANDIDATES = {
    "tick": ["tick", "t", "step", "TICK"],
    "visible_edges": ["visible_edges", "vis_edges", "visible"],
    "tension": ["max_acc_tension", "tension", "TENSION"],
    "mean_pressure": ["mean_pressure", "pressure_avg", "p_avg"],
}


def iter_rows(path):
    """Yield data rows from JSONL."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                if "data" in obj:
                    yield obj["data"]
                else:
                    yield obj
            except:
                continue


def detect_keys(sample):
    """Auto-detect field names from sample row."""
    out = {}
    for k, aliases in CANDIDATES.items():
        for a in aliases:
            if a in sample:
                out[k] = a
                break
    return out


def load_data():
    """Load data with auto-detected field names."""
    rows = list(iter_rows(JSONL_PATH))
    if not rows:
        raise ValueError("No data in JSONL file")
        
    sample = rows[-1]
    keys = detect_keys(sample)
    print("Detected fields:", keys)

    data = {k: [] for k in keys}
    for r in rows:
        t = r.get(keys["tick"])
        if t is None or t < START_TICK:
            continue
        for k, kk in keys.items():
            data[k].append(float(r.get(kk, 0.0)))

    for k in data:
        data[k] = np.asarray(data[k])

    return data


def delta(x):
    """First difference (removes linear trends)."""
    return np.diff(np.asarray(x))


def psd_alpha(signal):
    """
    Compute power spectral density and fit α.
    
    Returns:
        α: Spectral exponent (S(f) ∝ 1/f^α)
        f: Frequencies
        P: Power spectral density
    """
    # Remove mean
    signal = signal - np.mean(signal)
    
    # Welch's method (averages periodograms)
    f, P = welch(signal, nperseg=min(256, len(signal)))
    
    # Remove DC component (f=0)
    f, P = f[1:], P[1:]
    
    # Fit in log-log space within valid range
    mask = (f > 0) & (f < 0.2)  # Avoid too low/high frequencies
    lf = np.log10(f[mask])
    lP = np.log10(P[mask])
    
    slope, _ = np.polyfit(lf, lP, 1)
    alpha = -slope  # S(f) ∝ f^(-α)
    
    return alpha, f, P


def analyze(name, sig, ax_time, ax_psd):
    """Analyze signal and plot results."""
    a, f, P = psd_alpha(sig)

    # Time domain
    ax_time.plot(sig)
    ax_time.set_title(f"{name} (time)")
    ax_time.grid(alpha=0.3)

    # Frequency domain
    ax_psd.loglog(f, P)
    ax_psd.set_title(f"{name} PSD | α≈{a:.2f}")
    ax_psd.grid(alpha=0.3, which="both")

    # Interpretation
    if 0.5 <= a <= 1.5:
        verdict = "PINK NOISE (1/f - SOC)"
    elif a > 1.5:
        verdict = "BROWN NOISE"
    else:
        verdict = "WHITE NOISE"
    
    print(f"{name:20} α={a:.3f} | {verdict}")


def main():
    """Run spectral analysis."""
    data = load_data()

    # Compute Δ-signals
    series = {
        "Δ_visible_edges": delta(data["visible_edges"]),
        "Δ_tension": delta(data["tension"]),
        "Δ_mean_pressure": delta(data["mean_pressure"]),
    }

    n = len(series)
    fig, axs = plt.subplots(n, 2, figsize=(14, 3*n))

    print("\nSpectral Analysis Results:")
    print("-" * 50)
    
    for i, (name, sig) in enumerate(series.items()):
        analyze(name, sig, axs[i, 0], axs[i, 1])

    plt.tight_layout()
    plt.savefig("analysis/squid_spectral.png", dpi=160)
    print("\nSaved: analysis/squid_spectral.png")
    plt.show()


if __name__ == "__main__":
    main()
