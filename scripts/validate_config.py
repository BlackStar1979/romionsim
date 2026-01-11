#!/usr/bin/env python3
"""
Config Validator for ROMION

Validates .cfg files before running simulations.
Catches errors early, saves compute time.

Usage:
    python scripts/validate_config.py cfg/my_test.cfg
    python scripts/validate_config.py cfg/my_test.cfg --fix
    python scripts/validate_config.py --check-all
"""

import argparse
import configparser
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class ConfigValidator:
    """Validates ROMION config files."""
    
    # Required sections
    REQUIRED_SECTIONS = ['simulation', 'parameters']
    OPTIONAL_SECTIONS = ['output', 'analysis', 'notes']
    
    # Parameter constraints
    CONSTRAINTS = {
        # Simulation
        'ticks': {'type': int, 'min': 1, 'max': 100000, 'typical': (100, 2000)},
        'nodes': {'type': int, 'min': 10, 'max': 100000, 'typical': (1000, 5000)},
        'init_edges': {'type': int, 'min': 10, 'max': 1000000, 'typical': (3000, 10000)},
        'seed': {'type': int, 'min': 0, 'max': 2**31-1, 'typical': (0, 10000)},
        
        # Parameter scales
        'spawn_scale': {'type': float, 'min': 0.1, 'max': 10.0, 'typical': (0.7, 1.5)},
        'decay_scale': {'type': float, 'min': 0.1, 'max': 10.0, 'typical': (0.5, 1.5)},
        'tension_scale': {'type': float, 'min': 0.1, 'max': 10.0, 'typical': (0.7, 1.5)},
        'time_alpha_scale': {'type': float, 'min': 0.1, 'max': 10.0, 'typical': (0.8, 1.2)},
        
        # Output
        'dump_graph_every': {'type': int, 'min': 0, 'max': 1000, 'typical': (0, 200)},
        'log_interval': {'type': int, 'min': 1, 'max': 1000, 'typical': (10, 100)},
        
        # Base parameters (if overriding defaults)
        'spawn_threshold': {'type': float, 'min': 0.0, 'max': 1.0, 'typical': (0.1, 0.3)},
        'decay': {'type': float, 'min': 0.001, 'max': 0.1, 'typical': (0.005, 0.015)},
        'theta': {'type': float, 'min': 0.0, 'max': 1.0, 'typical': (0.2, 0.4)},
        'W_max': {'type': float, 'min': 1.0, 'max': 10.0, 'typical': (2.0, 3.0)},
    }
    
    # Relationships that must hold
    RELATIONSHIPS = [
        ('spawn_cap', 'init_edges', '>=', 'spawn_cap must be >= init_edges'),
        ('w_cap', 'W_max', '>=', 'w_cap should be >= W_max'),
    ]
    
    def __init__(self, config_path: Path, auto_fix: bool = False):
        self.config_path = config_path
        self.auto_fix = auto_fix
        self.config = configparser.ConfigParser()
        self.errors = []
        self.warnings = []
        self.info = []
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        
        self.config.read(config_path)
    
    def validate(self) -> bool:
        """Run all validations. Returns True if valid."""
        self._check_structure()
        self._check_types_and_ranges()
        self._check_relationships()
        self._check_consistency()
        
        return len(self.errors) == 0
    
    def _check_structure(self):
        """Check required sections present."""
        for section in self.REQUIRED_SECTIONS:
            if section not in self.config:
                self.errors.append(f"Missing required section: [{section}]")
    
    def _check_types_and_ranges(self):
        """Validate parameter types and ranges."""
        for section in self.config.sections():
            for key, value in self.config[section].items():
                if key not in self.CONSTRAINTS:
                    continue
                
                constraint = self.CONSTRAINTS[key]
                
                # Type check
                try:
                    if constraint['type'] == int:
                        val = int(value)
                    elif constraint['type'] == float:
                        val = float(value)
                    else:
                        continue
                except ValueError:
                    self.errors.append(
                        f"[{section}] {key}={value} invalid type "
                        f"(expected {constraint['type'].__name__})"
                    )
                    continue
                
                # Range check (hard limits)
                if 'min' in constraint and val < constraint['min']:
                    self.errors.append(
                        f"[{section}] {key}={val} below minimum ({constraint['min']})"
                    )
                
                if 'max' in constraint and val > constraint['max']:
                    self.errors.append(
                        f"[{section}] {key}={val} above maximum ({constraint['max']})"
                    )
                
                # Typical range check (warnings)
                if 'typical' in constraint:
                    typ_min, typ_max = constraint['typical']
                    if val < typ_min or val > typ_max:
                        self.warnings.append(
                            f"[{section}] {key}={val} outside typical range "
                            f"[{typ_min}, {typ_max}]"
                        )
    
    def _check_relationships(self):
        """Check parameter relationships."""
        # Get all params as dict
        params = {}
        for section in self.config.sections():
            for key, value in self.config[section].items():
                try:
                    params[key] = float(value)
                except ValueError:
                    params[key] = value
        
        # Check relationships
        for key1, key2, op, msg in self.RELATIONSHIPS:
            if key1 not in params or key2 not in params:
                continue
            
            val1, val2 = params[key1], params[key2]
            
            if op == '>=' and val1 < val2:
                self.errors.append(f"{msg} (found {key1}={val1}, {key2}={val2})")
            elif op == '>' and val1 <= val2:
                self.errors.append(f"{msg} (found {key1}={val1}, {key2}={val2})")
            elif op == '==' and val1 != val2:
                self.errors.append(f"{msg} (found {key1}={val1}, {key2}={val2})")
    
    def _check_consistency(self):
        """Check internal consistency."""
        
        # If dump_graph_every > 0, should be reasonable relative to ticks
        if 'simulation' in self.config and 'output' in self.config:
            sim = self.config['simulation']
            output = self.config['output']
            
            if 'ticks' in sim and 'dump_graph_every' in output:
                ticks = int(sim['ticks'])
                dump = int(output['dump_graph_every'])
                
                if dump > 0:
                    num_dumps = ticks // dump
                    if num_dumps > 1000:
                        self.warnings.append(
                            f"Will generate {num_dumps} graph dumps. "
                            f"Consider increasing dump_graph_every."
                        )
                    elif num_dumps < 5:
                        self.info.append(
                            f"Only {num_dumps} graph dumps. "
                            f"Consider decreasing dump_graph_every for more data."
                        )
        
        # Quantum Spark consistency
        if 'parameters' in self.config:
            params = self.config['parameters']
            if 'enable_spark' in params:
                enable_spark_str = params['enable_spark']
                enable_spark = str(enable_spark_str).lower() == 'true'
                
                if enable_spark:
                    if 'epsilon_spark' not in params:
                        self.warnings.append(
                            "Quantum Spark enabled but epsilon_spark not set"
                        )
                    elif float(params['epsilon_spark']) > 0.01:
                        self.warnings.append(
                            f"epsilon_spark={params['epsilon_spark']} is high. "
                            f"Typical: < 0.001"
                        )
    
    def print_report(self):
        """Print validation report."""
        print("=" * 70)
        print(f"CONFIG VALIDATION: {self.config_path.name}")
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
            print("[OK] Config is valid and optimal!")
        elif not self.errors:
            print(f"[OK] Config is valid ({len(self.warnings)} warnings)")
        else:
            print(f"[FAIL] Config has {len(self.errors)} errors")
            if self.auto_fix:
                print("\nRun with --fix to attempt auto-correction")
        
        print()
        print("=" * 70)


