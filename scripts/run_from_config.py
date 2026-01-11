#!/usr/bin/env python3
"""
Config-based runner for ROMION simulations.

Usage:
    python scripts/run_from_config.py cfg/baseline.cfg
    python scripts/run_from_config.py tests/test_c/cfg/R2_decay_slow.cfg
    python scripts/run_from_config.py my_test.cfg --out custom_output

Benefits:
    - Reproducible (all params in .cfg)
    - Validated (checks param validity)
    - Simple (one command)
    - Documented (config is documentation)
"""

import argparse
import configparser
import subprocess
import sys
from pathlib import Path


class ConfigRunner:
    """Runner that executes simulations from .cfg files."""
    
    REQUIRED_SECTIONS = ['simulation', 'parameters']
    OPTIONAL_SECTIONS = ['output', 'analysis', 'notes']
    
    # Parameter validation ranges
    PARAM_RANGES = {
        'ticks': (1, 10000),
        'nodes': (10, 10000),
        'init_edges': (10, 100000),
        'seed': (0, 2**31-1),
        'spawn_scale': (0.1, 10.0),
        'decay_scale': (0.1, 10.0),
        'tension_scale': (0.1, 10.0),
        'dump_graph_every': (0, 1000),
        'log_interval': (1, 1000),
    }
    
    def __init__(self, config_path: str, output_override: str = None, dry_run: bool = False):
        self.config_path = Path(config_path)
        self.output_override = output_override
        self.dry_run = dry_run
        self.config = configparser.ConfigParser()
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        self.config.read(self.config_path)
        self._validate_config()
    
    def _validate_config(self):
        """Validate config file structure and parameters."""
        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in self.config:
                raise ValueError(f"Missing required section: [{section}]")
        
        # Validate parameters
        if 'parameters' in self.config:
            for param, value in self.config['parameters'].items():
                if param in self.PARAM_RANGES:
                    try:
                        val = float(value)
                        min_val, max_val = self.PARAM_RANGES[param]
                        if not (min_val <= val <= max_val):
                            print(f"[WARN] {param}={val} outside typical range [{min_val}, {max_val}]")
                    except ValueError:
                        raise ValueError(f"Invalid value for {param}: {value}")
    
    def build_command(self) -> list:
        """Build command line arguments from config."""
        cmd = ['python', 'scripts/run_romion_extended.py']
        
        # Simulation parameters
        if 'simulation' in self.config:
            sim = self.config['simulation']
            if 'ticks' in sim:
                cmd.extend(['--ticks', sim['ticks']])
            if 'nodes' in sim:
                cmd.extend(['--nodes', sim['nodes']])
            if 'init_edges' in sim:
                cmd.extend(['--init-edges', sim['init_edges']])
            if 'seed' in sim:
                cmd.extend(['--seed', sim['seed']])
        
        # Parameter scales
        if 'parameters' in self.config:
            params = self.config['parameters']
            if 'spawn_scale' in params:
                cmd.extend(['--spawn-scale', params['spawn_scale']])
            if 'decay_scale' in params:
                cmd.extend(['--decay-scale', params['decay_scale']])
            if 'tension_scale' in params:
                cmd.extend(['--tension-scale', params['tension_scale']])
            
            # Quantum Spark (optional)
            if params.get('enable_spark', 'false').lower() == 'true':
                cmd.append('--enable-spark')
                if 'epsilon_spark' in params:
                    cmd.extend(['--epsilon-spark', params['epsilon_spark']])
                if 'spark_w' in params:
                    cmd.extend(['--spark-w', params['spark_w']])
            
            # S2-tail (optional)
            if params.get('enable_s2_tail', 'false').lower() == 'true':
                cmd.append('--enable-s2-tail')
            
            # Shock parameters (optional)
            if 'shock_tick' in params:
                cmd.extend(['--shock-tick', params['shock_tick']])
            if 'shock_len' in params:
                cmd.extend(['--shock-len', params['shock_len']])
            if 'shock_spawn' in params:
                cmd.extend(['--shock-spawn', params['shock_spawn']])
            if 'shock_decay' in params:
                cmd.extend(['--shock-decay', params['shock_decay']])
        
        # Output parameters
        if 'output' in self.config:
            out = self.config['output']
            if 'dump_graph_every' in out:
                cmd.extend(['--dump-graph-every', out['dump_graph_every']])
            if 'log_interval' in out:
                cmd.extend(['--log-interval', out['log_interval']])
        
        # Output directory (override or from config)
        if self.output_override:
            cmd.extend(['--out', self.output_override])
        elif 'simulation' in self.config and 'out' in self.config['simulation']:
            cmd.extend(['--out', self.config['simulation']['out']])
        else:
            # Default: derive from config filename
            default_out = f"results_{self.config_path.stem}"
            cmd.extend(['--out', default_out])
        
        return cmd
    
    def print_summary(self, cmd: list):
        """Print execution summary."""
        print(f"[*] Config: {self.config_path}")
        print(f"[>] Command: {' '.join(cmd)}")
        print()
        
        # Print key parameters
        if 'simulation' in self.config:
            print("Simulation:")
            for key, val in self.config['simulation'].items():
                print(f"  {key}: {val}")
        
        if 'parameters' in self.config:
            print("\nParameters:")
            for key, val in self.config['parameters'].items():
                if key.endswith('_scale'):
                    print(f"  {key}: {val}")
        
        if 'notes' in self.config:
            print("\nNotes:")
            for key, val in self.config['notes'].items():
                print(f"  {val}")
        
        print("\n" + "="*70)
    
    def run(self) -> int:
        """Execute the simulation."""
        cmd = self.build_command()
        self.print_summary(cmd)
        
        if self.dry_run:
            print("[DRY RUN] Command would be executed:")
            print(f"   {' '.join(cmd)}")
            return 0
        
        print("[START] Starting simulation...")
        try:
            result = subprocess.run(cmd, check=True)
            print("\n[OK] Simulation complete!")
            return result.returncode
        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] Simulation failed with exit code {e.returncode}")
            return e.returncode
        except KeyboardInterrupt:
            print("\n[STOP] Interrupted by user")
            return 130


def main():
    parser = argparse.ArgumentParser(
        description='Run ROMION simulation from config file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run baseline config
  python scripts/run_from_config.py cfg/baseline.cfg
  
  # Run Test C configuration
  python scripts/run_from_config.py tests/test_c/cfg/R2_decay_slow.cfg
  
  # Override output directory
  python scripts/run_from_config.py cfg/baseline.cfg --out my_test_output
  
  # Dry run (show command without executing)
  python scripts/run_from_config.py cfg/baseline.cfg --dry-run

Config file format:
  [simulation]
  ticks = 600
  seed = 42
  
  [parameters]
  decay_scale = 0.7
  
  [output]
  dump_graph_every = 100
        """
    )
    
    parser.add_argument('config', help='Path to .cfg file')
    parser.add_argument('--out', help='Override output directory')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show command without executing')
    
    args = parser.parse_args()
    
    try:
        runner = ConfigRunner(args.config, args.out, args.dry_run)
        return runner.run()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
