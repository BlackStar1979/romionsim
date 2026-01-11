# 🎯 Task Runner (Makefile)

**Quick commands for common tasks**

---

## 🚀 USAGE:

### Windows:
```bash
task.bat help           # Show all commands
task.bat baseline       # Run baseline
task.bat test-c         # Run all Test C
task.bat analyze-r2     # Analyze R2
```

### Linux/Mac:
```bash
make help              # Show all commands
make baseline          # Run baseline
make test-c            # Run all Test C
make analyze-r2        # Analyze R2
```

---

## 📋 AVAILABLE COMMANDS:

### Simulations:
- `baseline` - Run baseline config
- `decay-slow` - Run decay×0.7 (R2 winner)
- `test-c` - Run all 6 Test C configurations
- `test-c-r2` - Run only R2 (quick test)

### Sweeps:
- `sweep-pilot` - Pilot A (8 runs, ~1h)
- `sweep-full` - Full sweep (18 runs, ~2h)

### Analysis:
- `analyze-r2` - Analyze R2 @ tick 400
- `analyze-r0` - Analyze R0 @ tick 400
- `analyze-all` - Batch analyze all Test C

### Utilities:
- `clean` - Remove __pycache__ and temp files
- `list-configs` - Show all available configs
- `verify-paths` - Check paths are correct (Unix only)

---

## 💡 EXAMPLES:

### Quick Test:
```bash
# Windows
task baseline
task analyze-r2

# Unix
make baseline
make analyze-r2
```

### Full Test C:
```bash
# Run all 6 configs (~30-60 min)
task test-c

# Analyze results
task analyze-all
```

### Sweep:
```bash
# Pilot sweep
task sweep-pilot

# Full sweep
task sweep-full
```

---

## 📝 CUSTOMIZATION:

Edit `Makefile` or `task.bat` to add new commands.

Example:
```makefile
my-test:
	python scripts/run_from_config.py cfg/my_config.cfg
```

---

**See also:** docs/COMMANDS.md for manual commands
