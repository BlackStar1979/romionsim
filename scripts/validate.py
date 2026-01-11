#!/usr/bin/env python3
"""
Integrated ROMION Validator

Complete validation suite:
- Config validation (before run)
- Simulation sanity (after run)
- Theory consistency (deep checks)

Usage:
    python scripts/validate.py --config cfg/my_test.cfg
    python scripts/validate.py --simulation results/my_test/
    python scripts/validate.py --all results/my_test/
    python scripts/validate.py --theory results/my_test/
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Import our validators
try:
    from validate_config import ConfigValidator
    from validate_simulation import SimulationValidator
except ImportError:
    # Try relative import
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from validate_config import ConfigValidator
    from validate_simulation import SimulationValidator


class TheoryValidator:
    """Validates theory-level consistency of simulation results."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.log_path = output_dir / "simulation.jsonl"
        
        self.errors = []
        self.warnings = []
        self.info = []
        
        if not self.log_path.exists():
            raise FileNotFoundError(f"simulation.jsonl not found in {output_dir}")
    
    def validate(self) -> bool:
        """Run theory-level validations."""
        self._check_conservation_laws()
        self._check_edge_evolution()
        self._check_weight_bounds()
        self._check_graph_properties()
        
        return len(self.errors) == 0
    
    def _check_conservation_laws(self):
        """Check if total weight is approximately conserved."""
        weight_samples = []
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                    
                    if obj.get('type') == 'GRAPH':
                        edges = obj.get('edges', [])
                        total_w = sum(e[2] for e in edges if len(e) >= 3)
                        weight_samples.append((obj.get('tick'), total_w))
                
                except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                    continue
        
        if len(weight_samples) < 2:
            self.warnings.append("Not enough GRAPH samples to check conservation")
            return
        
        # Check if total weight stays within reasonable bounds
        weights = [w for _, w in weight_samples]
        min_w, max_w = min(weights), max(weights)
        mean_w = sum(weights) / len(weights)
        
        variation = (max_w - min_w) / mean_w if mean_w > 0 else 0
        
        self.info.append(f"Weight range: {min_w:.1f} to {max_w:.1f} (mean: {mean_w:.1f})")
        
        # With spawn and decay, we expect some variation
        # But if it's > 100%, something is wrong
        if variation > 1.0:
            self.warnings.append(
                f"Large weight variation: {variation*100:.1f}% "
                f"(spawn/decay may be unbalanced)"
            )
        elif variation > 0.5:
            self.info.append(f"Weight variation: {variation*100:.1f}% (normal with spawn/decay)")
    
    def _check_edge_evolution(self):
        """Check edge count evolution makes sense."""
        edge_samples = []
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                    
                    if obj.get('type') == 'GRAPH':
                        edges = obj.get('edges', [])
                        edge_samples.append((obj.get('tick'), len(edges)))
                
                except (json.JSONDecodeError, KeyError):
                    continue
        
        if len(edge_samples) < 2:
            return
        
        # Check for suspicious patterns
        edge_counts = [e for _, e in edge_samples]
        
        # Should not suddenly drop to 0 (unless very late)
        for i, (tick, count) in enumerate(edge_samples):
            if count == 0 and i < len(edge_samples) * 0.8:  # Before 80% complete
                self.warnings.append(f"Tick {tick}: All edges gone (premature freeze?)")
                break
        
        # Should not explode (>10x growth)
        if len(edge_counts) >= 2:
            max_ratio = max(edge_counts[i+1] / edge_counts[i] 
                           for i in range(len(edge_counts)-1) 
                           if edge_counts[i] > 0)
            
            if max_ratio > 10:
                self.warnings.append(
                    f"Edge count exploded ({max_ratio:.1f}x growth between ticks)"
                )
    
    def _check_weight_bounds(self):
        """Check all weights stay within theoretical bounds."""
        W_max_violations = []
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                    
                    if obj.get('type') == 'GRAPH':
                        tick = obj.get('tick')
                        edges = obj.get('edges', [])
                        
                        for edge in edges:
                            if len(edge) < 3:
                                continue
                            
                            w = edge[2]
                            
                            # Check against theoretical W_max (typically 2.5-3.0)
                            if w > 5.0:  # Conservative bound
                                W_max_violations.append((tick, edge[0], edge[1], w))
                                if len(W_max_violations) >= 5:
                                    break
                
                except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                    continue
        
        if W_max_violations:
            self.errors.append("Weights exceed theoretical maximum (W_max)")
            for tick, u, v, w in W_max_violations[:3]:
                self.errors.append(f"  Tick {tick}: edge {u}-{v}, w={w:.3f}")
    
    def _check_graph_properties(self):
        """Check graph remains simple (no multi-edges, self-loops)."""
        violations = []
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                    
                    if obj.get('type') == 'GRAPH':
                        tick = obj.get('tick')
                        edges = obj.get('edges', [])
                        
                        # Check for self-loops
                        for edge in edges:
                            if len(edge) < 2:
                                continue
                            
                            if edge[0] == edge[1]:
                                violations.append(f"Tick {tick}: self-loop {edge[0]}-{edge[1]}")
                                break
                        
                        # Check for multi-edges (same pair appears twice)
                        edge_set = set()
                        for edge in edges:
                            if len(edge) < 2:
                                continue
                            
                            pair = tuple(sorted([edge[0], edge[1]]))
                            if pair in edge_set:
                                violations.append(f"Tick {tick}: multi-edge {pair}")
                                break
                            edge_set.add(pair)
                        
                        if len(violations) >= 3:
                            break
                
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
        
        if violations:
            self.errors.append("Graph property violations:")
            for v in violations[:3]:
                self.errors.append(f"  {v}")
    
    def print_report(self):
        """Print theory validation report."""
        print("=" * 70)
        print("THEORY VALIDATION")
        print("=" * 70)
        print()
        
        if self.errors:
            print("[ERRORS]")
            for error in self.errors:
                print(f"  [X] {error}")
            print()
        
        if self.warnings:
            print("[WARNINGS]")
            for warning in self.warnings:
                print(f"  [!] {warning}")
            print()
        
        if self.info:
            print("[INFO]")
            for info_msg in self.info:
                print(f"  [i] {info_msg}")
            print()
        
        # Summary
        if not self.errors and not self.warnings:
            print("[OK] Theory-level consistency verified!")
        elif not self.errors:
            print(f"[OK] Consistent ({len(self.warnings)} warnings)")
        else:
            print(f"[FAIL] {len(self.errors)} theory violations")
        
        print()
        print("=" * 70)


