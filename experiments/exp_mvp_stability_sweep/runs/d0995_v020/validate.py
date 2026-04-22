import json
import subprocess
import sys
from pathlib import Path

from engine.api.engine import EngineParams, RomionEngine


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    params_path = base_dir / "params.json"
    out_dir = base_dir / "raw_logs"

    if not params_path.exists():
        print("FAIL: params.json not found")
        print(str(params_path))
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    with open(params_path, "r", encoding="utf-8") as f:
        params_dict = json.load(f)

    params = EngineParams(
        seed=int(params_dict.get("seed", 0)),
        n_nodes=int(params_dict.get("n_nodes", 0)),
        ticks=int(params_dict.get("ticks", 0)),
        spawn_scale=float(params_dict.get("spawn_scale", 1.0)),
        decay_scale=float(params_dict.get("decay_scale", 1.0)),
        w_max=params_dict.get("w_max", None),
        extra=dict(params_dict.get("extra", {})),
    )

    # 1) Run engine
    try:
        engine = RomionEngine(params)
        artifacts = engine.run(out_dir=str(out_dir))
    except Exception as e:
        print("FAIL: engine run crashed")
        print(str(e))
        return 3

    if not artifacts.log_path:
        print("FAIL: engine did not return log_path")
        return 4

    log_path = Path(artifacts.log_path)
    if not log_path.exists():
        print("FAIL: log_path does not exist")
        print(str(log_path))
        return 5

    print("OK: engine run finished")
    print("run_id:", artifacts.run_id)
    print("log_path:", str(log_path))

    # 2) Validate log using the minimal validator script
    validator = Path(__file__).resolve().parents[4] / "validation" / "validate_log_minimal.py"
    if not validator.exists():
        print("FAIL: validator script not found")
        print(str(validator))
        return 6

    cmd = [sys.executable, str(validator), "--log", str(log_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    # Forward validator output
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip())

    if proc.returncode != 0:
        print("FAIL: log validation failed")
        return 7

    print("OK: smoke test + validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())