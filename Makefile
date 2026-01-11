# ROMION O'LOGIC™ Makefile
# Common tasks for running simulations and analysis

.PHONY: help test-c sweep-pilot sweep-full analyze-r2 analyze-all clean

# Default target
help:
	@echo "ROMION O'LOGIC™ - Available Commands:"
	@echo ""
	@echo "Simulations:"
	@echo "  make baseline        - Run baseline config"
	@echo "  make decay-slow      - Run decay×0.7 (R2 winner)"
	@echo "  make test-c          - Run all Test C configurations"
	@echo ""
	@echo "Sweeps:"
	@echo "  make sweep-pilot     - Run Pilot A decay sweep (8 runs)"
	@echo "  make sweep-full      - Run full decay sweep (18 runs)"
	@echo ""
	@echo "Analysis:"
	@echo "  make analyze-r2      - Analyze R2 @ tick 400"
	@echo "  make analyze-all     - Analyze all Test C runs"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean           - Remove __pycache__ and temp files"
	@echo "  make verify-paths    - Verify all paths are correct"
	@echo "  make list-configs    - List all available configs"
	@echo ""
	@echo "For details: make help-<command>"

# === SIMULATIONS ===

baseline:
	python scripts/run_from_config.py cfg/baseline.cfg

decay-slow:
	python scripts/run_from_config.py cfg/decay_slow.cfg

spawn-up:
	python scripts/run_from_config.py cfg/spawn_up.cfg

tension-up:
	python scripts/run_from_config.py cfg/tension_up.cfg

combo:
	python scripts/run_from_config.py cfg/combo.cfg

# === TEST C ===

test-c:
	@echo "Running Test C: All 6 configurations..."
	python scripts/run_from_config.py tests/test_c/cfg/R0_baseline.cfg --out tests/test_c/results/R0_base
	python scripts/run_from_config.py tests/test_c/cfg/R1_spawn_up.cfg --out tests/test_c/results/R1_spawnUp
	python scripts/run_from_config.py tests/test_c/cfg/R2_decay_slow.cfg --out tests/test_c/results/R2_decayDown
	python scripts/run_from_config.py tests/test_c/cfg/R3_tension_up.cfg --out tests/test_c/results/R3_tensionUp
	python scripts/run_from_config.py tests/test_c/cfg/R4_combo.cfg --out tests/test_c/results/R4_combo
	python scripts/run_from_config.py tests/test_c/cfg/R5_shock.cfg --out tests/test_c/results/R5_shock
	@echo "Test C complete! Run 'make analyze-all' to analyze results."

test-c-r0:
	python scripts/run_from_config.py tests/test_c/cfg/R0_baseline.cfg --out tests/test_c/results/R0_base

test-c-r2:
	python scripts/run_from_config.py tests/test_c/cfg/R2_decay_slow.cfg --out tests/test_c/results/R2_decayDown

# === SWEEPS ===

sweep-pilot:
	@echo "Running Pilot A decay sweep (8 runs)..."
	python scripts/batch_sweep.py
	@echo "Sweep complete! Check tests/sweep_decay/results/"

sweep-full:
	@echo "Running full decay sweep (18 runs)..."
	python scripts/batch_sweep.py full
	@echo "Sweep complete! Check tests/sweep_decay/results/"

# === ANALYSIS ===

analyze-r2:
	@echo "Analyzing R2 (decay×0.7) @ tick 400..."
	python analysis/gravity_test.py \
		--log tests/test_c/results/R2_decayDown/simulation.jsonl \
		--tick 400 \
		--wcluster 0.02 --wbridge 0.0 --wdist 0.005 \
		--wdist-mode threshold --min-cluster-size 2

analyze-r0:
	@echo "Analyzing R0 (baseline) @ tick 400..."
	python analysis/gravity_test.py \
		--log tests/test_c/results/R0_base/simulation.jsonl \
		--tick 400 \
		--wcluster 0.02 --wbridge 0.0 --wdist 0.005 \
		--wdist-mode threshold --min-cluster-size 2

analyze-all:
	@echo "Analyzing all Test C runs..."
	python scripts/batch_test_c.py

# === UTILITIES ===

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.tmp" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	@echo "Clean complete!"

verify-paths:
	@echo "Verifying project paths..."
	@test -f scripts/run_from_config.py && echo "[OK] run_from_config.py" || echo "[FAIL] run_from_config.py"
	@test -f analysis/gravity_test.py && echo "[OK] gravity_test.py" || echo "[FAIL] gravity_test.py"
	@test -d tests/test_c/cfg && echo "[OK] test_c/cfg/" || echo "[FAIL] test_c/cfg/"
	@test -d tests/sweep_decay/cfg && echo "[OK] sweep_decay/cfg/" || echo "[FAIL] sweep_decay/cfg/"
	@test -f cfg/baseline.cfg && echo "[OK] cfg/baseline.cfg" || echo "[FAIL] cfg/baseline.cfg"
	@echo "Verification complete!"

list-configs:
	@echo "Available configurations:"
	@echo ""
	@echo "Global (cfg/):"
	@ls -1 cfg/*.cfg 2>/dev/null || dir /b cfg\*.cfg
	@echo ""
	@echo "Test C (tests/test_c/cfg/):"
	@ls -1 tests/test_c/cfg/*.cfg 2>/dev/null || dir /b tests\test_c\cfg\*.cfg
	@echo ""
	@echo "Sweep (tests/sweep_decay/cfg/):"
	@ls -1 tests/sweep_decay/cfg/*.cfg 2>/dev/null || dir /b tests\sweep_decay\cfg\*.cfg

# === HELP ===

help-baseline:
	@echo "make baseline"
	@echo "  Run baseline configuration (decay_scale=1.0)"
	@echo "  Output: results_baseline/"

help-test-c:
	@echo "make test-c"
	@echo "  Run all 6 Test C configurations:"
	@echo "    R0: baseline"
	@echo "    R1: spawn×1.2"
	@echo "    R2: decay×0.7 (winner)"
	@echo "    R3: tension×1.2"
	@echo "    R4: combo"
	@echo "    R5: shock"
	@echo "  Total time: ~30-60 minutes"

help-sweep:
	@echo "make sweep-pilot"
	@echo "  Run Pilot A decay sweep:"
	@echo "    decay_scale: [1.0, 0.85, 0.8, 0.75]"
	@echo "    seeds: [42, 123]"
	@echo "    Total: 8 runs"
	@echo ""
	@echo "make sweep-full"
	@echo "  Run full decay sweep:"
	@echo "    decay_scale: [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6]"
	@echo "    seeds: [42, 123]"
	@echo "    Total: 18 runs"

help-analyze:
	@echo "make analyze-r2"
	@echo "  Analyze R2 (decay×0.7, winner) @ tick 400"
	@echo "  Shows: bridges, hub%, range, clusters"
	@echo ""
	@echo "make analyze-all"
	@echo "  Batch analyze all Test C runs"
	@echo "  Creates: tests/test_c/results/test_c_corrected_results.csv"