def validate_all(output_dir: Path, verbose: bool = False):
    """Run all validators on simulation output."""
    
    print("=" * 70)
    print(f"COMPLETE VALIDATION: {output_dir.name}")
    print("=" * 70)
    print()
    
    all_valid = True
    
    # 1. Sanity checks
    print("[1/3] Running sanity checks...")
    try:
        sanity = SimulationValidator(output_dir, verbose)
        sanity_valid = sanity.validate()
        sanity.print_report()
        
        if not sanity_valid:
            all_valid = False
            print("\n[!] Sanity checks failed. Skipping theory validation.\n")
            return all_valid
    
    except Exception as e:
        print(f"[ERROR] Sanity validation failed: {e}\n")
        return False
    
    # 2. Theory checks
    print("\n[2/3] Running theory checks...")
    try:
        theory = TheoryValidator(output_dir)
        theory_valid = theory.validate()
        theory.print_report()
        
        if not theory_valid:
            all_valid = False
    
    except Exception as e:
        print(f"[ERROR] Theory validation failed: {e}\n")
        all_valid = False
    
    # 3. Final summary
    print("\n[3/3] Final Summary")
    print("=" * 70)
    
    if all_valid:
        print("[OK] All validations passed!")
        print("     Data is clean and theory-consistent.")
        print("     Results are publication-ready.")
    else:
        print("[FAIL] Some validations failed.")
        print("       Review errors above before using results.")
    
    print("=" * 70)
    
    return all_valid


def main():
    parser = argparse.ArgumentParser(
        description='Integrated ROMION Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate config before run
  python scripts/validate.py --config cfg/my_test.cfg
  
  # Quick sanity check after run
  python scripts/validate.py --simulation results/my_test/
  
  # Complete validation (sanity + theory)
  python scripts/validate.py --all results/my_test/
  
  # Theory checks only
  python scripts/validate.py --theory results/my_test/
        """
    )
    
    parser.add_argument('--config', help='Validate config file')
    parser.add_argument('--simulation', help='Quick sanity check')
    parser.add_argument('--theory', help='Theory consistency check')
    parser.add_argument('--all', help='Complete validation (sanity + theory)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        # Config validation
        if args.config:
            config_path = Path(args.config)
            validator = ConfigValidator(config_path)
            is_valid = validator.validate()
            validator.print_report()
            return 0 if is_valid else 1
        
        # Simulation sanity
        elif args.simulation:
            output_dir = Path(args.simulation)
            validator = SimulationValidator(output_dir, args.verbose)
            is_valid = validator.validate()
            validator.print_report()
            return 0 if is_valid else 1
        
        # Theory only
        elif args.theory:
            output_dir = Path(args.theory)
            validator = TheoryValidator(output_dir)
            is_valid = validator.validate()
            validator.print_report()
            return 0 if is_valid else 1
        
        # Complete validation
        elif args.all:
            output_dir = Path(args.all)
            is_valid = validate_all(output_dir, args.verbose)
            return 0 if is_valid else 1
        
        else:
            parser.print_help()
            return 1
    
    except Exception as e:
        import traceback
        print(f"[ERROR] {e}", file=sys.stderr)
        if args.verbose:
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
