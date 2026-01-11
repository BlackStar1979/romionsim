"""
I/O utilities for gravity_test.

Functions for loading simulation data and parsing parameters.
"""

import json
from pathlib import Path
from typing import Dict, Tuple


def load_graph_snapshot(log_path: str, tick: int) -> Dict:
    """
    Load GRAPH snapshot at specified tick from JSONL log.
    
    Args:
        log_path: Path to simulation.jsonl
        tick: Tick number to load
        
    Returns:
        Dictionary with 'nodes', 'edges', 'tick'
        
    Raises:
        FileNotFoundError: If log file not found
        ValueError: If tick not found in log
    """
    log_path = Path(log_path)
    if not log_path.exists():
        raise FileNotFoundError(f"Log not found: {log_path}")
    
    found = None
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            obj = json.loads(line)
            if obj.get('type') == 'GRAPH' and obj.get('tick') == tick:
                found = obj
                break
    
    if found is None:
        raise ValueError(f"No GRAPH entry found for tick={tick}")
    
    return found


def parse_tick_range(s: str) -> Tuple[int, int, int]:
    """
    Parse tick range string 'start end step'.
    
    Args:
        s: String like "100 600 100"
        
    Returns:
        Tuple of (start, end, step)
    """
    parts = s.split()
    if len(parts) != 3:
        raise ValueError("tick-range must be: start end step")
    return int(parts[0]), int(parts[1]), int(parts[2])
