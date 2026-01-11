@echo off
REM ROMION O'LOGIC™ - Task Runner for Windows
REM Usage: task.bat <command>

if "%1"=="" goto help

if "%1"=="help" goto help
if "%1"=="baseline" goto baseline
if "%1"=="decay-slow" goto decay-slow
if "%1"=="test-c" goto test-c
if "%1"=="test-c-r2" goto test-c-r2
if "%1"=="sweep-pilot" goto sweep-pilot
if "%1"=="sweep-full" goto sweep-full
if "%1"=="analyze-r2" goto analyze-r2
if "%1"=="analyze-all" goto analyze-all
if "%1"=="clean" goto clean
if "%1"=="list-configs" goto list-configs

echo Unknown command: %1
echo Run: task.bat help
exit /b 1

:help
echo ROMION O'LOGIC - Available Commands:
echo.
echo Simulations:
echo   task baseline        - Run baseline config
echo   task decay-slow      - Run decay x0.7 (R2 winner)
echo   task test-c          - Run all Test C configurations
echo.
echo Sweeps:
echo   task sweep-pilot     - Run Pilot A decay sweep (8 runs)
echo   task sweep-full      - Run full decay sweep (18 runs)
echo.
echo Analysis:
echo   task analyze-r2      - Analyze R2 @ tick 400
echo   task analyze-all     - Analyze all Test C runs
echo.
echo Utilities:
echo   task clean           - Remove temp files
echo   task list-configs    - List all configs
goto end

:baseline
echo Running baseline config...
python scripts/run_from_config.py cfg/baseline.cfg
goto end

:decay-slow
echo Running decay x0.7 config...
python scripts/run_from_config.py cfg/decay_slow.cfg
goto end

:test-c
echo Running Test C: All 6 configurations...
python scripts/run_from_config.py tests/test_c/cfg/R0_baseline.cfg --out tests/test_c/results/R0_base
python scripts/run_from_config.py tests/test_c/cfg/R1_spawn_up.cfg --out tests/test_c/results/R1_spawnUp
python scripts/run_from_config.py tests/test_c/cfg/R2_decay_slow.cfg --out tests/test_c/results/R2_decayDown
python scripts/run_from_config.py tests/test_c/cfg/R3_tension_up.cfg --out tests/test_c/results/R3_tensionUp
python scripts/run_from_config.py tests/test_c/cfg/R4_combo.cfg --out tests/test_c/results/R4_combo
python scripts/run_from_config.py tests/test_c/cfg/R5_shock.cfg --out tests/test_c/results/R5_shock
echo Test C complete! Run 'task analyze-all' to analyze.
goto end

:test-c-r2
echo Running Test C - R2 only...
python scripts/run_from_config.py tests/test_c/cfg/R2_decay_slow.cfg --out tests/test_c/results/R2_decayDown
goto end

:sweep-pilot
echo Running Pilot A decay sweep (8 runs)...
python scripts/batch_sweep.py
echo Sweep complete! Check tests/sweep_decay/results/
goto end

:sweep-full
echo Running full decay sweep (18 runs)...
python scripts/batch_sweep.py full
echo Sweep complete! Check tests/sweep_decay/results/
goto end

:analyze-r2
echo Analyzing R2 (decay x0.7) @ tick 400...
python analysis/gravity_test.py --log tests/test_c/results/R2_decayDown/simulation.jsonl --tick 400 --wcluster 0.02 --wbridge 0.0 --wdist 0.005 --wdist-mode threshold --min-cluster-size 2
goto end

:analyze-all
echo Analyzing all Test C runs...
python scripts/batch_test_c.py
goto end

:clean
echo Cleaning temporary files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
del /s /q *.tmp 2>nul
del /s /q *.log 2>nul
echo Clean complete!
goto end

:list-configs
echo Available configurations:
echo.
echo Global (cfg/):
dir /b cfg\*.cfg
echo.
echo Test C (tests/test_c/cfg/):
dir /b tests\test_c\cfg\*.cfg
echo.
echo Sweep (tests/sweep_decay/cfg/):
dir /b tests\sweep_decay\cfg\*.cfg
goto end

:end
