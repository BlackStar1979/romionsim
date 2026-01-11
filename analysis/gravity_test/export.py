"""
Export utilities for gravity_test results.

Provides JSON/CSV export for ROMION canonical metrics and distance tables.
"""

import json
from typing import Dict, List
from pathlib import Path


def export_distance_table_json(distance_rows: List[Dict], output_path: str) -> None:
    """
    Export bridge distance distribution to JSON.
    
    ROMION SEMANTICS:
    Exports P(dist | bridge) - probability distribution of distances
    FOR ACTUAL BRIDGED PAIRS.
    
    Args:
        distance_rows: Distance table from distance_table()
        output_path: Path to output JSON file
        
    Format:
        {
            "distances": [
                {
                    "dist": 1,
                    "bridged_pairs": 1079,
                    "p_dist_given_bridge": 1.0,        # PRIMARY ROMION METRIC
                    "bridges": 1389,
                    "weight": 14.659,
                    "avg_bridges_per_pair": 1.29,
                    "avg_weight_per_pair": 0.013,
                    "background_pairs": 1079,          # DIAGNOSTIC
                    "p_bridge_given_dist": 1.0         # DIAGNOSTIC
                },
                ...
            ],
            "metadata": {
                "total_bridged_pairs": 1079,
                "total_distances": 1,
                "d_max": 1
            }
        }
    """
    # Compute metadata
    total_bridged_pairs = sum(r['bridged_pairs'] for r in distance_rows)
    d_max = max(r['dist'] for r in distance_rows) if distance_rows else 0
    
    output = {
        "distances": distance_rows,
        "metadata": {
            "total_bridged_pairs": total_bridged_pairs,
            "total_distances": len(distance_rows),
            "d_max": d_max
        }
    }
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)


def export_distance_table_csv(distance_rows: List[Dict], output_path: str) -> None:
    """
    Export bridge distance distribution to CSV.
    
    ROMION SEMANTICS:
    Exports both PRIMARY (P(dist|bridge)) and DIAGNOSTIC (P(bridge|dist)) metrics.
    
    Args:
        distance_rows: Distance table from distance_table()
        output_path: Path to output CSV file
    """
    import csv
    
    if not distance_rows:
        return
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Updated field names for ROMION semantics
    fieldnames = [
        'dist', 
        'bridged_pairs',           # PRIMARY
        'p_dist_given_bridge',     # PRIMARY: P(dist|bridge)
        'bridges', 
        'weight', 
        'avg_bridges_per_pair',
        'avg_weight_per_pair',
        'background_pairs',        # DIAGNOSTIC
        'p_bridge_given_dist'      # DIAGNOSTIC: P(bridge|dist)
    ]
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(distance_rows)