def validate_all_configs(directory: Path):
    """Validate all .cfg files in directory."""
    cfg_files = list(directory.glob('**/*.cfg'))
    
    if not cfg_files:
        print(f"No .cfg files found in {directory}")
        return
    
    print(f"Found {len(cfg_files)} config files\n")
    
    results = {'valid': [], 'warnings': [], 'errors': []}
    
    for cfg_file in sorted(cfg_files):
        validator = ConfigValidator(cfg_file)
        is_valid = validator.validate()
        
        if is_valid and not validator.warnings:
            results['valid'].append(cfg_file)
            print(f"[OK] {cfg_file.relative_to(directory)}")
        elif is_valid:
            results['warnings'].append(cfg_file)
            print(f"[WARN] {cfg_file.relative_to(directory)} ({len(validator.warnings)} warnings)")
        else:
            results['errors'].append(cfg_file)
            print(f"[FAIL] {cfg_file.relative_to(directory)} ({len(validator.errors)} errors)")
    
    # Summary
    print()
    print("=" * 70)
    print(f"SUMMARY: {len(cfg_files)} configs checked")
    print(f"  Valid: {len(results['valid'])}")
    print(f"  Warnings: {len(results['warnings'])}")
    print(f"  Errors: {len(results['errors'])}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Validate ROMION config files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single config
  python scripts/validate_config.py cfg/baseline.cfg
  
  # Validate with auto-fix
  python scripts/validate_config.py cfg/my_test.cfg --fix
  
  # Validate all configs
  python scripts/validate_config.py --check-all
        """
    )
    
    parser.add_argument('config', nargs='?', help='Config file to validate')
    parser.add_argument('--fix', action='store_true', 
                       help='Attempt to auto-fix errors')
    parser.add_argument('--check-all', action='store_true',
                       help='Validate all .cfg files in project')
    
    args = parser.parse_args()
    
    if args.check_all:
        validate_all_configs(Path('.'))
        return 0
    
    if not args.config:
        parser.print_help()
        return 1
    
    try:
        config_path = Path(args.config)
        validator = ConfigValidator(config_path, args.fix)
        is_valid = validator.validate()
        validator.print_report()
        
        return 0 if is_valid else 1
    
    except Exception as e:
        import traceback
        print(f"[ERROR] {e}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
