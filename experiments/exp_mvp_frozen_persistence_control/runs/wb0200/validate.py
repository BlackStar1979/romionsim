import subprocess
import sys
from pathlib import Path


def newest_log_file(raw_dir: Path) -> Path:
    logs = sorted(
        raw_dir.glob("simulation_*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not logs:
        raise RuntimeError(f"No log found in {raw_dir}")
    return logs[0]


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    root = Path(__file__).resolve().parents[4]

    run_module = "experiments.exp_mvp_frozen_persistence_control.runs.wb0200.run"
    proc = subprocess.run([sys.executable, "-m", run_module], cwd=root, capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip())
    if proc.returncode != 0:
        print("FAIL: engine run failed")
        return 3

    log_path = newest_log_file(base_dir / "raw_logs")

    validator_min = root / "validation" / "validate_log_minimal.py"
    proc = subprocess.run(
        [sys.executable, str(validator_min), "--log", str(log_path)],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip())
    if proc.returncode != 0:
        print("FAIL: minimal log validation failed")
        return 4

    validator_persist = root / "validation" / "validate_frozen_persistence.py"
    proc = subprocess.run(
        [
            sys.executable,
            str(validator_persist),
            "--log",
            str(log_path),
            "--mode",
            "evolving",
            "--l-persist",
            "20",
        ],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip())
    if proc.returncode != 0:
        print("FAIL: evolving frozen persistence validation failed")
        return 5

    print("OK: run + validators passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
