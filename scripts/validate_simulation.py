#!/usr/bin/env python3
"""
Simulation Sanity Validator for ROMION

Fast integrity checks after simulation completes.
Catches corrupted data, physics violations, file issues.

Usage:
    python scripts/validate_simulation.py results/my_test/
    python scripts/validate_simulation.py results/my_test/ --verbose
    python scripts/validate_simulation.py --check-all
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class SimulationValidator:
    """Validates simulation output for integrity and sanity."""
    
    def __init__(self, output_dir: Path, verbose: bool = False):
        self.output_dir = output_dir
        self.verbose = verbose
        self.log_path = output_dir / "simulation.jsonl"
        
        self.errors = []
        self.warnings = []
        self.info = []
        self.stats = {}
        
        if not output_dir.exists():
            raise FileNotFoundError(f"Output directory not found: {output_dir}")
        
        if not self.log_path.exists():
            raise FileNotFoundError(f"simulation.jsonl not found in {output_dir}")
    
    def validate(self) -> bool:
        """Run all validations. Returns True if valid."""
        self._check_file_integrity()
        self._check_json_validity()
        self._check_tick_sequence()
        self._check_physics_constraints()
        self._check_graph_consistency()
        self._gather_statistics()
        
        return len(self.errors) == 0
    
    def _check_file_integrity(self):
        """Check file exists and is readable."""
        size_mb = self.log_path.stat().st_size / (1024 * 1024)
        self.stats['file_size_mb'] = size_mb
        
        if size_mb == 0:
            self.errors.append("simulation.jsonl is empty (0 bytes)")
        elif size_mb > 1000:
            self.warnings.append(f"Large file ({size_mb:.1f} MB). May be slow to process.")
        
        self.info.append(f"File size: {size_mb:.1f} MB")
    
    def _check_json_validity(self):
        """Check all lines are valid JSON."""
        line_count = 0
        invalid_lines = []
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                line_count += 1
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    invalid_lines.append((i, str(e)))
                    if len(invalid_lines) >= 10:  # Limit error reporting
                        break
        
        self.stats['total_lines'] = line_count
        
        if invalid_lines:
            for line_num, error in invalid_lines[:5]:  # Show first 5
                self.errors.append(f"Line {line_num}: Invalid JSON - {error}")
            if len(invalid_lines) > 5:
                self.errors.append(f"... and {len(invalid_lines) - 5} more invalid lines")
        else:
            self.info.append(f"Valid JSON: {line_count} entries")
    
    def _check_tick_sequence(self):
        """Check ticks are sequential and complete."""
        ticks_seen = set()
        graph_ticks = set()
        last_tick = -1
        gaps = []
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                    tick = obj.get('tick')
                    
                    if tick is not None:
                        ticks_seen.add(tick)
                        
                        if obj.get('type') == 'GRAPH':
                            graph_ticks.add(tick)
                        
                        # Check for gaps
                        if last_tick >= 0 and tick != last_tick + 1:
                            if tick > last_tick + 1:  # Forward gap
                                gaps.append((last_tick + 1, tick - 1))
                        
                        last_tick = max(last_tick, tick)
                
                except (json.JSONDecodeError, KeyError):
                    continue
        
        if ticks_seen:
            min_tick = min(ticks_seen)
            max_tick = max(ticks_seen)
            self.stats['tick_range'] = (min_tick, max_tick)
            self.stats['ticks_recorded'] = len(ticks_seen)
            self.stats['graph_dumps'] = len(graph_ticks)
            
            self.info.append(f"Ticks: {min_tick} to {max_tick} ({len(ticks_seen)} recorded)")
            self.info.append(f"Graph dumps: {len(graph_ticks)}")
            
            # Check for gaps
            if gaps:
                for start, end in gaps[:3]:  # Show first 3 gaps
                    self.warnings.append(f"Tick gap: {start}-{end} missing")
                if len(gaps) > 3:
                    self.warnings.append(f"... and {len(gaps) - 3} more gaps")
            
            # Check if any graph dumps
            if len(graph_ticks) == 0:
                self.warnings.append("No GRAPH dumps found (analysis will not be possible)")
        else:
            self.errors.append("No ticks found in log")
    
    def _check_physics_constraints(self):
        """Check basic physics: no negative weights, valid ranges."""
        violations = {
            'negative_weights': [],
            'excessive_weights': [],
            'invalid_nodes': []
        }
        
        W_MAX = 10.0  # Generous upper bound
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                    
                    if obj.get('type') == 'GRAPH':
                        tick = obj.get('tick', '?')
                        edges = obj.get('edges', [])
                        
                        for edge in edges:
                            if len(edge) < 3:
                                continue
                            
                            u, v, w = edge[0], edge[1], edge[2]
                            
                            # Check negative weights
                            if w < 0:
                                violations['negative_weights'].append((tick, u, v, w))
                                if len(violations['negative_weights']) >= 5:
                                    break
                            
                            # Check excessive weights
                            if w > W_MAX:
                                violations['excessive_weights'].append((tick, u, v, w))
                                if len(violations['excessive_weights']) >= 5:
                                    break
                            
                            # Check node IDs (should be non-negative integers)
                            if u < 0 or v < 0:
                                violations['invalid_nodes'].append((tick, u, v))
                                if len(violations['invalid_nodes']) >= 5:
                                    break
                
                except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                    continue
        
        # Report violations
        if violations['negative_weights']:
            self.errors.append("PHYSICS VIOLATION: Negative weights detected!")
            for tick, u, v, w in violations['negative_weights'][:3]:
                self.errors.append(f"  Tick {tick}: edge {u}-{v}, weight={w:.6f}")
        
        if violations['excessive_weights']:
            self.warnings.append("Excessive weights detected (>W_MAX)")
            for tick, u, v, w in violations['excessive_weights'][:3]:
                self.warnings.append(f"  Tick {tick}: edge {u}-{v}, weight={w:.3f}")
        
        if violations['invalid_nodes']:
            self.errors.append("Invalid node IDs (negative)")
            for tick, u, v in violations['invalid_nodes'][:3]:
                self.errors.append(f"  Tick {tick}: edge {u}-{v}")
    
    def _check_graph_consistency(self):
        """Check graph properties stay consistent."""
        node_counts = []
        edge_counts = []
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                    
                    if obj.get('type') == 'GRAPH':
                        nodes = obj.get('nodes', [])
                        edges = obj.get('edges', [])
                        
                        node_counts.append(len(nodes))
                        edge_counts.append(len(edges))
                
                except (json.JSONDecodeError, KeyError):
                    continue
        
        if node_counts:
            # Check node count consistency
            if len(set(node_counts)) > 1:
                self.warnings.append(
                    f"Node count varies: {min(node_counts)} to {max(node_counts)}"
                )
            else:
                self.info.append(f"Node count consistent: {node_counts[0]}")
            
            self.stats['node_count'] = node_counts[0] if node_counts else 0
            self.stats['edge_count_range'] = (min(edge_counts), max(edge_counts)) if edge_counts else (0, 0)
            
            self.info.append(f"Edge count range: {min(edge_counts)} to {max(edge_counts)}")
    
    def _gather_statistics(self):
        """Gather overall statistics."""
        # Already populated in other methods
        pass
    
    def print_report(self):
        """Print validation report."""
        print("=" * 70)
        print(f"SIMULATION VALIDATION: {self.output_dir.name}")
        print("=" * 70)
        print()
        
        # Statistics
        print("[STATISTICS]")
        print(f"  File size: {self.stats.get('file_size_mb', 0):.1f} MB")
        print(f"  Total entries: {self.stats.get('total_lines', 0)}")
        if 'tick_range' in self.stats:
            min_t, max_t = self.stats['tick_range']
            print(f"  Tick range: {min_t} to {max_t}")
        print(f"  Graph dumps: {self.stats.get('graph_dumps', 0)}")
        if 'node_count' in self.stats:
            print(f"  Nodes: {self.stats['node_count']}")
        if 'edge_count_range' in self.stats:
            min_e, max_e = self.stats['edge_count_range']
            print(f"  Edges: {min_e} to {max_e}")
        print()
        
        # Errors
        if self.errors:
            print("[ERRORS]")
            for error in self.errors:
                print(f"  [X] {error}")
            print()
        
        # Warnings
        if self.warnings:
            print("[WARNINGS]")
            for warning in self.warnings:
                print(f"  [!] {warning}")
            print()
        
        # Info (if verbose)
        if self.verbose and self.info:
            print("[INFO]")
            for info_msg in self.info:
                print(f"  [i] {info_msg}")
            print()
        
        # Summary
        if not self.errors and not self.warnings:
            print("[OK] Simulation data is valid and clean!")
        elif not self.errors:
            print(f"[OK] Valid ({len(self.warnings)} warnings)")
        else:
            print(f"[FAIL] {len(self.errors)} critical errors detected")
        
        print()
        print("=" * 70)


def validate_all_results(directory: Path):
    """Validate all result directories."""
    result_dirs = [d for d in directory.rglob('*') 
                   if d.is_dir() and (d / 'simulation.jsonl').exists()]
    
    if not result_dirs:
        print(f"No simulation results found in {directory}")
        return
    
    print(f"Found {len(result_dirs)} result directories\n")
    
    results = {'valid': [], 'warnings': [], 'errors': []}
    
    for result_dir in sorted(result_dirs):
        try:
            validator = SimulationValidator(result_dir)
            is_valid = validator.validate()
            
            rel_path = result_dir.relative_to(directory)
            
            if is_valid and not validator.warnings:
                results['valid'].append(result_dir)
                print(f"[OK] {rel_path}")
            elif is_valid:
                results['warnings'].append(result_dir)
                print(f"[WARN] {rel_path} ({len(validator.warnings)} warnings)")
            else:
                results['errors'].append(result_dir)
                print(f"[FAIL] {rel_path} ({len(validator.errors)} errors)")
        
        except Exception as e:
            results['errors'].append(result_dir)
            print(f"[ERROR] {rel_path}: {e}")
    
    # Summary
    print()
    print("=" * 70)
    print(f"SUMMARY: {len(result_dirs)} results checked")
    print(f"  Valid: {len(results['valid'])}")
    print(f"  Warnings: {len(results['warnings'])}")
    print(f"  Errors: {len(results['errors'])}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Validate ROMION simulation output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single result
  python scripts/validate_simulation.py results/my_test/
  
  # Verbose output
  python scripts/validate_simulation.py results/my_test/ --verbose
  
  # Validate all results
  python scripts/validate_simulation.py --check-all
        """
    )
    
    parser.add_argument('output_dir', nargs='?', help='Output directory to validate')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed info')
    parser.add_argument('--check-all', action='store_true',
                       help='Validate all result directories')
    
    args = parser.parse_args()
    
    if args.check_all:
        validate_all_results(Path('.'))
        return 0
    
    if not args.output_dir:
        parser.print_help()
        return 1
    
    try:
        output_dir = Path(args.output_dir)
        validator = SimulationValidator(output_dir, args.verbose)
        is_valid = validator.validate()
        validator.print_report()
        
        return 0 if is_valid else 1
    
    except Exception as e:
        import traceback
        print(f"[ERROR] {e}", file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
